#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

RATING_BLOCK = '"aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "127", "bestRating": "5", "worstRating": "1"}'

PAGES = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

for path in PAGES:
    c = read(path)
    if 'aggregateRating' in c:
        print(f'  SKIP {os.path.relpath(path, BASE)}')
        continue

    # Replace the closing of SoftwareApplication offers block
    # Handle both compact and spaced JSON
    c2 = re.sub(
        r'("offers"\s*:\s*\{"@type"\s*:\s*"Offer"\s*,\s*"price"\s*:\s*"0"\s*,\s*"priceCurrency"\s*:\s*"USD"\s*\})',
        r'\1, ' + RATING_BLOCK,
        c, count=1
    )
    if c2 != c:
        write(path, c2)
        print(f'✓ {os.path.relpath(path, BASE)}: rating added')
    else:
        print(f'  WARN {os.path.relpath(path, BASE)}: no match')

print('Done.')
