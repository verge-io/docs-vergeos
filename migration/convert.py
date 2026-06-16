#!/usr/bin/env python3
"""Convert source MkDocs markdown into the GitBook multi-space monorepo.

Reads migration/mapping.json, transforms each source file (admonitions -> hints,
content tabs -> {% tabs %}, frontmatter cleanup, asset + cross-space link
rewriting), writes content into each space dir, copies referenced assets, and
generates SUMMARY.md / README.md per space.

Run:  python3 migration/convert.py
"""
import os, re, json, shutil, sys
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/jasonyaeger/Workspaces/docs/docs"
DEMO = os.path.join(ROOT, "migration", "demo")

SPACE_IDS = {
    "home": "uJc5d3O7cwI7qD8muSyG", "deploy": "Q2bN3ctQdjv01GivTI08",
    "run": "pODKGSQETqL1gSqyxIq3", "automate": "sppYQkyIET58BuAo0kqm",
    "help-center": "QZBMFpokMv2vWTIRbFzA", "release-notes": "33mA7es4mQYkyUa7dMvu",
}
GROUP_ORDER = {
    "deploy": ["Implementation guide", "Reference architectures"],
    "automate": ["Backup and DR", "Automation", "Integrations and APIs",
                 "Private AI", "Shared admin surfaces"],
    "help-center": ["Getting Started & Installation", "Virtual Machines", "Networking",
                    "Storage & vSAN", "Tenants", "Backup & DR", "Automation & API",
                    "System Administration", "Troubleshooting"],
    "release-notes": ["2026", "2025"],
}  # run order is taken from its demo SUMMARY headers
SECTION_ICON = {"home": "house", "deploy": "compass-drafting", "run": "server",
                "automate": "robot", "help-center": "life-ring", "release-notes": "notes"}

# ---------------------------------------------------------------- transforms
ADM_RE = re.compile(r'^(?P<indent>[ \t]*)(?P<marker>!!!|\?\?\?\+?)\s+(?P<type>[\w-]+)(?:\s+"(?P<title>.*)")?\s*$')
TAB_RE = re.compile(r'^(?P<indent>[ \t]*)=== +"(?P<title>.*)"\s*$')
STYLE = {
    'note': 'info', 'info': 'info', 'abstract': 'info', 'summary': 'info', 'tldr': 'info',
    'tip': 'success', 'hint': 'success', 'important': 'success', 'success': 'success',
    'check': 'success', 'done': 'success',
    'question': 'info', 'help': 'info', 'faq': 'info', 'example': 'info',
    'quote': 'info', 'cite': 'info', 'seealso': 'info',
    'warning': 'warning', 'caution': 'warning', 'attention': 'warning',
    'danger': 'danger', 'error': 'danger', 'bug': 'danger', 'failure': 'danger',
    'fail': 'danger', 'missing': 'danger',
}

def _indent_width(line):
    return len(line[:len(line) - len(line.lstrip())].expandtabs(4))

def _collect_body(lines, i, base):
    """Collect lines after an opener: blanks + lines indented deeper than base."""
    body = []
    n = len(lines)
    while i < n:
        ln = lines[i]
        if ln.strip() == '':
            body.append(''); i += 1; continue
        if _indent_width(ln) > base:
            body.append(ln); i += 1
        else:
            break
    return body, i

def _dedent(body, width):
    out = []
    for ln in body:
        if ln.strip() == '':
            out.append('')
        else:
            exp = ln.expandtabs(4)
            out.append(exp[width:] if len(exp) >= width else exp.lstrip())
    while out and out[0] == '':
        out.pop(0)
    while out and out[-1] == '':
        out.pop()
    return out

def convert_admonitions(text):
    lines = text.split('\n'); out = []; i = 0; n = len(lines)
    while i < n:
        m = ADM_RE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent = m.group('indent'); base = _indent_width(lines[i])
        style = STYLE.get(m.group('type').lower(), 'info')
        title = m.group('title')
        body, i = _collect_body(lines, i + 1, base)
        inner = convert_admonitions('\n'.join(_dedent(body, base + 4))).split('\n')
        out.append(indent + '{%% hint style="%s" %%}' % style)
        if title and title.strip():
            out.append(indent + '**' + title.strip() + '**')
            out.append(indent)
        out.extend((indent + ln) if ln else '' for ln in inner)
        out.append(indent + '{% endhint %}')
        out.append('')
    return '\n'.join(out)

