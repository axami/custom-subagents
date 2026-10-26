# 01 — Build an Agent with the SDK
## Concepts
- **Agentic loop**: call model → if `stop_reason == "tool_use"` execute every `tool_use` block →
  append ONE user message containing all `tool_result` blocks (matching `tool_use_id`) → repeat.
  Stop on `end_turn`; handle `max_tokens` (continue/raise budget) and `pause_turn`/`refusal` explicitly.
- **Error handling layers**: (1) API errors (429/529/5xx → retry with exponential backoff + jitter;
  400 → fix request, don't retry); (2) tool errors → return `tool_result` with `is_error: true` and an
  actionable message so the *model* can recover; (3) loop guards → max iterations, token/cost budget.
- **Subagents**: a fresh conversation with its own narrow system prompt + tool subset; the parent sees
  only the subagent's **summary**, keeping parent context small. Use for isolatable, parallelisable work.
- **Session management**: the API is stateless — *you* persist `messages`. Save to disk after each turn,
  resume by reloading; trim/summarise old turns when nearing the context limit.
- **Claude Agent SDK** (`claude-agent-sdk`) packages the same loop + built-in tools, subagents,
  sessions (`resume`), hooks, permissions. This lab builds it by hand first so you understand it.

## Steps
1. `python agent.py --offline` — trace the loop with a scripted model.
2. `python agent.py "Server lnx-web-07 is slow, investigate"` — live run.
3. `python agent.py --resume <session_id> "now check disk too"` — session resume.
4. Read `run_subagent()` — note the parent only receives a text summary.

## Experiments
- Make `get_metrics` raise → watch the model react to `is_error`.
- Set `MAX_TURNS=2` → see the guard fire. Remove it → understand runaway-loop risk.
- Return tool results as separate user messages → API 400. Why? (all results go in one message)

## Exam traps
- Parallel tool calls: multiple `tool_use` blocks in one response — answer **all** of them.
- Don't retry a tool error at the API layer; surface it to the model.
- `tool_choice`: `auto` / `any` / `{"type":"tool","name":...}` / `none`.
