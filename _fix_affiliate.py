#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 4: Affiliate CTA blocks in calculator panels + inline blog links."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── Affiliate links — replace placeholders when approved ──────────────────────
LINKS = {
    'vultr':       'https://www.vultr.com/?ref=9904710-9J',           # LIVE
    'supabase':    '[SUPABASE_AFFILIATE_LINK]',
    'vercel':      '[VERCEL_AFFILIATE_LINK]',
    'do':          '[DIGITALOCEAN_AFFILIATE_LINK]',
    'hetzner':     '[HETZNER_AFFILIATE_LINK]',
    'pinecone':    '[PINECONE_AFFILIATE_LINK]',
    'elevenlabs':  '[ELEVENLABS_AFFILIATE_LINK]',
    'cloudflare':  '[CLOUDFLARE_AFFILIATE_LINK]',
}

def btn(href, icon, text, rel='sponsored'):
    return f'<a href="{href}" rel="{rel}" target="_blank" class="aff-btn">{icon} {text}</a>'

# ── CTA blocks per panel ───────────────────────────────────────────────────────
# lang -> panel_id -> html block
def cta(lang, panel_id):
    L = lang

    if panel_id == 'llm':
        if L == 'de':
            headline = 'Jetzt deployen — kostenlose Credits:'
            b1 = btn(LINKS['vultr'],  '☁️', '$300 Vultr-Guthaben')
            b2 = btn(LINKS['do'],     '🌊', '$200 DigitalOcean')
        elif L == 'fr':
            headline = 'Déployez maintenant — crédits offerts :'
            b1 = btn(LINKS['vultr'],  '☁️', '$300 crédit Vultr')
            b2 = btn(LINKS['do'],     '🌊', '$200 DigitalOcean')
        elif L == 'tr':
            headline = 'Hemen deploy et — ücretsiz kredi:'
            b1 = btn(LINKS['vultr'],  '☁️', '$300 Vultr Kredisi')
            b2 = btn(LINKS['do'],     '🌊', '$200 DigitalOcean')
        else:
            headline = 'Ready to build? Start with free credits:'
            b1 = btn(LINKS['vultr'],  '☁️', '$300 Vultr credit')
            b2 = btn(LINKS['do'],     '🌊', '$200 DigitalOcean')
        return _block(headline, [b1, b2], 'llm-affiliate')

    elif panel_id == 'vector':
        if L == 'de':
            headline = 'Vector-Suche aufbauen:'
            b1 = btn(LINKS['supabase'], '⚡', 'Supabase starten')
            b2 = btn(LINKS['pinecone'], '🌲', 'Pinecone kostenlos testen')
        elif L == 'fr':
            headline = 'Lancez votre recherche vectorielle :'
            b1 = btn(LINKS['supabase'], '⚡', 'Démarrer sur Supabase')
            b2 = btn(LINKS['pinecone'], '🌲', 'Essayer Pinecone gratuitement')
        elif L == 'tr':
            headline = 'Vektör aramanı kur:'
            b1 = btn(LINKS['supabase'], '⚡', 'Supabase ile başla')
            b2 = btn(LINKS['pinecone'], '🌲', 'Pinecone ücretsiz dene')
        else:
            headline = 'Start building your vector search:'
            b1 = btn(LINKS['supabase'], '⚡', 'Build on Supabase')
            b2 = btn(LINKS['pinecone'], '🌲', 'Try Pinecone free')
        return _block(headline, [b1, b2], 'vectordb-affiliate')

    elif panel_id == 'cloud':
        if L == 'de':
            headline = 'Server heute deployen:'
            b1 = btn(LINKS['vultr'],   '🖥️', '$300 Vultr-Guthaben')
            b2 = btn(LINKS['hetzner'], '🇩🇪', 'Hetzner — günstigstes EU')
            b3 = btn(LINKS['do'],      '🌊', '$200 DigitalOcean')
        elif L == 'fr':
            headline = 'Déployez votre serveur aujourd\'hui :'
            b1 = btn(LINKS['vultr'],   '🖥️', '$300 crédit Vultr')
            b2 = btn(LINKS['hetzner'], '🇩🇪', 'Hetzner — moins cher EU')
            b3 = btn(LINKS['do'],      '🌊', '$200 DigitalOcean')
        elif L == 'tr':
            headline = 'Sunucunu bugün kur:'
            b1 = btn(LINKS['vultr'],   '🖥️', '$300 Vultr Kredisi')
            b2 = btn(LINKS['hetzner'], '🇩🇪', 'Hetzner — EU\'nun en ucuzu')
            b3 = btn(LINKS['do'],      '🌊', '$200 DigitalOcean')
        else:
            headline = 'Deploy your server today:'
            b1 = btn(LINKS['vultr'],   '🖥️', '$300 Vultr credit')
            b2 = btn(LINKS['hetzner'], '🇩🇪', 'Hetzner — cheapest EU')
            b3 = btn(LINKS['do'],      '🌊', '$200 DigitalOcean')
        return _block(headline, [b1, b2, b3], 'vps-affiliate')

    elif panel_id == 'serverless':
        if L == 'de':
            headline = 'Serverless deployen:'
            b1 = btn(LINKS['vercel'],     '▲', 'Auf Vercel starten')
            b2 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        elif L == 'fr':
            headline = 'Déployez en serverless :'
            b1 = btn(LINKS['vercel'],     '▲', 'Déployer sur Vercel')
            b2 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        elif L == 'tr':
            headline = 'Serverless deploy et:'
            b1 = btn(LINKS['vercel'],     '▲', 'Vercel\'de yayınla')
            b2 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        else:
            headline = 'Ship serverless today:'
            b1 = btn(LINKS['vercel'],     '▲', 'Deploy on Vercel')
            b2 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        return _block(headline, [b1, b2], 'serverless-affiliate')

    elif panel_id == 'stt':
        if L == 'de':
            headline = 'Text-to-Speech API testen:'
            b1 = btn(LINKS['elevenlabs'], '🎙️', 'ElevenLabs kostenlos testen')
        elif L == 'fr':
            headline = 'Testez l\'API Text-to-Speech :'
            b1 = btn(LINKS['elevenlabs'], '🎙️', 'Essayer ElevenLabs gratuitement')
        elif L == 'tr':
            headline = 'Text-to-Speech API\'yi dene:'
            b1 = btn(LINKS['elevenlabs'], '🎙️', 'ElevenLabs\'ı ücretsiz dene')
        else:
            headline = 'Try the best TTS API:'
            b1 = btn(LINKS['elevenlabs'], '🎙️', 'Try ElevenLabs free')
        return _block(headline, [b1], 'tts-affiliate')

    elif panel_id == 'gateway':
        if L == 'de':
            headline = 'API Gateway deployen:'
            b1 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        elif L == 'fr':
            headline = 'Déployez votre API Gateway :'
            b1 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        elif L == 'tr':
            headline = 'API Gateway kur:'
            b1 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        else:
            headline = 'Deploy your API Gateway:'
            b1 = btn(LINKS['cloudflare'], '🔶', 'Cloudflare Workers')
        return _block(headline, [b1], 'gateway-affiliate')

    elif panel_id == 'embedding':
        if L == 'de':
            headline = 'Embeddings speichern:'
            b1 = btn(LINKS['supabase'], '⚡', 'Auf Supabase aufbauen')
        elif L == 'fr':
            headline = 'Stockez vos embeddings :'
            b1 = btn(LINKS['supabase'], '⚡', 'Construire sur Supabase')
        elif L == 'tr':
            headline = 'Embedding\'leri sakla:'
            b1 = btn(LINKS['supabase'], '⚡', 'Supabase ile inşa et')
        else:
            headline = 'Store your embeddings:'
            b1 = btn(LINKS['supabase'], '⚡', 'Build on Supabase')
        return _block(headline, [b1], 'embedding-affiliate')

    elif panel_id == 'agent':
        if L == 'de':
            headline = 'AI Agent infrastruktur deployen:'
            b1 = btn(LINKS['vultr'], '☁️', '$300 Vultr-Guthaben')
            b2 = btn(LINKS['do'],    '🌊', '$200 DigitalOcean')
        elif L == 'fr':
            headline = 'Déployez votre infrastructure AI Agent :'
            b1 = btn(LINKS['vultr'], '☁️', '$300 crédit Vultr')
            b2 = btn(LINKS['do'],    '🌊', '$200 DigitalOcean')
        elif L == 'tr':
            headline = 'AI Agent altyapını kur:'
            b1 = btn(LINKS['vultr'], '☁️', '$300 Vultr Kredisi')
            b2 = btn(LINKS['do'],    '🌊', '$200 DigitalOcean')
        else:
            headline = 'Deploy your AI Agent infrastructure:'
            b1 = btn(LINKS['vultr'], '☁️', '$300 Vultr credit')
            b2 = btn(LINKS['do'],    '🌊', '$200 DigitalOcean')
        return _block(headline, [b1, b2], 'agent-affiliate')

    return None  # image, pay, llm without sponsor

