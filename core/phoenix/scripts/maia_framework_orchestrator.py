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
    
    def _resolve_trusted_plugin_path(self, plugin_path):
        """
        Resolve a plugin path and enforce containment in a trusted directory.

        realpath resolves symlinks before containment is checked, while
        commonpath avoids unsafe string-prefix comparisons such as
        '/trusted-elsewhere' matching '/trusted'.
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
        if not os.path.isfile(resolved_path):
            raise FileNotFoundError("Plugin file does not exist or is not a regular file")

        for trusted_dir in self.trusted_plugin_dirs:
            if not os.path.isdir(trusted_dir):
                continue
            try:
                if os.path.commonpath((trusted_dir, resolved_path)) == trusted_dir:
                    return resolved_path
            except ValueError:
                # Different drives or incompatible path roots are not trusted.
                continue

        raise PermissionError("Plugin path is outside all trusted plugin directories")

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
            spec = importlib.util.spec_from_file_location(module_name, resolved_path)
            if spec is None or spec.loader is None:
                raise ImportError("Unable to create a loader for the plugin file")

            plugin_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = plugin_module
            spec.loader.exec_module(plugin_module)

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
