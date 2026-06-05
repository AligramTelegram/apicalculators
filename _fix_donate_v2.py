#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Complete donate cleanup + reinject: strip all donate HTML, add clean version"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Strip ALL donate-related HTML from every file
# ─────────────────────────────────────────────────────────────────────────────
all_html = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)

STRIP_PATTERNS = [
    # Full donate-box div
    r'\n?<div class="donate-box">.*?</div>\s*',
    # Orphan donate-id spans
    r'\n?\s*<span class="donate-id"[^>]*>.*?</span>\s*',
    # Orphan copy-btn buttons
    r'\n?\s*<button class="copy-btn"[^>]*>.*?</button>\s*',
    # Stray </div> after donate removal (only if line is just </div>)
]

for path in all_html:
    c = read(path)
    orig = c
    for pat in STRIP_PATTERNS:
        c = re.sub(pat, '\n', c, flags=re.DOTALL)
    # Clean up triple+ newlines
    c = re.sub(r'\n{3,}', '\n\n', c)
    if c != orig:
        write(path, c)

print('Step 1: All donate HTML stripped')

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Reinject ONE donate-box per panel in homepages
#         → right before </section> of each .panel
# ─────────────────────────────────────────────────────────────────────────────
DONATE_CSS = """.donate-box{margin:12px 0 0;padding:12px 16px;background:rgba(255,178,77,.05);border:1px solid rgba(255,178,77,.2);border-radius:10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.donate-box .d-msg{font-size:12.5px;color:var(--muted);flex:1;min-width:160px}
.donate-box .d-msg strong{color:#ffb24d;display:block;margin-bottom:1px;font-size:12.5px}
.donate-id{font-family:'Cascadia Code','Consolas',monospace;font-size:14px;font-weight:700;color:var(--text);background:var(--bg);border:1px solid var(--border2);border-radius:6px;padding:6px 11px}
.copy-btn{background:rgba(255,178,77,.12);border:1px solid rgba(255,178,77,.3);color:#ffb24d;border-radius:6px;padding:6px 12px;font-size:12px;font-weight:700;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:background .15s;white-space:nowrap}
.copy-btn:hover{background:rgba(255,178,77,.22)}
.copy-btn.copied{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.4);color:var(--lime)}"""

BID = '90082319'

MSGS = {
    'en': ('☕ If this tool helped you', 'Buy me a coffee via Binance', 'Copy ID', 'Copied!'),
    'de': ('☕ Wenn dieses Tool geholfen hat', 'Kaffee spendieren via Binance', 'ID kopieren', 'Kopiert!'),
    'fr': ("☕ Si cet outil vous a aide", 'Un cafe via Binance', "Copier l'ID", 'Copie!'),
    'tr': ('☕ Bu araç işine yaradıysa', 'Binance ile bir kahve ısmarla', 'ID kopyala', 'Kopyalandı!'),
}

def donate_html(lang, uid):
    m1, m2, copy, copied = MSGS.get(lang, MSGS['en'])
    return (
        f'<div class="donate-box">\n'
        f'  <div class="d-msg"><strong>{m1}</strong>{m2}:</div>\n'
        f'  <span class="donate-id">{BID}</span>\n'
        f'  <button class="copy-btn" onclick="(function(b){{navigator.clipboard.writeText(\'{BID}\');'
        f'b.textContent=\'{copied}\';b.classList.add(\'copied\');'
        f'setTimeout(function(){{b.textContent=\'{copy}\';b.classList.remove(\'copied\')}},2000)}})(this)">'
        f'{copy}</button>\n</div>'
    )

HOME_LANGS = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in HOME_LANGS.items():
    c = read(path)

    # Add CSS once
    if '.donate-box{' not in c:
        c = c.replace('</style>\n</head>', DONATE_CSS + '\n</style>\n</head>', 1)

    d = donate_html(lang, lang)

    # Inject once per <section class="panel"...> — before its </section>
    # Find each panel section and add donate before closing tag
    # Use a counter to give unique IDs
    counter = [0]
    def inject_donate(m):
        counter[0] += 1
        # Insert donate before </section>
        section = m.group(0)
        return section[:-len('</section>')] + d + '\n</section>'

    c = re.sub(r'<section class="panel".*?</section>', inject_donate, c, flags=re.DOTALL)

    write(path, c)
    print(f'✓ {lang}: {counter[0]} panels — donate injected')

print('\nStep 2: Donate boxes reinjected')

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Verify — count donate-box per homepage
# ─────────────────────────────────────────────────────────────────────────────
print('\n--- Verification ---')
for lang, path in HOME_LANGS.items():
    c = read(path)
    n = len(re.findall(r'<div class="donate-box">', c))
    panels = len(re.findall(r'<section class="panel"', c))
    print(f'{lang}: {n} donate boxes / {panels} panels')

print('\nDone.')
