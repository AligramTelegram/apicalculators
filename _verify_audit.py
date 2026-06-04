#!/usr/bin/env python3
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

print('=== TITLE CHECK ===')
titles = {
    'index.html': 60,
    'de/index.html': 60,
    'fr/index.html': 60,
    'tr/index.html': 60,
}
for f, limit in titles.items():
    c = open(os.path.join(BASE, f), encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', c)
    t = m.group(1).replace('&amp;', '&') if m else '?'
    ok = '✓' if len(t) <= limit else '✗'
    print(f'{ok} {f}: {len(t)} chars — {t}')

print('\n=== GEO TAG CHECK ===')
for f, region in [
    ('de/index.html', 'DE'), ('fr/index.html', 'FR'), ('tr/index.html', 'TR'),
    ('de/blog/llm-api-kosten-2026.html', 'DE'),
    ('fr/blog/cout-api-llm-2026.html', 'FR'),
    ('tr/blog/gpt-api-turkce-maliyet-2026.html', 'TR'),
]:
    c = open(os.path.join(BASE, f), encoding='utf-8').read()
    has_region = f'content="{region}"' in c and 'geo.region' in c
    has_place = 'geo.placename' in c
    ok = '✓' if has_region and has_place else '✗'
    print(f'{ok} geo in {f}')

print('\n=== SCHEMA CHECK (homepages) ===')
for f, schemas in [
    ('index.html', ['SoftwareApplication', 'FAQPage', 'BreadcrumbList']),
    ('de/index.html', ['SoftwareApplication', 'FAQPage', 'BreadcrumbList']),
    ('fr/index.html', ['SoftwareApplication', 'FAQPage', 'BreadcrumbList']),
    ('tr/index.html', ['SoftwareApplication', 'FAQPage', 'BreadcrumbList']),
]:
    c = open(os.path.join(BASE, f), encoding='utf-8').read()
    for s in schemas:
        has = f'"@type":"{s}"' in c or f'"@type": "{s}"' in c
        print(f'  {"✓" if has else "✗"} {s} in {f}')
