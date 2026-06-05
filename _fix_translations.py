#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4a + S4b: Translate calc input labels + keyword comments in DE/FR/TR homepages.
S5: Add Article + FAQPage JSON-LD schema to EN blog posts.
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

def apply_replacements(c, pairs):
    for old, new in pairs:
        c = c.replace(old, new)
    return c

# ─────────────────────────────────────────────────────────────────────────────
# S4a + S4b DE
# ─────────────────────────────────────────────────────────────────────────────
DE_REPLACEMENTS = [
    ('Keyword: <em>AWS Lambda cost calculator</em>', 'Keyword: <em>AWS Lambda Kostenrechner</em>'),
    ('Keyword: <em>API gateway pricing calculator</em>', 'Keyword: <em>API Gateway Kostenrechner</em>'),
    ('Keyword: <em>embedding API cost</em>', 'Keyword: <em>Embedding API Kosten</em>'),
    ('Keyword: <em>AI agent cost calculator</em>', 'Keyword: <em>KI-Agent Kostenschätzer</em>'),
    ('<label class="lbl" for="sttModel">Provider</label>', '<label class="lbl" for="sttModel">Anbieter</label>'),
    ('<label class="lbl" for="sttVol">Audio minutes / month</label>', '<label class="lbl" for="sttVol">Audiominuten / Monat</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="sttRate">—</b></div>', '<div class="brow"><span>Preis / 1M Token</span><b id="sttRate">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="sttAnnual">—</b></div>', '<div class="brow hl"><span>Jahresschätzung</span><b id="sttAnnual">—</b></div>'),
    ('<label class="lbl" for="slProvider">Platform</label>', '<label class="lbl" for="slProvider">Plattform</label>'),
    ('<label class="lbl" for="slInvoke">Invocations / month</label>', '<label class="lbl" for="slInvoke">Aufrufe / Monat</label>'),
    ('<label class="lbl" for="slDuration">Avg duration (ms)</label>', '<label class="lbl" for="slDuration">Ø Dauer (ms)</label>'),
    ('<label class="lbl" for="slMemory">Memory</label>', '<label class="lbl" for="slMemory">Arbeitsspeicher</label>'),
    ('<div class="brow"><span>Invocation cost</span><b id="slInvCost">—</b></div>', '<div class="brow"><span>Aufrufkosten</span><b id="slInvCost">—</b></div>'),
    ('<div class="brow"><span>Compute cost (GB-sec)</span><b id="slCompCost">—</b></div>', '<div class="brow"><span>Rechenkosten (GB-Sek.)</span><b id="slCompCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="slAnnual">—</b></div>', '<div class="brow hl"><span>Jahresschätzung</span><b id="slAnnual">—</b></div>'),
    ('<label class="lbl" for="gwProvider">Provider</label>', '<label class="lbl" for="gwProvider">Anbieter</label>'),
    ('<label class="lbl" for="gwReqs">Requests (millions/month)</label>', '<label class="lbl" for="gwReqs">Anfragen (Mio./Monat)</label>'),
    ('<label class="lbl" for="gwTransfer">Data transfer out (GB)</label>', '<label class="lbl" for="gwTransfer">Datenübertragung (GB)</label>'),
    ('<div class="brow"><span>Request cost</span><b id="gwReqCost">—</b></div>', '<div class="brow"><span>Anfragekosten</span><b id="gwReqCost">—</b></div>'),
    ('<div class="brow"><span>Transfer cost</span><b id="gwXferCost">—</b></div>', '<div class="brow"><span>Übertragungskosten</span><b id="gwXferCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="gwAnnual">—</b></div>', '<div class="brow hl"><span>Jahresschätzung</span><b id="gwAnnual">—</b></div>'),
    ('<label class="lbl" for="embModel">Model</label>', '<label class="lbl" for="embModel">Modell</label>'),
    ('<label class="lbl" for="embTokens">Tokens / month (millions)</label>', '<label class="lbl" for="embTokens">Token / Monat (Mio.)</label>'),
    ('<label class="lbl" for="embDocs">Documents</label>', '<label class="lbl" for="embDocs">Dokumente</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="embRate">—</b></div>', '<div class="brow"><span>Preis / 1M Token</span><b id="embRate">—</b></div>'),
]

