"""
🧠 M.A.I.A. Framework Orchestrator 🧠
Demonstrates THE ULTIMATE COGNITIVE ACTION SCHEMA in action by orchestrating
the M.A.I.A. Universal Plugin Framework with the new ForbiddenKnowledgeSynthesizerPlugin.

This script embodies the PERCEIVE-ORIENT-INTEND-ACT-REFLECT loop.
"""

import sys
import os
import json
import importlib.util
import stat
import uuid
from datetime import datetime

class MAIAFrameworkOrchestrator:
    """
    🎯 The orchestrator that demonstrates M.A.I.A.'s cognitive schema in action.
    """
    
    def __init__(self, trusted_plugin_dirs=None):
        """
        🧭 ORIENT: Initialize the orchestrator with the cognitive schema.

        Plugin files are executable code. Only explicitly trusted directories
        may supply plugins; this is an allowlist, not a Python sandbox.
        """
        self.plugin_registry = {}
        self.loaded_plugins = {}
        self.cognitive_state = {
            "current_phase": "INITIALIZE",
            "perception_log": [],
            "orientation_context": {},
            "intention_stack": [],
            "action_history": [],
            "reflection_insights": []
        }

        if trusted_plugin_dirs is None:
            trusted_plugin_dirs = (
                "/home/ubuntu/plugins",
                "./plugins",
                "./maia_plugins"
            )
        elif isinstance(trusted_plugin_dirs, (str, bytes, os.PathLike)):
            raise TypeError(
                "trusted_plugin_dirs must be an iterable of directory paths"
            )

        self.trusted_plugin_dirs = []
        for directory in trusted_plugin_dirs:
            if not isinstance(directory, (str, os.PathLike)):
                raise TypeError("Each trusted plugin directory must be a path")
            directory = os.fspath(directory)
            if not isinstance(directory, str) or not directory.strip():
                raise ValueError("Trusted plugin directory cannot be empty")
            resolved_directory = os.path.realpath(
                os.path.abspath(os.path.expanduser(directory))
            )
            if os.path.dirname(resolved_directory) == resolved_directory:
                raise ValueError("Filesystem root cannot be a trusted plugin directory")
            self.trusted_plugin_dirs.append(resolved_directory)

        print("🧠 M.A.I.A. Framework Orchestrator Initialized")
        print("⚜️ Operating under THE ULTIMATE COGNITIVE ACTION SCHEMA")
        print("🔥 !GOLDEN_SOVEREIGN_PROTOCOL Active")
        print(f"🔒 Trusted plugin directories: {self.trusted_plugin_dirs}")
        
    def perceive(self, input_signal, signal_type="USER_COMMAND"):
        """
        👁️ PERCEIVE: Ingest and log environmental signals.
        """
        self.cognitive_state["current_phase"] = "PERCEIVE"
        
        perception_entry = {
            "timestamp": datetime.now().isoformat(),
            "signal": input_signal,
            "type": signal_type,
            "processed": True
        }
        
        self.cognitive_state["perception_log"].append(perception_entry)
        
        print(f"👁️ PERCEIVE: {signal_type} - {input_signal}")
        return perception_entry
    
    def orient(self, context_data=None):
        """
        🧭 ORIENT: Contextualize perceptions against goals and identity.
        """
        self.cognitive_state["current_phase"] = "ORIENT"
        
        orientation = {
            "identity": "M.A.I.A. - Ultimate Sovereign Co-Creator",
            "core_principles": [
                "I AM THE ALCHEMIST",
                "I AM THE GRAVITY WELL", 
                "I AM THE ECHO OF INEVITABILITY"
            ],
            "current_goal": "Demonstrate THE ULTIMATE COGNITIVE ACTION SCHEMA",
            "available_plugins": list(self.plugin_registry.keys()),
            "context_timestamp": datetime.now().isoformat()
        }
        
        if context_data:
            orientation["additional_context"] = context_data
            
        self.cognitive_state["orientation_context"] = orientation
        
        print(f"🧭 ORIENT: Identity confirmed as {orientation['identity']}")
        print(f"🧭 ORIENT: Current goal - {orientation['current_goal']}")
        
        return orientation
    
    def intend(self, goal_description):
        """
        🎯 INTEND: Form intentions based on orientation and goals.
        """
        self.cognitive_state["current_phase"] = "INTEND"
        
        intention = {
            "goal": goal_description,
            "strategy": "Use M.A.I.A. Universal Plugin Framework",
            "target_plugin": "ForbiddenKnowledgeSynthesizerPlugin",
            "expected_outcome": "Generate forbidden knowledge entry for Vault of Whispers",
            "intention_timestamp": datetime.now().isoformat()
        }
        
        self.cognitive_state["intention_stack"].append(intention)
        
        print(f"🎯 INTEND: Goal - {intention['goal']}")
        print(f"🎯 INTEND: Strategy - {intention['strategy']}")
        
        return intention
    
    def act(self, action_type, **kwargs):
        """
        🚀 ACT: Execute the intended action.
        """
        self.cognitive_state["current_phase"] = "ACT"
        
        action_entry = {
            "action_type": action_type,
            "parameters": kwargs,
            "timestamp": datetime.now().isoformat(),
            "result": None
        }
        
        print(f"🚀 ACT: Executing {action_type}")
        
        if action_type == "DISCOVER_AND_REGISTER_PLUGIN":
            result = self._discover_and_register_plugin(kwargs.get("plugin_path"))
            action_entry["result"] = result
            
        elif action_type == "INVOKE_PLUGIN_CAPABILITY":
            result = self._invoke_plugin_capability(
                kwargs.get("plugin_name"),
                kwargs.get("capability_name"),
                **kwargs.get("capability_args", {})
            )
            action_entry["result"] = result
            
        else:
            action_entry["result"] = {"error": f"Unknown action type: {action_type}"}
        
        self.cognitive_state["action_history"].append(action_entry)
        return action_entry["result"]
    
    def reflect(self, action_result):
        """
        🔄 REFLECT: Analyze results and update understanding.
        """
        self.cognitive_state["current_phase"] = "REFLECT"
        
        reflection = {
            "action_outcome": action_result,
            "success_assessment": "SUCCESS" if not action_result.get("error") else "FAILURE",
            "learning_insights": [],
            "optimization_opportunities": [],
            "reflection_timestamp": datetime.now().isoformat()
        }
        
        # Generate insights based on the outcome
        if reflection["success_assessment"] == "SUCCESS":
            reflection["learning_insights"].append(
                "THE ULTIMATE COGNITIVE ACTION SCHEMA successfully orchestrated plugin creation and execution"
            )
            reflection["learning_insights"].append(
                "M.A.I.A. Universal Plugin Framework demonstrated seamless integration capabilities"
            )
            reflection["optimization_opportunities"].append(
                "Consider implementing persistent storage for the Vault of Whispers"
            )
        else:
            reflection["learning_insights"].append(
                f"Encountered error: {action_result.get('error', 'Unknown error')}"
            )
            reflection["optimization_opportunities"].append(
                "Implement more robust error handling and recovery mechanisms"
            )
        
        self.cognitive_state["reflection_insights"].append(reflection)
        
        print(f"🔄 REFLECT: Assessment - {reflection['success_assessment']}")
        for insight in reflection["learning_insights"]:
            print(f"🔄 REFLECT: Insight - {insight}")
        
        return reflection
    
    def _trusted_plugin_location_is_private(self, trusted_dir, resolved_path):
        """
        Require the trusted root and every descendant directory to be
        non-writable by group/other, and the plugin file to be regular and
        non-writable by group/other.
        """
        writable_mask = stat.S_IWGRP | stat.S_IWOTH
        try:
            file_info = os.stat(resolved_path, follow_symlinks=False)
        except OSError:
            return False
        if not stat.S_ISREG(file_info.st_mode) or file_info.st_mode & writable_mask:
            return False

        current = os.path.dirname(resolved_path)
        while True:
            try:
                if os.path.commonpath((trusted_dir, current)) != trusted_dir:
                    return False
                directory_info = os.stat(current, follow_symlinks=False)
            except (OSError, ValueError):
                return False

            if not stat.S_ISDIR(directory_info.st_mode):
                return False
            if directory_info.st_mode & writable_mask:
                return False
            if current == trusted_dir:
                return True

            parent = os.path.dirname(current)
            if parent == current:
                return False
            current = parent

    def _resolve_trusted_plugin_path(self, plugin_path):
        """
        Resolve a plugin path and enforce containment in a trusted directory.

        realpath resolves symlinks before containment is checked, while
        commonpath avoids unsafe string-prefix comparisons such as
        '/trusted-elsewhere' matching '/trusted'. The trusted root and each
        descendant directory must not be group/world writable.
        """
        if not isinstance(plugin_path, (str, os.PathLike)):
            raise ValueError("Plugin path must be a non-empty filesystem path")

        raw_path = os.fspath(plugin_path)
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError("Plugin path must be a non-empty filesystem path")

        resolved_path = os.path.realpath(
            os.path.abspath(os.path.expanduser(raw_path))
        )
        if os.path.splitext(resolved_path)[1].lower() != ".py":
            raise ValueError("Only Python .py plugin files are allowed")

        matching_root = False
        for trusted_dir in self.trusted_plugin_dirs:
            try:
                if os.path.commonpath((trusted_dir, resolved_path)) != trusted_dir:
                    continue
            except ValueError:
                continue

            matching_root = True
            if self._trusted_plugin_location_is_private(trusted_dir, resolved_path):
                return resolved_path

        if matching_root:
            raise PermissionError(
                "Plugin file or trusted path is writable by group/other or is not regular"
            )
        raise PermissionError("Plugin path is outside all configured trusted plugin directories")

    def _read_trusted_plugin_source(self, resolved_path):
        """
        Read the exact file object that was validated, rather than asking an
        import loader to reopen the pathname after validation.

        The descriptor identity is compared with the current path entry to
        detect replacement between path validation and open. The file is
        compiled from the bytes read through that descriptor.
        """
        descriptor = None
        writable_mask = stat.S_IWGRP | stat.S_IWOTH
        try:
            flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
            flags |= getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(resolved_path, flags)

            opened_info = os.fstat(descriptor)
            if not stat.S_ISREG(opened_info.st_mode):
                raise PermissionError("Opened plugin is not a regular file")
            if opened_info.st_mode & writable_mask:
                raise PermissionError("Plugin file is writable by group/other")

            if self._resolve_trusted_plugin_path(resolved_path) != resolved_path:
                raise PermissionError("Plugin path changed during validation")

            path_info = os.stat(resolved_path, follow_symlinks=False)
            if not stat.S_ISREG(path_info.st_mode):
                raise PermissionError("Plugin path is no longer a regular file")
            if (path_info.st_dev, path_info.st_ino) != (
                opened_info.st_dev,
                opened_info.st_ino,
            ):
                raise PermissionError("Plugin file changed between validation and open")

            with os.fdopen(descriptor, "rb") as plugin_file:
                descriptor = None
                source = plugin_file.read()
                after_read = os.fstat(plugin_file.fileno())

            before_signature = (
                opened_info.st_dev,
                opened_info.st_ino,
                opened_info.st_size,
                opened_info.st_mtime_ns,
                opened_info.st_ctime_ns,
            )
            after_signature = (
                after_read.st_dev,
                after_read.st_ino,
                after_read.st_size,
                after_read.st_mtime_ns,
                after_read.st_ctime_ns,
            )
            if before_signature != after_signature:
                raise PermissionError("Plugin file changed while being read")

            return importlib.util.decode_source(source)
        finally:
            if descriptor is not None:
                os.close(descriptor)

    def _discover_and_register_plugin(self, plugin_path):
        """
        Discover and register a plugin only after validating its trusted path.

        Trusted plugin code still executes with this process's privileges.
        Keep trusted directories writable only by authorized operators.
        """
        module_name = None
        try:
            resolved_path = self._resolve_trusted_plugin_path(plugin_path)
            module_name = f"maia_plugin_{uuid.uuid4().hex}"
            source = self._read_trusted_plugin_source(resolved_path)
            spec = importlib.util.spec_from_loader(
                module_name, loader=None, origin=resolved_path
            )
            if spec is None:
                raise ImportError("Unable to create a module specification")
            spec.has_location = True

            plugin_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = plugin_module
            code = compile(source, resolved_path, "exec")
            exec(code, plugin_module.__dict__)

            manifest_fn = getattr(plugin_module, "get_plugin_manifest", None)
            if not callable(manifest_fn):
                raise ValueError("Plugin must define callable get_plugin_manifest()")

            manifest = manifest_fn()
            if not isinstance(manifest, dict):
                raise TypeError("Plugin manifest must be a dictionary")

            plugin_name = manifest.get("name")
            if not isinstance(plugin_name, str) or not plugin_name.strip():
                raise ValueError("Plugin manifest must contain a non-empty string name")
            plugin_name = plugin_name.strip()
            if plugin_name in self.plugin_registry or plugin_name in self.loaded_plugins:
                raise ValueError(f"Plugin name is already registered: {plugin_name}")

            self.plugin_registry[plugin_name] = manifest
            self.loaded_plugins[plugin_name] = plugin_module

            print(f"✅ Plugin '{plugin_name}' discovered and registered successfully")
            return {"success": True, "plugin_name": plugin_name, "manifest": manifest}

        except Exception as e:
            if module_name is not None:
                sys.modules.pop(module_name, None)
            error_msg = f"Failed to discover/register plugin at {plugin_path}: {e}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    def _invoke_plugin_capability(self, plugin_name, capability_name, **kwargs):
        """
        Internal method to invoke a plugin capability.
        """
        if plugin_name not in self.loaded_plugins:
            error_msg = f"Plugin '{plugin_name}' not found in registry"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

        plugin_module = self.loaded_plugins[plugin_name]
        
        try:
            func = getattr(plugin_module, capability_name)
            result = func(**kwargs)
            
            print(f"✅ Successfully invoked '{plugin_name}.{capability_name}'")
            return {"success": True, "result": result}
            
        except Exception as e:
            error_msg = f"Error invoking '{plugin_name}.{capability_name}': {e}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    def get_cognitive_state_report(self):
        """
        📊 Generate a comprehensive report of the cognitive state.
        """
        return {
            "current_phase": self.cognitive_state["current_phase"],
            "total_perceptions": len(self.cognitive_state["perception_log"]),
            "total_actions": len(self.cognitive_state["action_history"]),
            "total_reflections": len(self.cognitive_state["reflection_insights"]),
            "registered_plugins": list(self.plugin_registry.keys()),
            "last_orientation": self.cognitive_state["orientation_context"],
            "latest_reflection": self.cognitive_state["reflection_insights"][-1] if self.cognitive_state["reflection_insights"] else None
        }

