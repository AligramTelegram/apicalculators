#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tonight fixes from brief v2:
1. FR "4 calculatrices" -> "10 calculatrices"
2. DE + TR: add geo.region + geo.placename
3. DE + FR + TR: add twitter:creator
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

# ── 1. FR: fix calculator count ───────────────────────────────────────────────
fr_path = os.path.join(BASE, 'fr', 'index.html')
c = read(fr_path)
old = '4 calculatrices'
new = '10 calculatrices'
if old in c:
    c = c.replace(old, new, 1)
    write(fr_path, c)
    print(f'✓ FR: "{old}" → "{new}"')
else:
    print(f'  SKIP FR count (not found or already fixed)')

# ── 2. DE: add geo tags + twitter:creator ────────────────────────────────────
de_path = os.path.join(BASE, 'de', 'index.html')
c = read(de_path)

# geo tags — inject before </head> if not present
if 'geo.region' not in c:
    geo_block = '''<meta name="geo.region" content="DE" />
<meta name="geo.placename" content="Germany" />
<meta name="language" content="German">'''
    c = c.replace('<!-- ICONS -->', geo_block + '\n\n<!-- ICONS -->', 1)
    print('✓ DE: added geo.region + geo.placename')
else:
    print('  SKIP DE geo (already present)')

# twitter:creator
if 'twitter:creator' not in c:
    c = c.replace(
        '<meta name="twitter:site" content="@apicalculators">',
        '<meta name="twitter:site" content="@apicalculators">\n<meta name="twitter:creator" content="@apicalculators">',
        1
    )
    print('✓ DE: added twitter:creator')
else:
    print('  SKIP DE twitter:creator (already present)')

write(de_path, c)

# ── 3. TR: add geo tags + twitter:creator ────────────────────────────────────
tr_path = os.path.join(BASE, 'tr', 'index.html')
c = read(tr_path)

if 'geo.region' not in c:
    geo_block = '<meta name="geo.region" content="TR" />\n<meta name="geo.placename" content="Turkey" />\n<meta name="language" content="Turkish">'
    # inject after the last hreflang line
    c = c.replace(
        '<meta property="og:type" content="website">',
        geo_block + '\n<meta property="og:type" content="website">',
        1
    )
    print('✓ TR: added geo.region + geo.placename')
else:
    print('  SKIP TR geo (already present)')

if 'twitter:creator' not in c:
    c = c.replace(
        '<meta name="twitter:site" content="@apicalculators">',
        '<meta name="twitter:site" content="@apicalculators">\n<meta name="twitter:creator" content="@apicalculators">',
        1
    )
    print('✓ TR: added twitter:creator')
else:
    print('  SKIP TR twitter:creator (already present)')

write(tr_path, c)

# ── 4. FR: add twitter:creator ───────────────────────────────────────────────
fr_path = os.path.join(BASE, 'fr', 'index.html')
c = read(fr_path)

if 'twitter:creator' not in c:
    c = c.replace(
        '<meta name="twitter:site" content="@apicalculators">',
        '<meta name="twitter:site" content="@apicalculators">\n<meta name="twitter:creator" content="@apicalculators">',
        1
    )
    write(fr_path, c)
    print('✓ FR: added twitter:creator')
else:
    print('  SKIP FR twitter:creator (already present)')

print('\nDone.')
