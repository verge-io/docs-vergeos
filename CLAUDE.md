# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **GitBook Git Sync monorepo**. Each top-level directory is the _Project directory_
for one GitBook space of the **VergeOS Docs** site. There is no app to build, lint, or
test — GitBook renders the content when each space's Project directory is synced. The
content was ported from the MkDocs source site at `/Users/jasonyaeger/Workspaces/docs/docs`
by the scripts in `migration/`.

GitBook target: org **Verge.io** (`FpusSnrkRHyZiVEsXf9X`), site **VergeOS Docs**
(`site_1U4gk`, published at `https://docs.verge.io/` — the old
`verge-io.gitbook.io/vergeos-docs` URL redirects there).

## Space directories and IDs

Each dir below git-syncs to one space. The **space IDs are load-bearing**: cross-space
links are written as `https://app.gitbook.com/s/<spaceId>/<page-path>`, where
`<page-path>` is the page's **GitBook page path** (from the space's SUMMARY group slug +
page slug, e.g. `system-administration/running-updates`), NOT the repo file path. GitBook
resolves these to published-site URLs **at import time**; a path that doesn't match a real
page in the target space is silently left as a literal `app.gitbook.com` URL, which sends
readers to the GitBook login. Verify paths against the content API
(`/v1/spaces/{spaceId}/content`, the `path` field). If a link's target page didn't exist
yet when the linking page last synced, the linking file must be touched (any content
change) to force re-import and re-resolution.

`.claude/scripts/check-cross-space-links.sh` validates every cross-space link in the repo
against the live content API; `--published` additionally scans the published pages for
unresolved `app.gitbook.com` anchors. Run it after renaming pages or SUMMARY groups
(page paths drift) and before merging link-heavy changes.

| Dir               | GitBook space                 | Space ID               | Published under                        |
| ----------------- | ----------------------------- | ---------------------- | -------------------------------------- |
| `home/`           | Home                          | `uJc5d3O7cwI7qD8muSyG` | `docs.verge.io/`                       |
| `deploy/`         | Plan and deploy               | `Q2bN3ctQdjv01GivTI08` | `docs.verge.io/plan-and-deploy/`       |
| `run/`            | Run the platform              | `pODKGSQETqL1gSqyxIq3` | `docs.verge.io/run-the-platform/`      |
| `automate/`       | Automate, protect, and extend | `sppYQkyIET58BuAo0kqm` | `docs.verge.io/automate-protect-and-extend/` |
| `learn/`          | Learn the platform            | `qLUTTK5fxfW4S9FoS9GE` | `docs.verge.io/learn-the-platform/`    |
| `knowledge-base/` | Knowledge Base                | `QZBMFpokMv2vWTIRbFzA` | `docs.verge.io/knowledge-base/`        |
| `release-notes/`  | Release notes                 | `33mA7es4mQYkyUa7dMvu` | `docs.verge.io/release-notes/`         |

A page's published URL is its "Published under" base + its GitBook page path
(e.g. `run/product-guide/system/running-updates.md` →
`docs.verge.io/run-the-platform/system-administration/running-updates`).

