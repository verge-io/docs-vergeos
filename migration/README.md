# Migration tooling (one-time)

Ports the VergeOS MkDocs site (`/Users/jasonyaeger/Workspaces/docs/docs`) into this
GitBook Git Sync monorepo. Each top-level dir (`home/ deploy/ run/ automate/
knowledge-base/ release-notes/`) is the Project directory for one GitBook space of
the **VergeOS Docs** site (org `Verge.io`, site `site_1U4gk`).

## Re-run

```bash
python3 migration/build_mapping.py   # source .md -> space placement (mapping.yaml/.json)
python3 migration/convert.py         # convert + write content, assets, SUMMARY, README
```

`convert.py` overwrites each space's content (it does not delete stale files; clean
with `find <space> -mindepth 1 -not -name .gitbook.yaml -delete` first for a pristine build).

## What it does

- Placement mirrors the GitBook-generated demo repo `gitbook-demo-sites/verge-demo-site-20260608`
  (`migration/demo/` holds its SUMMARYs/READMEs). Knowledge Base routing uses the live
  space's slug→group map (`migration/demo/helpcenter.json`).
- Converts MkDocs → GitBook: admonitions `!!!/???` → `{% hint %}`, content tabs
  `=== "x"` → `{% tabs %}`, drops `template:`/`draft:` frontmatter, strips abbr/attr_list.
- Rewrites assets into each space's `assets/` and rewrites image paths; same-space
  links stay relative, cross-space links become `https://app.gitbook.com/s/<id>/...`.

## Excluded from the port

- Training and API Reference spaces (no source equivalent — managed in GitBook).
- `index.md`, `how-to-write-a-verge-guide.md`, `knowledge-base/{index,template}.md`,
  `product-guide/vsan/*` (legacy dupes). `support.md`/`verge-bot.md` are folded into
  `home/support-and-services.md`.

## Next step: connect Git Sync

In GitBook, configure Git Sync per space with the matching Project directory. First
sync makes the repo the source of truth and overwrites current space content — pilot
`deploy/` first, verify the preview, then wire the rest.
