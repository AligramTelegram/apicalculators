#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Specific paragraph content to locate injection points
c = open('blog/llm-api-cost-guide-2026.html', encoding='utf-8').read()
# Find paragraphs with 'vector' or 'serverless'
import re
for m in re.finditer(r'<p[^>]*>([^<]{0,200}(vector|serverless|lambda)[^<]{0,200})</p>', c, re.IGNORECASE):
    print('LLM:', m.group()[:200])
    print()

c2 = open('blog/vector-database-cost-comparison-2026.html', encoding='utf-8').read()
# Find good paragraph before which to inject
idx = c2.find('text-embedding-3-small')
print('VEC context:', c2[max(0,idx-200):idx+300].replace('\n', ' '))
print()

c3 = open('blog/stripe-vs-paddle-fees-2026.html', encoding='utf-8').read()
idx = c3.find('infrastructure')
print('STR context:', c3[max(0,idx-100):idx+300].replace('\n', ' '))