de_path = os.path.join(BASE, 'de', 'index.html')
c = read(de_path)
c2 = apply_replacements(c, DE_REPLACEMENTS)
if c2 != c:
    write(de_path, c2)
    print('✓ DE: labels + keywords translated')
else:
    print('  SKIP DE (no changes)')

# ─────────────────────────────────────────────────────────────────────────────
# S4a + S4b FR
# ─────────────────────────────────────────────────────────────────────────────
FR_REPLACEMENTS = [
    ('Keyword: <em>AWS Lambda cost calculator</em>', 'Keyword: <em>calculateur cout AWS Lambda</em>'),
    ('Keyword: <em>API gateway pricing calculator</em>', 'Keyword: <em>calculateur cout API gateway</em>'),
    ('Keyword: <em>embedding API cost</em>', 'Keyword: <em>cout API embedding</em>'),
    ('Keyword: <em>AI agent cost calculator</em>', 'Keyword: <em>calculateur cout agent IA</em>'),
    ('<label class="lbl" for="sttModel">Provider</label>', '<label class="lbl" for="sttModel">Fournisseur</label>'),
    ('<label class="lbl" for="sttVol">Audio minutes / month</label>', '<label class="lbl" for="sttVol">Minutes audio / mois</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="sttRate">—</b></div>', '<div class="brow"><span>Tarif / 1M tokens</span><b id="sttRate">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="sttAnnual">—</b></div>', '<div class="brow hl"><span>Estimation annuelle</span><b id="sttAnnual">—</b></div>'),
    ('<label class="lbl" for="slProvider">Platform</label>', '<label class="lbl" for="slProvider">Plateforme</label>'),
    ('<label class="lbl" for="slInvoke">Invocations / month</label>', '<label class="lbl" for="slInvoke">Invocations / mois</label>'),
    ('<label class="lbl" for="slDuration">Avg duration (ms)</label>', '<label class="lbl" for="slDuration">Duree moy. (ms)</label>'),
    ('<label class="lbl" for="slMemory">Memory</label>', '<label class="lbl" for="slMemory">Memoire</label>'),
    ('<div class="brow"><span>Invocation cost</span><b id="slInvCost">—</b></div>', '<div class="brow"><span>Cout invocation</span><b id="slInvCost">—</b></div>'),
    ('<div class="brow"><span>Compute cost (GB-sec)</span><b id="slCompCost">—</b></div>', '<div class="brow"><span>Cout calcul (Go-sec)</span><b id="slCompCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="slAnnual">—</b></div>', '<div class="brow hl"><span>Estimation annuelle</span><b id="slAnnual">—</b></div>'),
    ('<label class="lbl" for="gwProvider">Provider</label>', '<label class="lbl" for="gwProvider">Fournisseur</label>'),
    ('<label class="lbl" for="gwReqs">Requests (millions/month)</label>', '<label class="lbl" for="gwReqs">Requetes (millions/mois)</label>'),
    ('<label class="lbl" for="gwTransfer">Data transfer out (GB)</label>', '<label class="lbl" for="gwTransfer">Transfert donnees (Go)</label>'),
    ('<div class="brow"><span>Request cost</span><b id="gwReqCost">—</b></div>', '<div class="brow"><span>Cout requetes</span><b id="gwReqCost">—</b></div>'),
    ('<div class="brow"><span>Transfer cost</span><b id="gwXferCost">—</b></div>', '<div class="brow"><span>Cout transfert</span><b id="gwXferCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="gwAnnual">—</b></div>', '<div class="brow hl"><span>Estimation annuelle</span><b id="gwAnnual">—</b></div>'),
    ('<label class="lbl" for="embModel">Model</label>', '<label class="lbl" for="embModel">Modele</label>'),
    ('<label class="lbl" for="embTokens">Tokens / month (millions)</label>', '<label class="lbl" for="embTokens">Tokens / mois (millions)</label>'),
    ('<label class="lbl" for="embDocs">Documents</label>', '<label class="lbl" for="embDocs">Documents</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="embRate">—</b></div>', '<div class="brow"><span>Tarif / 1M tokens</span><b id="embRate">—</b></div>'),
]

fr_path = os.path.join(BASE, 'fr', 'index.html')
c = read(fr_path)
c2 = apply_replacements(c, FR_REPLACEMENTS)
if c2 != c:
    write(fr_path, c2)
    print('✓ FR: labels + keywords translated')
else:
    print('  SKIP FR (no changes)')

