#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

BID = '90082319'
MSGS = {
    'en': ('☕ If this tool saved you time or money', 'Buy me a coffee via Binance', 'Copy ID', 'Copied!'),
    'de': ('☕ Wenn dieses Tool geholfen hat', 'Kaffee spendieren via Binance', 'ID kopieren', 'Kopiert!'),
    'fr': ("☕ Si cet outil vous a aide", 'Un cafe via Binance', "Copier l'ID", 'Copie!'),
    'tr': ('☕ Bu araç işine yaradıysa', 'Binance ile bir kahve ısmarla', 'ID kopyala', 'Kopyalandı!'),
}

DONATE_CSS = """.donate-wrap{max-width:1140px;margin:18px auto 0;padding:0 22px}
.donate-box{padding:14px 20px;background:rgba(255,178,77,.05);border:1px solid rgba(255,178,77,.2);border-radius:10px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.donate-box .d-msg{font-size:13px;color:var(--muted);flex:1;min-width:180px}
.donate-box .d-msg strong{color:#ffb24d;display:block;font-size:13px;margin-bottom:2px}
.donate-id{font-family:'Cascadia Code','Consolas',monospace;font-size:14px;font-weight:700;color:var(--text);background:var(--bg);border:1px solid var(--border2);border-radius:6px;padding:6px 12px}
.copy-btn{background:rgba(255,178,77,.12);border:1px solid rgba(255,178,77,.3);color:#ffb24d;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:700;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:background .15s;white-space:nowrap}
.copy-btn:hover{background:rgba(255,178,77,.25)}
.copy-btn.copied{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.4);color:var(--lime)}"""

MARKER = '<!-- DONATE-BOX -->'

def donate_html(lang):
    m1, m2, copy, copied = MSGS.get(lang, MSGS['en'])
    return (
        f'{MARKER}\n'
        f'<div class="donate-wrap"><div class="donate-box">\n'
        f'  <div class="d-msg"><strong>{m1}</strong>{m2}:</div>\n'
        f'  <span class="donate-id">{BID}</span>\n'
        f'  <button class="copy-btn" onclick="(function(b){{navigator.clipboard.writeText(\'{BID}\');'
        f'b.textContent=\'{copied}\';b.classList.add(\'copied\');'
        f'setTimeout(function(){{b.textContent=\'{copy}\';b.classList.remove(\'copied\')}},2000)}})(this)">'
        f'{copy}</button>\n</div></div>'
    )

# ── Step 1: Strip all donate HTML from every HTML file ────────────────────────
all_html = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
for path in all_html:
    c = read(path)
    orig = c
    c = re.sub(r'<!-- DONATE-BOX -->\n?', '', c)
    c = re.sub(r'<div class="donate-wrap">.*?</div></div>\n?', '', c, flags=re.DOTALL)
    c = re.sub(r'<div class="donate-box">.*?</div>\n?', '', c, flags=re.DOTALL)
    c = re.sub(r'<span class="donate-id"[^>]*>.*?</span>\n?', '', c, flags=re.DOTALL)
    c = re.sub(r'<button class="copy-btn"[^>]*>.*?</button>\n?', '', c, flags=re.DOTALL)
    c = re.sub(r'\n{3,}', '\n\n', c)
    if c != orig:
        write(path, c)
print('Step 1: Stripped')

# ── Step 2: Add CSS + ONE donate per homepage after </main> ───────────────────
HOME_LANGS = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in HOME_LANGS.items():
    c = read(path)

    # Add CSS if missing
    if 'donate-wrap' not in c:
        c = c.replace('</style>\n</head>', DONATE_CSS + '\n</style>\n</head>', 1)

    # Add donate HTML after </main>
    if MARKER not in c and '</main>' in c:
        c = c.replace('</main>', '</main>\n' + donate_html(lang), 1)

    write(path, c)
    n = c.count(MARKER)
    print(f'✓ {lang}: {n} donate box')

print('\nDone.')
