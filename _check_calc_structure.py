#!/usr/bin/env python3
import sys, re, os, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

c = open(os.path.join(BASE, 'llm-cost-calculator.html'), encoding='utf-8').read()
markers = ['<p class="intro"', '<div class="calc-shell"', '<h2>2026 LLM',
           '<h2>Real-World', '<h2>Frequently', '<h2>Related', '</main>', '<footer']
for m in markers:
    idx = c.find(m)
    if idx > 0:
        snippet = c[idx:idx+60].replace('\n', ' ')
        print(f'{idx:6d}: {snippet}')

# Also check all 15 calc pages for common structure patterns
print('\n--- Structural patterns across all calc pages ---')
calc_files = [f for f in glob.glob(os.path.join(BASE, '*.html'))
              if os.path.basename(f) not in ('index.html','404.html','privacy.html','about.html','terms.html')]

for pat in ['calc-shell', 'class="intro"', '<h2>Frequently', '<h2>Related', 'affiliate-cta']:
    count = sum(1 for f in calc_files if pat in open(f, encoding='utf-8').read())
    print(f'  "{pat}": {count}/{len(calc_files)} files')
