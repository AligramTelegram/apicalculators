#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'
path = os.path.join(BASE, 'index.html')

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

c = read(path)

# 1. Title — 61 → 59 chars
c = c.replace(
    '<title>API Cost Calculators: LLM, VPS, Serverless | APICalculators</title>',
    '<title>LLM & API Cost Calculators: Free Tools 2026 | APICalculators</title>'
)

# 2. Meta description — 189 → ~155 chars
c = c.replace(
    '<meta name="description" content="Free real-time cost calculators for LLM tokens, vector databases, cloud VPS, serverless (AWS Lambda), STT/TTS APIs, API gateway, embeddings, AI agents and payment fees. 10 tools, zero signup.">',
    '<meta name="description" content="Free AI infrastructure cost calculators. Compare LLM, vector DB, serverless, API gateway, embedding, auth and coding tool pricing. 12 tools, zero signup, runs in browser.">'
)

# 3. Meta keywords — add 2 new tools
c = c.replace(
    '<meta name="keywords" content="LLM cost calculator, AWS Lambda cost calculator, cloud VPS comparison, embedding API cost, STT TTS API pricing, API gateway pricing, AI agent cost, vector database pricing, payment processor fees">',
    '<meta name="keywords" content="LLM cost calculator, AWS Lambda cost calculator, cloud VPS comparison, embedding API cost, STT TTS API pricing, API gateway pricing, AI agent cost, vector database pricing, payment processor fees, AI coding tool cost, auth provider cost calculator, Clerk vs Supabase pricing, Cursor vs Copilot cost">'
)

# 4. H1 — add keyword signal
c = c.replace(
    '<h1 class="h">Know your <span class="em">infra costs</span><br>before the invoice does.</h1>',
    '<h1 class="h">Free <span class="em">API & AI Cost Calculators</span> — Know Your Infra Bill Before It Arrives.</h1>'
)

# 5. Hero tagpill — update count
c = c.replace(
    '2026 pricing · 10 calculators · runs 100% in your browser',
    '2026 pricing · 12 calculators · runs 100% in your browser'
)

# 6. OG title — match new title theme
c = c.replace(
    '<meta property="og:title" content="APICalculators — Developer Infrastructure Cost Hub">',
    '<meta property="og:title" content="Free LLM & API Cost Calculators 2026 | APICalculators">'
)

# 7. Twitter title
c = c.replace(
    '<meta name="twitter:title" content="APICalculators — Free Developer Cost Optimization Tools">',
    '<meta name="twitter:title" content="Free LLM & API Cost Calculators 2026 | APICalculators">'
)

# 8. WebPage schema — update name + dateModified
c = c.replace(
    '"name":"LLM Cost Calculator & AI Infrastructure Pricing Tools"',
    '"name":"Free LLM & API Cost Calculators 2026 — APICalculators"'
)
c = c.replace('"dateModified":"2026-06-02"', '"dateModified":"2026-06-05"')

# 9. SoftwareApplication schema — remove unverified aggregateRating
c = c.replace(
    ',"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","ratingCount":"150"}',
    ''
)

# 10. Hero sub text — add "12 tools"
c = c.replace(
    'Real-time cost estimators for LLM tokens, vector databases, AI image generation, and SaaS payment fees. Free, no signup, zero data leaves your device.',
    'Real-time cost calculators for LLM tokens, vector databases, cloud VPS, serverless, auth providers, AI coding tools and payment fees. 12 free tools, zero signup.'
)

write(path, c)
print('✓ EN homepage SEO fixes applied')

# Verify
c2 = read(path)
import re
title = re.search(r'<title>(.*?)</title>', c2).group(1)
desc  = re.search(r'<meta name="description" content="([^"]+)"', c2).group(1)
h1    = re.search(r'<h1[^>]*>(.*?)</h1>', c2, re.DOTALL).group(1)
h1_clean = re.sub(r'<[^>]+>', '', h1).strip()

print(f'\nTitle ({len(title)} chars): {title}')
print(f'Desc  ({len(desc)} chars): {desc}')
print(f'H1: {h1_clean}')
