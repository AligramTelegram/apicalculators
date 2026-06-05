#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add donate box to all calc panels across all 4 lang homepages + dedicated calc pages"""
import sys, os, glob, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

BINANCE_ID = '90082319'

# Donate box HTML — injected once per panel (after affiliate-cta, before </section>)
DONATE_CSS = """
.donate-box{margin:14px 0 0;padding:14px 18px;background:rgba(255,178,77,.05);border:1px solid rgba(255,178,77,.2);border-radius:10px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.donate-box .d-msg{font-size:13px;color:var(--muted);flex:1;min-width:180px}
.donate-box .d-msg strong{color:#ffb24d;display:block;margin-bottom:2px;font-size:13px}
.donate-id{font-family:'Cascadia Code','Consolas',monospace;font-size:14px;font-weight:700;color:var(--text);background:var(--bg);border:1px solid var(--border2);border-radius:7px;padding:7px 12px;letter-spacing:.04em}
.copy-btn{background:rgba(255,178,77,.12);border:1px solid rgba(255,178,77,.3);color:#ffb24d;border-radius:7px;padding:7px 14px;font-size:12px;font-weight:700;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:background .15s;white-space:nowrap}
.copy-btn:hover{background:rgba(255,178,77,.22)}
.copy-btn.copied{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.4);color:var(--lime)}"""

# Per-language donate messages
DONATE_MSG = {
    'en': ('☕ If this tool saved you time or money', 'Buy me a coffee via Binance'),
    'de': ('☕ Wenn dieses Tool Zeit oder Geld gespart hat', 'Einen Kaffee spendieren via Binance'),
    'fr': ('☕ Si cet outil vous a fait gagner du temps', 'Offrez-moi un cafe via Binance'),
    'tr': ('☕ Bu araç işine yaradıysa', 'Bir kahve ısmarla — Binance ile'),
}
COPY_LABEL = {'en': 'Copy ID', 'de': 'ID kopieren', 'fr': "Copier l'ID", 'tr': 'ID kopyala'}
COPIED_LABEL = {'en': 'Copied!', 'de': 'Kopiert!', 'fr': 'Copie!', 'tr': 'Kopyalandı!'}

def donate_html(lang):
    msg1, msg2 = DONATE_MSG.get(lang, DONATE_MSG['en'])
    copy = COPY_LABEL.get(lang, 'Copy ID')
    copied = COPIED_LABEL.get(lang, 'Copied!')
    return f'''<div class="donate-box">
  <div class="d-msg"><strong>{msg1}</strong>{msg2}:</div>
  <span class="donate-id" id="bnb-{lang}">{BINANCE_ID}</span>
  <button class="copy-btn" onclick="(function(b){{navigator.clipboard.writeText('{BINANCE_ID}');b.textContent='{copied}';b.classList.add('copied');setTimeout(function(){{b.textContent='{copy}';b.classList.remove('copied')}},2000)}})(this)">{copy}</button>
</div>'''

# ─────────────────────────────────────────────────────────────────────────────
# 1. Homepages — inject donate after EACH affiliate-cta div, before </section>
# ─────────────────────────────────────────────────────────────────────────────
HOME_FILES = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in HOME_FILES.items():
    c = read(path)

    # Inject CSS once into <style> block
    if 'donate-box' not in c:
        c = c.replace('</style>\n</head>', DONATE_CSS + '\n</style>\n</head>', 1)

    # After each </div>\n</section> that follows an affiliate-cta, inject donate
    # Pattern: affiliate-cta div closes → </div>\n</section>
    # We inject donate BEFORE </section> of each panel
    d_html = donate_html(lang)
    if 'donate-box' not in c or c.count('donate-box') < 5:
        # Replace each </div>\n</section> that's preceded by affiliate-cta closing
        # Strategy: find all affiliate-cta closing patterns
        c = re.sub(
            r'(</div>\n</div>\n</section>)',
            lambda m: m.group(1).replace(
                '</div>\n</section>',
                d_html + '\n</section>',
                1
            ),
            c
        )
        # Also handle: </div>\n</section> after affiliate-cta directly
        c = re.sub(
            r'(class="affiliate-cta"[^>]*>.*?</div>\n)(</section>)',
            r'\1' + d_html + '\n' + r'\2',
            c, flags=re.DOTALL
        )

    write(path, c)
    print(f'✓ {lang}: homepage donate added')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Dedicated calc pages — inject donate after affiliate-cta
# ─────────────────────────────────────────────────────────────────────────────
calc_files = []
# EN root calc pages
calc_files += glob.glob(os.path.join(BASE, '*-calculator*.html'))
calc_files += glob.glob(os.path.join(BASE, '*-cost*.html'))
calc_files += glob.glob(os.path.join(BASE, '*-comparison*.html'))
calc_files += glob.glob(os.path.join(BASE, 'auth-provider-cost.html'))
# DE/FR/TR dedicated calc pages
for sub in ['de','fr','tr']:
    calc_files += glob.glob(os.path.join(BASE, sub, '*.html'))

# Filter to only calc/tool pages (not blog, about, terms, privacy, index)
skip = {'index.html','about.html','terms.html','privacy.html','404.html','sitemap.html'}
calc_files = [f for f in calc_files
              if os.path.basename(f) not in skip
              and 'blog' not in f
              and os.path.exists(f)]

updated = 0
for path in calc_files:
    c = read(path)
    if 'donate-box' in c:
        continue

    # Detect lang from html tag
    lang = 'en'
    m = re.search(r'<html lang="([^"]+)"', c)
    if m:
        l = m.group(1)
        lang = 'de' if l=='de' else 'fr' if l=='fr' else 'tr' if l=='tr' else 'en'

    d_html = donate_html(lang)

    # Inject CSS
    if 'donate-box' not in c:
        c = c.replace('</style>', DONATE_CSS + '\n</style>', 1)

    # Inject donate after aff-box / affiliate-cta div
    for anchor in ['\n</div>\n<section class="sec">\n  <h2>Frequently',
                   '\n</div>\n<section class="sec">\n  <h2>FAQ',
                   '\n<section class="sec">\n  <h2>Related',
                   '\n<section class="sec">\n  <h2>Verwandte',
                   '\n<section class="sec">\n  <h2>Calculateurs',
                   '\n<section class="sec">\n  <h2>Ilgili']:
        if anchor in c:
            c = c.replace(anchor, '\n' + d_html + anchor, 1)
            updated += 1
            break
    else:
        # Fallback: before </div>\n</div>\n<footer
        if '\n</div>\n<footer>' in c:
            c = c.replace('\n</div>\n<footer>', '\n' + d_html + '\n</div>\n<footer>', 1)
            updated += 1

    write(path, c)

print(f'✓ {updated} dedicated calc pages updated')
print('\nAll done.')
