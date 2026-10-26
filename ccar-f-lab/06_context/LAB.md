# 06 — Context Management
## Concepts
- Context is a budget: every token of raw tool output competes with instructions. **Distil before you keep**:
  convert verbose output (logs, `ps`, JSON dumps) into a compact structured fact record, keep raw on disk.
- **Scratchpad / notes files**: persist progress (facts, decisions, open questions, next step) outside the
  window so work survives compaction, session restarts, or handoff (e.g. `NOTES.md`, `progress.json`).
- **Subagent delegation**: send noisy exploration to a subagent; return only a summary (see module 01).
- Also: put critical instructions in the system prompt; prompt caching for stable prefixes; trim old tool results;
  `/compact` and `/clear` in Claude Code.
## Steps
`python context_lab.py` — compares token estimate of raw vs distilled, writes `scratchpad.json`, then
simulates a "fresh session" that resumes using only the scratchpad.
## Exam traps
- "Use a bigger context window" is rarely the best answer; distil/delegate/persist is.
- Lost-in-the-middle: key facts buried in long transcripts get missed — surface them in structured notes.
