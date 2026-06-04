#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'
path = BASE + r'\index.html'
c = open(path, encoding='utf-8').read()
m = re.search(r'<title>(.*?)</title>', c)
if m:
    print(f'Current title ({len(m.group(1))} chars): {m.group(1)}')
    old = m.group(0)
    new = '<title>API Cost Calculators: LLM, VPS, Serverless | APICalculators</title>'
    c = c.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'New title (52 chars): API Cost Calculators: LLM, VPS, Serverless | APICalculators')
