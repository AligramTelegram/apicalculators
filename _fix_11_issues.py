#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all 11 issues in one pass"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'
B = 'https://apicalculators.com'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

stats = {i: 0 for i in range(1, 12)}

all_html = sorted(glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True))

# ─── FIX 1: Remove "Keyword: <em>...</em>" annotations ───────────────────────
print('=== FIX 1: Keyword annotations ===')
for fpath in all_html:
    c = read(fpath)
    # Remove " Keyword: <em>...</em>" (with optional period after)
    new_c = re.sub(r'\s*Keyword:\s*<em>[^<]*</em>\.?', '', c)
    if new_c != c:
        write(fpath, new_c)
        stats[1] += 1
        print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 2: Remove "← selected" text ─────────────────────────────────────────
print('\n=== FIX 2: ← selected ===')
for fpath in all_html:
    c = read(fpath)
    new_c = c.replace(' ← selected', '').replace('← selected', '')
    if new_c != c:
        write(fpath, new_c)
        stats[2] += 1
        print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 3: Title tag on EN pages ─────────────────────────────────────────────
print('\n=== FIX 3: Title tag ===')
OLD_TITLE = 'LLM & API Cost Calculators: Free Tools 2026 | APICalculators'
NEW_TITLE = 'Free LLM & API Cost Calculators 2026 | APICalculators'
for fpath in all_html:
    c = read(fpath)
    if OLD_TITLE in c:
        write(fpath, c.replace(OLD_TITLE, NEW_TITLE))
        stats[3] += 1
        print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 4: H1 on EN homepage ─────────────────────────────────────────────────
print('\n=== FIX 4: H1 homepage ===')
EN_H1_OLD = 'Free <span class="em">API &amp; AI Cost Calculators</span>'
EN_H1_NEW = 'Free <span class="em">LLM &amp; API Cost Calculator</span>'
EN_H1_OLD2 = 'Free <span class="em">API & AI Cost Calculators</span>'
EN_H1_NEW2 = 'Free <span class="em">LLM & API Cost Calculator</span>'

fpath = os.path.join(BASE, 'index.html')
c = read(fpath)
if EN_H1_OLD in c:
    write(fpath, c.replace(EN_H1_OLD, EN_H1_NEW))
    stats[4] += 1
    print('  index.html (amp encoded)')
elif EN_H1_OLD2 in c:
    write(fpath, c.replace(EN_H1_OLD2, EN_H1_NEW2))
    stats[4] += 1
    print('  index.html')
else:
    # Try regex
    c2 = re.sub(r'Free <span class="em">API &amp; AI Cost Calculators</span>', EN_H1_NEW, c)
    if c2 != c:
        write(fpath, c2)
        stats[4] += 1
        print('  index.html (regex)')
    else:
        print('  WARN: EN H1 pattern not matched, current H1:')
        m = re.search(r'<h1[^>]*>(.*?)</h1>', c, re.DOTALL)
        print(f'    {m.group(1)[:100] if m else "NOT FOUND"}')

# ─── FIX 5: geo.region for DE pages ──────────────────────────────────────────
print('\n=== FIX 5: DE geo.region ===')
DE_GEO = '<meta name="geo.region" content="DE" />\n<meta name="geo.placename" content="Germany" />'
de_pages = [f for f in all_html if os.sep + 'de' + os.sep in f or f.endswith(os.sep + 'de' + os.sep + 'index.html')]
de_pages = [f for f in all_html if 'APICalculators' + os.sep + 'de' + os.sep in f]
for fpath in de_pages:
    c = read(fpath)
    if 'geo.region' in c:
        continue
    c = c.replace('</head>', DE_GEO + '\n</head>', 1)
    write(fpath, c)
    stats[5] += 1
    print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 6: geo.region for TR pages ──────────────────────────────────────────
print('\n=== FIX 6: TR geo.region ===')
TR_GEO = '<meta name="geo.region" content="TR" />\n<meta name="geo.placename" content="Turkey" />'
tr_pages = [f for f in all_html if 'APICalculators' + os.sep + 'tr' + os.sep in f]
for fpath in tr_pages:
    c = read(fpath)
    if 'geo.region' in c:
        continue
    c = c.replace('</head>', TR_GEO + '\n</head>', 1)
    write(fpath, c)
    stats[6] += 1
    print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 7: twitter:creator on DE/FR/TR pages ─────────────────────────────────