def _block(headline, btns, block_id):
    btns_html = '\n    '.join(btns)
    return f'''
<div class="affiliate-cta" id="{block_id}">
  <p class="aff-headline">{headline}</p>
  <div class="aff-links">
    {btns_html}
  </div>
</div>'''

# ── CSS for affiliate CTAs (inject once into <head>) ───────────────────────────
AFF_CSS = '''<style>
.affiliate-cta{margin:1.5rem 0 0.5rem;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px;}
.aff-headline{margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;letter-spacing:.02em;}
.aff-links{display:flex;flex-wrap:wrap;gap:.5rem;}
.aff-btn{display:inline-block;padding:.35rem .75rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:6px;color:#e8eaed;text-decoration:none;font-size:.82rem;transition:background .15s,border-color .15s;}
.aff-btn:hover{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.5);color:#b8ff2e;}
</style>'''

# ── Process calculator pages ───────────────────────────────────────────────────
CALC_FILES = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

PANEL_IDS = ['llm', 'vector', 'image', 'pay', 'cloud', 'stt', 'serverless', 'gateway', 'embedding', 'agent']

changed = []

for lang, path in CALC_FILES.items():
    c = open(path, encoding='utf-8').read()
    orig = c

    # Skip if already done
    if 'affiliate-cta' in c:
        print(f'  SKIP {lang}/index.html (already has affiliate CTAs)')
        continue

    # Inject CSS into <head>
    c = c.replace('</head>', AFF_CSS + '\n</head>', 1)

    # Insert CTA into each panel before </section>
    for panel_id in PANEL_IDS:
        block = cta(lang, panel_id)
        if not block:
            continue
        # Find the panel section
        panel_marker = f'id="{panel_id}"'
        pos = c.find(f'<section class="panel" {panel_marker}')
        if pos < 0:
            pos = c.find(f'<section class="panel on" {panel_marker}')
        if pos < 0:
            print(f'  WARNING: panel "{panel_id}" not found in {lang}')
            continue
        # Find closing </section> for this panel
        section_end = c.find('</section>', pos)
        if section_end < 0:
            continue
        # Insert CTA before </section>
        c = c[:section_end] + block + '\n' + c[section_end:]

    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        changed.append(f'{lang}/index.html')
        print(f'  Done: {lang}/index.html')

