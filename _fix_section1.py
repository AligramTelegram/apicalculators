#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 1 bug fixes: hreflang, og:locale, geo meta, Vultr affiliate link."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── All HTML files ─────────────────────────────────────────────────────────────
def all_html():
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(root, f)

def rel(path):
    return path.replace(BASE, '').replace('\\', '/')

# ── 1a. Hreflang block ─────────────────────────────────────────────────────────
# For main pages (index, about, blog/index)
MAIN_HREFLANG = """<link rel="alternate" hreflang="en" href="https://apicalculators.com/" />
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/" />
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/" />
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/" />
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/" />"""

# Blog post hreflang mapping (EN slug -> DE/FR/TR slug)
BLOG_MAP = {
    'llm-api-cost-guide-2026': ('llm-kosten-leitfaden-2026', 'guide-couts-llm-2026', 'llm-maliyet-rehberi-2026'),
    'vector-database-cost-comparison-2026': ('vektordatenbank-kosten-vergleich-2026', 'comparaison-couts-base-vectorielle-2026', 'vektor-veritabani-maliyet-karsilastirmasi-2026'),
    'stripe-vs-paddle-fees-2026': ('stripe-vs-paddle-gebuehren-2026', 'stripe-vs-paddle-frais-2026', 'stripe-vs-paddle-ucretleri-2026'),
    'aws-lambda-cost-calculator-2026': ('aws-lambda-kosten-guide-2026', 'guide-cout-aws-lambda-2026', 'aws-lambda-maliyet-rehberi-2026'),
    'cloud-vps-cost-comparison-2026': ('cloud-vps-kostenvergleich-2026', 'comparaison-cloud-vps-2026', 'bulut-vps-karsilastirma-2026'),
    'dalle3-vs-stable-diffusion-cost-2026': ('dalle-vs-stable-diffusion-kosten-2026', 'dalle-vs-stable-diffusion-cout-2026', 'dalle-vs-stable-diffusion-maliyet-2026'),
    'embedding-api-cost-2026': ('embedding-api-kosten-2026', 'cout-api-embedding-2026', 'embedding-api-maliyet-2026'),
    'lemon-squeezy-vs-stripe-2026': ('lemon-squeezy-vs-stripe-2026', 'lemon-squeezy-vs-stripe-frais-2026', 'stripe-vs-paddle-ucretleri-2026'),
    'midjourney-vs-dalle-cost-2026': ('dalle-vs-stable-diffusion-kosten-2026', 'midjourney-vs-dalle-cout-2026', 'midjourney-vs-dalle-maliyet-2026'),
    'pinecone-pricing-guide-2026': ('embedding-api-kosten-2026', 'pinecone-guide-tarifs-2026', 'pinecone-fiyat-rehberi-2026'),
    'reduce-llm-api-costs-2026': ('llm-kosten-senken-2026', 'reduire-couts-llm-2026', 'llm-maliyet-dusurme-2026'),
    'stt-tts-api-cost-2026': ('stt-tts-api-kosten-2026', 'cout-api-stt-tts-2026', 'stt-tts-api-maliyet-2026'),
    'ai-agent-cost-calculator-2026': ('ki-agent-kosten-2026', 'cout-agent-ia-2026', 'yapay-zeka-ajan-maliyet-2026'),
    'api-gateway-pricing-2026': ('api-gateway-preise-2026', 'prix-api-gateway-2026', 'api-gateway-fiyat-2026'),
}

def build_blog_hreflang(en_slug, lang):
    """Build hreflang block for a blog post in a given language."""
    slugs = BLOG_MAP.get(en_slug)
    if not slugs:
        return None
    de_slug, fr_slug, tr_slug = slugs
    return f'''<link rel="alternate" hreflang="en" href="https://apicalculators.com/blog/{en_slug}.html" />
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/blog/{de_slug}.html" />
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/blog/{fr_slug}.html" />
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/blog/{tr_slug}.html" />'''

# ── 1b. og:locale fix ─────────────────────────────────────────────────────────
def fix_og_locale(c, correct_locale):
    return re.sub(
        r'<meta property="og:locale" content="[^"]+"\s*/?>',
        f'<meta property="og:locale" content="{correct_locale}" />',
        c
    )

