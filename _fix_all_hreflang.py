#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add/update hreflang on ALL pages that are missing cross-language alternates"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'
B = 'https://apicalculators.com'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

def strip_hreflang(c):
    return re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*/>\n?', '', c)

def inject_after_canonical(c, block):
    canon = re.search(r'(<link rel="canonical"[^>]*/>\n?)', c)
    if canon:
        return c.replace(canon.group(0), canon.group(0) + block + '\n', 1)
    return c.replace('</head>', block + '\n</head>', 1)

def hreflang(langs):
    """langs = list of (lang, url) tuples"""
    lines = [f'<link rel="alternate" hreflang="{l}" href="{u}"/>' for l, u in langs]
    return '\n'.join(lines)

def apply(fpath, langs):
    c = read(fpath)
    c = strip_hreflang(c)
    block = hreflang(langs)
    c = inject_after_canonical(c, block)
    write(fpath, c)

# ─── PAGE → HREFLANG MAP ──────────────────────────────────────────────────────

# format: file_rel_path -> list of (lang, full_url)
# We build this programmatically for large groups

PAGES = {}

def add(rel, langs_dict):
    """langs_dict: {lang: path} — path starts with /"""
    pairs = [(l, B + p) for l, p in langs_dict.items()]
    PAGES[rel.replace('/', os.sep)] = pairs

# ── HOMEPAGES ─────────────────────────────────────────────────────────────────
add('index.html', {'en':'/', 'de':'/de/', 'fr':'/fr/', 'tr':'/tr/', 'x-default':'/'})
add('de/index.html', {'en':'/', 'de':'/de/', 'fr':'/fr/', 'tr':'/tr/', 'x-default':'/'})
add('fr/index.html', {'en':'/', 'de':'/de/', 'fr':'/fr/', 'tr':'/tr/', 'x-default':'/'})
add('tr/index.html', {'en':'/', 'de':'/de/', 'fr':'/fr/', 'tr':'/tr/', 'x-default':'/'})

# ── ABOUT ─────────────────────────────────────────────────────────────────────
add('about.html', {'en':'/about.html', 'de':'/de/about.html', 'fr':'/fr/about.html', 'tr':'/tr/about.html', 'x-default':'/about.html'})
add('de/about.html', {'en':'/about.html', 'de':'/de/about.html', 'fr':'/fr/about.html', 'tr':'/tr/about.html', 'x-default':'/about.html'})
add('fr/about.html', {'en':'/about.html', 'de':'/de/about.html', 'fr':'/fr/about.html', 'tr':'/tr/about.html', 'x-default':'/about.html'})
add('tr/about.html', {'en':'/about.html', 'de':'/de/about.html', 'fr':'/fr/about.html', 'tr':'/tr/about.html', 'x-default':'/about.html'})

# ── PRIVACY ───────────────────────────────────────────────────────────────────
add('privacy.html', {'en':'/privacy.html', 'de':'/de/privacy.html', 'fr':'/fr/privacy.html', 'tr':'/tr/privacy.html', 'x-default':'/privacy.html'})
add('de/privacy.html', {'en':'/privacy.html', 'de':'/de/privacy.html', 'fr':'/fr/privacy.html', 'tr':'/tr/privacy.html', 'x-default':'/privacy.html'})
add('fr/privacy.html', {'en':'/privacy.html', 'de':'/de/privacy.html', 'fr':'/fr/privacy.html', 'tr':'/tr/privacy.html', 'x-default':'/privacy.html'})
add('tr/privacy.html', {'en':'/privacy.html', 'de':'/de/privacy.html', 'fr':'/fr/privacy.html', 'tr':'/tr/privacy.html', 'x-default':'/privacy.html'})

