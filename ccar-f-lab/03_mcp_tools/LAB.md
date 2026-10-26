# 03 — Design & Test MCP Tools
## Concepts
- MCP server exposes **tools** (model-invoked actions), **resources** (app-attached read data), **prompts** (user-invoked templates).
  Transports: stdio (local) / Streamable HTTP (remote).
- **Tool descriptions are prompts.** For similar tools state: what it does, when to use it, when NOT to
  (name the sibling), input format with examples, what it returns. Prefer fewer, higher-level tools over many thin ones.
- **Structured errors**: return machine-readable `{error_code, message, retryable, suggestion}` with `isError`
  so the model can self-correct instead of guessing.
## Steps
1. `python server.py` (stdio) — or `mcp dev server.py` for the Inspector UI.
2. `python test_tools.py` — unit-tests descriptions (distinctness) and error contract without a model.
3. Register in Claude Code: `claude mcp add supportops -- python 03_mcp_tools/server.py`, then ask
   "find tickets about VPN" vs "get ticket INC0012" — check the right tool is chosen.
## Experiments
- Rewrite both search descriptions as "Search tickets." → watch tool selection become random.
- Return a bare string "error" → the model retries blindly. Compare with structured error.
## Exam traps
- Fix wrong-tool selection by improving **descriptions** first (not by adding system-prompt hacks).
- Don't leak stack traces/secrets in errors. Validate inputs server-side even if the schema exists.
