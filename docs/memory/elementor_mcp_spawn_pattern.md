---
name: elementor-mcp spawn pattern on Windows
description: Claude Code reads MCP servers from `~/.claude.json` (NOT `~/.claude/settings.json`). On Windows 2.1.112+, spawn Node stdio MCPs via direct `node.exe`, not `cmd /c node`.
type: project
originSessionId: 10f3b6ac-1875-49ee-b76d-e6a925d66119
---
**Config file:** MCP servers must be added to `~/.claude.json` (the user's master config), NOT `~/.claude/settings.json`. Use `claude mcp add <name> --scope user <command> -- <args...>` to write to the correct file. On 2026-05-16 the elementor-mcp entry was placed only in `settings.json` and was silently ignored — `claude mcp list` did not show it. Adding via CLI to `.claude.json` made it appear and connect immediately.

**Spawn pattern:** `elementor-mcp` must use direct `node.exe` invocation, not `cmd /c node`:

```json
"elementor-mcp": {
  "type": "stdio",
  "command": "C:/Program Files/nodejs/node.exe",
  "args": ["C:/Users/Administrator/.kimi/mcp-wrappers/elementor-mcp-wrapper.js"]
}
```

**Why:** On 2026-05-16 the wrapper started failing — log showed "wrapper started" → "stdin ended" within 5ms, no `initialize` received. Yesterday (2026-05-14/15) the same wrapper handled 500+ requests successfully. Reproduction: piping `initialize` JSON-RPC directly to `node wrapper.js` returns a proper response with server info ("MCP Tools for Elementor v1.4.3"), so the wrapper code and WordPress endpoint (`https://suriota.com/wp-json/mcp/elementor-mcp-server`) are both healthy. The regression is in how Claude Code's MCP runtime forwards stdio through `cmd /c`. Other MCPs using `cmd /c npx -y …` still work because npx forks a grandchild process with its own stdio inheritance.

**How to apply:** Whenever spawning a Node-based stdio MCP on Windows from Claude Code, use the full `node.exe` path directly. Avoid `cmd /c node script.js`. If a previously-working MCP suddenly fails with "stdin ended" right after spawn and no incoming `initialize`, check the spawn command pattern first before suspecting the wrapper code.
