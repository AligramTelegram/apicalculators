#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 3: Add AdSense placeholder ad units to all blog posts.
   When AdSense is approved, replace ADSENSE_PUB_ID and slot IDs in one place.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── Config — replace these when AdSense approved ───────────────────────────────
ADSENSE_PUB_ID   = 'ca-pub-XXXXXXXXXXXXXXXX'
SLOT_TOP         = 'XXXXXXXXXX'   # after intro, before first H2
SLOT_MID         = 'YYYYYYYYYY'   # mid-article, after calculator CTA
SLOT_BOTTOM      = 'ZZZZZZZZZZ'   # after FAQ, before related posts

# ── AdSense script tag ─────────────────────────────────────────────────────────
ADSENSE_SCRIPT = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>'

# ── Ad unit HTML ───────────────────────────────────────────────────────────────
def ad_unit(slot, position_class, fmt='auto'):
    return f'''<div class="ad-unit {position_class}" style="margin:2rem 0;text-align:center;min-height:90px;">
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="{ADSENSE_PUB_ID}"
       data-ad-slot="{slot}"
       data-ad-format="{fmt}"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>'''

AD_TOP    = ad_unit(SLOT_TOP,    'ad-top-content')
AD_MID    = ad_unit(SLOT_MID,    'ad-mid-content', 'rectangle')
AD_BOTTOM = ad_unit(SLOT_BOTTOM, 'ad-bottom-content')

# ── Helpers ────────────────────────────────────────────────────────────────────
def insert_after(c, pattern, insertion, nth=1):
    """Insert insertion after nth occurrence of regex pattern match."""
    count = 0
    for m in re.finditer(pattern, c):
        count += 1
        if count == nth:
            pos = m.end()
            return c[:pos] + '\n' + insertion + '\n' + c[pos:]
    return c  # pattern not found — return unchanged

def has_adsense(c):
    return 'adsbygoogle' in c

def ensure_adsense_script(c):
    """Add AdSense script to <head> if not present."""
    if 'pagead2.googlesyndication.com' in c:
        return c
    # Insert just before </head>
    return c.replace('</head>', ADSENSE_SCRIPT + '\n</head>', 1)

# ── Process all blog posts ─────────────────────────────────────────────────────
changed = []

for lang in ['en', 'de', 'fr', 'tr']:
    blog_dir = os.path.join(BASE, 'blog') if lang == 'en' else os.path.join(BASE, lang, 'blog')
    files = sorted(f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html')

    for fname in files:
        path = os.path.join(blog_dir, fname)
        c = open(path, encoding='utf-8').read()

        if has_adsense(c):
            print(f'  SKIP (already has ads): {lang}/{fname}')
            continue

        orig = c

        # 1. Add script to <head>
        c = ensure_adsense_script(c)

        # 2. AD TOP — after first <p> tag in article body (after intro paragraph)
        # Find first <p> after <article or main content area
        # Strategy: insert after the first closing </p> that comes after <h1>
        h1_pos = c.find('<h1')
        if h1_pos > 0:
            first_p_end = c.find('</p>', h1_pos)
            if first_p_end > 0:
                insert_pos = first_p_end + 4  # after </p>
                c = c[:insert_pos] + '\n' + AD_TOP + '\n' + c[insert_pos:]

        # 3. AD MID — after 3rd <h2> (mid-article)
        c = insert_after(c, r'</h2>', AD_MID, nth=3)

        # 4. AD BOTTOM — before the last <h2> (typically FAQ or Related section)
        # Find last <h2>
        last_h2 = None
        for m in re.finditer(r'<h2[^>]*>', c):
            last_h2 = m
        if last_h2:
            pos = last_h2.start()
            c = c[:pos] + AD_BOTTOM + '\n' + c[pos:]

        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            rel_path = f'/blog/{fname}' if lang == 'en' else f'/{lang}/blog/{fname}'
            changed.append(rel_path)

print(f'\nTotal changed: {len(changed)} files')
for p in sorted(changed):
    print(f'  {p}')
