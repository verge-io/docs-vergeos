#!/usr/bin/env python3
"""Build migration/mapping.yaml: source .md -> {space, dest, group, title}.

Placement authority:
  - deploy/run/automate: parsed from the GitBook demo SUMMARY files (identity
    path mapping, already verified to exist in source).
  - product-guide files the demo omitted: routed by subdirectory to the same
    space/group the demo uses for that subdirectory.
  - knowledge-base posts: routed by frontmatter `slug` -> live Help Center group.
  - release-notes: grouped by version era (26.x -> 2026, 4.x -> 2025).
Run:  python3 migration/build_mapping.py
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/jasonyaeger/Workspaces/docs/docs"
DEMO = os.path.join(ROOT, "migration", "demo")

SPACE_IDS = {
    "home": "uJc5d3O7cwI7qD8muSyG",
    "deploy": "Q2bN3ctQdjv01GivTI08",
    "run": "pODKGSQETqL1gSqyxIq3",
    "automate": "sppYQkyIET58BuAo0kqm",
    "help-center": "QZBMFpokMv2vWTIRbFzA",
    "release-notes": "33mA7es4mQYkyUa7dMvu",
}

# product-guide subdir -> (space, group) for files the demo did not list
PG_SUBDIR_ROUTE = {
    "intro": ("run", "Platform overview"),
    "storage": ("run", "Storage"),
    "networks": ("run", "Networking"),
    "vpn": ("run", "VPN"),
    "auth": ("run", "Authentication"),
    "system": ("run", "System administration"),
    "nas": ("run", "NAS"),
    "maintenance-monitoring": ("run", "Maintenance and monitoring"),
    "operations": ("run", "Operations"),
    "tenants": ("run", "Tenants"),
    "virtual-machines": ("run", "Virtual machines"),
    "backup-dr": ("automate", "Backup and DR"),
    "automation": ("automate", "Automation"),
    "tools-integrations": ("automate", "Integrations and APIs"),
    "private-ai": ("automate", "Private AI"),
}

# Source files intentionally NOT ported 1:1 (handled elsewhere or dropped).
EXCLUDE = {
    "index.md",                      # home README is bespoke
    "how-to-write-a-verge-guide.md", # internal contributor doc
    "support.md",                    # folded into home/support-and-services.md
    "verge-bot.md",                  # folded into home/support-and-services.md
    "knowledge-base/index.md",       # blog landing
    "knowledge-base/template.md",    # blog template
}
EXCLUDE_PREFIX = ("product-guide/vsan/",)  # legacy dupes of product-guide/storage/*

def read_frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    fm = {}
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end != -1:
            block = txt[3:end]
            for line in block.splitlines():
                m = re.match(r'^([A-Za-z_][\w]*):\s*(.*)$', line)
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm, txt

def title_of(path):
    fm, txt = read_frontmatter(path)
    if fm.get("title"):
        return fm["title"]
    for line in txt.splitlines():
        m = re.match(r'^#\s+(.*)', line)
        if m:
            return m.group(1).strip()
    return os.path.splitext(os.path.basename(path))[0]

def parse_summary(space):
    """Yield (group, content_path, title) from a demo SUMMARY (skips README)."""
    path = os.path.join(DEMO, f"{space}__SUMMARY.md")
    group = None
    for line in open(path, encoding="utf-8"):
        m = re.match(r'^##\s+(.*)', line)
        if m:
            group = m.group(1).strip(); continue
        m = re.match(r'^\*\s+\[(.*?)\]\((.*?\.md)\)', line)
        if m:
            title, p = m.group(1), m.group(2)
            if p == "README.md":
                continue
            yield (group, p, title)

def all_source_md():
    out = []
    for dp, _, files in os.walk(SRC):
        for f in files:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, f), SRC)
                out.append(rel)
    return sorted(out)

def main():
    hc = json.load(open(os.path.join(DEMO, "helpcenter.json")))
    slug2group = hc["slug2group"]; group2prefix = hc["group2prefix"]

    rows = []          # {src, space, dest, group, title}
    mapped = set()     # source rel paths consumed

    # 1. deploy / run / automate from demo SUMMARYs
    for space in ("deploy", "run", "automate"):
        for group, cpath, title in parse_summary(space):
            src = cpath  # identity to source-relative
            if not os.path.isfile(os.path.join(SRC, src)):
                print(f"WARN demo path missing in source: {src}", file=sys.stderr); continue
            rows.append(dict(src=src, space=space, dest=cpath, group=group, title=title))
            mapped.add(src)

    # 2. remaining product-guide files -> subdir route
    for rel in all_source_md():
        if rel in mapped or rel in EXCLUDE: continue
        if any(rel.startswith(p) for p in EXCLUDE_PREFIX): continue
        if rel.startswith("product-guide/"):
            parts = rel.split("/")
            if len(parts) == 2:            # product-guide/<file>.md (e.g. ui-overview)
                space, group = ("run", "Platform overview")
            else:
                sub = parts[1]
                if sub not in PG_SUBDIR_ROUTE:
                    continue
                space, group = PG_SUBDIR_ROUTE[sub]
            rows.append(dict(src=rel, space=space, dest=rel, group=group,
                             title=title_of(os.path.join(SRC, rel))))
            mapped.add(rel)

    # 3. knowledge-base posts -> help-center by slug
    for rel in all_source_md():
        if rel in mapped or rel in EXCLUDE: continue
        if rel.startswith("knowledge-base/posts/"):
            fm, _ = read_frontmatter(os.path.join(SRC, rel))
            slug = fm.get("slug") or os.path.splitext(os.path.basename(rel))[0].lower()
            group = slug2group.get(slug)
            if not group:
                group = "Troubleshooting"  # safe default; reported below
            prefix = group2prefix[group]
            dest = f"{prefix}/{slug}.md"
            rows.append(dict(src=rel, space="help-center", dest=dest, group=group,
                             title=fm.get("title") or title_of(os.path.join(SRC, rel))))
            mapped.add(rel)

    # 4. release-notes -> by version era
    for rel in all_source_md():
        if rel in mapped or rel in EXCLUDE: continue
        if rel.startswith("release-notes/"):
            base = os.path.basename(rel)
            if base == "release-notes-overview.md":
                rows.append(dict(src=rel, space="release-notes", dest="README.md",
                                 group=None, title="Changelog"))
            else:
                ver = base.split("-")[0]
                era = "2026" if ver.startswith("26") else "2025"
                rows.append(dict(src=rel, space="release-notes",
                                 dest=f"{era}/{base}", group=era,
                                 title=title_of(os.path.join(SRC, rel))))
            mapped.add(rel)

    # 5. glossary -> home page
    if "glossary.md" in all_source_md() and "glossary.md" not in mapped:
        rows.append(dict(src="glossary.md", space="home", dest="glossary.md",
                         group=None, title="Glossary"))
        mapped.add("glossary.md")

    # ---- coverage report ----
    src_all = set(all_source_md())
    excluded = {r for r in src_all if r in EXCLUDE or any(r.startswith(p) for p in EXCLUDE_PREFIX)}
    unmapped = sorted(src_all - mapped - excluded)
    print(f"source .md total : {len(src_all)}")
    print(f"mapped           : {len(mapped)}")
    print(f"excluded         : {len(excluded)}")
    print(f"UNMAPPED         : {len(unmapped)}")
    for u in unmapped:
        print("   UNMAPPED:", u)
    # per-space counts
    from collections import Counter
    c = Counter(r["space"] for r in rows)
    print("per-space:", dict(c))
    # dest collisions
    seen = {}
    for r in rows:
        key = (r["space"], r["dest"])
        if key in seen:
            print("COLLISION:", key, "<-", r["src"], "and", seen[key])
        seen[key] = r["src"]

    # ---- emit mapping.yaml (hand-written, no yaml dep) ----
    out = os.path.join(ROOT, "migration", "mapping.yaml")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("# generated by build_mapping.py — source .md -> space placement\n")
        for r in sorted(rows, key=lambda r: (r["space"], r["dest"])):
            g = "" if r["group"] is None else r["group"]
            fh.write("- src: %s\n  space: %s\n  dest: %s\n  group: %r\n  title: %r\n" %
                     (r["src"], r["space"], r["dest"], g, r["title"]))
    json.dump(rows, open(os.path.join(ROOT, "migration", "mapping.json"), "w"), indent=1)
    print("wrote", out, "and mapping.json (", len(rows), "rows )")

if __name__ == "__main__":
    main()
