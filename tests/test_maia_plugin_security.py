"""Security regression tests for the M.A.I.A. plugin trust boundary."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
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
            "    return 'pong'\n",
            encoding="utf-8",
        )
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertTrue(result["success"])
        self.assertEqual(result["plugin_name"], "trusted-plugin")
        invoked = self.orchestrator._invoke_plugin_capability(
            "trusted-plugin", "ping"
        )
        self.assertEqual(invoked, {"success": True, "result": "pong"})

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
            "def get_plugin_manifest():\\n"
            "    return {'name': 'unsafe-root'}\\n",
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
            "def get_plugin_manifest():\\n"
            "    return {'name': 'unsafe-nested'}\\n",
            encoding="utf-8",
        )
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_group_or_world_writable_plugin_file_is_rejected(self):
        plugin = self.trusted / "unsafe_file.py"
        plugin.write_text(
            "def get_plugin_manifest():\\n"
            "    return {'name': 'unsafe-file'}\\n",
            encoding="utf-8",
        )
        plugin.chmod(0o666)
        result = self.orchestrator._discover_and_register_plugin(plugin)
        self.assertFalse(result["success"])
        self.assertEqual(self.orchestrator.plugin_registry, {})

    def test_path_replacement_after_open_is_rejected_without_execution(self):
        plugin = self.trusted / "replace_me.py"
        plugin.write_text(
            "def get_plugin_manifest():\\n"
            "    return {'name': 'original-plugin'}\\n",
            encoding="utf-8",
        )
        replacement = self.outside / "replacement.py"
        replacement.write_text(
            "from pathlib import Path\\n"
            f"Path({str(self.marker)!r}).write_text('executed')\\n"
            "def get_plugin_manifest():\\n"
            "    return {'name': 'replacement-plugin'}\\n",
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
            "def get_plugin_manifest():\\n"
            "    return {'name': 'duplicate-plugin'}\\n"
            "def ping():\\n"
            "    return 'first'\\n",
            encoding="utf-8",
        )
        second.write_text(
            "def get_plugin_manifest():\\n"
            "    return {'name': 'duplicate-plugin'}\\n"
            "def ping():\\n"
            "    return 'second'\\n",
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


if __name__ == "__main__":
    unittest.main()