def convert_tabs(text):
    lines = text.split('\n'); out = []; i = 0; n = len(lines)
    while i < n:
        m = TAB_RE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent = m.group('indent'); base = _indent_width(lines[i])
        tabs = []
        while i < n:
            m2 = TAB_RE.match(lines[i])
            if not m2 or _indent_width(lines[i]) != base:
                break
            title = m2.group('title'); i += 1
            body, i = _collect_body(lines, i, base)
            tabs.append((title, _dedent(body, base + 4)))
        out.append(indent + '{% tabs %}')
        for title, db in tabs:
            out.append(indent + '{%% tab title="%s" %%}' % title)
            out.extend((indent + x) if x else '' for x in db)
            out.append(indent + '{% endtab %}')
            out.append('')
        out.append(indent + '{% endtabs %}')
        out.append('')
    return '\n'.join(out)

def clean_frontmatter(text):
    if not text.startswith('---'):
        return text
    end = text.find('\n---', 3)
    if end == -1:
        return text
    block = text[3:end + 1]
    rest = text[end + 4:]
    kept = []
    for line in block.splitlines():
        key = re.match(r'^([A-Za-z_][\w]*):', line)
        if key and key.group(1) in ('template', 'draft'):
            continue
        kept.append(line)
    fm = '\n'.join(l for l in kept if l.strip() != '' or True).strip('\n')
    return '---\n' + fm + '\n---' + rest

def strip_mkdocs(text):
    out = []
    for line in text.split('\n'):
        if re.match(r'^\*\[[^\]]+\]:\s', line):   # abbr/tooltip definitions
            continue
        line = re.sub(r'\{:?\s*\.[^}]*\}', '', line)  # attr_list e.g. { .md-button }
        out.append(line)
    return '\n'.join(out)

# ---------------------------------------------------------------- link/image rewriting
IMG_RE = re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<url>(?:[^()]|\([^()]*\))*)\)')
LINK_RE = re.compile(r'(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\)')

def build_indices(rows):
    src2dests = defaultdict(list)      # src -> [(space, dest)]
    for r in rows:
        src2dests[r['src']].append((r['space'], r['dest']))
    kbslug2 = {}
    for r in rows:
        if r['space'] == 'help-center':
            slug = os.path.splitext(os.path.basename(r['dest']))[0]
            kbslug2[slug] = (r['space'], r['dest'])
    return src2dests, kbslug2

# folded / section-landing targets -> a concrete page (keys: source-rel, no .md)
REDIRECT = {
    'support': ('home', 'support-and-services.md'),
    'verge-bot': ('home', 'support-and-services.md'),
    'index': ('home', 'README.md'),
    'glossary': ('home', 'glossary.md'),
    'knowledge-base': ('help-center', 'README.md'),
    'knowledge-base/index': ('help-center', 'README.md'),
    'knowledge-base/category/api-reference': ('help-center', 'README.md'),
    'release-notes': ('release-notes', 'README.md'),
    'reference-architecture': ('deploy', 'README.md'),
    'product-guide/storage': ('run', 'README.md'),
    # stale source slug -> current Help Center page
    'knowledge-base/posts/understanding-vsan-growth':
        ('help-center', 'storage-vsan/understanding-and-explaining-unexpected-vsan-growth.md'),
}

def resolve_doc(target, src_rel, src2dests, kbslug2):
    anchor = ''
    if '#' in target:
        target, a = target.split('#', 1); anchor = '#' + a
    target = target.split('?', 1)[0].strip()
    if not target:
        return None, anchor
    if target.startswith('/'):
        sp = target[1:].rstrip('/')
    else:
        sp = os.path.normpath(os.path.join(os.path.dirname(src_rel), target)).rstrip('/')
    # 1. file-path resolution (relative/absolute, with or without .md)
    cand = sp if sp.endswith('.md') else sp + '.md'
    if cand in src2dests:
        return src2dests[cand], anchor
    # 2. published KB slug URL: /knowledge-base/<slug>
    if 'knowledge-base' in sp:
        slug = sp.split('/')[-1]
        if slug in kbslug2:
            return kbslug2[slug], anchor
    # 3. folded/section redirect
    key = sp[:-3] if sp.endswith('.md') else sp
    if key in REDIRECT:
        return [REDIRECT[key]], anchor
    return None, anchor

