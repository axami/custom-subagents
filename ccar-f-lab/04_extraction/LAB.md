# 04 — Extraction Pipeline
## Concepts
- **Structured output via tool_use**: define a tool whose `input_schema` IS your output schema and force it
  with `tool_choice={"type":"tool","name":"record_incident"}`. Read `block.input` — no text parsing.
- **Validation-retry loop**: validate with jsonschema/pydantic (business rules too); on failure send the
  errors back as a `tool_result` with `is_error: true` and ask for a corrected call. Cap retries (e.g. 2), then route to human review.
- Make uncertain fields **nullable** + add `confidence` so the model doesn't hallucinate to satisfy `required`.
- **Message Batches API**: async, ~50% cost, results within 24h, each request has `custom_id`.
  Use for non-urgent bulk work; NOT for interactive/latency-sensitive flows. Results may arrive in any order → join on `custom_id`.
## Steps
1. `python pipeline.py --offline` then live `python pipeline.py`.
2. `python batch.py submit` → `python batch.py status <id>` → `python batch.py results <id>`.
## Exam traps
- Prompt "respond in JSON" alone is weaker than forced tool_use with schema.
- Retrying without feeding back the specific validation error = same failure again.
