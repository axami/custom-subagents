# CCAR-F Hands-On Lab — "SupportOps Agent"
One running project, eight modules. Each module builds on a shared scenario: an internal
**IT/CloudOps support agent** that triages tickets, queries systems via tools/MCP,
extracts structured data, manages context, and escalates correctly.

## Setup (≈10 min)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export CLAUDE_MODEL=claude-sonnet-4-5      # any current model you have access to
npm install -g @anthropic-ai/claude-code   # for module 02
```
Modules 01/04/05/06/07 also run in `--offline` mode (mock client) so you can study the
control flow without an API key.

## Study plan (4 weeks, ~1 h/day)
| Week | Modules | Exit check |
|---|---|---|
| 1 | 01 Agent loop, 03 MCP tools | You can explain every `stop_reason` and what the loop does for each |
| 2 | 04 Extraction, 05 Prompting | Pipeline passes validation on all 6 sample docs; batch job submitted |
| 3 | 02 Claude Code, 06 Context | Rules load only for matching paths; scratchpad survives a "reset" |
| 4 | 07 Escalation, 08 Exam ×3 | ≥80% in every domain on two consecutive exam runs |

Each module folder has a `LAB.md`: **Concepts → Steps → Experiments (break it on purpose) → Exam traps**.
