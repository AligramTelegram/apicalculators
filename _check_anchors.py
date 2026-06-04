#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')

for fname, searches in [
    ('blog/llm-api-cost-guide-2026.html', ['vector database', 'serverless', 'RAG', 'Lambda']),
    ('blog/vector-database-cost-comparison-2026.html', ['embedding', 'LLM', 'language model']),
    ('blog/stripe-vs-paddle-fees-2026.html', ['infrastructure', 'VPS', 'server']),
]:
    c = open(fname, encoding='utf-8').read()
    print(f'=== {fname} ===')
    for s in searches:
        idx = c.lower().find(s.lower())
        if idx >= 0:
            snippet = c[max(0,idx-30):idx+80].replace('\n', ' ')
            print(f'  "{s}": ...{snippet}...')
    print()
