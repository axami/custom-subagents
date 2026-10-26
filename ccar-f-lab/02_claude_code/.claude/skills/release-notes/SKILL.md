---
name: release-notes
description: Generate customer-facing release notes from git commits. Use when the user asks for release notes, a changelog, or "what changed" between versions/tags.
allowed-tools: Bash(git log:*), Bash(git tag:*), Read
---
# Release notes
1. Run `git log --oneline <from>..<to>` (default: last tag..HEAD).
2. Group into Features / Fixes / Breaking changes using `template.md`.
3. Plain English; omit internal refactors.
