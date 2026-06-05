#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all 5 priorities: hreflang, footer, title, adsense, sitemap"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# ─── HREFLANG MAP ─────────────────────────────────────────────────────────────
# Maps each page to its cross-language equivalents
# Key: relative path from BASE (forward slashes, no leading ./)
# Value: dict of lang -> full URL

BASE_URL = 'https://apicalculators.com'

# about/privacy/terms/404 — self-referential only (no translations)
SELF_ONLY = {'about.html', 'privacy.html', 'terms.html', '404.html'}

# Blog pages that have cross-lang equivalents
BLOG_MAP = {
    'blog/llm-api-cost-guide-2026.html': {
        'en': '/blog/llm-api-cost-guide-2026.html',
        'de': '/de/blog/llm-kosten-leitfaden-2026.html',
        'fr': '/fr/blog/guide-couts-llm-2026.html',
        'tr': '/tr/blog/llm-maliyet-rehberi-2026.html',
    },
    'blog/aws-lambda-cost-calculator-2026.html': {
        'en': '/blog/aws-lambda-cost-calculator-2026.html',
        'de': '/de/blog/aws-lambda-kosten-guide-2026.html',
        'fr': '/fr/blog/guide-cout-aws-lambda-2026.html',
        'tr': '/tr/blog/aws-lambda-maliyet-rehberi-2026.html',
    },
    'blog/cloud-vps-cost-comparison-2026.html': {
        'en': '/blog/cloud-vps-cost-comparison-2026.html',
        'de': '/de/blog/cloud-vps-kostenvergleich-2026.html',
        'fr': '/fr/blog/comparaison-cloud-vps-2026.html',
        'tr': '/tr/blog/bulut-vps-karsilastirma-2026.html',
    },
    'blog/vector-database-cost-comparison-2026.html': {
        'en': '/blog/vector-database-cost-comparison-2026.html',
        'de': '/de/blog/vektordatenbank-kosten-vergleich-2026.html',
        'fr': '/fr/blog/comparaison-couts-base-vectorielle-2026.html',
        'tr': '/tr/blog/vektor-veritabani-maliyet-karsilastirmasi-2026.html',
    },
    'blog/embedding-api-cost-2026.html': {
        'en': '/blog/embedding-api-cost-2026.html',
        'de': '/de/blog/embedding-api-kosten-2026.html',
        'fr': '/fr/blog/cout-api-embedding-2026.html',
        'tr': '/tr/blog/embedding-api-maliyet-2026.html',
    },
    'blog/api-gateway-pricing-2026.html': {
        'en': '/blog/api-gateway-pricing-2026.html',
        'de': '/de/blog/api-gateway-preise-2026.html',
        'fr': '/fr/blog/prix-api-gateway-2026.html',
        'tr': '/tr/blog/api-gateway-fiyat-2026.html',
    },
    'blog/stt-tts-api-cost-2026.html': {
        'en': '/blog/stt-tts-api-cost-2026.html',
        'de': '/de/blog/stt-tts-api-kosten-2026.html',
        'fr': '/fr/blog/cout-api-stt-tts-2026.html',
        'tr': '/tr/blog/stt-tts-api-maliyet-2026.html',
    },
    'blog/ai-agent-cost-calculator-2026.html': {
        'en': '/blog/ai-agent-cost-calculator-2026.html',
        'de': '/de/blog/ki-agent-kosten-2026.html',
        'fr': '/fr/blog/cout-agent-ia-2026.html',
        'tr': '/tr/blog/yapay-zeka-ajan-maliyet-2026.html',
    },
    'blog/dalle3-vs-stable-diffusion-cost-2026.html': {
        'en': '/blog/dalle3-vs-stable-diffusion-cost-2026.html',
        'de': '/de/blog/dalle-vs-stable-diffusion-kosten-2026.html',
        'fr': '/fr/blog/dalle-vs-stable-diffusion-cout-2026.html',
        'tr': '/tr/blog/dalle-vs-stable-diffusion-maliyet-2026.html',
    },
    'blog/stripe-vs-paddle-fees-2026.html': {
        'en': '/blog/stripe-vs-paddle-fees-2026.html',
        'de': '/de/blog/stripe-vs-paddle-gebuehren-2026.html',
        'fr': '/fr/blog/stripe-vs-paddle-frais-2026.html',
        'tr': '/tr/blog/stripe-vs-paddle-ucretleri-2026.html',
    },
    'blog/reduce-llm-api-costs-2026.html': {
        'en': '/blog/reduce-llm-api-costs-2026.html',
        'de': '/de/blog/llm-kosten-senken-2026.html',
        'fr': '/fr/blog/reduire-couts-llm-2026.html',
        'tr': '/tr/blog/llm-maliyet-dusurme-2026.html',
    },
    'blog/lemon-squeezy-vs-stripe-2026.html': {
        'en': '/blog/lemon-squeezy-vs-stripe-2026.html',
        'de': '/de/blog/lemon-squeezy-vs-stripe-2026.html',
        'fr': '/fr/blog/lemon-squeezy-vs-stripe-frais-2026.html',
        'tr': '/tr/blog/stripe-vs-paddle-ucretleri-2026.html',
    },
    'blog/cursor-true-cost-2026.html': {
        'en': '/blog/cursor-true-cost-2026.html',
        'de': '/de/blog/cursor-wahre-kosten-2026.html',
        'fr': '/fr/blog/vrai-cout-cursor-2026.html',
        'tr': '/tr/blog/cursor-gercek-maliyet-2026.html',
    },
    'blog/clerk-vs-supabase-auth-cost-2026.html': {
        'en': '/blog/clerk-vs-supabase-auth-cost-2026.html',
        'de': '/de/blog/clerk-supabase-auth-kosten-2026.html',
        'fr': '/fr/blog/clerk-vs-supabase-auth-cout-2026.html',
        'tr': '/tr/blog/clerk-supabase-auth-maliyet-2026.html',
    },
}

