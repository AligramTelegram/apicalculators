#!/usr/bin/env python3
import sys, os, glob, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def check_file(path):
    c = open(path, encoding='utf-8').read()
    rel = os.path.relpath(path, BASE)
    has_script = 'pagead2.googlesyndication.com' in c
    has_ins = 'adsbygoogle' in c
    ad_units = len(re.findall(r'class="ad-unit|ad-top-content|ad-mid-content|ad-bottom-content|adsbygoogle"', c))
    pub_id = re.search(r'ca-pub-([A-Z0-9]+)', c)
    pub = pub_id.group(1) if pub_id else None
    slots = re.findall(r'data-ad-slot="([^"]+)"', c)
    return {
        'rel': rel,
        'has_script': has_script,
        'has_ins': has_ins,
        'ad_count': len(slots),
        'pub': pub,
        'slots': slots,
        'placeholder_pub': pub == 'XXXXXXXXXXXXXXXX' if pub else False,
        'placeholder_slots': any(s in ('XXXXXXXXXX','YYYYYYYYYY','ZZZZZZZZZZ') for s in slots),
    }

# Categorize all HTML files
cats = {
    'EN homepage': ['index.html'],
    'DE homepage': ['de/index.html'],
    'FR homepage': ['fr/index.html'],
    'TR homepage': ['tr/index.html'],
    'EN blog': sorted(glob.glob(os.path.join(BASE, 'blog', '*.html'))),
    'DE blog': sorted(glob.glob(os.path.join(BASE, 'de', 'blog', '*.html'))),
    'FR blog': sorted(glob.glob(os.path.join(BASE, 'fr', 'blog', '*.html'))),
    'TR blog': sorted(glob.glob(os.path.join(BASE, 'tr', 'blog', '*.html'))),
    'EN calc pages': [f for f in glob.glob(os.path.join(BASE, '*.html'))
                      if 'index' not in f and 'privacy' not in f and 'about' not in f and 'terms' not in f],
}

print('=' * 70)
print('ADSENSE AD PLACEMENT REPORT')
print('=' * 70)

total_with_ads = 0
total_files = 0
total_no_ads = []
total_placeholder = []

for cat, files in cats.items():
    if not files: continue
    results = []
    for f in files:
        path = os.path.join(BASE, f) if isinstance(f, str) and not os.path.isabs(f) else f
        if not os.path.exists(path): continue
        r = check_file(path)
        results.append(r)

    with_ads = [r for r in results if r['has_ins']]
    no_ads   = [r for r in results if not r['has_ins']]
    placeholders = [r for r in with_ads if r['placeholder_pub'] or r['placeholder_slots']]

    print(f'\n── {cat} ({len(results)} files) ──')
    print(f'  With AdSense : {len(with_ads)}/{len(results)}')
    print(f'  No ads       : {len(no_ads)}')
    print(f'  Placeholder  : {len(placeholders)} (pub/slot not real)')

    if no_ads:
        for r in no_ads:
            print(f'    ✗ NO ADS: {r["rel"]}')
    if with_ads:
        # Show ad unit count distribution
        counts = {}
        for r in with_ads:
            n = r['ad_count']
            counts[n] = counts.get(n, 0) + 1
        print(f'  Ad units/page: {dict(sorted(counts.items()))}')
        if placeholders:
            print(f'  Placeholder pub IDs still active: {len(placeholders)} files')

    total_with_ads += len(with_ads)
    total_files += len(results)
    total_no_ads.extend(no_ads)
    total_placeholder.extend(placeholders)

print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)
print(f'Total files   : {total_files}')
print(f'With AdSense  : {total_with_ads}')
print(f'No AdSense    : {len(total_no_ads)}')
print(f'Placeholder   : {len(total_placeholder)} files still using ca-pub-XXXX')

print('\nFiles WITHOUT any AdSense:')
for r in total_no_ads:
    print(f'  ✗ {r["rel"]}')

print('\nAd slot placeholder patterns still in use:')
# Collect all unique slot IDs across all files
all_slots = set()
for cat, files in cats.items():
    for f in files:
        path = os.path.join(BASE, f) if isinstance(f, str) and not os.path.isabs(f) else f
        if not os.path.exists(path): continue
        c = open(path, encoding='utf-8').read()
        slots = re.findall(r'data-ad-slot="([^"]+)"', c)
        all_slots.update(slots)
print(f'  Unique slot IDs found: {sorted(all_slots)}')
print(f'  → All placeholder: {all(s in ("XXXXXXXXXX","YYYYYYYYYY","ZZZZZZZZZZ") for s in all_slots)}')