# ── TERMS ─────────────────────────────────────────────────────────────────────
add('terms.html', {'en':'/terms.html', 'de':'/de/terms.html', 'fr':'/fr/terms.html', 'tr':'/tr/terms.html', 'x-default':'/terms.html'})
add('de/terms.html', {'en':'/terms.html', 'de':'/de/terms.html', 'fr':'/fr/terms.html', 'tr':'/tr/terms.html', 'x-default':'/terms.html'})
add('fr/terms.html', {'en':'/terms.html', 'de':'/de/terms.html', 'fr':'/fr/terms.html', 'tr':'/tr/terms.html', 'x-default':'/terms.html'})
add('tr/terms.html', {'en':'/terms.html', 'de':'/de/terms.html', 'fr':'/fr/terms.html', 'tr':'/tr/terms.html', 'x-default':'/terms.html'})

# ── CALC PAGES ────────────────────────────────────────────────────────────────
CALC_GROUPS = [
    {'en':'/llm-cost-calculator.html', 'de':'/de/llm-kostenrechner.html', 'fr':'/fr/calculateur-cout-llm.html', 'tr':'/tr/llm-maliyet-hesaplayici.html'},
    {'en':'/aws-lambda-calculator.html', 'de':'/de/aws-lambda-rechner.html', 'fr':'/fr/calculateur-cout-aws-lambda.html', 'tr':'/tr/aws-lambda-maliyet.html'},
    {'en':'/cloud-vps-comparison.html', 'de':'/de/cloud-vps-kostenvergleich.html', 'fr':'/fr/comparateur-vps-cloud.html', 'tr':'/tr/bulut-vps-maliyet.html'},
    {'en':'/vector-db-cost.html', 'de':'/de/vektordatenbank-kosten.html', 'fr':'/fr/cout-base-vectorielle.html', 'tr':'/tr/vektor-veritabani-maliyet.html'},
    {'en':'/embedding-api-cost.html', 'de':'/de/embedding-api-kosten.html', 'fr':'/fr/cout-api-embedding.html', 'tr':'/tr/embedding-api-maliyet.html'},
    {'en':'/api-gateway-cost.html', 'de':'/de/api-gateway-kosten.html', 'fr':'/fr/cout-api-gateway.html', 'tr':'/tr/api-gateway-maliyet.html'},
    {'en':'/stt-tts-api-cost.html', 'de':'/de/stt-tts-api-kosten.html', 'fr':'/fr/cout-api-stt-tts.html', 'tr':'/tr/stt-tts-api-maliyet.html'},
    {'en':'/ai-agent-cost-calculator.html', 'de':'/de/ki-agent-kostenrechner.html', 'fr':'/fr/cout-agent-ia.html', 'tr':'/tr/yz-ajan-maliyet.html'},
    {'en':'/ai-image-cost-calculator.html', 'de':'/de/ki-bildgenerierung-kosten.html', 'fr':'/fr/cout-generation-image-ia.html', 'tr':'/tr/yz-gorsel-uretim-maliyet.html'},
    {'en':'/stripe-vs-paddle-calculator.html', 'de':'/de/stripe-vs-paddle-rechner.html', 'fr':'/fr/comparateur-stripe-paddle.html', 'tr':'/tr/stripe-vs-paddle-hesaplayici.html'},
    {'en':'/ai-coding-tool-cost.html', 'de':'/de/ki-coding-tool-kosten.html', 'fr':'/fr/cout-outil-ia-coding.html', 'tr':'/tr/yapay-zeka-kodlama-arac-maliyeti.html'},
    {'en':'/auth-provider-cost.html', 'de':'/de/auth-anbieter-kosten.html', 'fr':'/fr/cout-fournisseur-auth.html', 'tr':'/tr/kimlik-dogrulama-maliyet.html'},
]

EN_ONLY_CALCS = [
    '/chatgpt-api-pricing-calculator.html',
    '/claude-api-cost-calculator.html',
    '/gemini-api-cost-calculator.html',
    '/openai-api-cost-calculator.html',
]

for grp in CALC_GROUPS:
    langs = dict(grp)
    langs['x-default'] = grp['en']
    for lang, path in grp.items():
        rel = path.lstrip('/')
        add(rel, langs)

for path in EN_ONLY_CALCS:
    rel = path.lstrip('/')
    add(rel, {'en': path, 'x-default': path})