# ── Blog inline affiliate links ────────────────────────────────────────────────
# cloud-vps: add Hetzner + Vultr CTA after main comparison section
BLOG_AFFILS = {
    os.path.join(BASE, 'blog', 'cloud-vps-cost-comparison-2026.html'): {
        'marker': 'Hetzner',  # after first mention of Hetzner in body content
        'insert_after_h2': 'Provider Comparison',
        'block': f'''<div class="affiliate-cta" style="margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px;">
  <p style="margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;">Deploy your server today:</p>
  <div style="display:flex;flex-wrap:wrap;gap:.5rem;">
    <a href="{LINKS['vultr']}" rel="sponsored" target="_blank" class="aff-btn">🖥️ $300 Vultr credit</a>
    <a href="{LINKS['hetzner']}" rel="sponsored" target="_blank" class="aff-btn">🇩🇪 Hetzner — cheapest EU</a>
    <a href="{LINKS['do']}" rel="sponsored" target="_blank" class="aff-btn">🌊 $200 DigitalOcean</a>
  </div>
</div>''',
    },
    os.path.join(BASE, 'blog', 'vector-database-cost-comparison-2026.html'): {
        'block': f'''<div class="affiliate-cta" style="margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px;">
  <p style="margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;">Start building your vector search:</p>
  <div style="display:flex;flex-wrap:wrap;gap:.5rem;">
    <a href="{LINKS['supabase']}" rel="sponsored" target="_blank" class="aff-btn">⚡ Build on Supabase</a>
    <a href="{LINKS['pinecone']}" rel="sponsored" target="_blank" class="aff-btn">🌲 Try Pinecone free</a>
  </div>
</div>''',
    },
    os.path.join(BASE, 'blog', 'aws-lambda-cost-calculator-2026.html'): {
        'block': f'''<div class="affiliate-cta" style="margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px;">
  <p style="margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;">Ship serverless today:</p>
  <div style="display:flex;flex-wrap:wrap;gap:.5rem;">
    <a href="{LINKS['vercel']}" rel="sponsored" target="_blank" class="aff-btn">▲ Deploy on Vercel</a>
    <a href="{LINKS['cloudflare']}" rel="sponsored" target="_blank" class="aff-btn">🔶 Cloudflare Workers</a>
  </div>
</div>''',
    },
    os.path.join(BASE, 'blog', 'stt-tts-api-cost-2026.html'): {
        'block': f'''<div class="affiliate-cta" style="margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px;">
  <p style="margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;">Try the best TTS API:</p>
  <div style="display:flex;flex-wrap:wrap;gap:.5rem;">
    <a href="{LINKS['elevenlabs']}" rel="sponsored" target="_blank" class="aff-btn">🎙️ Try ElevenLabs free</a>
  </div>
</div>''',
    },
}

for path, cfg in BLOG_AFFILS.items():
    if not os.path.exists(path):
        print(f'  MISSING: {path}')
        continue
    c = open(path, encoding='utf-8').read()
    if 'affiliate-cta' in c:
        print(f'  SKIP blog (already has CTA): {os.path.basename(path)}')
        continue
    orig = c

    # Inject CSS if not present
    if 'aff-btn' not in c:
        c = c.replace('</head>', AFF_CSS + '\n</head>', 1)

    # Insert block before last <h2> (FAQ/Related section)
    last_h2 = None
    for m in re.finditer(r'<h2[^>]*>', c):
        last_h2 = m
    if last_h2:
        pos = last_h2.start()
        c = c[:pos] + cfg['block'] + '\n' + c[pos:]

    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        changed.append('blog/' + os.path.basename(path))
        print(f'  Done blog: {os.path.basename(path)}')

print(f'\nTotal changed: {len(changed)} files')
for p in sorted(changed):
    print(f'  {p}')