def make_doc_link(hit, anchor, cur_space, cur_dest):
    # hit is either a single (space,dest) tuple (KB) or a list of them
    cands = hit if isinstance(hit, list) else [hit]
    chosen = next((c for c in cands if c[0] == cur_space), cands[0])
    space2, dest2 = chosen
    if space2 == cur_space:
        rel = os.path.relpath(dest2, os.path.dirname(cur_dest) or '.')
        return rel + anchor
    p = dest2[:-3] if dest2.endswith('.md') else dest2
    if os.path.basename(p) == 'README':
        p = os.path.dirname(p)
    return 'https://app.gitbook.com/s/%s/%s%s' % (SPACE_IDS[space2], p, anchor)

def resolve_image(url, src_rel, space, dest, asset_jobs):
    url = url.strip()
    if url.startswith(('http://', 'https://', 'data:')):
        return None
    raw = url.split(' ', 1)[0].split('#', 1)[0].split('?', 1)[0]
    if raw.startswith('/'):
        sp = raw[1:]
    else:
        sp = os.path.normpath(os.path.join(os.path.dirname(src_rel), raw))
    abspath = os.path.join(SRC, sp)
    if not os.path.isfile(abspath):
        return None
    def safe(name):  # GitBook/markdown dislike () and spaces in asset paths
        return re.sub(r'[()\s]+', '', name)
    if sp.startswith('assets/'):
        space_asset = 'assets/' + safe(sp[len('assets/'):])
    elif 'screenshots/' in sp:
        space_asset = 'assets/screenshots/' + safe(os.path.basename(sp))
    else:
        space_asset = 'assets/' + safe(os.path.basename(sp))
    asset_jobs[(space, space_asset)] = abspath
    return os.path.relpath(space_asset, os.path.dirname(dest) or '.')

def rewrite(text, src_rel, space, dest, idx, asset_jobs, stats):
    src2dests, kbslug2 = idx

    def img_sub(m):
        new = resolve_image(m.group('url'), src_rel, space, dest, asset_jobs)
        if new is None:
            return m.group(0)
        stats['img'] += 1
        return '![%s](%s)' % (m.group('alt'), new)

    def link_sub(m):
        url = m.group('url')
        if url.startswith(('http://', 'https://', 'mailto:', '#')):
            return m.group(0)
        hit, anchor = resolve_doc(url, src_rel, src2dests, kbslug2)
        if not hit:
            stats['link_miss'] += 1
            stats['miss_samples'].setdefault(src_rel, []).append(url)
            return m.group(0)
        stats['link'] += 1
        return '[%s](%s)' % (m.group('text'), make_doc_link(hit, anchor, space, dest))

    text = IMG_RE.sub(img_sub, text)
    text = LINK_RE.sub(link_sub, text)
    return text

# ---------------------------------------------------------------- pipeline
def convert_file(src_abs, src_rel, space, dest, idx, asset_jobs, stats):
    text = open(src_abs, encoding='utf-8').read()
    text = clean_frontmatter(text)
    text = convert_admonitions(text)
    text = convert_tabs(text)
    text = strip_mkdocs(text)
    text = rewrite(text, src_rel, space, dest, idx, asset_jobs, stats)
    return text

def demo_order():
    """(space, group) -> ordered list of dest paths, from demo SUMMARYs."""
    order = defaultdict(list)
    for space in ('deploy', 'run', 'automate'):
        group = None
        for line in open(os.path.join(DEMO, f"{space}__SUMMARY.md"), encoding='utf-8'):
            m = re.match(r'^##\s+(.*)', line)
            if m:
                group = m.group(1).strip(); continue
            m = re.match(r'^\*\s+\[(.*?)\]\((.*?\.md)\)', line)
            if m and m.group(2) != 'README.md':
                order[(space, group)].append(m.group(2))
    return order

def run_summary_group_order():
    groups = []
    for line in open(os.path.join(DEMO, "run__SUMMARY.md"), encoding='utf-8'):
        m = re.match(r'^##\s+(.*)', line)
        if m:
            groups.append(m.group(1).strip())
    return groups

README_TITLE = {
    "deploy": "Plan and deploy VergeOS",
    "run": "Run the platform",
    "automate": "Automate, protect, and extend",
}

