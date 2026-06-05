#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# ─────────────────────────────────────────────────────────────────────────────
# Per-language panel content
# ─────────────────────────────────────────────────────────────────────────────
PANELS = {
    'en': {
        'coding_head': 'AI Coding Tool Cost Calculator',
        'coding_desc': 'Compare real monthly costs for Cursor, GitHub Copilot, Claude Code &amp; Windsurf based on your usage.',
        'coding_pdesc': 'Compare real monthly costs for Cursor, Copilot, Claude Code &amp; Windsurf. Keyword: <em>ai coding tool cost calculator</em>.',
        'usage_label': 'Daily usage intensity',
        'usage_opts': [('light','Light (1-2h/day)'),('medium','Medium (2-4h/day) ← selected'),('heavy','Heavy (4h+/day, agents)')],
        'type_label': 'Primary use case',
        'type_opts': [('complete','Code completion only'),('chat','Completion + chat'),('agent','Agentic tasks'),('all','All combined')],
        'team_label': 'Team size',
        'team_opts': [('1','Individual (1)'),('3','Small team (3)'),('5','Small team (5)'),('10','Medium (10)'),('20','Medium (20)')],
        'result_label': 'Cheapest option',
        'per_text': '— per month',
        'breakdown_label': 'All tools (sorted)',
        'link_text': 'Full calculator &amp; comparison →',
        'link_url': '/ai-coding-tool-cost.html',
        'coding_aff': '<p class="aff-headline">Best value AI coding tools:</p><div class="aff-links"><a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">🐙 GitHub Copilot — $10/mo</a><a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">🌊 Windsurf — Try free</a></div>',

        'auth_head': 'Authentication Provider Cost Calculator',
        'auth_desc': 'Compare Clerk vs Auth0 vs Supabase Auth by monthly active users. At 100K MAU the difference is $1,825 vs $25.',
        'auth_pdesc': 'Clerk vs Auth0 vs Supabase Auth — 73x price difference at 100K MAU. Keyword: <em>auth provider cost calculator</em>.',
        'mau_label': 'Monthly Active Users (MAU)',
        'tier_label': 'Feature requirements',
        'tier_opts': [('basic','Basic (email + social login)'),('mid','Standard (MFA + orgs)'),('enterprise','Enterprise (SSO + SAML)')],
        'auth_result_label': 'Cheapest option',
        'auth_per': '— per month',
        'auth_breakdown': 'All providers (sorted)',
        'auth_link': 'Full calculator &amp; comparison →',
        'auth_link_url': '/auth-provider-cost.html',
        'auth_aff': '<p class="aff-headline">Start with auth included:</p><div class="aff-links"><a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">⚡ Supabase — 50K MAU free</a><a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">🔐 Clerk — 10K MAU free</a></div>',
    },
    'de': {
        'coding_head': 'KI Coding Tool Kostenrechner',
        'coding_desc': 'Echte Monatskosten fuer Cursor, GitHub Copilot, Claude Code &amp; Windsurf vergleichen.',
        'coding_pdesc': 'Cursor vs Copilot vs Claude Code echte Monatskosten. Keyword: <em>KI Coding Tool Kostenrechner</em>.',
        'usage_label': 'Taegl. Nutzungsintensitaet',
        'usage_opts': [('light','Leicht (1-2h/Tag)'),('medium','Mittel (2-4h/Tag)'),('heavy','Intensiv (4h+/Tag)')],
        'type_label': 'Hauptanwendungsfall',
        'type_opts': [('complete','Nur Vervollstaendigung'),('chat','Vervollstaendigung + Chat'),('agent','Agentenaufgaben'),('all','Alles kombiniert')],
        'team_label': 'Teamgroesse',
        'team_opts': [('1','Einzelperson (1)'),('3','Kleines Team (3)'),('5','Kleines Team (5)'),('10','Mittleres Team (10)'),('20','Mittleres Team (20)')],
        'result_label': 'Guenstigste Option',
        'per_text': '— pro Monat',
        'breakdown_label': 'Alle Tools (sortiert)',
        'link_text': 'Vollstaendiger Rechner →',
        'link_url': '/de/ki-coding-tool-kosten.html',
        'coding_aff': '<p class="aff-headline">Bester Einstieg:</p><div class="aff-links"><a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">GitHub Copilot — $10/Mo</a><a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">Windsurf kostenlos</a></div>',

        'auth_head': 'Auth-Anbieter Kostenrechner',
        'auth_desc': 'Clerk vs Auth0 vs Supabase Auth nach monatlich aktiven Nutzern vergleichen.',
        'auth_pdesc': 'Clerk vs Auth0 vs Supabase — 73x Preisunterschied bei 100K MAU. Keyword: <em>Auth Anbieter Kostenrechner</em>.',
        'mau_label': 'Monatlich aktive Nutzer (MAU)',
        'tier_label': 'Funktionsanforderungen',
        'tier_opts': [('basic','Basis (E-Mail + Social)'),('mid','Standard (MFA + Org)'),('enterprise','Enterprise (SSO + SAML)')],
        'auth_result_label': 'Guenstigste Option',
        'auth_per': '— pro Monat',
        'auth_breakdown': 'Alle Anbieter (sortiert)',
        'auth_link': 'Vollstaendiger Rechner →',
        'auth_link_url': '/de/auth-anbieter-kosten.html',
        'auth_aff': '<p class="aff-headline">Jetzt starten:</p><div class="aff-links"><a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU kostenlos</a><a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU kostenlos</a></div>',
    },
    'fr': {
        'coding_head': 'Calculateur Cout Outils IA Coding',
        'coding_desc': 'Comparez les vrais couts mensuels de Cursor, GitHub Copilot, Claude Code &amp; Windsurf.',
        'coding_pdesc': 'Cursor vs Copilot vs Claude Code couts reels. Keyword: <em>calculateur cout outil IA coding</em>.',
        'usage_label': "Intensite d'utilisation quotidienne",
        'usage_opts': [('light','Legere (1-2h/jour)'),('medium','Moderee (2-4h/jour)'),('heavy','Intensive (4h+/jour)')],
        'type_label': "Cas d'usage principal",
        'type_opts': [('complete','Completion uniquement'),('chat','Completion + chat'),('agent','Taches agentiques'),('all','Tout combine')],
        'team_label': "Taille de l'equipe",
        'team_opts': [('1','Individuel (1)'),('3','Petite equipe (3)'),('5','Petite equipe (5)'),('10','Equipe moyenne (10)'),('20','Equipe moyenne (20)')],
        'result_label': 'Option la moins chere',
        'per_text': '— par mois',
        'breakdown_label': 'Tous les outils (tries)',
        'link_text': 'Calculateur complet →',
        'link_url': '/fr/cout-outil-ia-coding.html',
        'coding_aff': '<p class="aff-headline">Meilleure option:</p><div class="aff-links"><a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">GitHub Copilot — 10$/mois</a><a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">Windsurf gratuit</a></div>',

        'auth_head': "Calculateur Cout Fournisseur Auth",
        'auth_desc': 'Comparez Clerk vs Auth0 vs Supabase Auth par MAU. A 100K MAU: 1 825$ vs 25$.',
        'auth_pdesc': 'Clerk vs Auth0 vs Supabase — 73x d\'ecart a 100K MAU. Keyword: <em>calculateur cout fournisseur auth</em>.',
        'mau_label': 'Utilisateurs actifs mensuels (MAU)',
        'tier_label': 'Niveau de fonctionnalites',
        'tier_opts': [('basic','Basique (email + social)'),('mid','Standard (MFA + orgs)'),('enterprise','Entreprise (SSO + SAML)')],
        'auth_result_label': 'Option la moins chere',
        'auth_per': '— par mois',
        'auth_breakdown': 'Tous les fournisseurs (tries)',
        'auth_link': 'Calculateur complet →',
        'auth_link_url': '/fr/cout-fournisseur-auth.html',
        'auth_aff': '<p class="aff-headline">Commencer avec auth incluse:</p><div class="aff-links"><a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU gratuits</a><a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU gratuits</a></div>',
    },
    'tr': {
        'coding_head': 'YZ Kodlama Araci Maliyet Hesaplayici',
        'coding_desc': 'Cursor, GitHub Copilot, Claude Code ve Windsurf icin gercek aylik maliyetleri karsilastirin.',
        'coding_pdesc': 'Cursor vs Copilot vs Claude Code gercek maliyet. Keyword: <em>YZ kodlama araci maliyet hesaplayici</em>.',
        'usage_label': 'Gunluk kullanim yogunlugu',
        'usage_opts': [('light','Hafif (1-2 saat/gun)'),('medium','Orta (2-4 saat/gun)'),('heavy','Yogun (4+ saat/gun)')],
        'type_label': 'Kullanim tipi',
        'type_opts': [('complete','Sadece tamamlama'),('chat','Tamamlama + chat'),('agent','Ajan gorevleri'),('all','Hepsi')],
        'team_label': 'Ekip buyuklugu',
        'team_opts': [('1','Bireysel (1)'),('3','Kucuk ekip (3)'),('5','Kucuk ekip (5)'),('10','Orta ekip (10)'),('20','Orta ekip (20)')],
        'result_label': 'En ucuz secenek',
        'per_text': '— aylik',
        'breakdown_label': 'Tum araclar (sirali)',
        'link_text': 'Tam hesaplayici →',
        'link_url': '/tr/yapay-zeka-kodlama-arac-maliyeti.html',
        'coding_aff': '<p class="aff-headline">En iyi baslangiç:</p><div class="aff-links"><a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">GitHub Copilot — $10/ay</a><a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">Windsurf ucretsiz</a></div>',

        'auth_head': 'Kimlik Dogrulama Maliyet Hesaplayici',
        'auth_desc': 'Clerk vs Auth0 vs Supabase Auth MAU bazli karsilastirin. 100K MAU: $1.825 vs $25.',
        'auth_pdesc': 'Clerk vs Auth0 vs Supabase — 100K MAU\'da 73x fiyat farki. Keyword: <em>kimlik dogrulama maliyet hesaplayici</em>.',
        'mau_label': 'Aylik Aktif Kullanici (MAU)',
        'tier_label': 'Ozellik gereksinimleri',
        'tier_opts': [('basic','Temel (e-posta + sosyal)'),('mid','Standart (MFA + org)'),('enterprise','Kurumsal (SSO + SAML)')],
        'auth_result_label': 'En ucuz secenek',
        'auth_per': '— aylik',
        'auth_breakdown': 'Tum saglayicilar (sirali)',
        'auth_link': 'Tam hesaplayici →',
        'auth_link_url': '/tr/kimlik-dogrulama-maliyet.html',
        'auth_aff': '<p class="aff-headline">Auth dahil baslayın:</p><div class="aff-links"><a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU ucretsiz</a><a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU ucretsiz</a></div>',
    },
}