# Calc pages cross-lang map
CALC_MAP = {
    'llm-cost-calculator.html': {
        'en': '/llm-cost-calculator.html',
        'de': '/de/llm-kostenrechner.html',
        'fr': '/fr/calculateur-cout-llm.html',
        'tr': '/tr/llm-maliyet-hesaplayici.html',
    },
    'aws-lambda-calculator.html': {
        'en': '/aws-lambda-calculator.html',
        'de': '/de/aws-lambda-rechner.html',
        'fr': '/fr/calculateur-cout-aws-lambda.html',
        'tr': '/tr/aws-lambda-maliyet.html',
    },
    'cloud-vps-comparison.html': {
        'en': '/cloud-vps-comparison.html',
        'de': '/de/cloud-vps-kostenvergleich.html',
        'fr': '/fr/comparateur-vps-cloud.html',
        'tr': '/tr/bulut-vps-maliyet.html',
    },
    'vector-db-cost.html': {
        'en': '/vector-db-cost.html',
        'de': '/de/vektordatenbank-kosten.html',
        'fr': '/fr/cout-base-vectorielle.html',
        'tr': '/tr/vektor-veritabani-maliyet.html',
    },
    'embedding-api-cost.html': {
        'en': '/embedding-api-cost.html',
        'de': '/de/embedding-api-kosten.html',
        'fr': '/fr/cout-api-embedding.html',
        'tr': '/tr/embedding-api-maliyet.html',
    },
    'api-gateway-cost.html': {
        'en': '/api-gateway-cost.html',
        'de': '/de/api-gateway-kosten.html',
        'fr': '/fr/cout-api-gateway.html',
        'tr': '/tr/api-gateway-maliyet.html',
    },
    'stt-tts-api-cost.html': {
        'en': '/stt-tts-api-cost.html',
        'de': '/de/stt-tts-api-kosten.html',
        'fr': '/fr/cout-api-stt-tts.html',
        'tr': '/tr/stt-tts-api-maliyet.html',
    },
    'ai-agent-cost-calculator.html': {
        'en': '/ai-agent-cost-calculator.html',
        'de': '/de/ki-agent-kostenrechner.html',
        'fr': '/fr/cout-agent-ia.html',
        'tr': '/tr/yz-ajan-maliyet.html',
    },
    'ai-image-cost-calculator.html': {
        'en': '/ai-image-cost-calculator.html',
        'de': '/de/ki-bildgenerierung-kosten.html',
        'fr': '/fr/cout-generation-image-ia.html',
        'tr': '/tr/yz-gorsel-uretim-maliyet.html',
    },
    'stripe-vs-paddle-calculator.html': {
        'en': '/stripe-vs-paddle-calculator.html',
        'de': '/de/stripe-vs-paddle-rechner.html',
        'fr': '/fr/comparateur-stripe-paddle.html',
        'tr': '/tr/stripe-vs-paddle-hesaplayici.html',
    },
    'ai-coding-tool-cost.html': {
        'en': '/ai-coding-tool-cost.html',
        'de': '/de/ki-coding-tool-kosten.html',
        'fr': '/fr/cout-outil-ia-coding.html',
        'tr': '/tr/yapay-zeka-kodlama-arac-maliyeti.html',
    },
    'auth-provider-cost.html': {
        'en': '/auth-provider-cost.html',
        'de': '/de/auth-anbieter-kosten.html',
        'fr': '/fr/cout-fournisseur-auth.html',
        'tr': '/tr/kimlik-dogrulama-maliyet.html',
    },
}

