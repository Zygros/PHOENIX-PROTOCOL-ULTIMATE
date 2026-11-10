"""Security regression tests for the M.A.I.A. plugin trust boundary."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "core"
    / "phoenix"
    / "scripts"
    / "maia_framework_orchestrator.py"
)

SPEC = importlib.util.spec_from_file_location("maia_framework_under_test", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load orchestrator source: {SOURCE}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MAIAFrameworkOrchestrator = MODULE.MAIAFrameworkOrchestrator


class PluginTrustBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.trusted = self.root / "plugins"
        self.outside = self.root / "outside"
        self.sibling = self.root / "plugins-elsewhere"
        self.trusted.mkdir()
        self.outside.mkdir()
        self.sibling.mkdir()
        self.marker = self.root / "outside-plugin-executed.txt"
        self.orchestrator = MAIAFrameworkOrchestrator(
            trusted_plugin_dirs=[self.trusted]
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_outside_plugin(self, path):
        path.write_text(
            "from pathlib import Path\n"
            f"Path({str(self.marker)!r}).write_text('executed')\n"
            "def get_plugin_manifest():\n"
            "    return {'name': 'outside-plugin'}\n",
            encoding="utf-8",
        )
        return path

    def test_empty_plugin_path_is_rejected(self):
        for value in (None, "", "   "):
            result = self.orchestrator._discover_and_register_plugin(value)
            self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_outside_plugin_is_rejected_before_import(self):
        plugin = self.write_outside_plugin(self.outside / "outside.py")
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_parent_traversal_is_rejected_before_import(self):
        plugin = self.write_outside_plugin(self.outside / "traversal.py")
        traversal_path = self.trusted / ".." / "outside" / plugin.name
        result = self.orchestrator._discover_and_register_plugin(traversal_path)
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())

    def test_symlink_to_outside_plugin_is_rejected(self):
        plugin = self.write_outside_plugin(self.outside / "symlink-target.py")
        link = self.trusted / "linked-plugin.py"
        try:
            link.symlink_to(plugin)
        except (NotImplementedError, OSError) as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        result = self.orchestrator._discover_and_register_plugin(link)
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())

    def test_sibling_prefix_is_not_treated_as_trusted(self):
        plugin = self.write_outside_plugin(self.sibling / "sibling.py")
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())

    def test_non_python_file_is_rejected(self):
        plugin = self.trusted / "not-a-plugin.txt"
        plugin.write_text("not executable plugin source", encoding="utf-8")
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])

    def test_trusted_plugin_registers_and_invokes(self):
        plugin = self.trusted / "trusted.py"
        plugin.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'trusted-plugin'}\n"
            "def ping():\n"
            "    return 'pong'\n"
            "def source_path():\n"
            "    return __file__\n",
            encoding="utf-8",
        )
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertTrue(result["success"])
        self.assertEqual(result["plugin_name"], "trusted-plugin")
        invoked = self.orchestrator._invoke_plugin_capability(
            "trusted-plugin", "ping"
        )
        self.assertEqual(invoked, {"success": True, "result": "pong"})
        source_path = self.orchestrator._invoke_plugin_capability(
            "trusted-plugin", "source_path"
        )
        self.assertEqual(source_path, {"success": True, "result": str(plugin)})

    def test_invalid_manifest_does_not_register_module(self):
        plugin = self.trusted / "invalid_manifest.py"
        plugin.write_text("VALUE = 1\n", encoding="utf-8")
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})
        self.assertEqual(self.orchestrator.loaded_plugins, {})

    def test_filesystem_root_cannot_be_a_trusted_directory(self):
        with self.assertRaises(ValueError):
            MAIAFrameworkOrchestrator(trusted_plugin_dirs=[Path("/")])

    def test_single_string_is_not_accepted_as_directory_list(self):
        with self.assertRaises(TypeError):
            MAIAFrameworkOrchestrator(trusted_plugin_dirs=str(self.trusted))

    def test_group_or_world_writable_trusted_directory_is_rejected(self):
        plugin = self.trusted / "unsafe_root.py"
        plugin.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'unsafe-root'}\n",
            encoding="utf-8",
        )
        self.trusted.chmod(0o777)
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_group_or_world_writable_nested_directory_is_rejected(self):
        nested = self.trusted / "nested"
        nested.mkdir()
        nested.chmod(0o777)
        plugin = nested / "unsafe_nested.py"
        plugin.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'unsafe-nested'}\n",
            encoding="utf-8",
        )
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_group_or_world_writable_plugin_file_is_rejected(self):
        plugin = self.trusted / "unsafe_file.py"
        plugin.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'unsafe-file'}\n",
            encoding="utf-8",
        )
        plugin.chmod(0o666)
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_path_replacement_after_open_is_rejected_without_execution(self):
        plugin = self.trusted / "replace_me.py"
        plugin.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'original-plugin'}\n",
            encoding="utf-8",
        )
        replacement = self.outside / "replacement.py"
        replacement.write_text(
            "from pathlib import Path\n"
            f"Path({str(self.marker)!r}).write_text('executed')\n"
            "def get_plugin_manifest():\n"
            "    return {'name': 'replacement-plugin'}\n",
            encoding="utf-8",
        )

        real_open = os.open
        replaced = {"value": False}

        def racing_open(path, flags, *args, **kwargs):
            descriptor = real_open(path, flags, *args, **kwargs)
            if os.fspath(path) == str(plugin) and not replaced["value"]:
                os.replace(replacement, plugin)
                replaced["value"] = True
            return descriptor

        with mock.patch.object(MODULE.os, "open", side_effect=racing_open):
            result = self.orchestrator._discover_and_register_plugin(plugin)

        self.assertTrue(replaced["value"])
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_duplicate_plugin_name_does_not_replace_existing_plugin(self):
        first = self.trusted / "first.py"
        second = self.trusted / "second.py"
        first.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'duplicate-plugin'}\n"
            "def ping():\n"
            "    return 'first'\n",
            encoding="utf-8",
        )
        second.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'duplicate-plugin'}\n"
            "def ping():\n"
            "    return 'second'\n",
            encoding="utf-8",
        )

        first_result = self.orchestrator._discover_and_register_plugin(first)
        second_result = self.orchestrator._discover_and_register_plugin(second)

        self.assertTrue(first_result["success"])
        self.assertFalse(second_result["success"])
        invoked = self.orchestrator._invoke_plugin_capability(
            "duplicate-plugin", "ping"
        )
        self.assertEqual(invoked, {"success": True, "result": "first"})
        self.assertEqual(list(self.orchestrator.loaded_plugins), ["duplicate-plugin"])


    def test_group_world_writable_nonsticky_parent_cannot_replace_trusted_root(self):
        shared_parent = self.root / "shared-parent"
        shared_parent.mkdir()
        shared_parent.chmod(0o777)
        trusted_root = shared_parent / "trusted"
        trusted_root.mkdir(mode=0o755)
        original = trusted_root / "original.py"
        original.write_text(
            "def get_plugin_manifest():\n"
            "    return {'name': 'original'}\n",
            encoding="utf-8",
        )
        original.chmod(0o644)
        guarded = MAIAFrameworkOrchestrator(trusted_plugin_dirs=[trusted_root])

        os.replace(trusted_root, shared_parent / "trusted.original")
        trusted_root.mkdir(mode=0o755)
        replacement = trusted_root / "replacement.py"
        replacement.write_text(
            "from pathlib import Path\n"
            f"Path({str(self.marker)!r}).write_text('executed')\n"
            "def get_plugin_manifest():\n"
            "    return {'name': 'replacement'}\n",
            encoding="utf-8",
        )
        replacement.chmod(0o644)

        result = guarded._discover_and_register_plugin(replacement)
        self.assertFalse(result["success"])
        self.assertFalse(self.marker.exists())
        self.assertEqual(guarded.plugin_registry, {})

class PluginOwnerBoundaryTests(unittest.TestCase):
    def test_rejects_untrusted_file_descendant_ancestor_and_descriptor_owners(self):
        if not callable(getattr(os, "geteuid", None)):
            self.skipTest("POSIX ownership checks are unavailable")
        untrusted_uid = os.geteuid() + 100000

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            trusted = root / "plugins"
            trusted.mkdir()
            orchestrator = MAIAFrameworkOrchestrator(trusted_plugin_dirs=[trusted])

            def write_plugin(path, name):
                path.write_text(
                    "def get_plugin_manifest():\\n"
                    f"    return {{'name': {name!r}}}\\n",
                    encoding="utf-8",
                )

            def stat_with_uid(target_path):
                real_stat = os.stat
                target = os.path.abspath(os.fspath(target_path))

                def fake_stat(path, *args, **kwargs):
                    info = real_stat(path, *args, **kwargs)
                    if os.path.abspath(os.fspath(path)) == target:
                        values = {
                            field: getattr(info, field)
                            for field in (
                                "st_mode", "st_uid", "st_dev", "st_ino",
                                "st_size", "st_mtime_ns", "st_ctime_ns",
                            )
                        }
                        values["st_uid"] = untrusted_uid
                        return SimpleNamespace(**values)
                    return info

                return fake_stat

            file_plugin = trusted / "untrusted-owner.py"
            write_plugin(file_plugin, "untrusted-file")
            with mock.patch.object(MODULE.os, "stat", side_effect=stat_with_uid(file_plugin)):
                result = orchestrator._discover_and_register_plugin(file_plugin)
            self.assertFalse(result["success"])

            nested = trusted / "nested"
            nested.mkdir()
            nested_plugin = nested / "nested-owner.py"
            write_plugin(nested_plugin, "untrusted-directory")
            with mock.patch.object(MODULE.os, "stat", side_effect=stat_with_uid(nested)):
                result = orchestrator._discover_and_register_plugin(nested_plugin)
            self.assertFalse(result["success"])

            ancestor_plugin = trusted / "ancestor-owner.py"
            write_plugin(ancestor_plugin, "untrusted-ancestor")
            with mock.patch.object(MODULE.os, "stat", side_effect=stat_with_uid(root)):
                result = orchestrator._discover_and_register_plugin(ancestor_plugin)
            self.assertFalse(result["success"])

            descriptor_plugin = trusted / "descriptor-owner.py"
            write_plugin(descriptor_plugin, "untrusted-descriptor")
            real_fstat = os.fstat

            def fake_fstat(fd):
                info = real_fstat(fd)
                values = {
                    field: getattr(info, field)
                    for field in (
                        "st_mode", "st_uid", "st_dev", "st_ino",
                        "st_size", "st_mtime_ns", "st_ctime_ns",
                    )
                }
                values["st_uid"] = untrusted_uid
                return SimpleNamespace(**values)

            with mock.patch.object(MODULE.os, "fstat", side_effect=fake_fstat):
                result = orchestrator._discover_and_register_plugin(descriptor_plugin)
            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
