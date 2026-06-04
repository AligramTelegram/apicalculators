#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Audit Fix — Priority 1, 2, 3
1. Geo tags — homepages + all DE/FR/TR blog posts
2. Title shortening — 4 homepages under 60 chars
3. Schema — FR/TR SoftwareApplication + DE/FR/TR BreadcrumbList on homepages
"""
import sys, os, re, glob, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

changed = []

# ═══════════════════════════════════════════════════════════════════════════════
# PRIORITY 1 — Geo tags
# ═══════════════════════════════════════════════════════════════════════════════

GEO = {
    'de': '<meta name="geo.region" content="DE" />\n<meta name="geo.placename" content="Germany" />',
    'fr': '<meta name="geo.region" content="FR" />\n<meta name="geo.placename" content="France" />',
    'tr': '<meta name="geo.region" content="TR" />\n<meta name="geo.placename" content="Turkey" />',
}

def inject_geo(path, lang):
    c = read(path)
    if f'geo.region" content="{lang.upper()}"' in c:
        return False  # already has it
    geo_block = GEO[lang]
    # Insert before </head>
    c = c.replace('</head>', geo_block + '\n</head>', 1)
    write(path, c)
    return True

# Homepages
for lang in ['de', 'fr', 'tr']:
    path = os.path.join(BASE, lang, 'index.html')
    if inject_geo(path, lang):
        changed.append(path)
        print(f'✓ GEO homepage: {lang}/index.html')

# All DE/FR/TR blog posts
for lang in ['de', 'fr', 'tr']:
    pattern = os.path.join(BASE, lang, 'blog', '*.html')
    for path in glob.glob(pattern):
        if inject_geo(path, lang):
            changed.append(path)
            print(f'  ✓ GEO blog: {os.path.relpath(path, BASE)}')

print(f'\nGeo tags: {len(changed)} files updated\n')

# ═══════════════════════════════════════════════════════════════════════════════
# PRIORITY 2 — Title shortening (homepages only, under 60 chars)
# ═══════════════════════════════════════════════════════════════════════════════

TITLES = {
    'index.html':    ('LLM, Cloud VPS, Serverless &amp; Embedding Cost Calculators | APICalculators',
                      'API Cost Calculators: LLM, VPS, Serverless | APICalculators'),
    'de/index.html': ('LLM, Cloud VPS, Serverless &amp; Embedding Kostenrechner | APICalculators',
                      'LLM &amp; API Kostenrechner 2026 | APICalculators'),
    'fr/index.html': ('Calculatrices LLM, Cloud VPS, Serverless &amp; Embeddings | APICalculators',
                      'Calculateur LLM &amp; API Coûts 2026 | APICalculators'),
    'tr/index.html': ('LLM, Cloud VPS, Serverless ve Embedding Maliyet Hesaplayıcıları | APICalculators',
                      'LLM &amp; API Maliyet Hesaplayıcı 2026 | APICalculators'),
}

title_count = 0
for rel, (old_title, new_title) in TITLES.items():
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  SKIP (not found): {rel}')
        continue
    c = read(path)
    old_tag = f'<title>{old_title}</title>'
    new_tag = f'<title>{new_title}</title>'
    if old_tag in c:
        c = c.replace(old_tag, new_tag, 1)
        write(path, c)
        if path not in changed: changed.append(path)
        title_count += 1
        plain = new_title.replace('&amp;', '&')
        print(f'✓ TITLE ({len(plain)} chars): {rel} → {plain}')
    elif new_tag in c:
        print(f'  SKIP (already short): {rel}')
    else:
        # Try to find the actual title
        m = re.search(r'<title>(.*?)</title>', c)
        if m:
            print(f'  WARN: title mismatch in {rel}: {m.group(1)[:60]}')

print(f'\nTitles: {title_count} updated\n')

# ═══════════════════════════════════════════════════════════════════════════════
# PRIORITY 3 — Schema completion on homepages
# ═══════════════════════════════════════════════════════════════════════════════

# 3a: FR homepage — add SoftwareApplication schema
FR_SW_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "APICalculators — Calculatrices de Coûts Infrastructure IA",
    "operatingSystem": "Web",
    "applicationCategory": "DeveloperApplication",
    "inLanguage": "fr",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "url": "https://apicalculators.com/fr/"
})

# 3b: TR homepage — add SoftwareApplication schema
TR_SW_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "APICalculators — YZ Altyapı Maliyet Hesaplayıcıları",
    "operatingSystem": "Web",
    "applicationCategory": "DeveloperApplication",
    "inLanguage": "tr",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "url": "https://apicalculators.com/tr/"
})

# 3c: DE/FR/TR homepages — add BreadcrumbList schema
def breadcrumb_schema(lang):
    home = f"https://apicalculators.com/{lang}/"
    label = {"de": "Startseite", "fr": "Accueil", "tr": "Ana Sayfa"}[lang]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": label, "item": home}
        ]
    })

schema_count = 0

def inject_schema(path, schema_json, check_type):
    c = read(path)
    if f'"@type":"{check_type}"' in c or f'"@type": "{check_type}"' in c:
        print(f'  SKIP ({check_type} exists): {os.path.relpath(path, BASE)}')
        return False
    tag = f'<script type="application/ld+json">{schema_json}</script>\n'
    c = c.replace('</head>', tag + '</head>', 1)
    write(path, c)
    return True

# FR SoftwareApplication
path = os.path.join(BASE, 'fr', 'index.html')
if inject_schema(path, FR_SW_SCHEMA, 'SoftwareApplication'):
    if path not in changed: changed.append(path)
    schema_count += 1
    print('✓ SCHEMA SoftwareApplication → fr/index.html')

# TR SoftwareApplication
path = os.path.join(BASE, 'tr', 'index.html')
if inject_schema(path, TR_SW_SCHEMA, 'SoftwareApplication'):
    if path not in changed: changed.append(path)
    schema_count += 1
    print('✓ SCHEMA SoftwareApplication → tr/index.html')

# DE/FR/TR BreadcrumbList
for lang in ['de', 'fr', 'tr']:
    path = os.path.join(BASE, lang, 'index.html')
    if inject_schema(path, breadcrumb_schema(lang), 'BreadcrumbList'):
        if path not in changed: changed.append(path)
        schema_count += 1
        print(f'✓ SCHEMA BreadcrumbList → {lang}/index.html')

print(f'\nSchema: {schema_count} injected\n')

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print(f'Total files modified: {len(set(changed))}')
print('Done.')
