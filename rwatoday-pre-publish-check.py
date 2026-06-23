#!/usr/bin/env python3
"""
RWAToday.news — Pre-Publish HTML Check
Run this before pushing any new or edited HTML files to GitHub.
Usage: python3 rwatoday-pre-publish-check.py [file.html] [file2.html ...]
       python3 rwatoday-pre-publish-check.py  (checks all .html in current directory)
"""

import sys, re, os

def check_file(path):
    fname = os.path.basename(path)
    with open(path) as f:
        c = f.read()
    
    issues = []

    # ── 1. CSS/text leaking between </style> and <script> in <head> ──
    head_end = c.find('</head>')
    style_tags = list(re.finditer(r'</style>', c[:head_end]))
    if style_tags:
        last_style_pos = style_tags[-1].end()
        between = c[last_style_pos:head_end]
        clean = re.sub(r'<script[^>]*>.*?</script>', '', between, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        if clean:
            issues.append(f"HEAD LEAK — visible text between </style> and </head>: {repr(clean[:80])}")

    # ── 2. Content visible before <nav> in <body> ──
    body_start = c.find('<body>')
    nav_start  = c.find('<nav', body_start) if body_start > 0 else -1
    if body_start > 0 and nav_start > 0:
        between = c[body_start+6:nav_start]
        visible = re.sub(r'<[^>]+>', '', between).strip()
        if visible:
            issues.append(f"BODY LEAK — visible text before <nav>: {repr(visible[:80])}")

    # ── 3. Canonical tag must be a clean URL (no .html) ──
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', c)
    if canon and canon.group(1).endswith('.html'):
        issues.append(f"CANONICAL .html — canonical should be clean URL: {canon.group(1)}")

    # ── 4. og:url must match canonical ──
    ogurl = re.search(r'<meta property="og:url" content="([^"]+)"', c)
    if ogurl and ogurl.group(1).endswith('.html'):
        issues.append(f"OG:URL .html — og:url should be clean URL: {ogurl.group(1)}")

    # ── 5. og:image must be hosted URL (not base64) ──
    ogimg = re.search(r'<meta property="og:image" content="([^"]+)"', c)
    if ogimg and ogimg.group(1).startswith('data:'):
        issues.append("OG:IMAGE base64 — og:image must be a hosted URL, not base64")

    # ── 6. Back-link must appear AFTER </nav>, not before ──
    nav_end = c.find('</nav>')
    back_before_nav = c.find('class="back-link"', body_start)
    if back_before_nav > 0 and nav_start > 0 and back_before_nav < nav_start:
        issues.append("BACK-LINK BEFORE NAV — back-link appears before <nav> tag")

    # ── 7. No ticker widget ──
    if 'ticker-wrap' in c or 'ticker-track' in c:
        issues.append("TICKER FOUND — ticker has been removed from the site, do not include")

    return issues

# ── Run ───────────────────────────────────────────────────────
files = sys.argv[1:] if len(sys.argv) > 1 else [f for f in os.listdir('.') if f.endswith('.html')]

total_issues = 0
for path in sorted(files):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        continue
    issues = check_file(path)
    if issues:
        total_issues += len(issues)
        print(f"\n❌ {os.path.basename(path)}")
        for issue in issues:
            print(f"   → {issue}")
    else:
        print(f"✅ {os.path.basename(path)}")

print(f"\n{'='*50}")
if total_issues == 0:
    print(f"✅ All {len(files)} file(s) passed — ready to publish")
else:
    print(f"❌ {total_issues} issue(s) found across {len(files)} file(s) — fix before pushing")