The site also has an **API Reference** space that is intentionally NOT in this repo — it
has no source equivalent and is edited directly in GitBook. (`learn/` was ported from the
`vergeos-technical-training` repo; its space's Git Sync is active against this repo.)

## Per-space layout (GitBook conventions)

Every space dir contains:

- `.gitbook.yaml` — always `root: ./` + `structure.readme: README.md` + `structure.summary: SUMMARY.md`.
- `README.md` — the space root page. Frontmatter uses `description` + `icon` (FontAwesome name).
- `SUMMARY.md` — the table of contents and the source of truth for sidebar order/titles:
  `# Table of contents`, then `## Group Name` headers create sidebar groups, and
  `* [Title](relative/path.md)` bullets are pages. The link text — not the page H1 — is
  what GitBook shows in the sidebar.
- Content `.md` files, which **preserve the original MkDocs source paths** (e.g.
  `run/product-guide/storage/overview.md`, `deploy/implementation-guide/intro.md`).
- `.gitbook/assets/` — images for that space, stored **flat** in GitBook's canonical
  per-space asset directory (GitBook does not share assets across spaces). This is where
  GitBook's Git Sync write-back copies every referenced image and the path it rewrites all
  `![…](…)` / `<img src="…">` references to point at — so **new images must go in
  `<space>/.gitbook/assets/` and be referenced as `../.gitbook/assets/<name>`** (relative to
  the page), or the next sync will re-home them and produce churn. The migration-era
  `assets/screenshots/` layout has been pruned (its files were byte-identical duplicates of
  the `.gitbook/assets/` copies); do not reintroduce it.

When adding/moving a page, update that space's `SUMMARY.md` too, or it won't appear.

## Migration tooling (`migration/`)

One-time port from the MkDocs source. `migration/demo/` holds the GitBook-generated
reference repo's SUMMARYs/READMEs and the live Knowledge Base slug→group map, which are the
authority for page placement.

```bash
python3 migration/build_mapping.py   # source .md -> {space, dest, group, title}; writes mapping.yaml/.json
python3 migration/convert.py         # convert + write content, copy assets, generate SUMMARY/README
```

`convert.py` overwrites content but does not delete stale files. For a pristine rebuild
of a space first run:

```bash
find <space> -mindepth 1 -not -name .gitbook.yaml -delete
```

`build_mapping.py` prints a coverage report (mapped / excluded / UNMAPPED / collisions) —
UNMAPPED must be 0. Placement rules: `deploy`/`run`/`automate` come from the demo
SUMMARYs; other `product-guide/*` route by subdirectory; KB posts route by frontmatter
`slug` → live Knowledge Base group; release notes group by version era (26.x→2026, 4.x→2025).

### Conversion rules (MkDocs → GitBook), all in `convert.py`

- Admonitions `!!! type "Title"` / `???` → `{% hint style="info|success|warning|danger" %}` (see `STYLE` map).
- Content tabs `=== "Tab"` → `{% tabs %}{% tab %}…`.
- Frontmatter: drops `template:` and `draft:`, keeps the rest.
- Links: same-space → relative `.md`; cross-space → `app.gitbook.com/s/<id>/…`;
  `/knowledge-base/<slug>` resolves via the slug map; folded targets (`/support`, etc.)
  use the `REDIRECT` table.
- Images: `convert.py` copies them into the space `assets/` with parens/spaces stripped.
  Note this is migration-era behavior — on sync GitBook re-homes images to
  `<space>/.gitbook/assets/` (see the per-space layout section); a fresh rebuild would need
  its output re-homed there to match the current convention.

## Validating a rebuild

After re-running the converter, these must all come back clean:

```bash
SPACES="home deploy run automate learn knowledge-base release-notes"
grep -rEl '^[[:space:]]*([!]{3}|[?]{3})' $SPACES   # leftover admonitions (expect none)
grep -rEl '^[[:space:]]*=== "' $SPACES             # leftover content tabs (expect none)
grep -rhoE '\]\((/assets/|/product-guide/|\.\./assets/)[^)]*\)' $SPACES  # unrewritten asset paths (expect none)
```

`convert.py` itself reports `link misses` (must be 0) and broken-image counts.

## GitBook API

`.env.local` holds `GITBOOK_API_TOKEN` (gitignored). To query the API:

```bash
source .env.local
curl -s -H "Authorization: Bearer $GITBOOK_API_TOKEN" "https://api.gitbook.com/v1/orgs/FpusSnrkRHyZiVEsXf9X/sites/site_1U4gk/structure"
```

Useful endpoints: `/v1/orgs/{org}/sites/{site}/structure` (sections + spaces),
`/v1/spaces/{spaceId}/content` (page tree).

## Git Sync status and direction

All seven spaces have **active Git Sync** against this repo (`main` branch). Sync is
one-way GitHub → GitBook: this repo is the source of truth, and GitBook does not push
back. If a new space is ever connected, note the **first sync overwrites the existing
space content** — verify the GitBook preview before wiring it.