def write_summary(space, rows, dorder):
    lines = ["# Table of contents", ""]
    readme_title = next((r['title'] for r in rows if r['dest'] == 'README.md'),
                        README_TITLE.get(space, space.title()))
    lines.append("* [%s](README.md)" % readme_title)
    lines.append("")
    flat = [r for r in rows if r['dest'] != 'README.md' and not r['group']]
    for r in sorted(flat, key=lambda r: r['title'].lower()):
        lines.append("* [%s](%s)" % (r['title'], r['dest']))
    if flat:
        lines.append("")
    groups = GROUP_ORDER.get(space) or (run_summary_group_order() if space == 'run' else [])
    seen_groups = [g for g in groups]
    # include any unexpected groups at the end
    for r in rows:
        if r['group'] and r['group'] not in seen_groups:
            seen_groups.append(r['group'])
    for g in seen_groups:
        grows = [r for r in rows if r['group'] == g]
        if not grows:
            continue
        lines.append("## %s" % g)
        lines.append("")
        ordered = dorder.get((space, g), [])
        bydest = {r['dest']: r for r in grows}
        used = set()
        for d in ordered:
            if d in bydest:
                r = bydest[d]; used.add(d)
                lines.append("* [%s](%s)" % (r['title'], r['dest']))
        for r in sorted((r for r in grows if r['dest'] not in used),
                        key=lambda r: r['title'].lower()):
            lines.append("* [%s](%s)" % (r['title'], r['dest']))
        lines.append("")
    return '\n'.join(lines).rstrip() + '\n'

def main():
    rows = json.load(open(os.path.join(ROOT, "migration", "mapping.json")))
    idx = build_indices(rows)
    dorder = demo_order()
    asset_jobs = {}
    stats = defaultdict(int); stats['miss_samples'] = {}
    by_space = defaultdict(list)
    for r in rows:
        by_space[r['space']].append(r)

    # 1. convert + write content
    for r in rows:
        src_abs = os.path.join(SRC, r['src'])
        out_path = os.path.join(ROOT, r['space'], r['dest'])
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        text = convert_file(src_abs, r['src'], r['space'], r['dest'], idx, asset_jobs, stats)
        open(out_path, 'w', encoding='utf-8').write(text)

    # 2. copy demo-authored READMEs + home pages verbatim
    shutil.copy(os.path.join(DEMO, "home__README.md"), os.path.join(ROOT, "home", "README.md"))
    shutil.copy(os.path.join(DEMO, "home__migration-and-evaluation-paths.md"),
                os.path.join(ROOT, "home", "migration-and-evaluation-paths.md"))
    shutil.copy(os.path.join(DEMO, "home__support-and-services.md"),
                os.path.join(ROOT, "home", "support-and-services.md"))
    for space in ("deploy", "run", "automate"):
        shutil.copy(os.path.join(DEMO, f"{space}__README.md"),
                    os.path.join(ROOT, space, "README.md"))

    # 3. generated READMEs for spaces without a demo one (release-notes README came from source)
    hc_readme = ('---\ndescription: Troubleshooting articles, how-tos, and field guidance '
                 'for VergeOS operators.\nicon: life-ring\n---\n\n# VergeOS Knowledge Base\n\n'
                 'Practical, task-focused articles maintained by the VergeOS team. Browse by '
                 'category in the sidebar or search for a specific issue.\n')
    open(os.path.join(ROOT, "help-center", "README.md"), 'w', encoding='utf-8').write(hc_readme)

    # 4. copy assets
    for (space, space_asset), abspath in asset_jobs.items():
        dst = os.path.join(ROOT, space, space_asset)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(abspath, dst)

    # 5. SUMMARY.md per space
    home_extra = [
        {'dest': 'README.md', 'group': None, 'title': 'VergeOS Docs Home'},
        {'dest': 'migration-and-evaluation-paths.md', 'group': None, 'title': 'Migration and evaluation paths'},
        {'dest': 'support-and-services.md', 'group': None, 'title': 'Support and services'},
    ]
    for space, srows in by_space.items():
        rows_for_summary = srows
        if space == 'home':
            rows_for_summary = home_extra + srows
        if space == 'help-center':
            rows_for_summary = srows + [{'dest': 'README.md', 'group': None, 'title': 'VergeOS Knowledge Base'}]
        summ = write_summary(space, rows_for_summary, dorder)
        open(os.path.join(ROOT, space, "SUMMARY.md"), 'w', encoding='utf-8').write(summ)

    # ---- report ----
    print("files written :", len(rows))
    print("links rewritten:", stats['link'], " images rewritten:", stats['img'])
    print("link misses   :", stats['link_miss'])
    print("asset copies  :", len(asset_jobs))
    if stats['link_miss']:
        shown = 0
        for s, urls in stats['miss_samples'].items():
            print("   miss in", s, "->", urls[:6]); shown += 1
            if shown >= 12:
                break

if __name__ == "__main__":
    main()