print('\n=== FIX 7: twitter:creator ===')
TC = '<meta name="twitter:creator" content="@apicalculators" />'
non_en_pages = [f for f in all_html if (
    'APICalculators' + os.sep + 'de' + os.sep in f or
    'APICalculators' + os.sep + 'fr' + os.sep in f or
    'APICalculators' + os.sep + 'tr' + os.sep in f
)]
for fpath in non_en_pages:
    c = read(fpath)
    if 'twitter:creator' in c:
        continue
    # Inject after twitter:card or twitter:site
    if 'twitter:site' in c:
        c = re.sub(r'(<meta name="twitter:site"[^>]*/>\n?)', r'\1' + TC + '\n', c, count=1)
    else:
        c = c.replace('</head>', TC + '\n</head>', 1)
    write(fpath, c)
    stats[7] += 1
    print(f'  {os.path.relpath(fpath, BASE)}')

# ─── FIX 8: hreflang (already done in previous script, but ensure completeness) ─
print('\n=== FIX 8: hreflang (checking remaining) ===')
no_hreflang = []
for fpath in all_html:
    if fpath.endswith('404.html'):
        continue
    c = read(fpath)
    if 'hreflang' not in c:
        no_hreflang.append(fpath)
        stats[8] += 1
        print(f'  MISSING: {os.path.relpath(fpath, BASE)}')
if not no_hreflang:
    print('  All pages have hreflang ✓')

# ─── FIX 9: Footer calculator links (homepages only — others already done) ────
print('\n=== FIX 9: Footer links on homepages ===')

FOOTER_CALCS = {
    'index.html': {
        'heading': 'Calculators',
        'links': [
            '<a href="#llm">LLM Token Cost</a>',
            '<a href="#vector">Vector DB Cost</a>',
            '<a href="#image">AI Image Generation</a>',
            '<a href="#pay">Payment Fees</a>',
            '<a href="#vps">Cloud VPS Comparison</a>',
            '<a href="#stt">STT / TTS API Cost</a>',
            '<a href="#serverless">Serverless Cost</a>',
            '<a href="#gateway">API Gateway Cost</a>',
            '<a href="#embeddings">Embedding API Cost</a>',
            '<a href="#agent">AI Agent Cost</a>',
            '<a href="/ai-coding-tool-cost.html">AI Coding Tool Cost</a>',
            '<a href="/auth-provider-cost.html">Auth Provider Cost</a>',
        ]
    },
    'de/index.html': {
        'heading': 'Rechner',
        'links': [
            '<a href="/de/#llm">LLM Token Kosten</a>',
            '<a href="/de/#vector">Vektordatenbank</a>',
            '<a href="/de/#image">KI Bildgenerierung</a>',
            '<a href="/de/#pay">Zahlungsgebühren</a>',
            '<a href="/de/#vps">Cloud VPS</a>',
            '<a href="/de/#stt">STT / TTS</a>',
            '<a href="/de/#serverless">Serverless</a>',
            '<a href="/de/#gateway">API Gateway</a>',
            '<a href="/de/#embeddings">Embeddings</a>',
            '<a href="/de/#agent">KI Agent</a>',
            '<a href="/de/ki-coding-tool-kosten.html">KI Coding Tool</a>',
            '<a href="/de/auth-anbieter-kosten.html">Auth Kosten</a>',
        ]
    },
    'fr/index.html': {
        'heading': 'Calculatrices',
        'links': [
            '<a href="/fr/#llm">Coût Tokens LLM</a>',
            '<a href="/fr/#vector">Base Vectorielle</a>',
            '<a href="/fr/#image">Génération Images</a>',
            '<a href="/fr/#pay">Frais Paiement</a>',
            '<a href="/fr/#vps">VPS Cloud</a>',
            '<a href="/fr/#stt">STT / TTS</a>',
            '<a href="/fr/#serverless">Serverless</a>',
            '<a href="/fr/#gateway">API Gateway</a>',
            '<a href="/fr/#embeddings">Embeddings</a>',
            '<a href="/fr/#agent">Agent IA</a>',
            '<a href="/fr/cout-outil-ia-coding.html">Outil IA Coding</a>',
            '<a href="/fr/cout-fournisseur-auth.html">Coût Auth</a>',
        ]
    },
    'tr/index.html': {
        'heading': 'Hesaplayıcılar',
        'links': [
            '<a href="/tr/#llm">LLM Token Maliyeti</a>',
            '<a href="/tr/#vector">Vektör Veritabanı</a>',
            '<a href="/tr/#image">AI Görüntü Oluşturma</a>',
            '<a href="/tr/#pay">Ödeme Ücretleri</a>',
            '<a href="/tr/#vps">Bulut VPS</a>',
            '<a href="/tr/#stt">STT / TTS</a>',
            '<a href="/tr/#serverless">Sunucusuz</a>',
            '<a href="/tr/#gateway">API Gateway</a>',
            '<a href="/tr/#embeddings">Embeddingler</a>',
            '<a href="/tr/#agent">AI Ajan</a>',
            '<a href="/tr/yapay-zeka-kodlama-arac-maliyeti.html">AI Kodlama Aracı</a>',
            '<a href="/tr/kimlik-dogrulama-maliyet.html">Kimlik Doğrulama</a>',
        ]
    },
}