# ─────────────────────────────────────────────────────────────────────────────
# S4a + S4b TR
# ─────────────────────────────────────────────────────────────────────────────
TR_REPLACEMENTS = [
    ('Keyword: <em>AWS Lambda cost calculator</em>', 'Keyword: <em>AWS Lambda maliyet hesaplayici</em>'),
    ('Keyword: <em>API gateway pricing calculator</em>', 'Keyword: <em>API gateway maliyet hesaplayici</em>'),
    ('Keyword: <em>embedding API cost</em>', 'Keyword: <em>embedding API maliyeti</em>'),
    ('Keyword: <em>AI agent cost calculator</em>', 'Keyword: <em>YZ ajan maliyet hesaplayici</em>'),
    ('<label class="lbl" for="sttModel">Provider</label>', '<label class="lbl" for="sttModel">Saglayici</label>'),
    ('<label class="lbl" for="sttVol">Audio minutes / month</label>', '<label class="lbl" for="sttVol">Ses dakikasi / ay</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="sttRate">—</b></div>', '<div class="brow"><span>Oran / 1M token</span><b id="sttRate">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="sttAnnual">—</b></div>', '<div class="brow hl"><span>Yillik tahmin</span><b id="sttAnnual">—</b></div>'),
    ('<label class="lbl" for="slProvider">Platform</label>', '<label class="lbl" for="slProvider">Platform</label>'),
    ('<label class="lbl" for="slInvoke">Invocations / month</label>', '<label class="lbl" for="slInvoke">Cagri / ay</label>'),
    ('<label class="lbl" for="slDuration">Avg duration (ms)</label>', '<label class="lbl" for="slDuration">Ort. sure (ms)</label>'),
    ('<label class="lbl" for="slMemory">Memory</label>', '<label class="lbl" for="slMemory">Bellek</label>'),
    ('<div class="brow"><span>Invocation cost</span><b id="slInvCost">—</b></div>', '<div class="brow"><span>Cagri maliyeti</span><b id="slInvCost">—</b></div>'),
    ('<div class="brow"><span>Compute cost (GB-sec)</span><b id="slCompCost">—</b></div>', '<div class="brow"><span>Hesaplama maliyeti (GB-sn)</span><b id="slCompCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="slAnnual">—</b></div>', '<div class="brow hl"><span>Yillik tahmin</span><b id="slAnnual">—</b></div>'),
    ('<label class="lbl" for="gwProvider">Provider</label>', '<label class="lbl" for="gwProvider">Saglayici</label>'),
    ('<label class="lbl" for="gwReqs">Requests (millions/month)</label>', '<label class="lbl" for="gwReqs">Istek (milyon/ay)</label>'),
    ('<label class="lbl" for="gwTransfer">Data transfer out (GB)</label>', '<label class="lbl" for="gwTransfer">Veri transferi (GB)</label>'),
    ('<div class="brow"><span>Request cost</span><b id="gwReqCost">—</b></div>', '<div class="brow"><span>Istek maliyeti</span><b id="gwReqCost">—</b></div>'),
    ('<div class="brow"><span>Transfer cost</span><b id="gwXferCost">—</b></div>', '<div class="brow"><span>Transfer maliyeti</span><b id="gwXferCost">—</b></div>'),
    ('<div class="brow hl"><span>Annual estimate</span><b id="gwAnnual">—</b></div>', '<div class="brow hl"><span>Yillik tahmin</span><b id="gwAnnual">—</b></div>'),
    ('<label class="lbl" for="embModel">Model</label>', '<label class="lbl" for="embModel">Model</label>'),
    ('<label class="lbl" for="embTokens">Tokens / month (millions)</label>', '<label class="lbl" for="embTokens">Token / ay (milyon)</label>'),
    ('<label class="lbl" for="embDocs">Documents</label>', '<label class="lbl" for="embDocs">Belgeler</label>'),
    ('<div class="brow"><span>Rate / 1M tokens</span><b id="embRate">—</b></div>', '<div class="brow"><span>Oran / 1M token</span><b id="embRate">—</b></div>'),
]

tr_path = os.path.join(BASE, 'tr', 'index.html')
c = read(tr_path)
c2 = apply_replacements(c, TR_REPLACEMENTS)
if c2 != c:
    write(tr_path, c2)
    print('✓ TR: labels + keywords translated')
else:
    print('  SKIP TR (no changes)')

