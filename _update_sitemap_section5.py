#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add new dedicated calculator pages to sitemap.xml."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'
DOMAIN = 'https://apicalculators.com'
LASTMOD = '2026-06-04'

NEW_PAGES = [
    # EN dedicated calculator pages
    (f'{DOMAIN}/llm-cost-calculator.html', '0.9',
     [('en', f'{DOMAIN}/llm-cost-calculator.html'),
      ('de', f'{DOMAIN}/de/llm-kostenrechner.html'),
      ('fr', f'{DOMAIN}/fr/calculateur-cout-llm.html'),
      ('tr', f'{DOMAIN}/tr/llm-maliyet-hesaplayici.html')]),
    (f'{DOMAIN}/aws-lambda-calculator.html', '0.9',
     [('en', f'{DOMAIN}/aws-lambda-calculator.html'),
      ('de', f'{DOMAIN}/de/aws-lambda-rechner.html'),
      ('tr', f'{DOMAIN}/tr/aws-lambda-maliyet.html')]),
    (f'{DOMAIN}/vector-db-cost.html', '0.9', []),
    (f'{DOMAIN}/cloud-vps-comparison.html', '0.9',
     [('en', f'{DOMAIN}/cloud-vps-comparison.html'),
      ('de', f'{DOMAIN}/de/cloud-vps-kostenvergleich.html'),
      ('fr', f'{DOMAIN}/fr/comparateur-vps-cloud.html')]),
    (f'{DOMAIN}/embedding-api-cost.html', '0.8', []),
    (f'{DOMAIN}/ai-agent-cost-calculator.html', '0.8', []),
    (f'{DOMAIN}/api-gateway-cost.html', '0.8', []),
    (f'{DOMAIN}/stt-tts-api-cost.html', '0.8', []),
    (f'{DOMAIN}/stripe-vs-paddle-calculator.html', '0.8', []),
    (f'{DOMAIN}/ai-image-cost-calculator.html', '0.8', []),
    # DE pages
    (f'{DOMAIN}/de/llm-kostenrechner.html', '0.8', []),
    (f'{DOMAIN}/de/cloud-vps-kostenvergleich.html', '0.8', []),
    (f'{DOMAIN}/de/aws-lambda-rechner.html', '0.8', []),
    # FR pages
    (f'{DOMAIN}/fr/calculateur-cout-llm.html', '0.8', []),
    (f'{DOMAIN}/fr/comparateur-vps-cloud.html', '0.8', []),
    # TR pages
    (f'{DOMAIN}/tr/llm-maliyet-hesaplayici.html', '0.8', []),
    (f'{DOMAIN}/tr/aws-lambda-maliyet.html', '0.8', []),
]

def url_entry(loc, priority, hreflang=None):
    lines = ['  <url>',
             f'    <loc>{loc}</loc>',
             f'    <lastmod>{LASTMOD}</lastmod>',
             f'    <changefreq>monthly</changefreq>',
             f'    <priority>{priority}</priority>']
    if hreflang:
        for hl, href in hreflang:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{href}"/>')
    lines.append('  </url>')
    return '\n'.join(lines)

sitemap_path = os.path.join(BASE, 'sitemap.xml')
c = open(sitemap_path, encoding='utf-8').read()

# Check which URLs already exist
existing = set(re.findall(r'<loc>([^<]+)</loc>', c))

new_entries = []
for loc, priority, hreflang in NEW_PAGES:
    if loc in existing:
        print(f'  SKIP (exists): {loc}')
        continue
    new_entries.append(url_entry(loc, priority, hreflang if hreflang else None))

if new_entries:
    insert = '\n' + '\n'.join(new_entries) + '\n'
    c = c.replace('</urlset>', insert + '</urlset>')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Added {len(new_entries)} new URLs to sitemap')

# Validate
locs = re.findall(r'<loc>([^<]+)</loc>', c)
dupes = [l for l in set(locs) if locs.count(l) > 1]
print(f'Total URLs: {len(locs)}, Unique: {len(set(locs))}, Dupes: {len(dupes)}')
