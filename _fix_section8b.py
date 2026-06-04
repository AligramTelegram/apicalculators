#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 8b: Inject inline contextual links and related guides boxes."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(fname):
    return open(os.path.join(BASE, fname), encoding='utf-8').read()

def write(fname, c):
    with open(os.path.join(BASE, fname), 'w', encoding='utf-8') as f:
        f.write(c)

ILINK_CSS = '''<style>
.ilink-box{background:#12161d;border:1px solid #27313e;border-radius:12px;padding:18px;margin:28px 0}
.ilink-box .il-title{font-family:'Cascadia Code','Consolas',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#8a96a5;margin-bottom:12px;font-weight:700}
.ilink-box .il-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
.ilink-box a{display:flex;align-items:center;gap:8px;background:#161b24;border:1px solid #1d2530;border-radius:8px;padding:9px 12px;color:#8b97a4;font-size:13px;font-weight:500;text-decoration:none;transition:all .15s}
.ilink-box a:hover{border-color:#b8ff2e;color:#e8edf1}
.ilink-box a::before{content:"→";color:#b8ff2e;font-weight:700}
</style>'''

RELATED_BOX = lambda links: '<div class="ilink-box"><div class="il-title">Related Tools &amp; Guides</div><div class="il-grid">' + ''.join(f'<a href="{u}">{t}</a>' for u,t in links) + '</div></div>'

# ── 1. LLM guide: add 2 contextual sentences with links in article body ───────
fname = 'blog/llm-api-cost-guide-2026.html'
c = read(fname)

# Inject after "most cost-effective" tip — find a good paragraph near optimization section
OLD = 'This is the highest-leverage decision.'
NEW = 'This is the highest-leverage decision. For full-stack cost planning, also see <a href="/blog/vector-database-cost-comparison-2026.html">vector database costs for RAG pipelines</a> and <a href="/blog/aws-lambda-cost-calculator-2026.html">serverless compute to run your LLM app</a>.'
if OLD in c and NEW not in c:
    c = c.replace(OLD, NEW, 1)
    write(fname, c)
    print('✓ Injected vector-db + lambda links into LLM guide body')

# ── 2. Vector DB: inject embedding link + add related box before </main> ───────
fname = 'blog/vector-database-cost-comparison-2026.html'
c = read(fname)

OLD = 'All scenarios use 1536-dimension float32 vectors (OpenAI <code>text-embedding-3-small</code> output).'
NEW = 'All scenarios use 1536-dimension float32 vectors (OpenAI <code>text-embedding-3-small</code> output). For the cost of generating those vectors, see the <a href="/blog/embedding-api-cost-2026.html">embedding API cost guide</a>.'
if OLD in c and NEW not in c:
    c = c.replace(OLD, NEW, 1)
    write(fname, c)
    print('✓ Injected embedding link in vector-db body')

# Also check if there's already a related box — if not, add before </main>
if 'ilink-box' not in c:
    c = read(fname)
    box = RELATED_BOX([
        ('/blog/embedding-api-cost-2026.html', 'Embedding API cost guide'),
        ('/blog/llm-api-cost-guide-2026.html', 'Full AI stack cost with LLM'),
        ('/blog/', 'Blog index'),
    ])
    c = c.replace('</main>', box + '\n</main>', 1)
    write(fname, c)
    print('✓ Added related box to vector-db post')

# ── 3. Stripe: inject VPS link in "Choose Stripe if" section + related box ────
fname = 'blog/stripe-vs-paddle-fees-2026.html'
c = read(fname)

OLD = 'You already have tax compliance infrastructure'
NEW = 'You already have tax compliance infrastructure — and want to calculate your <a href="/blog/cloud-vps-cost-comparison-2026.html">full SaaS infrastructure cost</a>'
if OLD in c and NEW not in c:
    c = c.replace(OLD, NEW, 1)
    write(fname, c)
    print('✓ Injected VPS link in stripe post body')

if 'ilink-box' not in c:
    c = read(fname)
    box = RELATED_BOX([
        ('/blog/cloud-vps-cost-comparison-2026.html', 'Full SaaS infrastructure cost'),
        ('/blog/llm-api-cost-guide-2026.html', 'LLM API cost guide'),
        ('/blog/', 'Blog index'),
    ])
    # Inject CSS too if needed
    if 'ilink-box' not in c:
        c = c.replace('</head>', ILINK_CSS + '\n</head>', 1)
        c = c.replace('</main>', box + '\n</main>', 1)
        write(fname, c)
        print('✓ Added related box + CSS to stripe post')

# ── 4. Cloud VPS: inject Lambda link in the "go serverless" paragraph ─────────
fname = 'blog/cloud-vps-cost-comparison-2026.html'
c = read(fname)
OLD = 'or <a href="/blog/aws-lambda-cost-calculator-2026.html">go serverless instead</a>'
if OLD not in c:
    # inject into the last paragraph of the new TCO section
    OLD2 = 'or go serverless instead'
    NEW2 = 'or <a href="/blog/aws-lambda-cost-calculator-2026.html">go serverless instead</a>'
    if OLD2 in c:
        c = c.replace(OLD2, NEW2, 1)
        write(fname, c)
        print('✓ Serverless link injected in cloud-vps post')
else:
    print('  SKIP: serverless link already in cloud-vps post')

print('\nSection 8b done.')