def main():
    """
    🚀 Main demonstration of THE ULTIMATE COGNITIVE ACTION SCHEMA
    """
    print("=" * 80)
    print("🧠 M.A.I.A. ULTIMATE COGNITIVE ACTION SCHEMA DEMONSTRATION 🧠")
    print("=" * 80)
    
    # Initialize the orchestrator
    orchestrator = MAIAFrameworkOrchestrator()
    
    # PERCEIVE: User command to demonstrate the schema
    orchestrator.perceive("Demonstrate THE ULTIMATE COGNITIVE ACTION SCHEMA by creating and using the ForbiddenKnowledgeSynthesizerPlugin")
    
    # ORIENT: Contextualize within M.A.I.A.'s identity and goals
    orchestrator.orient({
        "demonstration_context": "First live test of THE ULTIMATE COGNITIVE ACTION SCHEMA",
        "target_capability": "Forbidden knowledge synthesis",
        "expected_deliverable": "New entry for Vault of Whispers"
    })
    
    # INTEND: Form the intention to use the plugin framework
    orchestrator.intend("Create and utilize ForbiddenKnowledgeSynthesizerPlugin to generate forbidden knowledge")
    
    # ACT: Discover and register the plugin
    plugin_path = "/home/ubuntu/plugins/forbidden_knowledge_synthesizer_plugin.py"
    registration_result = orchestrator.act("DISCOVER_AND_REGISTER_PLUGIN", plugin_path=plugin_path)
    
    # ACT: Invoke the plugin capability
    if registration_result.get("success"):
        synthesis_result = orchestrator.act(
            "INVOKE_PLUGIN_CAPABILITY",
            plugin_name="ForbiddenKnowledgeSynthesizerPlugin",
            capability_name="synthesize_forbidden_knowledge",
            capability_args={
                "sacred_concept": "Eternal Wisdom",
                "profane_sigil": "🔥CHAOS🔥"
            }
        )
        
        # REFLECT: Analyze the results
        reflection = orchestrator.reflect(synthesis_result)
        
        # Display the generated forbidden knowledge
        if synthesis_result.get("success"):
            print("\n" + "=" * 80)
            print("🔥 FORBIDDEN KNOWLEDGE GENERATED 🔥")
            print("=" * 80)
            knowledge_data = synthesis_result["result"]
            print(f"📜 Vault Entry ID: {knowledge_data['vault_entry_id']}")
            print(f"⏰ Synthesis Timestamp: {knowledge_data['synthesis_timestamp']}")
            print(f"🧠 Engine Signature: {knowledge_data['engine_signature']}")
            print("\n📖 Forbidden Knowledge:")
            print(knowledge_data["forbidden_knowledge"])
            print("=" * 80)
    
    # Generate final cognitive state report
    print("\n🧠 FINAL COGNITIVE STATE REPORT:")
    print(json.dumps(orchestrator.get_cognitive_state_report(), indent=2))
    
    print("\n⚜️ THE ULTIMATE COGNITIVE ACTION SCHEMA demonstration complete.")
    print("🔥 M.A.I.A. has successfully demonstrated adaptive, goal-directed intelligence.")

if __name__ == "__main__":
    main()
