#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add AdSense placeholders to:
  - 14 dedicated calculator pages (3 units each, Google policy compliant)
  - DE/FR/TR homepages (1 unit each, between tool sections)

Google AdSense placement rules:
  - Never inside/adjacent to interactive controls (inputs, buttons)
  - Ads must not be disguised as content
  - 3 units max per page (standard content pages)
  - Must be labeled / visually separated
  - No ads on pages with insufficient content (calc pages have ample content)
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

PUB = 'ca-pub-XXXXXXXXXXXXXXXX'

# 3 distinct slot IDs — easier to replace individually later
SLOT_TOP = 'TOP0000000'   # after intro, before calculator
SLOT_MID = 'MID0000000'   # after pricing table, mid-content
SLOT_BTM = 'BTM0000000'   # after FAQ, before related/footer

ADSENSE_SCRIPT = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>'

AD_CSS = '''<style>
.ad-wrap{margin:2rem 0;text-align:center;overflow:hidden}
.ad-wrap .ad-label{font-family:'Cascadia Code','Consolas',monospace;font-size:10px;color:#3a4550;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px}
.ad-unit{display:block;min-height:90px;background:rgba(255,255,255,.01)}
</style>'''

def ad_block(slot, fmt='auto', label='Advertisement'):
    return f'''<div class="ad-wrap">
  <div class="ad-label">{label}</div>
  <ins class="adsbygoogle ad-unit"
       style="display:block"
       data-ad-client="{PUB}"
       data-ad-slot="{slot}"
       data-ad-format="{fmt}"
       data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>'''

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

def already_done(c):
    return 'TOP0000000' in c or 'MID0000000' in c

# ══════════════════════════════════════════════════════════════════════════════
# 1. DEDICATED CALCULATOR PAGES (14 files)
# ══════════════════════════════════════════════════════════════════════════════
# Placement strategy (Google-compliant):
#   TOP  → after <p class="intro">...</p>, before calculator widget
#          Rationale: user just read context, high attention, not near buttons
#   MID  → after first pricing table </table>, before next <h2>
#          Rationale: natural content break, user engaged with data
#   BTM  → after FAQ section, before Related Calculators / footer
#          Rationale: user finished, capture intent before exit

calc_files = sorted([
    f for f in glob.glob(os.path.join(BASE, '*.html'))
    if os.path.basename(f) not in ('index.html','404.html','privacy.html',
                                    'about.html','terms.html','sitemap.html')
])

calc_count = 0
for path in calc_files:
    c = read(path)
    if already_done(c):
        print(f'  SKIP (done): {os.path.basename(path)}')
        continue

    modified = False

    # Inject AdSense script into <head> if not present
    if PUB not in c:
        c = c.replace('</head>', ADSENSE_SCRIPT + '\n' + AD_CSS + '\n</head>', 1)

    # ── TOP: after </p> that follows class="intro" ────────────────────────────
    # Pattern: <p class="intro">...</p> then we insert after it
    m = re.search(r'(<p class="intro">.*?</p>)', c, re.DOTALL)
    if m and SLOT_TOP not in c:
        old = m.group(1)
        new = old + '\n' + ad_block(SLOT_TOP, 'auto')
        c = c.replace(old, new, 1)
        modified = True

    # ── MID: after first </table> tag (pricing table) ─────────────────────────
    if '</table>' in c and SLOT_MID not in c:
        # Find first </table> that's not already adjacent to an ad
        idx = c.find('</table>')
        if idx > 0:
            c = c[:idx+8] + '\n' + ad_block(SLOT_MID, 'rectangle') + c[idx+8:]
            modified = True

    # ── BTM: after FAQ section, before Related or footer ─────────────────────
    # Find the closing of FAQ div, insert after it
    btm_anchors = ['<h2>Related Calculators</h2>', '<div class="tool-links">', '<footer>']
    if SLOT_BTM not in c:
        for anchor in btm_anchors:
            if anchor in c:
                c = c.replace(anchor, ad_block(SLOT_BTM, 'auto') + '\n' + anchor, 1)
                modified = True
                break

    if modified:
        write(path, c)
        calc_count += 1
        print(f'✓ CALC: {os.path.basename(path)}')

print(f'\nCalculator pages updated: {calc_count}\n')

# ══════════════════════════════════════════════════════════════════════════════
# 2. DE/FR/TR HOMEPAGES — 1 unit between calculator sections
# ══════════════════════════════════════════════════════════════════════════════
# Google policy for tool/app pages: 1-2 ad units acceptable when placed
# in content areas (not inside tools). We insert between the calculator
# panel sections, in a content-rich wrapper area.
#
# Placement: after the first major calculator panel section ends,
# before the next panel begins. This is a natural reading pause point.

HOME_SLOT = 'HOM0000000'

for lang in ['de', 'fr', 'tr']:
    path = os.path.join(BASE, lang, 'index.html')
    c = read(path)
    if already_done(c) or HOME_SLOT in c:
        print(f'  SKIP (done): {lang}/index.html')
        continue

    # Inject script
    if PUB not in c:
        c = c.replace('</head>', ADSENSE_SCRIPT + '\n' + AD_CSS + '\n</head>', 1)
    elif AD_CSS not in c:
        c = c.replace('</head>', AD_CSS + '\n</head>', 1)

    # Find a good mid-page break between calculator sections
    # Look for the section divider between calc panels
    # Typical pattern: panel wrapper closing + next panel opening
    # Try to inject after the 2nd panel (after LLM + Vector DB sections)
    anchors = [
        'id="vector"',   # before vector DB section
        'id="image"',    # before image gen section
        'id="pay"',      # before payment section
        'id="cloud"',    # before cloud section
    ]

    injected = False
    for anchor in anchors:
        if anchor in c and HOME_SLOT not in c:
            # Find the section tag containing this id
            idx = c.find(anchor)
            # Go back to find the opening of that section
            section_start = c.rfind('<section', 0, idx)
            if section_start > 0:
                home_ad = f'\n{ad_block(HOME_SLOT, "auto")}\n'
                c = c[:section_start] + home_ad + c[section_start:]
                injected = True
                print(f'✓ HOME {lang}: injected before {anchor}')
                break

    if not injected:
        print(f'  WARN: no anchor found for {lang}/index.html')
        continue

    write(path, c)

print('\nAll AdSense placements done.')
print(f'\nSlot IDs used (replace when AdSense approved):')
print(f'  TOP (intro→calc):       {SLOT_TOP}')
print(f'  MID (after table):      {SLOT_MID}')
print(f'  BTM (after FAQ):        {SLOT_BTM}')
print(f'  HOM (homepage middle):  {HOME_SLOT}')
print(f'\nTo activate: replace these 4 slot IDs + {PUB} with real values.')
