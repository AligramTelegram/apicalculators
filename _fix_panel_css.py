#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add panel-body grid CSS to match grid2 layout on all 4 homepages"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# Inject after .grid2 definition
FIX_CSS = """
.panel-body{display:grid;grid-template-columns:1.05fr .95fr;gap:26px;padding:28px}
.panel-body .inputs{display:flex;flex-direction:column;gap:0}
.lbl{display:block;font-size:13px;font-weight:600;color:var(--muted);margin-bottom:7px;margin-top:14px}
.lbl:first-child{margin-top:0}
.panel-body .result{position:relative}
.panel-body .result::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--lime),var(--cyan));border-radius:2px 2px 0 0}
@media(max-width:780px){.panel-body{grid-template-columns:1fr;padding:20px}}"""

PATHS = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

ANCHOR = '.grid2{display:grid;grid-template-columns:1.05fr .95fr;gap:26px}'

for path in PATHS:
    c = read(path)
    if '.panel-body{display:grid' in c:
        print(f'  SKIP: {os.path.relpath(path, BASE)}')
        continue
    if ANCHOR in c:
        c = c.replace(ANCHOR, ANCHOR + FIX_CSS, 1)
        write(path, c)
        print(f'✓ {os.path.relpath(path, BASE)}')
    else:
        # Try inserting before </style>
        c = c.replace('</style>\n</head>', FIX_CSS + '\n</style>\n</head>', 1)
        write(path, c)
        print(f'✓ (fallback) {os.path.relpath(path, BASE)}')

print('Done.')
