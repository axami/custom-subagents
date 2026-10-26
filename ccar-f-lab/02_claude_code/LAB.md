# 02 — Configure Claude Code
## Concepts — memory hierarchy (loaded at start, more specific wins on conflict)
| Level | Location | Shared via git? | Use for |
|---|---|---|---|
| Enterprise/managed policy | OS-level managed path set by IT | n/a | Org-wide mandatory rules |
| User | `~/.claude/CLAUDE.md` | No | Personal preferences across all projects |
| Project | `./CLAUDE.md` (or `./.claude/CLAUDE.md`) | **Yes** | Team conventions, build/test commands |
| Local project | `./CLAUDE.local.md` (git-ignored) | No | Your sandbox URLs, personal overrides |
| Subdirectory | `services/api/CLAUDE.md` | Yes | Loaded on demand when Claude works in that dir |
- `@path/to/file` imports another file into CLAUDE.md. `#` at the prompt / `/memory` edits memory.
- **Path rules** `.claude/rules/*.md`: frontmatter `paths:` globs → rule is applied only when Claude
  touches matching files. Keeps root CLAUDE.md small (context economy).
- **Skills** `.claude/skills/<name>/SKILL.md`: frontmatter `name`, `description` (what + WHEN — this is
  what Claude matches on), optional `allowed-tools`. Body + supporting files load only when invoked
  (progressive disclosure).
- **Subagents** `.claude/agents/*.md`: frontmatter `name`, `description`, `tools`, `model`; own context window.
- **Slash commands** `.claude/commands/*.md` (`$ARGUMENTS`). **Settings** `.claude/settings.json`: permissions allow/deny, hooks.

## Steps
1. `cd 02_claude_code && claude` → run `/memory` — confirm which files loaded.
2. Ask: "add an endpoint in services/api" → verify the api rule is applied; ask about `infra/` → it is not.
3. Ask "draft release notes for the last 5 commits" → the `release-notes` skill should trigger.
4. `/agents` → see `security-reviewer`; ask "use the security-reviewer on services/api".
5. Try `rm -rf build` → blocked by `settings.json` deny rule.
## Exam traps
- Personal prefs in project CLAUDE.md = wrong (affects team). Secrets in any CLAUDE.md = wrong.
- Vague skill `description` → skill never triggers. Fix the description, not the body.
- Huge root CLAUDE.md → wasted context every session; move scoped guidance to path rules.
