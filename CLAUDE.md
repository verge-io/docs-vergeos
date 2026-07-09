# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **GitBook Git Sync monorepo**. Each top-level directory is the _Project directory_
for one GitBook space of the **VergeOS Docs** site. There is no app to build, lint, or
test — GitBook renders the content when each space's Project directory is synced. The
content was ported from the MkDocs source site at `/Users/jasonyaeger/Workspaces/docs/docs`
by the scripts in `migration/`.

GitBook target: org **Verge.io** (`FpusSnrkRHyZiVEsXf9X`), site **VergeOS Docs**
(`site_1U4gk`, published at `https://verge-io.gitbook.io/vergeos-docs/`).

## Space directories and IDs

Each dir below git-syncs to one space. The **space IDs are load-bearing**: cross-space
links are written as `https://app.gitbook.com/s/<spaceId>/<dest-path-without-.md>`, so
any new cross-space link must use the correct ID.

| Dir              | GitBook space                                      | Space ID               |
| ---------------- | -------------------------------------------------- | ---------------------- |
| `home/`          | Home                                               | `uJc5d3O7cwI7qD8muSyG` |
| `deploy/`        | Plan and deploy                                    | `Q2bN3ctQdjv01GivTI08` |
| `run/`           | Run the platform                                   | `pODKGSQETqL1gSqyxIq3` |
| `automate/`      | Automate, protect, and extend                      | `sppYQkyIET58BuAo0kqm` |
| `learn/`         | Learn the platform (space still titled "Training") | `qLUTTK5fxfW4S9FoS9GE` |
| `knowledge-base/` | Knowledge Base                                    | `QZBMFpokMv2vWTIRbFzA` |
| `release-notes/` | Release notes                                      | `33mA7es4mQYkyUa7dMvu` |

The site also has an **API Reference** space that is intentionally NOT in this repo — it
has no source equivalent and is edited directly in GitBook. (**Training** previously had no
source equivalent; it now lives here as `learn/`, ported from the `vergeos-technical-training`
repo. Its **Learn the platform** section — `sitesc_pD33P` — already exists on the site; the
remaining step is repointing that space's Git Sync at this repo's `learn/` directory.)

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
SPACES="home deploy run automate knowledge-base release-notes"
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

## Important: Git Sync direction

Connecting Git Sync makes this repo the source of truth and the **first sync overwrites
the existing space content**. Pilot one space (`deploy/`, smallest) and verify the GitBook
preview before wiring the rest.