def make_usage_opts(opts):
    out = []
    for i, (val, label) in enumerate(opts):
        sel = ' selected' if i == 1 else ''
        out.append(f'<option value="{val}"{sel}>{label}</option>')
    return '\n          '.join(out)

def make_select_opts(opts):
    out = []
    for i, (val, label) in enumerate(opts):
        sel = ' selected' if i == 1 else ''
        out.append(f'<option value="{val}"{sel}>{label}</option>')
    return '\n          '.join(out)

def make_team_opts(opts):
    out = []
    for i, (val, label) in enumerate(opts):
        sel = ' selected' if i == 0 else ''
        out.append(f'<option value="{val}"{sel}>{label}</option>')
    return '\n          '.join(out)

def make_tier_opts(opts):
    out = []
    for i, (val, label) in enumerate(opts):
        sel = ' selected' if i == 1 else ''
        out.append(f'<option value="{val}"{sel}>{label}</option>')
    return '\n          '.join(out)

def coding_panel(lang, p, suffix=''):
    # suffix for uniqueness across lang homepages — all share same DOM so use lang prefix
    pid = f'coding{suffix}'
    return f'''  <!-- PANEL 11: AI Coding Tool -->
  <section class="panel" id="{pid}" role="tabpanel">
    <div class="panel-head">
      <h2>{p['coding_head']}</h2>
      <p class="pdesc">{p['coding_pdesc']}</p>
    </div>
    <div class="grid2">
      <div>
        <div class="field">
          <label for="{lang}CodingUsage">{p['usage_label']}</label>
          <select class="sel" id="{lang}CodingUsage">
          {make_usage_opts(p['usage_opts'])}
          </select>
        </div>
        <div class="field">
          <label for="{lang}CodingType">{p['type_label']}</label>
          <select class="sel" id="{lang}CodingType">
          {make_select_opts(p['type_opts'])}
          </select>
        </div>
        <div class="field">
          <label for="{lang}CodingTeam">{p['team_label']}</label>
          <select class="sel" id="{lang}CodingTeam">
          {make_team_opts(p['team_opts'])}
          </select>
        </div>
      </div>
      <div class="result">
        <div class="rlabel">{p['result_label']}</div>
        <div class="big" id="{lang}CodingBest">$10</div>
        <div class="per" id="{lang}CodingPer">{p['per_text']}</div>
        <div class="breakdown" id="{lang}CodingBreakdown">
          <div class="brow"><span>{p['breakdown_label']}</span><b>—</b></div>
        </div>
        <a href="{p['link_url']}" style="display:inline-block;margin-top:14px;font-size:12px;color:var(--lime);font-family:'Cascadia Code','Consolas',monospace">{p['link_text']}</a>
      </div>
    </div>
  <div class="affiliate-cta" id="{lang}-coding-affiliate">
  {p['coding_aff']}
  </div>
  </section>'''

