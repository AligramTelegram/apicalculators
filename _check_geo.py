#!/usr/bin/env python3
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

# Check geo status on homepages and a few blog posts
for f in ['de/index.html', 'fr/index.html', 'tr/index.html',
          'de/blog/llm-kosten-leitfaden-2026.html',
          'fr/blog/guide-couts-llm-2026.html',
          'tr/blog/llm-maliyet-rehberi-2026.html']:
    c = open(os.path.join(BASE, f), encoding='utf-8').read()
    has = 'geo.region' in c
    print(f'{"✓" if has else "✗"} geo.region in {f}')
    if has:
        # show what's there
        idx = c.find('geo.region')
        print(f'   → {c[max(0,idx-5):idx+60]}')

# Count blog posts without geo in each lang
for lang in ['de', 'fr', 'tr']:
    pattern = os.path.join(BASE, lang, 'blog', '*.html')
    files = glob.glob(pattern)
    missing = [f for f in files if 'geo.region' not in open(f, encoding='utf-8').read()]
    print(f'\n{lang}/blog: {len(missing)}/{len(files)} missing geo.region')
    for f in missing[:5]:
        print(f'   {os.path.basename(f)}')