# ── BLOG INDEX PAGES ──────────────────────────────────────────────────────────
add('blog/index.html', {'en':'/blog/', 'de':'/de/blog/', 'fr':'/fr/blog/', 'tr':'/tr/blog/', 'x-default':'/blog/'})
add('de/blog/index.html', {'en':'/blog/', 'de':'/de/blog/', 'fr':'/fr/blog/', 'tr':'/tr/blog/', 'x-default':'/blog/'})
add('fr/blog/index.html', {'en':'/blog/', 'de':'/de/blog/', 'fr':'/fr/blog/', 'tr':'/tr/blog/', 'x-default':'/blog/'})
add('tr/blog/index.html', {'en':'/blog/', 'de':'/de/blog/', 'fr':'/fr/blog/', 'tr':'/tr/blog/', 'x-default':'/blog/'})

# ── BLOG POSTS (cross-lang groups) ────────────────────────────────────────────
BLOG_GROUPS = [
    {'en':'/blog/llm-api-cost-guide-2026.html', 'de':'/de/blog/llm-kosten-leitfaden-2026.html', 'fr':'/fr/blog/guide-couts-llm-2026.html', 'tr':'/tr/blog/llm-maliyet-rehberi-2026.html'},
    {'en':'/blog/aws-lambda-cost-calculator-2026.html', 'de':'/de/blog/aws-lambda-kosten-guide-2026.html', 'fr':'/fr/blog/guide-cout-aws-lambda-2026.html', 'tr':'/tr/blog/aws-lambda-maliyet-rehberi-2026.html'},
    {'en':'/blog/cloud-vps-cost-comparison-2026.html', 'de':'/de/blog/cloud-vps-kostenvergleich-2026.html', 'fr':'/fr/blog/comparaison-cloud-vps-2026.html', 'tr':'/tr/blog/bulut-vps-karsilastirma-2026.html'},
    {'en':'/blog/vector-database-cost-comparison-2026.html', 'de':'/de/blog/vektordatenbank-kosten-vergleich-2026.html', 'fr':'/fr/blog/comparaison-couts-base-vectorielle-2026.html', 'tr':'/tr/blog/vektor-veritabani-maliyet-karsilastirmasi-2026.html'},
    {'en':'/blog/embedding-api-cost-2026.html', 'de':'/de/blog/embedding-api-kosten-2026.html', 'fr':'/fr/blog/cout-api-embedding-2026.html', 'tr':'/tr/blog/embedding-api-maliyet-2026.html'},
    {'en':'/blog/api-gateway-pricing-2026.html', 'de':'/de/blog/api-gateway-preise-2026.html', 'fr':'/fr/blog/prix-api-gateway-2026.html', 'tr':'/tr/blog/api-gateway-fiyat-2026.html'},
    {'en':'/blog/stt-tts-api-cost-2026.html', 'de':'/de/blog/stt-tts-api-kosten-2026.html', 'fr':'/fr/blog/cout-api-stt-tts-2026.html', 'tr':'/tr/blog/stt-tts-api-maliyet-2026.html'},
    {'en':'/blog/ai-agent-cost-calculator-2026.html', 'de':'/de/blog/ki-agent-kosten-2026.html', 'fr':'/fr/blog/cout-agent-ia-2026.html', 'tr':'/tr/blog/yapay-zeka-ajan-maliyet-2026.html'},
    {'en':'/blog/dalle3-vs-stable-diffusion-cost-2026.html', 'de':'/de/blog/dalle-vs-stable-diffusion-kosten-2026.html', 'fr':'/fr/blog/dalle-vs-stable-diffusion-cout-2026.html', 'tr':'/tr/blog/dalle-vs-stable-diffusion-maliyet-2026.html'},
    {'en':'/blog/stripe-vs-paddle-fees-2026.html', 'de':'/de/blog/stripe-vs-paddle-gebuehren-2026.html', 'fr':'/fr/blog/stripe-vs-paddle-frais-2026.html', 'tr':'/tr/blog/stripe-vs-paddle-ucretleri-2026.html'},
    {'en':'/blog/reduce-llm-api-costs-2026.html', 'de':'/de/blog/llm-kosten-senken-2026.html', 'fr':'/fr/blog/reduire-couts-llm-2026.html', 'tr':'/tr/blog/llm-maliyet-dusurme-2026.html'},
    {'en':'/blog/lemon-squeezy-vs-stripe-2026.html', 'de':'/de/blog/lemon-squeezy-vs-stripe-2026.html', 'fr':'/fr/blog/lemon-squeezy-vs-stripe-frais-2026.html', 'tr':'/tr/blog/stripe-vs-paddle-ucretleri-2026.html'},
    {'en':'/blog/cursor-true-cost-2026.html', 'de':'/de/blog/cursor-wahre-kosten-2026.html', 'fr':'/fr/blog/vrai-cout-cursor-2026.html', 'tr':'/tr/blog/cursor-gercek-maliyet-2026.html'},
    {'en':'/blog/clerk-vs-supabase-auth-cost-2026.html', 'de':'/de/blog/clerk-supabase-auth-kosten-2026.html', 'fr':'/fr/blog/clerk-vs-supabase-auth-cout-2026.html', 'tr':'/tr/blog/clerk-supabase-auth-maliyet-2026.html'},
]