def auth_panel(lang, p, suffix=''):
    pid = f'auth{suffix}'
    return f'''  <!-- PANEL 12: Auth Provider -->
  <section class="panel" id="{pid}" role="tabpanel">
    <div class="panel-head">
      <h2>{p['auth_head']}</h2>
      <p class="pdesc">{p['auth_pdesc']}</p>
    </div>
    <div class="grid2">
      <div>
        <div class="field">
          <label for="{lang}AuthMau">{p['mau_label']}</label>
          <input class="inp" id="{lang}AuthMau" type="number" value="10000" min="0" step="1000">
        </div>
        <div class="field">
          <label for="{lang}AuthTier">{p['tier_label']}</label>
          <select class="sel" id="{lang}AuthTier">
          {make_tier_opts(p['tier_opts'])}
          </select>
        </div>
      </div>
      <div class="result">
        <div class="rlabel">{p['auth_result_label']}</div>
        <div class="big" id="{lang}AuthBest">$0</div>
        <div class="per" id="{lang}AuthPer">{p['auth_per']}</div>
        <div class="breakdown" id="{lang}AuthBreakdown">
          <div class="brow"><span>{p['auth_breakdown']}</span><b>—</b></div>
        </div>
        <a href="{p['auth_link_url']}" style="display:inline-block;margin-top:14px;font-size:12px;color:var(--lime);font-family:'Cascadia Code','Consolas',monospace">{p['auth_link']}</a>
      </div>
    </div>
  <div class="affiliate-cta" id="{lang}-auth-affiliate">
  {p['auth_aff']}
  </div>
  </section>'''

