# Memory — Suriota Project Knowledge Base

This directory mirrors the project knowledge base from Claude Code's per-project memory (`~/.claude/projects/.../memory/`). It contains architecture notes, deploy decisions, audit findings, and the active sitewide snippet inventory.

**Two sensitive files are deliberately excluded** from this public mirror:
- `suriota_wp_admin_credentials.md` — wp-admin password
- `suriota_wp_rest_access.md` — Application Password + REST auth patterns

Those stay local-only in `~/.claude/projects/C--Users-Administrator-Music-Website-Suriota/memory/`.

## Index

See [`MEMORY.md`](MEMORY.md) for the canonical index.

## How to use

When picking up work on suriota.com after a break:
1. Read `MEMORY.md` first — it's the table of contents
2. Read the entries matching what you're about to touch (e.g., `suriota_active_snippets.md` before editing snippets)
3. After making changes, update the matching memory file + sync to this directory

## Update procedure

```bash
# After updating ~/.claude/projects/.../memory/*.md
cp ~/.claude/projects/C--Users-Administrator-Music-Website-Suriota/memory/*.md docs/memory/
# Manually exclude the 2 credential files from docs/memory/
rm -f docs/memory/suriota_wp_admin_credentials.md docs/memory/suriota_wp_rest_access.md
# Strip refs from MEMORY.md
sed -i '/suriota_wp_admin_credentials\.md/d; /suriota_wp_rest_access\.md/d' docs/memory/MEMORY.md
```