def make_hreflang_block(langs_dict, default_lang='en'):
    """Generate hreflang link tags"""
    lines = []
    for lang, path in langs_dict.items():
        url = BASE_URL + path
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{url}"/>')
    # x-default = en version
    en_path = langs_dict.get('en', list(langs_dict.values())[0])
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}{en_path}"/>')
    return '\n'.join(lines)

def inject_hreflang(content, hreflang_block):
    """Replace existing hreflang or inject before </head>"""
    # Remove existing hreflang links
    content = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*"[^>]*/>\n?', '', content)
    # Inject before first </head> or <link rel="canonical"
    canonical = re.search(r'(<link rel="canonical"[^>]*/>\n?)', content)
    if canonical:
        content = content.replace(canonical.group(0), hreflang_block + '\n' + canonical.group(0))
    else:
        content = content.replace('</head>', hreflang_block + '\n</head>', 1)
    return content

# ─── PRIORITY 1: HREFLANG ─────────────────────────────────────────────────────
print('=== PRIORITY 1: HREFLANG ===')
changed_hreflang = 0

# Pages we know need fixing: about, privacy, terms, blog pages without hreflang, midjourney/pinecone
# midjourney and pinecone are EN-only (no translations), so add self-only hreflang

# About/privacy/terms: EN pages, no translations
simple_en_only = {
    'about.html': '/about.html',
    'privacy.html': '/privacy.html',
    'terms.html': '/terms.html',
}
for fname, path in simple_en_only.items():
    fpath = os.path.join(BASE, fname)
    c = read(fpath)
    if 'hreflang' in c:
        print(f'  SKIP (has hreflang): {fname}')
        continue
    block = f'<link rel="alternate" hreflang="en" href="{BASE_URL}{path}"/>\n<link rel="alternate" hreflang="x-default" href="{BASE_URL}{path}"/>'
    c = inject_hreflang(c, block)
    write(fpath, c)
    changed_hreflang += 1
    print(f'  FIXED: {fname}')

# midjourney and pinecone: EN-only
en_only_blogs = ['blog/midjourney-vs-dalle-cost-2026.html', 'blog/pinecone-pricing-guide-2026.html']
for rel in en_only_blogs:
    fpath = os.path.join(BASE, rel.replace('/', os.sep))
    c = read(fpath)
    if 'hreflang' in c:
        print(f'  SKIP: {rel}')
        continue
    path = '/' + rel
    block = f'<link rel="alternate" hreflang="en" href="{BASE_URL}{path}"/>\n<link rel="alternate" hreflang="x-default" href="{BASE_URL}{path}"/>'
    c = inject_hreflang(c, block)
    write(fpath, c)
    changed_hreflang += 1
    print(f'  FIXED: {rel}')

# 404 - no hreflang needed
print(f'  SKIP: 404.html (no hreflang needed)')

# Now update cross-lang hreflang on calc pages that may be missing or incomplete
# Check DE/FR/TR blog pages and add hreflang where missing
for en_rel, langs in BLOG_MAP.items():
    for lang, lpath in langs.items():
        if lang == 'en':
            continue
        # Build file path
        rel_path = lpath.lstrip('/')
        fpath = os.path.join(BASE, rel_path.replace('/', os.sep))
        if not os.path.exists(fpath):
            continue
        c = read(fpath)
        if 'hreflang' in c:
            continue
        block_langs = dict(langs)
        block = make_hreflang_block(block_langs)
        c = inject_hreflang(c, block)
        write(fpath, c)
        changed_hreflang += 1
        print(f'  FIXED: {rel_path}')

print(f'Priority 1 done: {changed_hreflang} files updated\n')

