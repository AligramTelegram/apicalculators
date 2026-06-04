#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Find all occurrences of search terms with context
for fname, searches in [
    ('blog/llm-api-cost-guide-2026.html', ['vector database', 'serverless', 'Lambda', 'RAG pipeline']),
    ('blog/vector-database-cost-comparison-2026.html', ['embedding', 'LLM cost', 'language model']),
    ('blog/stripe-vs-paddle-fees-2026.html', ['server', 'infra', 'hosting']),
]:
    c = open(fname, encoding='utf-8').read()
    print(f'=== {fname} ===')
    for s in searches:
        for m in re.finditer(re.escape(s), c, re.IGNORECASE):
            idx = m.start()
            snippet = c[max(0,idx-60):idx+100].replace('\n', ' ')
            if '<a href' not in c[max(0,idx-5):idx+len(s)+5]:
                print(f'  UNLINKED "{s}": ...{snippet}...')
    print()
