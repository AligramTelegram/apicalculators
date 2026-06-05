#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# New URLs to add (not in sitemap yet)
TODAY = '2026-06-05'

def url(loc, lastmod=TODAY, freq='monthly', pri='0.8', alternates=None):
    out = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n'
    if alternates:
        for lang, href in alternates:
            out += f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>\n'
    out += '  </url>'
    return out

NEW_URLS = [
    # ── AI Coding Tool calc pages ─────────────────────────────────────────────
    url('https://apicalculators.com/ai-coding-tool-cost.html', pri='0.9',
        alternates=[
            ('en','https://apicalculators.com/ai-coding-tool-cost.html'),
            ('de','https://apicalculators.com/de/ki-coding-tool-kosten.html'),
            ('fr','https://apicalculators.com/fr/cout-outil-ia-coding.html'),
            ('tr','https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html'),
            ('x-default','https://apicalculators.com/ai-coding-tool-cost.html'),
        ]),
    url('https://apicalculators.com/de/ki-coding-tool-kosten.html', pri='0.8',
        alternates=[
            ('en','https://apicalculators.com/ai-coding-tool-cost.html'),
            ('de','https://apicalculators.com/de/ki-coding-tool-kosten.html'),
            ('fr','https://apicalculators.com/fr/cout-outil-ia-coding.html'),
            ('tr','https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html'),
        ]),
    url('https://apicalculators.com/fr/cout-outil-ia-coding.html', pri='0.8'),
    url('https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html', pri='0.8'),

    # ── Auth Provider calc pages ──────────────────────────────────────────────
    url('https://apicalculators.com/auth-provider-cost.html', pri='0.9',
        alternates=[
            ('en','https://apicalculators.com/auth-provider-cost.html'),
            ('de','https://apicalculators.com/de/auth-anbieter-kosten.html'),
            ('fr','https://apicalculators.com/fr/cout-fournisseur-auth.html'),
            ('tr','https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html'),
            ('x-default','https://apicalculators.com/auth-provider-cost.html'),
        ]),
    url('https://apicalculators.com/de/auth-anbieter-kosten.html', pri='0.8'),
    url('https://apicalculators.com/fr/cout-fournisseur-auth.html', pri='0.8'),
    url('https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html', pri='0.8'),

    # ── New blog posts — Cursor true cost ─────────────────────────────────────
    url('https://apicalculators.com/blog/cursor-true-cost-2026.html',
        alternates=[
            ('en','https://apicalculators.com/blog/cursor-true-cost-2026.html'),
            ('de','https://apicalculators.com/de/blog/cursor-wahre-kosten-2026.html'),
            ('fr','https://apicalculators.com/fr/blog/vrai-cout-cursor-2026.html'),
            ('tr','https://apicalculators.com/tr/blog/cursor-gercek-maliyet-2026.html'),
        ]),
    url('https://apicalculators.com/de/blog/cursor-wahre-kosten-2026.html'),
    url('https://apicalculators.com/fr/blog/vrai-cout-cursor-2026.html'),
    url('https://apicalculators.com/tr/blog/cursor-gercek-maliyet-2026.html'),

    # ── New blog posts — Clerk vs Supabase ────────────────────────────────────
    url('https://apicalculators.com/blog/clerk-vs-supabase-auth-cost-2026.html',
        alternates=[
            ('en','https://apicalculators.com/blog/clerk-vs-supabase-auth-cost-2026.html'),
            ('de','https://apicalculators.com/de/blog/clerk-supabase-auth-kosten-2026.html'),
            ('fr','https://apicalculators.com/fr/blog/clerk-vs-supabase-auth-cout-2026.html'),
            ('tr','https://apicalculators.com/tr/blog/clerk-supabase-auth-maliyet-2026.html'),
        ]),
    url('https://apicalculators.com/de/blog/clerk-supabase-auth-kosten-2026.html'),
    url('https://apicalculators.com/fr/blog/clerk-vs-supabase-auth-cout-2026.html'),
    url('https://apicalculators.com/tr/blog/clerk-supabase-auth-maliyet-2026.html'),

    # ── Geo blogs (Section 7 — added before but missing from sitemap) ─────────
    url('https://apicalculators.com/de/blog/llm-api-kosten-2026.html'),
    url('https://apicalculators.com/de/blog/hetzner-digitalocean-vergleich-2026.html'),
    url('https://apicalculators.com/fr/blog/cout-api-llm-2026.html'),
    url('https://apicalculators.com/fr/blog/comparatif-vps-cloud-france-2026.html'),
    url('https://apicalculators.com/tr/blog/gpt-api-turkce-maliyet-2026.html'),
    url('https://apicalculators.com/tr/blog/stripe-turkiye-komisyon-2026.html'),

    # ── FR/TR misc blogs missing from sitemap ─────────────────────────────────
    url('https://apicalculators.com/fr/blog/comparatif-vps-cloud-france-2026.html'),  # might dup, handled below
]

# Read current sitemap
sitemap_path = os.path.join(BASE, 'sitemap.xml')
c = read(sitemap_path)

# Fix missing </urlset> closing tag
if not c.rstrip().endswith('</urlset>'):
    c = c.rstrip() + '\n</urlset>\n'

# Collect existing locs
existing = set()
import re
for m in re.finditer(r'<loc>(.*?)</loc>', c):
    existing.add(m.group(1))

# Inject new URLs before </urlset>
added = 0
inject = ''
seen = set()
for block in NEW_URLS:
    loc_m = re.search(r'<loc>(.*?)</loc>', block)
    if not loc_m:
        continue
    loc = loc_m.group(1)
    if loc in existing or loc in seen:
        continue
    seen.add(loc)
    inject += '\n' + block + '\n'
    added += 1

c = c.replace('</urlset>', inject + '</urlset>')

# Update lastmod on existing entries to today
c = re.sub(r'<lastmod>2026-06-0[1-4]</lastmod>', f'<lastmod>{TODAY}</lastmod>', c)

write(sitemap_path, c)

# Count total URLs
total = len(re.findall(r'<loc>', c))
print(f'✓ Added {added} new URLs')
print(f'✓ Total URLs in sitemap: {total}')
print(f'✓ </urlset> present: {"</urlset>" in c}')