def coding_js(lang):
    return f'''
/* ===== {lang.upper()} AI CODING CALC ===== */
(function(){{
  var TOOLS_{lang} = [
    {{name:'GitHub Copilot', light:10,  medium:10,  heavy:19,  note:'Predictable'}},
    {{name:'Windsurf',       light:15,  medium:15,  heavy:45,  note:'Credit-based'}},
    {{name:'Cursor',         light:20,  medium:20,  heavy:80,  note:'$20-200/mo'}},
    {{name:'Claude Code',    light:20,  medium:20,  heavy:120, note:'$20-200/mo'}},
    {{name:'Tabnine',        light:12,  medium:12,  heavy:12,  note:'No overages'}}
  ];
  function calcCoding_{lang}(){{
    var usage=document.getElementById('{lang}CodingUsage').value;
    var type=document.getElementById('{lang}CodingType').value;
    var team=parseInt(document.getElementById('{lang}CodingTeam').value)||1;
    var mult=type==='agent'?2.5:type==='all'?3:type==='chat'?1.2:1;
    var rows=TOOLS_{lang}.map(function(t){{
      var base=usage==='light'?t.light:usage==='medium'?t.medium:t.heavy;
      if(usage==='heavy'&&(t.name==='Cursor'||t.name==='Claude Code')) base=Math.min(base*mult,200);
      return {{name:t.name,note:t.note,per:base,total:base*team}};
    }}).sort(function(a,b){{return a.total-b.total;}});
    document.getElementById('{lang}CodingBest').textContent='$'+rows[0].total.toLocaleString();
    var bd=document.getElementById('{lang}CodingBreakdown');
    bd.innerHTML=rows.map(function(r,i){{
      return '<div class="brow'+(i===0?' hl':'')+'">'
        +'<span>'+r.name+'</span>'
        +'<b>$'+r.total.toLocaleString()+'/mo'+(team>1?' ($'+r.per+'/seat)':'')+'</b>'
        +'</div>';
    }}).join('');
  }}
  ['{lang}CodingUsage','{lang}CodingType','{lang}CodingTeam'].forEach(function(id){{
    var el=document.getElementById(id);
    if(el)el.addEventListener('change',calcCoding_{lang});
  }});
  calcCoding_{lang}();
}})();
'''

