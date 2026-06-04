#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 8: Fix internal linking — Coming placeholders + internal link map."""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(fname):
    return open(os.path.join(BASE, fname), encoding='utf-8').read()

def write(fname, c):
    with open(os.path.join(BASE, fname), 'w', encoding='utf-8') as f:
        f.write(c)

# ── 1. Fix "Coming" placeholders in llm-api-cost-guide-2026.html ──────────────

llm_file = 'blog/llm-api-cost-guide-2026.html'
c = read(llm_file)

c = c.replace(
    '<a href="#" class="rel-card">\n                <div class="rt">Coming · Vector DB</div>\n                <p>Pinecone vs Supabase vs Qdrant: Vector Database Cost Showdown</p>\n              </a>',
    '<a href="/blog/vector-database-cost-comparison-2026.html" class="rel-card">\n                <div class="rt">Guide · Vector DB</div>\n                <p>Pinecone vs Supabase vs Qdrant: Vector Database Cost Showdown</p>\n              </a>'
)

c = c.replace(
    '<a href="#" class="rel-card">\n                <div class="rt">Coming · Payment</div>\n                <p>Stripe vs Paddle: Which Is Actually Cheaper for SaaS?</p>\n              </a>',
    '<a href="/blog/stripe-vs-paddle-fees-2026.html" class="rel-card">\n                <div class="rt">Guide · Payment</div>\n                <p>Stripe vs Paddle: Which Is Actually Cheaper for SaaS?</p>\n              </a>'
)

c = c.replace(
    '<a href="#" class="rel-card">\n                <div class="rt">Coming · Image Gen</div>\n                <p>DALL·E 3 vs Stable Diffusion XL: Cost &amp; Quality at Scale</p>\n              </a>',
    '<a href="/blog/dalle3-vs-stable-diffusion-cost-2026.html" class="rel-card">\n                <div class="rt">Guide · Image Gen</div>\n                <p>DALL·E 3 vs Stable Diffusion XL: Cost &amp; Quality at Scale</p>\n              </a>'
)

write(llm_file, c)
print('✓ Fixed Coming placeholders in llm-api-cost-guide-2026.html')

# ── 2. Internal link map ───────────────────────────────────────────────────────
# Strategy: inject contextual inline links into existing paragraph text.
# We find a unique substring in each source file and inject an <a> tag.

LINKS = [
    # (file, find_text, replace_with) — exactly once per file
    (
        'blog/llm-api-cost-guide-2026.html',
        'vector database costs for RAG pipelines',
        '<a href="/blog/vector-database-cost-comparison-2026.html">vector database costs for RAG pipelines</a>'
    ),
    (
        'blog/llm-api-cost-guide-2026.html',
        'serverless compute to run your LLM app',
        '<a href="/blog/aws-lambda-cost-calculator-2026.html">serverless compute to run your LLM app</a>'
    ),
    (
        'blog/vector-database-cost-comparison-2026.html',
        'full AI stack cost with LLM',
        '<a href="/blog/llm-api-cost-guide-2026.html">full AI stack cost with LLM</a>'
    ),
    (
        'blog/stripe-vs-paddle-fees-2026.html',
        'full SaaS infrastructure cost',
        '<a href="/blog/cloud-vps-cost-comparison-2026.html">full SaaS infrastructure cost</a>'
    ),
]

for fname, needle, replacement in LINKS:
    c = read(fname)
    if needle in c:
        # Check it's not already linked
        if f'href=' in replacement and replacement in c:
            print(f'  SKIP (already linked): {needle[:40]} in {fname}')
        elif needle in c:
            c = c.replace(needle, replacement, 1)
            write(fname, c)
            print(f'✓ Injected link "{needle[:50]}" in {fname}')
    else:
        print(f'  MISSING anchor: "{needle[:50]}" in {fname}')

# ── 3. Add ilink-box entries where missing ────────────────────────────────────
# For aws-lambda: link to cloud-vps and api-gateway
# For cloud-vps: link to aws-lambda
# For vector-db: link to embedding-api and llm

def add_to_ilink(fname, new_links):
    """Add links to .ilink-box .il-grid if not already present."""
    c = read(fname)
    for url, label in new_links:
        if url in c:
            print(f'  SKIP (exists): {url} in {fname}')
            continue
        insert = f'          <a href="{url}">{label}</a>\n'
        marker = '<a href="/blog/">Blog Index</a>'
        if marker in c:
            c = c.replace(marker, insert + '          ' + marker, 1)
            print(f'✓ Added ilink: {label} → {url} in {fname}')
        else:
            print(f'  SKIP (no marker): {fname}')
    write(fname, c)

add_to_ilink('blog/aws-lambda-cost-calculator-2026.html', [
    ('/blog/cloud-vps-cost-comparison-2026.html', 'When Lambda costs more than a VPS'),
    ('/blog/api-gateway-pricing-2026.html', 'API Gateway: $3.50/M hidden cost'),
])

add_to_ilink('blog/cloud-vps-cost-comparison-2026.html', [
    ('/blog/aws-lambda-cost-calculator-2026.html', 'Go serverless instead'),
])

add_to_ilink('blog/vector-database-cost-comparison-2026.html', [
    ('/blog/embedding-api-cost-2026.html', 'Embedding API cost to generate vectors'),
    ('/blog/llm-api-cost-guide-2026.html', 'Full AI stack cost: LLM + Vector DB'),
])

add_to_ilink('blog/stripe-vs-paddle-fees-2026.html', [
    ('/blog/cloud-vps-cost-comparison-2026.html', 'Full SaaS infrastructure cost'),
])

# ── 4. Inject contextual inline links into aws-lambda and cloud-vps ───────────
# aws-lambda: link to cloud-vps in the "When to Choose" comparison table footer
# cloud-vps: link to aws-lambda in existing related paragraph

fname_lambda = 'blog/aws-lambda-cost-calculator-2026.html'
c = read(fname_lambda)
# Already injected by section 6 — find the sentence about VPS
old = 'a $6 VPS may undercut Lambda on total cost'
new = 'a <a href="/blog/cloud-vps-cost-comparison-2026.html">$6 VPS</a> may undercut Lambda on total cost'
if old in c and new not in c:
    c = c.replace(old, new, 1)
    write(fname_lambda, c)
    print('✓ Inline VPS link injected in aws-lambda post')

fname_vps = 'blog/cloud-vps-cost-comparison-2026.html'
c = read(fname_vps)
old = 'or go serverless instead'
new = 'or <a href="/blog/aws-lambda-cost-calculator-2026.html">go serverless instead</a>'
if old in c and new not in c:
    c = c.replace(old, new, 1)
    write(fname_vps, c)
    print('✓ Inline serverless link injected in cloud-vps post')

# vector-db: inject embedding link in body
fname_vec = 'blog/vector-database-cost-comparison-2026.html'
c = read(fname_vec)
old_emb = 'embedding API cost to generate your vectors'
new_emb = '<a href="/blog/embedding-api-cost-2026.html">embedding API cost to generate your vectors</a>'
if old_emb in c and new_emb not in c:
    c = c.replace(old_emb, new_emb, 1)
    write(fname_vec, c)
    print('✓ Inline embedding link injected in vector-db post')

print('\nSection 8 done.')
