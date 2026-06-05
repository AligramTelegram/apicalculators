#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

OLD_CSS = """.donate-wrap{max-width:1140px;margin:18px auto 0;padding:0 22px}
.donate-box{padding:14px 20px;background:rgba(255,178,77,.05);border:1px solid rgba(255,178,77,.2);border-radius:10px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.donate-box .d-msg{font-size:13px;color:var(--muted);flex:1;min-width:180px}
.donate-box .d-msg strong{color:#ffb24d;display:block;font-size:13px;margin-bottom:2px}
.donate-id{font-family:'Cascadia Code','Consolas',monospace;font-size:14px;font-weight:700;color:var(--text);background:var(--bg);border:1px solid var(--border2);border-radius:6px;padding:6px 12px}
.copy-btn{background:rgba(255,178,77,.12);border:1px solid rgba(255,178,77,.3);color:#ffb24d;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:700;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:background .15s;white-space:nowrap}
.copy-btn:hover{background:rgba(255,178,77,.25)}
.copy-btn.copied{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.4);color:var(--lime)}"""

NEW_CSS = """.donate-wrap{max-width:1140px;margin:24px auto 0;padding:0 22px}
.donate-box{padding:20px 28px;background:linear-gradient(135deg,rgba(255,178,77,.08),rgba(255,178,77,.03));border:1px solid rgba(255,178,77,.35);border-radius:14px;display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;text-align:center;position:relative;overflow:hidden}
.donate-box::before{content:"";position:absolute;inset:0;background:radial-gradient(600px 120px at 50% 0%,rgba(255,178,77,.06),transparent);pointer-events:none}
.donate-box .d-msg{font-size:14px;color:var(--muted);text-align:center}
.donate-box .d-msg strong{color:#ffb24d;display:block;font-size:15px;font-weight:700;margin-bottom:3px;letter-spacing:-.01em}
.donate-id{font-family:'Cascadia Code','Consolas',monospace;font-size:16px;font-weight:700;color:var(--text);background:var(--bg);border:1px solid rgba(255,178,77,.4);border-radius:8px;padding:8px 16px;letter-spacing:.06em}
.copy-btn{background:rgba(255,178,77,.15);border:1px solid rgba(255,178,77,.4);color:#ffb24d;border-radius:8px;padding:9px 18px;font-size:13px;font-weight:700;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:all .15s;white-space:nowrap}
.copy-btn:hover{background:rgba(255,178,77,.3);transform:translateY(-1px)}
.copy-btn.copied{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.4);color:var(--lime)}"""

PATHS = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

for path in PATHS:
    c = read(path)
    if OLD_CSS in c:
        c = c.replace(OLD_CSS, NEW_CSS, 1)
        write(path, c)
        print(f'✓ {os.path.relpath(path, BASE)}')
    else:
        print(f'  SKIP {os.path.relpath(path, BASE)} (CSS not found verbatim)')

print('Done.')
