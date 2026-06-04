#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild sitemap.xml cleanly from actual files — no duplicates, no merge issues."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'
DOMAIN = 'https://apicalculators.com'

HREFLANG_MAIN = [
    ('en', f'{DOMAIN}/'),
    ('de', f'{DOMAIN}/de/'),
    ('fr', f'{DOMAIN}/fr/'),
    ('tr', f'{DOMAIN}/tr/'),
]

def url_entry(loc, lastmod, changefreq, priority, hreflang=None):
    lines = ['  <url>']
    lines.append(f'    <loc>{loc}</loc>')
    lines.append(f'    <lastmod>{lastmod}</lastmod>')
    lines.append(f'    <changefreq>{changefreq}</changefreq>')
    lines.append(f'    <priority>{priority}</priority>')
    if hreflang:
        for hl, href in hreflang:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>')
    lines.append('  </url>')
    return '\n'.join(lines)

entries = []

# ── Main pages ─────────────────────────────────────────────────────────────────
entries.append(url_entry(f'{DOMAIN}/', '2026-06-04', 'weekly', '1.0', HREFLANG_MAIN + [('x-default', f'{DOMAIN}/')]))
entries.append(url_entry(f'{DOMAIN}/de/', '2026-06-04', 'weekly', '0.9', HREFLANG_MAIN))
entries.append(url_entry(f'{DOMAIN}/fr/', '2026-06-04', 'weekly', '0.9', HREFLANG_MAIN))
entries.append(url_entry(f'{DOMAIN}/tr/', '2026-06-04', 'weekly', '0.9', HREFLANG_MAIN))

# ── About pages ────────────────────────────────────────────────────────────────
for lang, prefix in [('en', ''), ('de', '/de'), ('fr', '/fr'), ('tr', '/tr')]:
    entries.append(url_entry(f'{DOMAIN}{prefix}/about.html', '2026-06-04', 'monthly', '0.5'))

# ── Blog index pages ───────────────────────────────────────────────────────────
BLOG_HREFLANG = [
    ('en', f'{DOMAIN}/blog/'),
    ('de', f'{DOMAIN}/de/blog/'),
    ('fr', f'{DOMAIN}/fr/blog/'),
    ('tr', f'{DOMAIN}/tr/blog/'),
]
entries.append(url_entry(f'{DOMAIN}/blog/', '2026-06-04', 'weekly', '0.8', BLOG_HREFLANG))
entries.append(url_entry(f'{DOMAIN}/de/blog/', '2026-06-04', 'weekly', '0.7', BLOG_HREFLANG))
entries.append(url_entry(f'{DOMAIN}/fr/blog/', '2026-06-04', 'weekly', '0.7', BLOG_HREFLANG))
entries.append(url_entry(f'{DOMAIN}/tr/blog/', '2026-06-04', 'weekly', '0.7', BLOG_HREFLANG))

# ── Blog posts — scan actual files ────────────────────────────────────────────
BLOG_DIRS = {
    'en': ('blog', f'{DOMAIN}/blog/', '0.9'),
    'de': ('de/blog', f'{DOMAIN}/de/blog/', '0.8'),
    'fr': ('fr/blog', f'{DOMAIN}/fr/blog/', '0.8'),
    'tr': ('tr/blog', f'{DOMAIN}/tr/blog/', '0.8'),
}

# Lastmod per batch (rough dates)
LASTMOD = {
    'llm': '2026-06-02', 'reduce': '2026-06-02', 'vector': '2026-06-02',
    'stripe': '2026-06-02', 'dalle': '2026-06-02', 'lemon': '2026-06-03',
    'midjourney': '2026-06-03', 'pinecone': '2026-06-03', 'vektordatenbank': '2026-06-02',
    'llm-kosten': '2026-06-02', 'dalle-vs': '2026-06-02', 'guide-couts': '2026-06-02',
    'reduire': '2026-06-02', 'comparaison-couts': '2026-06-02',
}

for lang, (rel_dir, url_prefix, priority) in BLOG_DIRS.items():
    blog_path = os.path.join(BASE, rel_dir)
    if not os.path.exists(blog_path):
        continue
    files = sorted(f for f in os.listdir(blog_path) if f.endswith('.html') and f != 'index.html')
    for fname in files:
        # Determine lastmod
        lastmod = '2026-06-04'
        for key, date in LASTMOD.items():
            if fname.startswith(key):
                lastmod = date
                break
        # Specific overrides
        if any(x in fname for x in ['lemon', 'midjourney', 'pinecone']):
            lastmod = '2026-06-03'
        entries.append(url_entry(f'{url_prefix}{fname}', lastmod, 'monthly', priority))

# ── Write sitemap ──────────────────────────────────────────────────────────────
sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
sitemap += '\n'.join(entries)
sitemap += '\n</urlset>\n'

out = os.path.join(BASE, 'sitemap.xml')
with open(out, 'w', encoding='utf-8') as f:
    f.write(sitemap)

# ── Validate ───────────────────────────────────────────────────────────────────
locs = [m for m in __import__('re').findall(r'<loc>([^<]+)</loc>', sitemap)]
dupes = [l for l in locs if locs.count(l) > 1]
print(f'Total URLs: {len(locs)}')
print(f'Unique URLs: {len(set(locs))}')
print(f'Duplicates: {len(set(dupes))}')
if dupes:
    for d in sorted(set(dupes)):
        print(f'  DUP: {d}')
print(f'urlset tags: {sitemap.count("</urlset>")}')
print(f'Sitemap written: {len(sitemap)} chars')