for fname, cfg in FOOTER_CALCS.items():
    fpath = os.path.join(BASE, fname.replace('/', os.sep))
    c = read(fpath)
    heading = cfg['heading']
    links_html = '\n        '.join(cfg['links'])
    new_div = f'''      <div>
        <h4>{heading}</h4>
        {links_html}
      </div>'''
    # Match any existing calcs div (4-link or 12-link)
    pattern = r'<div>\s*<h4>' + re.escape(heading) + r'</h4>.*?</div>'
    new_c = re.sub(pattern, new_div, c, flags=re.DOTALL)
    # Also try compact single-line format
    if new_c == c:
        pattern2 = r'<div><h4>' + re.escape(heading) + r'</h4>.*?</div>'
        new_c = re.sub(pattern2, new_div, c, flags=re.DOTALL)
    if new_c != c:
        write(fpath, new_c)
        stats[9] += 1
        print(f'  {fname}')
    else:
        # Check if already has 12 links
        footer_idx = c.rfind('<footer')
        footer = c[footer_idx:] if footer_idx != -1 else ''
        has_12 = 'auth-provider' in footer or 'auth-anbieter' in footer or 'cout-fournisseur' in footer or 'kimlik-dogrulama' in footer
        if has_12:
            print(f'  SKIP (already 12): {fname}')
        else:
            print(f'  WARN: pattern not matched for {fname}')

# ─── FIX 10: Sitemap ──────────────────────────────────────────────────────────
print('\n=== FIX 10: Sitemap ===')
sitemap_path = os.path.join(BASE, 'sitemap.xml')
c = read(sitemap_path)

changed_sm = False

# Add xhtml namespace
if 'xmlns:xhtml' not in c:
    c = c.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:xhtml="http://www.w3.org/1999/xhtml"'
    )
    changed_sm = True
    print('  Added xmlns:xhtml')

existing_locs = set(re.findall(r'<loc>(.*?)</loc>', c))
TODAY = '2026-06-06'

MISSING_PAGES = [
    'https://apicalculators.com/ai-coding-tool-cost.html',
    'https://apicalculators.com/auth-provider-cost.html',
    'https://apicalculators.com/de/ki-coding-tool-kosten.html',
    'https://apicalculators.com/de/auth-anbieter-kosten.html',
    'https://apicalculators.com/fr/cout-outil-ia-coding.html',
    'https://apicalculators.com/fr/cout-fournisseur-auth.html',
    'https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html',
    'https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html',
]

inject = ''
for loc in MISSING_PAGES:
    if loc not in existing_locs:
        inject += f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        changed_sm = True
        print(f'  Added: {loc}')

if inject:
    c = c.replace('</urlset>', inject + '</urlset>')

if changed_sm:
    write(sitemap_path, c)
    stats[10] = 1
    print(f'  Total URLs: {len(re.findall(r"<loc>", c))}')
else:
    print('  Sitemap already up to date')

# ─── FIX 11: og:locale en_EN → en_US ─────────────────────────────────────────
print('\n=== FIX 11: og:locale en_EN ===')
for fpath in all_html:
    c = read(fpath)
    if 'en_EN' in c:
        write(fpath, c.replace('en_EN', 'en_US'))
        stats[11] += 1
        print(f'  {os.path.relpath(fpath, BASE)}')

# ─── SUMMARY ──────────────────────────────────────────────────────────────────
print('\n' + '='*50)
print('ÖZET:')
total = sum(stats.values())
for i, count in stats.items():
    labels = {
        1: 'Keyword annotations kaldırıldı',
        2: '← selected kaldırıldı',
        3: 'Title tag düzeltildi',
        4: 'H1 düzeltildi',
        5: 'DE geo.region eklendi',
        6: 'TR geo.region eklendi',
        7: 'twitter:creator eklendi',
        8: 'hreflang eksik (sorun)',
        9: 'Footer 12 link güncellendi',
        10: 'Sitemap güncellendi',
        11: 'og:locale en_EN→en_US',
    }
    if count > 0:
        print(f'  Fix {i:2d}: {count:3d} dosya — {labels[i]}')
print(f'  TOPLAM: {total} dosya değiştirildi')
