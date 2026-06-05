#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 12 calculator links to ALL page footers (calc, blog, about, etc.)"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# ─── FOOTER CALC LINKS BY LANGUAGE ────────────────────────────────────────────

CALC_LINKS = {
    'en': {
        'heading': 'Calculators',
        'home': '/',
        'links': [
            ('<a href="/#llm">LLM Token Cost</a>'),
            ('<a href="/#vector">Vector DB Cost</a>'),
            ('<a href="/#image">AI Image Generation</a>'),
            ('<a href="/#pay">Payment Fees</a>'),
            ('<a href="/#vps">Cloud VPS Comparison</a>'),
            ('<a href="/#stt">STT / TTS API Cost</a>'),
            ('<a href="/#serverless">Serverless Cost</a>'),
            ('<a href="/#gateway">API Gateway Cost</a>'),
            ('<a href="/#embeddings">Embedding API Cost</a>'),
            ('<a href="/#agent">AI Agent Cost</a>'),
            ('<a href="/ai-coding-tool-cost.html">AI Coding Tool Cost</a>'),
            ('<a href="/auth-provider-cost.html">Auth Provider Cost</a>'),
        ]
    },
    'de': {
        'heading': 'Rechner',
        'home': '/de/',
        'links': [
            '<a href="/de/#llm">LLM Token Kosten</a>',
            '<a href="/de/#vector">Vektordatenbank</a>',
            '<a href="/de/#image">KI Bildgenerierung</a>',
            '<a href="/de/#pay">Zahlungsgebühren</a>',
            '<a href="/de/#vps">Cloud VPS</a>',
            '<a href="/de/#stt">STT/TTS</a>',
            '<a href="/de/#serverless">Serverless</a>',
            '<a href="/de/#gateway">API Gateway</a>',
            '<a href="/de/#embeddings">Embeddings</a>',
            '<a href="/de/#agent">KI Agent</a>',
            '<a href="/de/ki-coding-tool-kosten.html">KI Coding Tool</a>',
            '<a href="/de/auth-anbieter-kosten.html">Auth Kosten</a>',
        ]
    },
    'fr': {
        'heading': 'Calculateurs',
        'home': '/fr/',
        'links': [
            '<a href="/fr/#llm">Coût Tokens LLM</a>',
            '<a href="/fr/#vector">Base Vectorielle</a>',
            '<a href="/fr/#image">Génération Images</a>',
            '<a href="/fr/#pay">Frais Paiement</a>',
            '<a href="/fr/#vps">VPS Cloud</a>',
            '<a href="/fr/#stt">STT/TTS</a>',
            '<a href="/fr/#serverless">Serverless</a>',
            '<a href="/fr/#gateway">API Gateway</a>',
            '<a href="/fr/#embeddings">Embeddings</a>',
            '<a href="/fr/#agent">Agent IA</a>',
            '<a href="/fr/cout-outil-ia-coding.html">Outil IA Coding</a>',
            '<a href="/fr/cout-fournisseur-auth.html">Coût Auth</a>',
        ]
    },
    'tr': {
        'heading': 'Hesaplayıcılar',
        'home': '/tr/',
        'links': [
            '<a href="/tr/#llm">LLM Token Maliyeti</a>',
            '<a href="/tr/#vector">Vektör Veritabanı</a>',
            '<a href="/tr/#image">AI Görüntü Oluşturma</a>',
            '<a href="/tr/#pay">Ödeme Ücretleri</a>',
            '<a href="/tr/#vps">Bulut VPS</a>',
            '<a href="/tr/#stt">STT/TTS</a>',
            '<a href="/tr/#serverless">Sunucusuz</a>',
            '<a href="/tr/#gateway">API Gateway</a>',
            '<a href="/tr/#embeddings">Embeddingler</a>',
            '<a href="/tr/#agent">AI Ajan</a>',
            '<a href="/tr/yapay-zeka-kodlama-arac-maliyeti.html">AI Kodlama Aracı</a>',
            '<a href="/tr/kimlik-dogrulama-maliyet.html">Kimlik Doğrulama</a>',
        ]
    },
}

def get_lang(fpath):
    """Determine language from file path"""
    norm = fpath.replace('\\', '/')
    if '/de/' in norm: return 'de'
    if '/fr/' in norm: return 'fr'
    if '/tr/' in norm: return 'tr'
    return 'en'

def make_calc_nav(lang):
    cfg = CALC_LINKS[lang]
    links_html = '\n          '.join(cfg['links'])
    return f'''<div class="foot-calcs">
        <strong>{cfg['heading']}</strong>
        <nav>
          {links_html}
        </nav>
      </div>'''

def add_calc_nav_css(content):
    """Inject CSS for foot-calcs if not present"""
    if 'foot-calcs' in content:
        return content
    css = '''<style>
.foot-calcs{padding:18px 0 10px;border-top:1px solid #1e2535;margin-top:12px}
.foot-calcs strong{display:block;font-size:11px;font-weight:700;color:var(--muted,#6b7a99);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.foot-calcs nav{display:flex;flex-wrap:wrap;gap:4px 14px}
.foot-calcs nav a{font-size:12px;color:var(--muted,#6b7a99);text-decoration:none;white-space:nowrap}
.foot-calcs nav a:hover{color:var(--lime,#b8ff2e)}
</style>'''
    content = content.replace('</head>', css + '\n</head>', 1)
    return content

def already_has_full_calcs(footer_html):
    """Check if footer already has all 12 calc links"""
    return ('coding' in footer_html.lower() or 'kodlama' in footer_html.lower()) and \
           ('auth' in footer_html.lower() or 'kimlik' in footer_html.lower())

changed = 0
skipped = 0
errors = []

for root, dirs, files in os.walk(BASE):
    # Skip hidden/script dirs
    dirs[:] = [d for d in dirs if not d.startswith('_') and d != '.git' and d != 'node_modules']
    for fname in sorted(files):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, BASE)

        # Skip 404
        if fname == '404.html':
            continue

        c = read(fpath)

        # Detect footer type
        footer_idx = c.rfind('<footer')
        if footer_idx == -1:
            continue
        footer_html = c[footer_idx:]

        # Skip if already has full 12-link footer
        if already_has_full_calcs(footer_html):
            skipped += 1
            continue

        lang = get_lang(fpath)
        calc_nav = make_calc_nav(lang)

        # CASE 1: Full grid footer (homepages) — already handled, skip
        if 'foot-grid' in footer_html:
            skipped += 1
            continue

        # CASE 2: Minimal footer with foot-in div
        # Pattern: <footer>...<div class="wrap foot-in">...</div></footer>
        # Inject calc nav before </footer>
        if 'foot-in' in footer_html:
            new_c = c.replace('</footer>', f'  <div class="wrap">{calc_nav}</div>\n</footer>', 1)
            new_c = add_calc_nav_css(new_c)
            if new_c != c:
                write(fpath, new_c)
                changed += 1
                print(f'  FIXED: {rel}')
                continue

        # CASE 3: Any other footer — inject before </footer>
        if '</footer>' in c:
            new_c = c.replace('</footer>', f'  <div class="wrap">{calc_nav}</div>\n</footer>', 1)
            new_c = add_calc_nav_css(new_c)
            if new_c != c:
                write(fpath, new_c)
                changed += 1
                print(f'  FIXED (generic): {rel}')
            else:
                errors.append(rel)
        else:
            errors.append(f'NO </footer>: {rel}')

print(f'\n✓ Changed: {changed}')
print(f'✓ Already OK (skipped): {skipped}')
if errors:
    print(f'✗ Errors: {len(errors)}')
    for e in errors: print(f'  {e}')
