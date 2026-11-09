# M.A.I.A. Plugin Trust Boundary

## Why this exists

M.A.I.A. loads Python plugin files with `importlib`. Importing a Python file executes its top-level code with the privileges of the orchestrator process. A plugin directory is therefore an execution trust boundary, not merely a discovery location.

## Allowed locations

`MAIAFrameworkOrchestrator` accepts an optional `trusted_plugin_dirs` iterable. When omitted, the existing demonstration locations remain available:

- `/home/ubuntu/plugins`
- `./plugins`
- `./maia_plugins`

An explicit list replaces those defaults. A single string is rejected so it cannot accidentally be interpreted as a sequence of individual path characters. The filesystem root is not accepted as a trust directory.

## Path validation

Before import, the orchestrator:

1. Expands the user path and resolves it to a canonical absolute path with `realpath`.
2. Requires a regular `.py` file.
3. Resolves each configured trust directory and requires it to exist as a directory.
4. Uses `commonpath` containment rather than string-prefix matching.
5. Rejects paths outside all configured roots. Symlinks resolving outside a trusted root are rejected.
6. Requires the trusted root and every descendant directory, plus the plugin file, to be non-writable by group/other. The trusted root must be owned by the service user or root; ancestor directories are checked up to the filesystem root, rejecting group/other-writable ancestors unless the sticky bit prevents other users from replacing children.
7. Opens the validated file with no-follow semantics where supported, checks the opened descriptor against the current path entry, and compiles the exact bytes read from that descriptor. A pathname swap between validation and import is rejected rather than reopened by an import loader.
8. Preserves the module's `__file__` location metadata for plugins that resolve resources relative to their source file.
9. Rejects duplicate plugin names rather than silently replacing an already registered plugin.

The plugin manifest must be a dictionary with a non-empty string `name`. A failed import or invalid manifest is not registered and its temporary module entry is removed from `sys.modules`.

## Operational requirements

- Keep trusted plugin directories writable only by authorized operators.
- Do not place unreviewed downloads or user uploads in a trusted plugin directory.
- Review plugin source before adding it to an allowlisted directory.
- The permission checks do not isolate processes sharing the same operating-system identity. Keep trusted directories and their contents writable only by authorized operators. The descriptor check narrows pathname replacement races, but it is not a substitute for a separately privileged process boundary.
- The allowlist does **not** sandbox plugin code. A trusted plugin can still read files, access the network, spawn processes, or modify data allowed to the orchestrator process.
- For untrusted or multi-tenant plugins, use a separate process or container with reduced OS permissions and explicit IPC instead of in-process import.

## Verification

`tests/test_maia_plugin_security.py` covers empty paths, parent traversal, symlink escape, sibling-prefix confusion, non-Python files, invalid manifests, group/world-writable roots/files, pathname replacement after open, duplicate plugin names, and successful registration/invocation of a trusted fixture.

The focused GitHub Actions workflow is `MAIA Plugin Trust Tests`. The broader Phoenix Audit also discovers the `tests/` directory.
