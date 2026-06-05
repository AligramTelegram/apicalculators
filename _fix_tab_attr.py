#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

FIXES = [
    # Fix tab buttons: data-panel → data-tab
    ('data-panel="coding"', 'data-tab="coding"'),
    ('data-panel="auth"',   'data-tab="auth"'),
]

paths = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

for path in paths:
    c = read(path)
    orig = c
    for old, new in FIXES:
        c = c.replace(old, new)
    if c != orig:
        write(path, c)
        lang = path.split(os.sep)[-2] if 'index' not in path.split(os.sep)[-2] else 'en'
        print(f'✓ Fixed: {os.path.relpath(path, BASE)}')
    else:
        print(f'  SKIP: {os.path.relpath(path, BASE)}')

print('Done.')