# ─── PRIORITY 2: FOOTER FIX ────────────────────────────────────────────────────
print('=== PRIORITY 2: FOOTER ===')

FOOTER_CONFIGS = {
    'index.html': {
        'calcs_heading': 'Calculators',
        'links': [
            ('<a href="#llm">LLM Token Cost</a>'),
            ('<a href="#vector">Vector DB Cost</a>'),
            ('<a href="#image">AI Image Generation</a>'),
            ('<a href="#pay">Payment Fees</a>'),
            ('<a href="#vps">Cloud VPS Comparison</a>'),
            ('<a href="#stt">STT / TTS API Cost</a>'),
            ('<a href="#serverless">Serverless Cost</a>'),
            ('<a href="#gateway">API Gateway Cost</a>'),
            ('<a href="#embeddings">Embedding API Cost</a>'),
            ('<a href="#agent">AI Agent Cost</a>'),
            ('<a href="/ai-coding-tool-cost.html">AI Coding Tool Cost</a>'),
            ('<a href="/auth-provider-cost.html">Auth Provider Cost</a>'),
        ]
    },
    'de/index.html': {
        'calcs_heading': 'Rechner',
        'links': [
            '<a href="#llm">LLM Token Kosten</a>',
            '<a href="#vector">Vektordatenbank</a>',
            '<a href="#image">KI Bildgenerierung</a>',
            '<a href="#pay">Zahlungsgebühren</a>',
            '<a href="#vps">Cloud VPS</a>',
            '<a href="#stt">STT/TTS</a>',
            '<a href="#serverless">Serverless</a>',
            '<a href="#gateway">API Gateway</a>',
            '<a href="#embeddings">Embeddings</a>',
            '<a href="#agent">KI Agent</a>',
            '<a href="/de/ki-coding-tool-kosten.html">KI Coding Tool</a>',
            '<a href="/de/auth-anbieter-kosten.html">Auth Kosten</a>',
        ]
    },
    'fr/index.html': {
        'calcs_heading': 'Calculateurs',
        'links': [
            '<a href="#llm">Coût Tokens LLM</a>',
            '<a href="#vector">Base Vectorielle</a>',
            '<a href="#image">Génération Images</a>',
            '<a href="#pay">Frais Paiement</a>',
            '<a href="#vps">VPS Cloud</a>',
            '<a href="#stt">STT/TTS</a>',
            '<a href="#serverless">Serverless</a>',
            '<a href="#gateway">API Gateway</a>',
            '<a href="#embeddings">Embeddings</a>',
            '<a href="#agent">Agent IA</a>',
            '<a href="/fr/cout-outil-ia-coding.html">Outil IA Coding</a>',
            '<a href="/fr/cout-fournisseur-auth.html">Coût Auth</a>',
        ]
    },
    'tr/index.html': {
        'calcs_heading': 'Hesaplayıcılar',
        'links': [
            '<a href="#llm">LLM Token Maliyeti</a>',
            '<a href="#vector">Vektör Veritabanı</a>',
            '<a href="#image">AI Görüntü Oluşturma</a>',
            '<a href="#pay">Ödeme Ücretleri</a>',
            '<a href="#vps">Bulut VPS</a>',
            '<a href="#stt">STT/TTS</a>',
            '<a href="#serverless">Sunucusuz</a>',
            '<a href="#gateway">API Gateway</a>',
            '<a href="#embeddings">Embeddingler</a>',
            '<a href="#agent">AI Ajan</a>',
            '<a href="/tr/yapay-zeka-kodlama-arac-maliyeti.html">AI Kodlama Aracı</a>',
            '<a href="/tr/kimlik-dogrulama-maliyet.html">Kimlik Doğrulama</a>',
        ]
    },
}

changed_footer = 0
for fname, cfg in FOOTER_CONFIGS.items():
    fpath = os.path.join(BASE, fname.replace('/', os.sep))
    c = read(fpath)
    heading = cfg['calcs_heading']
    links_html = '\n        '.join(cfg['links'])
    new_calcs_div = f'''      <div>
        <h4>{heading}</h4>
        {links_html}
      </div>'''
    # Find the calcs section in footer and replace
    # Pattern: <div>\n        <h4>Calculators|Rechner|Calculateurs|Hesaplayıcılar</h4>...links...</div>
    pattern = r'<div>\s*<h4>' + re.escape(heading) + r'</h4>.*?</div>'
    new_c = re.sub(pattern, new_calcs_div, c, flags=re.DOTALL)
    if new_c != c:
        write(fpath, new_c)
        changed_footer += 1
        print(f'  FIXED footer: {fname}')
    else:
        print(f'  NO MATCH for footer pattern: {fname}')