# ─────────────────────────────────────────────────────────────────────────────
# S4a — Agent panel labels (all 3 lang homepages)
# ─────────────────────────────────────────────────────────────────────────────
AGENT_DE = [
    ('<label class="lbl">Step 1 — Planner / Router</label>', '<label class="lbl">Schritt 1 — Planer / Router</label>'),
    ('<label class="lbl">Step 2 — Main Worker</label>', '<label class="lbl">Schritt 2 — Hauptworker</label>'),
    ('<label class="lbl">Step 3 — Summariser</label>', '<label class="lbl">Schritt 3 — Zusammenfasser</label>'),
    ('<div class="brow"><span>Step 1 — Planner</span><b id="agS1">—</b></div>', '<div class="brow"><span>Schritt 1 — Planer</span><b id="agS1">—</b></div>'),
    ('<div class="brow"><span>Step 2 — Worker</span><b id="agS2">—</b></div>', '<div class="brow"><span>Schritt 2 — Worker</span><b id="agS2">—</b></div>'),
    ('<div class="brow"><span>Step 3 — Summariser</span><b id="agS3">—</b></div>', '<div class="brow"><span>Schritt 3 — Zusammenfasser</span><b id="agS3">—</b></div>'),
]
AGENT_FR = [
    ('<label class="lbl">Step 1 — Planner / Router</label>', '<label class="lbl">Etape 1 — Planificateur / Routeur</label>'),
    ('<label class="lbl">Step 2 — Main Worker</label>', '<label class="lbl">Etape 2 — Travailleur principal</label>'),
    ('<label class="lbl">Step 3 — Summariser</label>', '<label class="lbl">Etape 3 — Resumeur</label>'),
    ('<div class="brow"><span>Step 1 — Planner</span><b id="agS1">—</b></div>', '<div class="brow"><span>Etape 1 — Planificateur</span><b id="agS1">—</b></div>'),
    ('<div class="brow"><span>Step 2 — Worker</span><b id="agS2">—</b></div>', '<div class="brow"><span>Etape 2 — Travailleur</span><b id="agS2">—</b></div>'),
    ('<div class="brow"><span>Step 3 — Summariser</span><b id="agS3">—</b></div>', '<div class="brow"><span>Etape 3 — Resumeur</span><b id="agS3">—</b></div>'),
]
AGENT_TR = [
    ('<label class="lbl">Step 1 — Planner / Router</label>', '<label class="lbl">Adim 1 — Planlayici / Yonlendirici</label>'),
    ('<label class="lbl">Step 2 — Main Worker</label>', '<label class="lbl">Adim 2 — Ana Iscisi</label>'),
    ('<label class="lbl">Step 3 — Summariser</label>', '<label class="lbl">Adim 3 — Ozetleyici</label>'),
    ('<div class="brow"><span>Step 1 — Planner</span><b id="agS1">—</b></div>', '<div class="brow"><span>Adim 1 — Planlayici</span><b id="agS1">—</b></div>'),
    ('<div class="brow"><span>Step 2 — Worker</span><b id="agS2">—</b></div>', '<div class="brow"><span>Adim 2 — Isci</span><b id="agS2">—</b></div>'),
    ('<div class="brow"><span>Step 3 — Summariser</span><b id="agS3">—</b></div>', '<div class="brow"><span>Adim 3 — Ozetleyici</span><b id="agS3">—</b></div>'),
]

for path, pairs, lang in [
    (de_path, AGENT_DE, 'DE'),
    (fr_path, AGENT_FR, 'FR'),
    (tr_path, AGENT_TR, 'TR'),
]:
    c = read(path)
    c2 = apply_replacements(c, pairs)
    if c2 != c:
        write(path, c2)
        print(f'✓ {lang}: agent panel translated')
    else:
        print(f'  SKIP {lang} agent (no changes)')

