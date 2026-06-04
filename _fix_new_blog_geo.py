#!/usr/bin/env python3
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

GEO = {
    'de': ('<meta name="geo.region" content="DE" />\n<meta name="geo.placename" content="Germany" />', 'DE'),
    'fr': ('<meta name="geo.region" content="FR" />\n<meta name="geo.placename" content="France" />', 'FR'),
    'tr': ('<meta name="geo.region" content="TR" />\n<meta name="geo.placename" content="Turkey" />', 'TR'),
}

# Check and fix ALL DE/FR/TR blog posts - ensure both geo.region AND geo.placename present
fixed = 0
for lang, (geo_block, region) in GEO.items():
    for path in glob.glob(os.path.join(BASE, lang, 'blog', '*.html')):
        c = open(path, encoding='utf-8').read()
        has_region = f'geo.region" content="{region}"' in c
        has_place = 'geo.placename' in c
        if not has_region or not has_place:
            # Remove any partial geo tags first
            import re
            c = re.sub(r'<meta name="geo\.region"[^>]*/>\n?', '', c)
            c = re.sub(r'<meta name="geo\.placename"[^>]*/>\n?', '', c)
            c = c.replace('</head>', geo_block + '\n</head>', 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            fixed += 1
            print(f'✓ Fixed geo: {os.path.relpath(path, BASE)}')

print(f'\nFixed {fixed} files.')

# Verify the 3 failing ones
for f, region in [
    ('de/blog/llm-api-kosten-2026.html', 'DE'),
    ('fr/blog/cout-api-llm-2026.html', 'FR'),
    ('tr/blog/gpt-api-turkce-maliyet-2026.html', 'TR'),
]:
    c = open(os.path.join(BASE, f), encoding='utf-8').read()
    has_r = f'geo.region" content="{region}"' in c
    has_p = 'geo.placename' in c
    print(f'{"✓" if has_r and has_p else "✗"} {f}: region={has_r} place={has_p}')
