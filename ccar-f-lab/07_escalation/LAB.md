# 07 — Escalation Patterns
## Decision rule
Resolve autonomously only when **all** are true: policy explicitly covers it, action is reversible/low-risk,
you have the permissions, and confidence is high. Otherwise escalate with a **handoff package**.
| Trigger | Example | Action |
|---|---|---|
| Policy gap | Refund for a case policy doesn't mention | Escalate — don't invent policy |
| Customer explicitly requests a human | "Let me speak to a person" | Escalate promptly (honour it) |
| Inability to progress | Same tool error 3×, loop/max turns, missing access | Escalate with what was tried |
| High-risk / irreversible | Delete prod data, change > authority limit | Human approval |
| Low confidence / conflicting data | Two sources disagree | Ask clarifying Q or escalate |
| Covered, reversible, confident | Restart non-prod service per runbook | Resolve, log it |
Handoff package: summary, customer ask, evidence, steps tried, why escalating, suggested next step — so the human doesn't restart.
## Steps
`python escalation.py` — runs a deterministic policy engine over 8 scenarios; compare with your own answer first.
`python escalation.py --llm` — same via Claude with an `escalate_to_human` tool.
## Exam traps
- Escalating everything = also wrong (defeats automation). Sentiment alone ≠ escalation unless policy says so.
- Don't loop retrying when progress is impossible; don't hide failure from the user.
