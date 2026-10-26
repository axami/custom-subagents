# SupportOps — project memory
## Build & test
- `make test` runs pytest; `make lint` runs ruff. Always run both before proposing a commit.
## Conventions
- Python 3.11, type hints required, no prints in library code (use `logging`).
- Never commit secrets; config comes from env vars.
@docs/architecture.md
