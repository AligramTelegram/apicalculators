#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

FIXES = [
    # EN
    ('<button class="tab" data-tab="coding" role="tab">💻 AI Coding</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="coding" data-tab="coding"><span class="ic">💻</span> AI Coding <span class="num">11</span></button>'),
    ('<button class="tab" data-tab="auth" role="tab">🔑 Auth Cost</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="auth" data-tab="auth"><span class="ic">🔑</span> Auth Cost <span class="num">12</span></button>'),
    # DE
    ('<button class="tab" data-tab="coding" role="tab">💻 KI Coding</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="coding" data-tab="coding"><span class="ic">💻</span> KI Coding <span class="num">11</span></button>'),
    ('<button class="tab" data-tab="auth" role="tab">🔑 Auth Kosten</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="auth" data-tab="auth"><span class="ic">🔑</span> Auth Kosten <span class="num">12</span></button>'),
    # FR
    ('<button class="tab" data-tab="coding" role="tab">💻 Outils IA</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="coding" data-tab="coding"><span class="ic">💻</span> Outils IA <span class="num">11</span></button>'),
    ('<button class="tab" data-tab="auth" role="tab">🔑 Cout Auth</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="auth" data-tab="auth"><span class="ic">🔑</span> Cout Auth <span class="num">12</span></button>'),
    # TR
    ('<button class="tab" data-tab="coding" role="tab">💻 YZ Kodlama</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="coding" data-tab="coding"><span class="ic">💻</span> YZ Kodlama <span class="num">11</span></button>'),
    ('<button class="tab" data-tab="auth" role="tab">🔑 Auth Maliyet</button>',
     '<button class="tab" role="tab" aria-selected="false" aria-controls="auth" data-tab="auth"><span class="ic">🔑</span> Auth Maliyet <span class="num">12</span></button>'),
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
        print(f'✓ {os.path.relpath(path, BASE)}')
    else:
        print(f'  SKIP {os.path.relpath(path, BASE)}')

print('Done.')