def auth_js(lang):
    return f'''
/* ===== {lang.upper()} AUTH CALC ===== */
(function(){{
  var PROVIDERS_{lang}=[
    {{name:'Supabase Auth', free:50000, rate:0.00325}},
    {{name:'WorkOS',        free:1000000,rate:0.001}},
    {{name:'Firebase Auth', free:50000, rate:0.0055}},
    {{name:'Better Auth',   free:10000, rate:0.01}},
    {{name:'Clerk',         free:10000, rate:0.02}},
    {{name:'Auth0 (Okta)',  free:7500,  rate:0.07}}
  ];
  function calcAuth_{lang}(){{
    var mau=parseInt(document.getElementById('{lang}AuthMau').value)||0;
    var tier=document.getElementById('{lang}AuthTier').value;
    var sso=tier==='enterprise'?130:0;
    var rows=PROVIDERS_{lang}.map(function(p){{
      var cost=Math.max(0,mau-p.free)*p.rate+sso;
      return {{name:p.name,cost:Math.round(cost*100)/100}};
    }}).sort(function(a,b){{return a.cost-b.cost;}});
    document.getElementById('{lang}AuthBest').textContent='$'+rows[0].cost.toLocaleString('en-US',{{maximumFractionDigits:0}});
    var bd=document.getElementById('{lang}AuthBreakdown');
    bd.innerHTML=rows.map(function(r,i){{
      return '<div class="brow'+(i===0?' hl':'')+'">'
        +'<span>'+r.name+'</span>'
        +'<b>$'+r.cost.toLocaleString('en-US',{{maximumFractionDigits:0}})+'/mo</b>'
        +'</div>';
    }}).join('');
  }}
  ['{lang}AuthMau','{lang}AuthTier'].forEach(function(id){{
    var el=document.getElementById(id);
    if(el){{el.addEventListener('input',calcAuth_{lang});el.addEventListener('change',calcAuth_{lang});}}
  }});
  calcAuth_{lang}();
}})();
'''

# ─────────────────────────────────────────────────────────────────────────────
# Apply to each homepage
# ─────────────────────────────────────────────────────────────────────────────
LANG_PATHS = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in LANG_PATHS.items():
    c = read(path)
    p = PANELS[lang]

    # Build replacement panels
    new_coding = coding_panel(lang, p)
    new_auth   = auth_panel(lang, p)

    # Replace existing placeholder panels using regex
    # Match: <!-- PANEL 11 ... --> <section ...id="coding"...>...</section>
    c = re.sub(
        r'  <!-- PANEL 11.*?</section>',
        new_coding,
        c, flags=re.DOTALL
    )
    c = re.sub(
        r'  <!-- PANEL 12.*?</section>',
        new_auth,
        c, flags=re.DOTALL
    )

    # Inject JS before </script> at end
    new_js = coding_js(lang) + auth_js(lang)
    c = c.replace('</script>\n</body>', new_js + '\n</script>\n</body>', 1)

    write(path, c)
    print(f'✓ {lang}: inline panels + JS added')

print('\nDone.')
