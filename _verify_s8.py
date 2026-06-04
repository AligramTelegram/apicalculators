#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

checks = [
    ('blog/llm-api-cost-guide-2026.html', [
        '/blog/vector-database-cost-comparison-2026.html',
        '/blog/stripe-vs-paddle-fees-2026.html',
        '/blog/dalle3-vs-stable-diffusion-cost-2026.html',
        '/blog/aws-lambda-cost-calculator-2026.html',
    ]),
    ('blog/aws-lambda-cost-calculator-2026.html', [
        '/blog/cloud-vps-cost-comparison-2026.html',
        '/blog/api-gateway-pricing-2026.html',
    ]),
    ('blog/cloud-vps-cost-comparison-2026.html', [
        '/blog/aws-lambda-cost-calculator-2026.html',
    ]),
    ('blog/vector-database-cost-comparison-2026.html', [
        '/blog/embedding-api-cost-2026.html',
        '/blog/llm-api-cost-guide-2026.html',
    ]),
    ('blog/stripe-vs-paddle-fees-2026.html', [
        '/blog/cloud-vps-cost-comparison-2026.html',
    ]),
]

all_ok = True
for fname, urls in checks:
    c = open(fname, encoding='utf-8').read()
    for url in urls:
        if url in c:
            print(f'  ✓ {url} in {fname}')
        else:
            print(f'  ✗ MISSING: {url} in {fname}')
            all_ok = False

# Check Coming placeholders gone
c = open('blog/llm-api-cost-guide-2026.html', encoding='utf-8').read()
if 'Coming ·' in c:
    print('  ✗ Still has "Coming" placeholders!')
    all_ok = False
else:
    print('  ✓ No "Coming" placeholders remaining')

print('\nAll OK!' if all_ok else '\nSome issues found.')