# EN-only blog posts (no translations)
EN_ONLY_BLOGS = [
    '/blog/midjourney-vs-dalle-cost-2026.html',
    '/blog/pinecone-pricing-guide-2026.html',
]

for grp in BLOG_GROUPS:
    langs = dict(grp)
    langs['x-default'] = grp['en']
    for lang, path in grp.items():
        rel = path.lstrip('/')
        fpath = os.path.join(BASE, rel.replace('/', os.sep))
        if os.path.exists(fpath):
            add(rel, langs)

for path in EN_ONLY_BLOGS:
    rel = path.lstrip('/')
    add(rel, {'en': path, 'x-default': path})

# DE-only blog posts (no EN/FR/TR equivalents)
DE_ONLY_BLOGS = [
    '/de/blog/hetzner-digitalocean-vergleich-2026.html',
    '/de/blog/llm-api-kosten-2026.html',
]
FR_ONLY_BLOGS = [
    '/fr/blog/comparatif-vps-cloud-france-2026.html',
    '/fr/blog/cout-api-llm-2026.html',
    '/fr/blog/midjourney-vs-dalle-cout-2026.html',
    '/fr/blog/pinecone-guide-tarifs-2026.html',
]
TR_ONLY_BLOGS = [
    '/tr/blog/gpt-api-turkce-maliyet-2026.html',
    '/tr/blog/stripe-turkiye-komisyon-2026.html',
    '/tr/blog/midjourney-vs-dalle-maliyet-2026.html',
    '/tr/blog/pinecone-fiyat-rehberi-2026.html',
]

for path in DE_ONLY_BLOGS:
    rel = path.lstrip('/')
    add(rel, {'de': path, 'x-default': path})

for path in FR_ONLY_BLOGS:
    rel = path.lstrip('/')
    add(rel, {'fr': path, 'x-default': path})

for path in TR_ONLY_BLOGS:
    rel = path.lstrip('/')
    add(rel, {'tr': path, 'x-default': path})

# ── FR blog posts missing from groups ─────────────────────────────────────────
FR_EXTRA = ['/fr/blog/lemon-squeezy-vs-stripe-frais-2026.html']
for path in FR_EXTRA:
    rel = path.lstrip('/')
    if rel not in PAGES:
        add(rel, {'fr': path, 'x-default': path})

# ─── APPLY ────────────────────────────────────────────────────────────────────
changed = 0
skipped = 0
missing = []

for rel_key, langs in PAGES.items():
    fpath = os.path.join(BASE, rel_key)
    if not os.path.exists(fpath):
        missing.append(rel_key)
        continue
    apply(fpath, langs)
    changed += 1

print(f'✓ Updated hreflang: {changed} files')
if missing:
    print(f'  Files not found ({len(missing)}):')
    for m in missing: print(f'    {m}')