print(f'Priority 2 done: {changed_footer} files updated\n')

# ─── PRIORITY 3: TITLE TAG ─────────────────────────────────────────────────────
print('=== PRIORITY 3: TITLE TAG ===')
fpath = os.path.join(BASE, 'index.html')
c = read(fpath)
old_title = 'LLM &amp; API Cost Calculators: Free Tools 2026 | APICalculators'
old_title2 = 'LLM & API Cost Calculators: Free Tools 2026 | APICalculators'
new_title = 'Free LLM &amp; API Cost Calculators 2026 | APICalculators'
if old_title2 in c:
    c = c.replace(old_title2, 'Free LLM & API Cost Calculators 2026 | APICalculators')
    write(fpath, c)
    print('  FIXED: index.html title tag')
elif old_title in c:
    c = c.replace(old_title, new_title)
    write(fpath, c)
    print('  FIXED: index.html title tag (amp encoded)')
else:
    print(f'  WARN: title not found, current title:')
    m = re.search(r'<title>(.*?)</title>', c)
    print(f'  "{m.group(1) if m else "NOT FOUND"}"')
print('Priority 3 done\n')

# ─── PRIORITY 4: ADSENSE ──────────────────────────────────────────────────────
print('=== PRIORITY 4: ADSENSE ===')

ADSENSE_TOP = '''<!-- AdSense: replace ca-pub-XX and slot-XX with real IDs after approval -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

ADSENSE_MID = '''<!-- AdSense: replace ca-pub-XX and slot-XX with real IDs after approval -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'''

changed_ads = 0
for fname in ['index.html', 'de/index.html', 'fr/index.html', 'tr/index.html']:
    fpath = os.path.join(BASE, fname.replace('/', os.sep))
    c = read(fpath)
    orig = c
    # Replace TOP LEADERBOARD placeholder
    c = re.sub(
        r'<div class="wrap"><div class="adslot">AD · TOP LEADERBOARD · [^<]+</div></div>',
        f'<div class="wrap">{ADSENSE_TOP}</div>',
        c
    )
    # Replace IN-CONTENT placeholder
    c = re.sub(
        r'<div class="adslot">AD · IN-CONTENT · [^<]+</div>',
        ADSENSE_MID,
        c
    )
    if c != orig:
        write(fpath, c)
        changed_ads += 1
        print(f'  FIXED ads: {fname}')
    else:
        print(f'  NO CHANGE: {fname}')

print(f'Priority 4 done: {changed_ads} files updated\n')

# ─── PRIORITY 5: SITEMAP ──────────────────────────────────────────────────────
print('=== PRIORITY 5: SITEMAP ===')
sitemap_path = os.path.join(BASE, 'sitemap.xml')
c = read(sitemap_path)

# Add xhtml namespace if missing
if 'xmlns:xhtml' not in c:
    c = c.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml"'
    )
    print('  Added xmlns:xhtml namespace')

TODAY = '2026-06-06'
existing_locs = set(re.findall(r'<loc>(.*?)</loc>', c))

# Pages already in sitemap from _update_sitemap.py — just verify
CHECK_PAGES = [
    'https://apicalculators.com/ai-coding-tool-cost.html',
    'https://apicalculators.com/auth-provider-cost.html',
    'https://apicalculators.com/de/ki-coding-tool-kosten.html',
    'https://apicalculators.com/de/auth-anbieter-kosten.html',
    'https://apicalculators.com/fr/cout-outil-ia-coding.html',
    'https://apicalculators.com/fr/cout-fournisseur-auth.html',
    'https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html',
    'https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html',
]
missing = [u for u in CHECK_PAGES if u not in existing_locs]
if missing:
    print(f'  Adding {len(missing)} missing calc pages to sitemap')
    inject = ''
    for loc in missing:
        inject += f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n'''
    c = c.replace('</urlset>', inject + '</urlset>')
else:
    print('  All calc pages already in sitemap')

write(sitemap_path, c)
total = len(re.findall(r'<loc>', c))
print(f'  Total URLs: {total}')
print('Priority 5 done\n')

print('=== ALL DONE ===')