# ─────────────────────────────────────────────────────────────────────────────
# S5 — Article + FAQPage schema for EN blog posts
# ─────────────────────────────────────────────────────────────────────────────
BLOG_SCHEMAS = {
    'blog/llm-api-cost-guide-2026.html': {
        'title': 'LLM API Cost Guide 2026: GPT-4o, Claude, Gemini Pricing',
        'faq': [
            ('How much does GPT-4o cost per 1 million tokens?',
             'GPT-4o costs $2.50/M input tokens and $10.00/M output tokens (pay-as-you-go, 2026).'),
            ('What is the cheapest LLM API in 2026?',
             'GPT-4o mini ($0.15/$0.60) and Gemini 1.5 Flash ($0.075/$0.30) are cheapest. Claude 3.5 Haiku is best for quality-sensitive workloads on a budget.'),
            ('Is this LLM cost calculator free?',
             'Yes. APICalculators is free with no signup. All calculations run in your browser - no data sent to any server.'),
        ]
    },
    'blog/stripe-vs-paddle-fees-2026.html': {
        'title': 'Stripe vs Paddle vs Lemon Squeezy: Which Is Actually Cheaper for SaaS?',
        'faq': [
            ('Is Stripe cheaper than Paddle for SaaS?',
             'At raw fee level yes (2.9% vs 5%), but adding Stripe Tax, international fees and chargebacks puts break-even at $12-18K MRR. Below that Paddle is often cheaper total.'),
            ('What is a Merchant of Record?',
             'A Merchant of Record handles all tax obligations globally. Paddle and Lemon Squeezy are MoRs - they collect VAT/sales tax. Stripe is not.'),
        ]
    },
    'blog/vector-database-cost-comparison-2026.html': {
        'title': 'Vector Database Cost Comparison 2026: Pinecone vs Qdrant vs Supabase',
        'faq': [
            ('What is the cheapest vector database in 2026?',
             'Under 5M vectors: Supabase pgvector at $25/month. Over 50M vectors: self-hosted Qdrant on spot VMs at $150-300/month.'),
            ('How much does Pinecone cost for 1 million vectors?',
             'Approximately $10-30/month. Storage ~$3, plus $16 per million read units.'),
        ]
    },
    'blog/aws-lambda-cost-calculator-2026.html': {
        'title': 'AWS Lambda Cost Calculator 2026: True Serverless Pricing',
        'faq': [
            ('How much does AWS Lambda cost per million requests?',
             '$0.20 per million invocations after free tier (1M/month). Compute adds $0.0000166725 per GB-second.'),
            ('Is Cloudflare Workers cheaper than Lambda?',
             'For short high-frequency functions yes. Workers at $0.50/M beats Lambda for APIs under 30ms. For longer compute (500ms+) Lambda may be cheaper.'),
        ]
    },
    'blog/cloud-vps-cost-comparison-2026.html': {
        'title': 'Cloud VPS Cost Comparison 2026: Hetzner vs DigitalOcean vs Vultr',
        'faq': [
            ('Is Hetzner cheaper than DigitalOcean?',
             'Yes - 3-5x cheaper for EU. Hetzner CX22 (2 vCPU/4GB) is 4.50 EUR/mo vs DigitalOcean $24/mo.'),
            ('Which VPS is best for a small SaaS?',
             'Hetzner for EU audience. Vultr for global reach (32 locations). DigitalOcean if you need managed Postgres alongside compute.'),
        ]
    },
}

def make_article_schema(title):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": "2026-06-02",
        "dateModified": "2026-06-04",
        "author": {"@type": "Organization", "name": "APICalculators"},
        "publisher": {
            "@type": "Organization",
            "name": "APICalculators",
            "url": "https://apicalculators.com"
        }
    }

def make_faq_schema(faq_items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            }
            for q, a in faq_items
        ]
    }

schema_updated = 0
schema_skipped = 0

for rel_path, data in BLOG_SCHEMAS.items():
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print(f'  MISSING: {rel_path}')
        continue
    c = read(path)

    if '"Article"' in c or "'Article'" in c:
        schema_skipped += 1
        print(f'  SKIP schema (exists): {rel_path}')
        continue

    article_json = json.dumps(make_article_schema(data['title']), ensure_ascii=False, indent=2)
    faq_json = json.dumps(make_faq_schema(data['faq']), ensure_ascii=False, indent=2)

    inject = (
        f'<script type="application/ld+json">\n{article_json}\n</script>\n'
        f'<script type="application/ld+json">\n{faq_json}\n</script>\n'
    )

    if '</head>' in c:
        c = c.replace('</head>', inject + '</head>', 1)
        write(path, c)
        schema_updated += 1
        print(f'✓ Schema added: {rel_path}')
    else:
        print(f'  WARN: no </head> in {rel_path}')

print(f'\nSchema: {schema_updated} added, {schema_skipped} skipped')
print('All done.')
