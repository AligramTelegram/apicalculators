#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Remove ALL affiliate-cta divs from all HTML files
2. Remove duplicate donate-box (keep only first per panel)
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

all_html = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
all_html = [f for f in all_html if 'node_modules' not in f]

aff_removed = 0
dup_removed = 0

for path in all_html:
    c = read(path)
    orig = c

    # ── 1. Remove ALL affiliate-cta divs ─────────────────────────────────────
    # Pattern: <div class="affiliate-cta"...>...</div>
    c = re.sub(
        r'\n?<div class="affiliate-cta"[^>]*>.*?</div>\s*',
        '\n',
        c, flags=re.DOTALL
    )

    # ── 2. Remove duplicate donate-box — keep first, remove subsequent ────────
    count = len(re.findall(r'<div class="donate-box"', c))
    if count > 1:
        # Find all donate-box positions
        positions = [m.start() for m in re.finditer(r'<div class="donate-box"', c)]
        # Build new string: keep first, remove rest
        # Find end of each donate-box div
        result = c
        # Remove from last to first to preserve positions
        for start in reversed(positions[1:]):
            # Find matching </div>
            end = result.find('</div>', start) + len('</div>')
            # Also remove surrounding newlines
            while end < len(result) and result[end] == '\n':
                end += 1
            result = result[:start] + result[end:]
        c = result
        dup_removed += (count - 1)

    if c != orig:
        write(path, c)
        if aff_removed == 0 and '</div>' in orig and 'affiliate-cta' in orig:
            aff_removed += 1

# Count stats
total_aff = 0
total_dup = 0
for path in all_html:
    c = read(path)
    if 'affiliate-cta' in c:
        total_aff += 1
    cnt = len(re.findall(r'<div class="donate-box"', c))
    if cnt > 1:
        total_dup += 1

print(f'Affiliate-cta remaining: {total_aff} files')
print(f'Files with duplicate donate: {total_dup}')
print('Done.')
