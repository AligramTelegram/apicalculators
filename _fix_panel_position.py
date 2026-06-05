#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move panels 11/12 inside .calc div (right after panel 10 agent)"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

PATHS = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

for path in PATHS:
    c = read(path)

    # Extract panels 11 and 12
    p11 = re.search(r'\n  <!-- PANEL 11.*?</section>', c, re.DOTALL)
    p12 = re.search(r'\n  <!-- PANEL 12.*?</section>', c, re.DOTALL)
    if not p11 or not p12:
        print(f'  SKIP {os.path.relpath(path, BASE)}')
        continue

    p11_html = p11.group(0)
    p12_html = p12.group(0)

    # Remove from current location
    c = c.replace(p11_html, '', 1)
    c = c.replace(p12_html, '', 1)

    # Find end of agent panel (id="agent") — insert right after its </section>
    m = re.search(r'(id="agent"[^<]*(?:<[^>]*>)*.*?</section>)', c, re.DOTALL)
    if m:
        pos = m.end()
        c = c[:pos] + p11_html + p12_html + c[pos:]
        write(path, c)
        print(f'✓ {os.path.relpath(path, BASE)}')
    else:
        print(f'  WARN: agent panel not found in {os.path.relpath(path, BASE)}')

print('Done.')
