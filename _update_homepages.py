#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 2 new tool cards to all 4 homepages"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

# New tool panels to inject — per language
NEW_PANELS = {
    'en': (
        # Anchor: look for the newsletter section or footer of calc panels
        # Inject before the newsletter/signup section
        '''
  <!-- PANEL 11: AI Coding Tool -->
  <section class="panel" id="coding" role="tabpanel">
    <div class="panel-head">
      <h2>AI Coding Tool Cost Calculator</h2>
      <p class="pdesc">Compare real monthly costs for Cursor, Copilot, Claude Code &amp; Windsurf. Keyword: <em>ai coding tool cost calculator</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Cursor says $20/month. Your bill says $180. Find your true monthly cost based on usage intensity and team size.</p>
      <a href="/ai-coding-tool-cost.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">💻 Open Calculator →</a>
    </div>
  </section>

  <!-- PANEL 12: Auth Provider -->
  <section class="panel" id="auth" role="tabpanel">
    <div class="panel-head">
      <h2>Auth Provider Cost Calculator</h2>
      <p class="pdesc">Clerk vs Auth0 vs Supabase Auth — at 100K users the difference is $1,800 vs $25/month. Keyword: <em>auth provider cost calculator</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Calculate your authentication cost by monthly active users. Supabase Auth is 73x cheaper than Clerk at 100K MAU.</p>
      <a href="/auth-provider-cost.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">🔑 Open Calculator →</a>
    </div>
  </section>
''',
        '''<button class="tab" data-panel="coding" role="tab">💻 AI Coding</button>
    <button class="tab" data-panel="auth" role="tab">🔑 Auth Cost</button>'''
    ),
    'de': (
        '''
  <!-- PANEL 11: KI Coding Tool -->
  <section class="panel" id="coding" role="tabpanel">
    <div class="panel-head">
      <h2>KI Coding Tool Kostenrechner</h2>
      <p class="pdesc">Cursor vs Copilot vs Claude Code echte Monatskosten berechnen. Keyword: <em>KI Coding Tool Kostenrechner</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Cursor sagt $20/Monat. Ihre Rechnung zeigt $180. Finden Sie Ihre wahren Kosten nach Nutzungsintensitaet.</p>
      <a href="/de/ki-coding-tool-kosten.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">💻 Rechner oeffnen →</a>
    </div>
  </section>

  <!-- PANEL 12: Auth-Anbieter -->
  <section class="panel" id="auth" role="tabpanel">
    <div class="panel-head">
      <h2>Auth-Anbieter Kostenrechner</h2>
      <p class="pdesc">Clerk vs Auth0 vs Supabase — 73-facher Preisunterschied bei 100K Nutzern. Keyword: <em>Auth Anbieter Kostenrechner</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Berechnen Sie Ihre Authentifizierungskosten nach monatlich aktiven Nutzern. Supabase Auth ist 73x guenstiger als Clerk bei 100K MAU.</p>
      <a href="/de/auth-anbieter-kosten.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">🔑 Rechner oeffnen →</a>
    </div>
  </section>
''',
        '''<button class="tab" data-panel="coding" role="tab">💻 KI Coding</button>
    <button class="tab" data-panel="auth" role="tab">🔑 Auth Kosten</button>'''
    ),
    'fr': (
        '''
  <!-- PANEL 11: Outils IA Coding -->
  <section class="panel" id="coding" role="tabpanel">
    <div class="panel-head">
      <h2>Calculateur Cout Outils IA Coding</h2>
      <p class="pdesc">Cursor vs Copilot vs Claude Code: calculez votre vrai cout mensuel. Keyword: <em>calculateur cout outil IA coding</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Cursor annonce 20$/mois. Votre facture affiche 180$. Trouvez votre vrai cout selon votre usage.</p>
      <a href="/fr/cout-outil-ia-coding.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">💻 Ouvrir le calculateur →</a>
    </div>
  </section>

  <!-- PANEL 12: Fournisseur Auth -->
  <section class="panel" id="auth" role="tabpanel">
    <div class="panel-head">
      <h2>Calculateur Cout Fournisseur Auth</h2>
      <p class="pdesc">Clerk vs Auth0 vs Supabase — 73x d'ecart de prix a 100K utilisateurs. Keyword: <em>calculateur cout fournisseur auth</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Calculez votre cout d'authentification par MAU. Supabase Auth est 73x moins cher que Clerk a 100K MAU.</p>
      <a href="/fr/cout-fournisseur-auth.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">🔑 Ouvrir le calculateur →</a>
    </div>
  </section>
''',
        '''<button class="tab" data-panel="coding" role="tab">💻 Outils IA</button>
    <button class="tab" data-panel="auth" role="tab">🔑 Cout Auth</button>'''
    ),
    'tr': (
        '''
  <!-- PANEL 11: YZ Kodlama Araci -->
  <section class="panel" id="coding" role="tabpanel">
    <div class="panel-head">
      <h2>YZ Kodlama Araci Maliyet Hesaplayici</h2>
      <p class="pdesc">Cursor vs Copilot vs Claude Code: gercek aylik maliyetinizi hesaplayin. Keyword: <em>YZ kodlama araci maliyet hesaplayici</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Cursor $20/ay diyor. Faturaniz $180 gosteriyor. Kullanim yogunlugunuza gore gercek maliyetinizi bulun.</p>
      <a href="/tr/yapay-zeka-kodlama-arac-maliyeti.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">💻 Hesaplayiciyi Ac →</a>
    </div>
  </section>

  <!-- PANEL 12: Kimlik Dogrulama -->
  <section class="panel" id="auth" role="tabpanel">
    <div class="panel-head">
      <h2>Kimlik Dogrulama Maliyet Hesaplayici</h2>
      <p class="pdesc">Clerk vs Auth0 vs Supabase — 100K kullanicida $1.800 vs $25/ay farki. Keyword: <em>kimlik dogrulama maliyet hesaplayici</em>.</p>
    </div>
    <div class="panel-body" style="display:block;padding:20px 28px">
      <p style="color:var(--muted);font-size:15px;margin-bottom:16px">MAU bazli kimlik dogrulama maliyetinizi hesaplayin. Supabase Auth, 100K MAU'da Clerk'ten 73 kat ucuz.</p>
      <a href="/tr/kimlik-dogrulama-maliyet.html" style="display:inline-flex;align-items:center;gap:8px;background:var(--lime);color:#06210a;font-weight:700;padding:12px 20px;border-radius:10px;font-size:15px;text-decoration:none">🔑 Hesaplayiciyi Ac →</a>
    </div>
  </section>
''',
        '''<button class="tab" data-panel="coding" role="tab">💻 YZ Kodlama</button>
    <button class="tab" data-panel="auth" role="tab">🔑 Auth Maliyet</button>'''
    ),
}

PATHS = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, (panel_html, tab_html) in NEW_PANELS.items():
    path = PATHS[lang]
    c = read(path)

    if 'data-panel="coding"' in c:
        print(f'  SKIP {lang} (already added)')
        continue

    # Inject panels before </main> or before newsletter section
    injected = False
    for anchor in ['</main>', '<section class="newsletter', '<div class="newsletter']:
        if anchor in c:
            c = c.replace(anchor, panel_html + '\n' + anchor, 1)
            injected = True
            break

    if not injected:
        print(f'  WARN {lang}: no main/newsletter anchor found')
        continue

    # Inject tabs — find last tab button and add after
    # Look for the last </button> in tab row
    tab_area_match = re.search(r'(<div[^>]+class="tabs"[^>]*>)(.*?)(</div>)', c, re.DOTALL)
    if tab_area_match:
        tabs_content = tab_area_match.group(2)
        new_tabs = tabs_content.rstrip() + '\n    ' + tab_html + '\n  '
        c = c[:tab_area_match.start(2)] + new_tabs + c[tab_area_match.end(2):]

    write(path, c)
    print(f'✓ {lang}: homepage updated with 2 new tool panels')

print('\nHomepage updates done.')