# ── 1c. Geo meta ───────────────────────────────────────────────────────────────
GEO_BLOCKS = {
    'de': '<meta name="geo.region" content="DE" />\n<meta name="geo.placename" content="Germany" />',
    'fr': '<meta name="geo.region" content="FR" />\n<meta name="geo.placename" content="France" />',
    'tr': '<meta name="geo.region" content="TR" />\n<meta name="geo.placename" content="Turkey" />',
}

def ensure_geo(c, lang):
    if 'geo.region' in c:
        # Already has geo — make sure it's correct for this lang
        region = {'de': 'DE', 'fr': 'FR', 'tr': 'TR'}[lang]
        place = {'de': 'Germany', 'fr': 'France', 'tr': 'Turkey'}[lang]
        c = re.sub(r'<meta name="geo\.region" content="[^"]*"\s*/?>', f'<meta name="geo.region" content="{region}" />', c)
        c = re.sub(r'<meta name="geo\.placename" content="[^"]*"\s*/?>', f'<meta name="geo.placename" content="{place}" />', c)
        return c
    # Insert before </head>
    geo = GEO_BLOCKS[lang]
    return c.replace('</head>', f'{geo}\n</head>', 1)

def ensure_hreflang(c, hreflang_block):
    if 'hreflang' in c:
        # Already has hreflang — skip (don't double-add)
        return c
    # Insert after <link rel="canonical" ...> or before </head>
    canon = re.search(r'<link rel="canonical"[^>]+>', c)
    if canon:
        insert_pos = canon.end()
        return c[:insert_pos] + '\n' + hreflang_block + c[insert_pos:]
    return c.replace('</head>', hreflang_block + '\n</head>', 1)

# ── 1d. Vultr affiliate link in cloud-vps post ─────────────────────────────────
VULTR_PLACEHOLDER = re.compile(
    r'APICalculators affiliate link|"affiliate link"|placeholder affiliate',
    re.IGNORECASE
)
VULTR_LINK = '<a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank">Get $300 Vultr credit →</a>'

# ── Process all files ──────────────────────────────────────────────────────────
changed = []

for path in all_html():
    r = rel(path)
    c = open(path, encoding='utf-8').read()
    orig = c

    # Determine page context
    parts = r.strip('/').split('/')
    # lang: '', 'de', 'fr', 'tr'
    if parts[0] in ('de', 'fr', 'tr'):
        lang = parts[0]
        is_blog_post = len(parts) == 3 and parts[1] == 'blog'
        is_blog_index = len(parts) == 3 and parts[1] == 'blog' and parts[2] == 'index.html'
        is_index = parts[-1] == 'index.html' and len(parts) == 2
    else:
        lang = 'en'
        is_blog_post = len(parts) == 3 and parts[1] == 'blog'
        is_blog_index = len(parts) == 3 and parts[1] == 'blog' and parts[2] == 'index.html'
        is_index = parts[-1] == 'index.html' and len(parts) == 1

    # 1a. Hreflang
    if is_index or r in ('/index.html', '/de/index.html', '/fr/index.html', '/tr/index.html'):
        c = ensure_hreflang(c, MAIN_HREFLANG)
    elif is_blog_post and not is_blog_index:
        fname = parts[-1].replace('.html', '')
        # Find EN slug
        if lang == 'en':
            en_slug = fname
        else:
            # Find EN slug from BLOG_MAP
            idx = {'de': 0, 'fr': 1, 'tr': 2}[lang]
            en_slug = next((k for k, v in BLOG_MAP.items() if v[idx] == fname), None)
        if en_slug:
            hreflang_block = build_blog_hreflang(en_slug, lang)
            if hreflang_block:
                c = ensure_hreflang(c, hreflang_block)

    # 1b. og:locale
    locale_map = {'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'tr': 'tr_TR'}
    correct_locale = locale_map[lang]
    if 'og:locale' in c:
        c = fix_og_locale(c, correct_locale)
    # If no og:locale tag exists, don't add (not required by brief)

    # 1c. Geo meta for DE/FR/TR pages
    if lang in ('de', 'fr', 'tr'):
        c = ensure_geo(c, lang)

    # 1d. Vultr broken affiliate link (cloud-vps blog post)
    if 'cloud-vps' in r and lang == 'en':
        # Fix any plain-text affiliate placeholder
        if VULTR_PLACEHOLDER.search(c):
            c = VULTR_PLACEHOLDER.sub(VULTR_LINK, c)

    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        changed.append(r)

print(f'Fixed {len(changed)} files:')
for r in sorted(changed):
    print(f'  {r}')
