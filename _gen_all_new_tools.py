#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate DE/FR/TR AI coding calc + all Auth calc pages (EN/DE/FR/TR)"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def write(path, c):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

CSS = """:root{--bg:#0a0c10;--bg2:#0c0f15;--surface:#12161d;--surface2:#161b24;--border:#1d2530;--border2:#27313e;--text:#e8edf1;--muted:#8b97a4;--lime:#b8ff2e;--cyan:#4dd6ff;--amber:#ffb24d;--shadow:0 24px 60px -20px rgba(0,0,0,.7)}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;z-index:-2;background:radial-gradient(800px 400px at 75% -5%,rgba(184,255,46,.07),transparent 60%)}
a{color:inherit;text-decoration:none}.wrap{max-width:1100px;margin:0 auto;padding:0 22px}
header.nav{position:sticky;top:0;z-index:50;backdrop-filter:blur(14px);background:rgba(10,12,16,.72);border-bottom:1px solid var(--border)}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:18px;color:var(--text)}.logo b{color:var(--lime)}
.nav-r{display:flex;gap:22px}.nav-r a{color:var(--muted);font-size:14px;font-weight:500;transition:color .18s}.nav-r a:hover{color:var(--text)}
.hero{padding:58px 0 30px;text-align:center}
.chip{display:inline-flex;align-items:center;gap:8px;font-family:'Cascadia Code','Consolas',monospace;font-size:11px;color:var(--muted);border:1px solid var(--border2);background:var(--surface);padding:6px 14px;border-radius:100px;margin-bottom:18px}
.chip .dot{width:6px;height:6px;border-radius:50%;background:var(--lime);box-shadow:0 0 8px var(--lime);animation:pulse 2s infinite}
@keyframes pulse{50%{opacity:.4}}
h1.ph{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:clamp(26px,5vw,48px);letter-spacing:-.03em;line-height:1.05;margin-bottom:14px}
h1.ph .em{color:var(--lime)}
p.intro{color:var(--muted);font-size:17px;max-width:580px;margin:0 auto 26px}
.calc-shell{background:linear-gradient(180deg,var(--surface),var(--bg2));border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow);overflow:hidden;margin-bottom:48px}
.calc-header{padding:22px 28px 16px;border-bottom:1px solid var(--border)}
.calc-header h2{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:19px;margin-bottom:3px}
.calc-header p{color:var(--muted);font-size:14px}
.calc-body{padding:24px 28px;display:grid;grid-template-columns:1.1fr .9fr;gap:24px}
@media(max-width:720px){.calc-body{grid-template-columns:1fr;padding:18px}}
.field{margin-bottom:15px}.field label{display:block;font-size:13px;font-weight:600;color:var(--muted);margin-bottom:7px}
.inp,.sel{width:100%;background:var(--bg);border:1px solid var(--border2);border-radius:10px;padding:11px 14px;color:var(--text);font-size:15px;font-family:'Cascadia Code','Consolas',monospace;transition:border-color .18s}
.inp:focus,.sel:focus{outline:none;border-color:var(--lime);box-shadow:0 0 0 3px rgba(184,255,46,.12)}
.sel{appearance:none;cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%238b97a4' stroke-width='2'%3E%3Cpath d='M2 4l4 4 4-4'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:36px}
.result-grid{display:flex;flex-direction:column;gap:10px}
.tool-result{background:var(--surface2);border:1px solid var(--border2);border-radius:12px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.tool-result.best{border-color:rgba(184,255,46,.4);background:rgba(184,255,46,.05)}
.tool-result .tname{font-weight:700;font-size:14px}
.tool-result .tprice{font-family:'Cascadia Code','Consolas',monospace;font-size:18px;font-weight:700;color:var(--lime)}
.tool-result .tnote{font-size:11px;color:var(--muted);margin-top:2px}
section.sec{padding:0 0 48px}
section.sec h2{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:clamp(20px,3vw,30px);letter-spacing:-.02em;margin-bottom:6px}
.sh-sub{color:var(--muted);margin-bottom:20px;font-size:15px}
.ptable{width:100%;border-collapse:collapse;font-size:14px;overflow-x:auto;display:block}
.ptable th{text-align:left;font-family:'Cascadia Code','Consolas',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:10px 14px;border-bottom:2px solid var(--border);white-space:nowrap}
.ptable td{padding:11px 14px;border-bottom:1px solid var(--border);color:#cdd6dd}
.ptable tr:hover td{background:rgba(255,255,255,.02)}
.ptable .best td{background:rgba(184,255,46,.04)}.ptable .best td:first-child{border-left:2px solid var(--lime)}
.badge{font-family:'Cascadia Code','Consolas',monospace;font-size:10px;background:var(--lime);color:#06210a;padding:2px 6px;border-radius:4px;margin-left:6px;font-weight:700}
.mono{font-family:'Cascadia Code','Consolas',monospace}
.callout{border-radius:12px;padding:16px 20px;margin:20px 0;border-left:3px solid}.callout p{margin:0;color:#cdd6dd;font-size:14px}
.callout .cl{font-family:'Cascadia Code','Consolas',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;font-weight:700}
.callout.tip{background:rgba(184,255,46,.07);border-color:var(--lime)}.callout.tip .cl{color:var(--lime)}
.callout.warn{background:rgba(255,178,77,.07);border-color:var(--amber)}.callout.warn .cl{color:var(--amber)}
.faq{display:flex;flex-direction:column;gap:10px;margin:18px 0 40px}
.qa{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.qa .q{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 20px;cursor:pointer;font-weight:600;font-size:14.5px}
.qa .q .plus{color:var(--lime);font-size:20px;transition:transform .25s;flex-shrink:0}
.qa.open .q .plus{transform:rotate(45deg)}
.qa .a{max-height:0;overflow:hidden;transition:max-height .3s ease;color:var(--muted);font-size:14px}
.qa .a p{padding:0 20px 16px}
.tool-links{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:16px 0 40px}
.tool-link{display:flex;align-items:center;gap:13px;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:15px 17px;transition:border-color .2s,transform .2s;color:var(--text)}
.tool-link:hover{border-color:var(--border2);transform:translateY(-2px)}
.tool-link .ic{font-size:22px}.tool-link .tl-name{font-weight:700;font-size:14px;margin-bottom:2px}.tool-link .tl-desc{color:var(--muted);font-size:12px}
.aff-box{margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px}
.aff-box p{margin:0 0 .6rem;font-size:.85rem;color:var(--lime);font-weight:600}
.aff-box .btns{display:flex;flex-wrap:wrap;gap:.5rem}
.aff-btn{display:inline-block;padding:.35rem .75rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:6px;color:#e8eaed;text-decoration:none;font-size:.82rem;transition:background .15s}
.aff-btn:hover{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.5);color:var(--lime)}
footer{border-top:1px solid var(--border);padding:26px 0;font-family:'Cascadia Code','Consolas',monospace;font-size:12px;color:var(--muted)}
.foot-in{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
footer a{color:var(--muted)}"""

CODING_JS = """
const TOOLS = {
  copilot:  { name:'GitHub Copilot', light:10,  medium:10,  heavy:19,  note:'Predictable flat pricing' },
  cursor:   { name:'Cursor',         light:20,  medium:20,  heavy:80,  note:'$20-200 depending on usage' },
  claude:   { name:'Claude Code',    light:20,  medium:20,  heavy:120, note:'$20-200 depending on tasks' },
  windsurf: { name:'Windsurf',       light:15,  medium:15,  heavy:45,  note:'Credits deplete on heavy use' },
  tabnine:  { name:'Tabnine',        light:12,  medium:12,  heavy:12,  note:'Fixed price, no overages' }
};
function calc() {
  const usage = document.getElementById('usage').value;
  const type  = document.getElementById('type').value;
  const team  = parseInt(document.getElementById('team').value) || 1;
  let mult = type==='agent'?2.5:type==='all'?3:type==='chat'?1.2:1;
  const rows = Object.entries(TOOLS).map(([k,t]) => {
    let base = usage==='light'?t.light:usage==='medium'?t.medium:t.heavy;
    if(usage==='heavy'&&(k==='cursor'||k==='claude')) base=Math.min(base*mult,200);
    return {name:t.name, per:base, total:base*team, note:t.note};
  }).sort((a,b)=>a.total-b.total);
  document.getElementById('results').innerHTML = rows.map((r,i)=>`
    <div class="tool-result${i===0?' best':''}">
      <div><div class="tname">${r.name}</div><div class="tnote">${r.note}</div></div>
      <div style="text-align:right">
        <div class="tprice">$${r.total.toLocaleString()}/mo</div>
        ${team>1?`<div class="tnote">$${r.per}/seat</div>`:''}
      </div>
    </div>`).join('');
}
document.querySelectorAll('.sel').forEach(el=>el.addEventListener('change',calc));
calc();
document.querySelectorAll('.qa .q').forEach(q=>{
  q.addEventListener('click',()=>{
    const qa=q.parentElement, open=qa.classList.toggle('open');
    const a=qa.querySelector('.a');
    if(a) a.style.maxHeight=open?'300px':'0';
  });
});
"""

AUTH_JS = """
const PROVIDERS = {
  clerk:    { name:'Clerk',        free:10000, rate:0.02,    min_paid:0,    note:'Best DX, pricey at scale' },
  auth0:    { name:'Auth0 (Okta)', free:7500,  rate:0.07,    min_paid:23,   note:'Enterprise grade, complex' },
  supabase: { name:'Supabase Auth',free:50000, rate:0.00325, min_paid:0,    note:'Cheapest at scale' },
  firebase: { name:'Firebase Auth',free:50000, rate:0.0055,  min_paid:0,    note:'Google ecosystem' },
  better:   { name:'Better Auth',  free:10000, rate:0.01,    min_paid:0,    note:'Open source option' },
  workos:   { name:'WorkOS',       free:1000000,rate:0.001,  min_paid:0,    note:'Enterprise SSO focus' }
};
function calc() {
  const mau  = parseInt(document.getElementById('mau').value) || 10000;
  const tier = document.getElementById('tier').value;
  let sso_add = tier==='enterprise' ? 130 : 0;
  const rows = Object.entries(PROVIDERS).map(([k,p])=>{
    const billable = Math.max(0, mau - p.free);
    let cost = billable * p.rate + sso_add;
    if(p.min_paid>0 && billable>0) cost = Math.max(cost, p.min_paid);
    return {name:p.name, cost:Math.round(cost*100)/100, note:p.note};
  }).sort((a,b)=>a.cost-b.cost);
  document.getElementById('results').innerHTML = rows.map((r,i)=>`
    <div class="tool-result${i===0?' best':''}">
      <div><div class="tname">${r.name}</div><div class="tnote">${r.note}</div></div>
      <div style="text-align:right">
        <div class="tprice">$${r.cost.toLocaleString('en-US',{minimumFractionDigits:0,maximumFractionDigits:0})}/mo</div>
      </div>
    </div>`).join('');
}
document.querySelectorAll('.sel,.inp').forEach(el=>el.addEventListener('input',calc));
calc();
document.querySelectorAll('.qa .q').forEach(q=>{
  q.addEventListener('click',()=>{
    const qa=q.parentElement, open=qa.classList.toggle('open');
    const a=qa.querySelector('.a');
    if(a) a.style.maxHeight=open?'300px':'0';
  });
});
"""

# ─────────────────────────────────────────────────────────────────────────────
# AI CODING TOOL — DE
# ─────────────────────────────────────────────────────────────────────────────
coding_de = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>KI Coding Tool Kostenrechner 2026 — Cursor vs Copilot vs Claude Code</title>
<meta name="description" content="Kostenloser Rechner fuer KI-Coding-Tools. Cursor vs GitHub Copilot vs Claude Code vs Windsurf. Finden Sie Ihre tatsaechliche Monatsrechnung.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="DE"/>
<meta name="geo.placename" content="Germany"/>
<link rel="canonical" href="https://apicalculators.com/de/ki-coding-tool-kosten.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/ki-coding-tool-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-outil-ia-coding.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<meta property="og:locale" content="de_DE"/>
<meta property="og:title" content="KI Coding Tool Kostenrechner 2026 — Cursor vs Copilot vs Claude Code">
<meta property="og:url" content="https://apicalculators.com/de/ki-coding-tool-kosten.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Kostet Cursor wirklich nur 20 Dollar im Monat?","acceptedAnswer":{{"@type":"Answer","text":"Cursor Pro beginnt bei $20/Monat, aber bei intensiver Nutzung koennen die Kosten auf $60-200/Monat steigen. Das Pro-Limit wird schnell ueberschritten."}}}},{{"@type":"Question","name":"Welches KI-Coding-Tool ist 2026 am guenstigsten?","acceptedAnswer":{{"@type":"Answer","text":"GitHub Copilot fuer $10/Monat bietet den besten Wert fuer normale Nutzer. Fuer agentenbasierte Aufgaben konkurrieren Claude Code Max ($100/Monat) und Cursor Pro ($20/Monat mit Limits)."}}}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"}},{{"@type":"ListItem","position":2,"name":"KI Coding Tool Kostenrechner 2026"}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/de/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/de/">Rechner</a><a href="/de/blog/">Blog</a><a href="/de/about.html">Ueber uns</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Juni 2026 · Aktuelle Preise</span>
  <h1 class="ph"><span class="em">KI Coding Tool</span> Kostenrechner</h1>
  <p class="intro">Cursor sagt $20/Monat. Die Rechnung zeigt $180. Finden Sie heraus, was Sie wirklich fuer Cursor, GitHub Copilot, Claude Code und Windsurf zahlen.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>💻 KI Coding Tool Kostenrechner</h2><p>Nutzungsmuster waehlen · Ergebnisse aktualisieren sich live</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="usage">Taeglich Nutzungsintensitaet</label>
        <select class="sel" id="usage">
          <option value="light">Leicht (1-2 Stunden/Tag)</option>
          <option value="medium" selected>Mittel (2-4 Stunden/Tag)</option>
          <option value="heavy">Intensiv (4+ Stunden/Tag, Agenten)</option>
        </select></div>
      <div class="field"><label for="type">Hauptanwendungsfall</label>
        <select class="sel" id="type">
          <option value="complete">Nur Code-Vervollstaendigung</option>
          <option value="chat" selected>Vervollstaendigung + Chat</option>
          <option value="agent">Agentenaufgaben</option>
          <option value="all">Alles kombiniert</option>
        </select></div>
      <div class="field"><label for="team">Teamgroesse</label>
        <select class="sel" id="team">
          <option value="1" selected>Einzelperson (1)</option>
          <option value="3">Kleines Team (3)</option>
          <option value="5">Kleines Team (5)</option>
          <option value="10">Mittleres Team (10)</option>
          <option value="20">Mittleres Team (20)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Geschaetzte Monatskosten — guenstigste zuerst</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<div class="callout warn"><div class="cl">Versteckte Kosten</div><p>Cursor Pro ($20) wird automatisch auf Pro+ ($60) oder Ultra ($200) hochgestuft, wenn Sie die Limits erreichen. Claude Code API-Nutzung kann pro intensiver Sitzung $15+ hinzufuegen.</p></div>
<section class="sec">
  <h2>Wahrer Monatspreis: Was die Preisseiten nicht zeigen</h2>
  <p class="sh-sub">Preisangabe vs. tatsaechliche Rechnung bei verschiedenen Nutzungsniveaus.</p>
  <table class="ptable">
    <thead><tr><th>Tool</th><th>Listenpreis</th><th>Leichtnutzer</th><th>Intensivnutzer</th><th>Team von 10</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GitHub Copilot</strong><span class="badge">VORHERSEHBAR</span></td><td class="mono">$10/Mo</td><td class="mono">$10</td><td class="mono">$19</td><td class="mono">$190</td></tr>
      <tr><td><strong>Windsurf</strong></td><td class="mono">$15/Mo</td><td class="mono">$15</td><td class="mono">$30-60</td><td class="mono">$300</td></tr>
      <tr><td><strong>Cursor</strong></td><td class="mono">$20/Mo</td><td class="mono">$20</td><td class="mono">$60-200</td><td class="mono">$400+</td></tr>
      <tr><td><strong>Claude Code</strong></td><td class="mono">$20/Mo</td><td class="mono">$20</td><td class="mono">$100-200</td><td class="mono">$200-1.000</td></tr>
    </tbody>
  </table>
</section>
<div class="aff-box"><p>Bester Einstieg:</p><div class="btns">
  <a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">GitHub Copilot — $10/Mo</a>
  <a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">Windsurf kostenlos testen</a>
</div></div>
<section class="sec"><h2>Haeufig gestellte Fragen</h2><div class="faq">
  <div class="qa"><div class="q">Kostet Cursor wirklich nur 20 Dollar?<span class="plus">+</span></div><div class="a"><p>Cursor Pro beginnt bei $20/Monat, aber bei intensiver Agenten-Nutzung koennen Rechnungen auf $60-200/Monat steigen.</p></div></div>
  <div class="qa"><div class="q">Welches KI-Coding-Tool ist am guenstigsten?<span class="plus">+</span></div><div class="a"><p>GitHub Copilot bei $10/Monat bietet den besten Wert fuer normale Nutzer. Verwenden Sie den Rechner oben fuer Ihren spezifischen Anwendungsfall.</p></div></div>
</div></section>
<section class="sec"><h2>Verwandte Rechner</h2><div class="tool-links">
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Kosten</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/de/auth-anbieter-kosten.html" class="tool-link"><span class="ic">🔑</span><div><div class="tl-name">Auth-Anbieter Kosten</div><div class="tl-desc">Clerk vs Auth0 vs Supabase</div></div></a>
  <a href="/de/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Alle Rechner</div><div class="tl-desc">Zurueck zur Uebersicht</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/de/">APICalculators</a> · Kostenlose Infra-Kostentools</span>
  <span>Preise sind Schaetzungen · vor dem Einsatz pruefen</span>
</div></footer>
<script>{CODING_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'de', 'ki-coding-tool-kosten.html'), coding_de)
print('✓ DE: ki-coding-tool-kosten.html')

# ─────────────────────────────────────────────────────────────────────────────
# AI CODING TOOL — FR
# ─────────────────────────────────────────────────────────────────────────────
coding_fr = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Calculateur Cout Outils IA Coding 2026 — Cursor vs Copilot vs Claude Code</title>
<meta name="description" content="Calculateur gratuit pour comparer les vrais couts des outils IA. Cursor vs GitHub Copilot vs Claude Code vs Windsurf. Trouvez votre facture mensuelle reelle.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="FR"/>
<meta name="geo.placename" content="France"/>
<link rel="canonical" href="https://apicalculators.com/fr/cout-outil-ia-coding.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/ki-coding-tool-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-outil-ia-coding.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<meta property="og:locale" content="fr_FR"/>
<meta property="og:title" content="Calculateur Cout Outils IA Coding 2026 — Cursor vs Copilot vs Claude Code">
<meta property="og:url" content="https://apicalculators.com/fr/cout-outil-ia-coding.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Cursor coute-t-il vraiment 20$ par mois?","acceptedAnswer":{{"@type":"Answer","text":"Cursor Pro commence a 20$/mois, mais une utilisation intensive peut porter la facture a 60-200$/mois selon l'usage agentic."}}}},{{"@type":"Question","name":"Quel outil IA de coding est le moins cher en 2026?","acceptedAnswer":{{"@type":"Answer","text":"GitHub Copilot a 10$/mois offre le meilleur rapport qualite-prix. Pour les taches agentiques, Claude Code Max (100$/mois) et Cursor Pro (20$/mois) sont competitifs."}}}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/fr/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/fr/">Calculateurs</a><a href="/fr/blog/">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Juin 2026 · Prix mis a jour</span>
  <h1 class="ph"><span class="em">Outils IA Coding</span> — Calculateur de Cout</h1>
  <p class="intro">Cursor annonce 20$/mois. Votre facture affiche 180$. Calculez ce que vous paierez vraiment pour Cursor, GitHub Copilot, Claude Code et Windsurf selon votre usage reel.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>💻 Calculateur Cout Outils IA Coding</h2><p>Selectionnez votre profil d'utilisation · Resultats en temps reel</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="usage">Intensite d'utilisation quotidienne</label>
        <select class="sel" id="usage">
          <option value="light">Legere (1-2h/jour)</option>
          <option value="medium" selected>Moderee (2-4h/jour)</option>
          <option value="heavy">Intensive (4h+/jour, agents)</option>
        </select></div>
      <div class="field"><label for="type">Cas d'usage principal</label>
        <select class="sel" id="type">
          <option value="complete">Completion de code uniquement</option>
          <option value="chat" selected>Completion + chat</option>
          <option value="agent">Taches agentiques</option>
          <option value="all">Tout combine</option>
        </select></div>
      <div class="field"><label for="team">Taille de l'equipe</label>
        <select class="sel" id="team">
          <option value="1" selected>Individuel (1 personne)</option>
          <option value="3">Petite equipe (3)</option>
          <option value="5">Petite equipe (5)</option>
          <option value="10">Equipe moyenne (10)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Cout mensuel estime — du moins cher au plus cher</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<div class="callout warn"><div class="cl">Couts caches</div><p>Cursor Pro ($20) passe automatiquement en Pro+ ($60) ou Ultra ($200) quand vous atteignez les limites. L'usage API de Claude Code peut ajouter $15+ par session intensive.</p></div>
<section class="sec">
  <h2>Vrai cout mensuel: ce que les pages de tarifs ne montrent pas</h2>
  <p class="sh-sub">Prix affiche vs facture reelle selon le niveau d'utilisation.</p>
  <table class="ptable">
    <thead><tr><th>Outil</th><th>Prix affiche</th><th>Usage leger</th><th>Usage intensif</th><th>Equipe de 10</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GitHub Copilot</strong><span class="badge">PREVISIBLE</span></td><td class="mono">$10/mois</td><td class="mono">$10</td><td class="mono">$19</td><td class="mono">$190</td></tr>
      <tr><td><strong>Windsurf</strong></td><td class="mono">$15/mois</td><td class="mono">$15</td><td class="mono">$30-60</td><td class="mono">$300</td></tr>
      <tr><td><strong>Cursor</strong></td><td class="mono">$20/mois</td><td class="mono">$20</td><td class="mono">$60-200</td><td class="mono">$400+</td></tr>
      <tr><td><strong>Claude Code</strong></td><td class="mono">$20/mois</td><td class="mono">$20</td><td class="mono">$100-200</td><td class="mono">$200-1.000</td></tr>
    </tbody>
  </table>
</section>
<div class="aff-box"><p>Commencer avec la meilleure option:</p><div class="btns">
  <a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">GitHub Copilot — $10/mois</a>
  <a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">Essayer Windsurf gratuitement</a>
</div></div>
<section class="sec"><h2>Questions frequentes</h2><div class="faq">
  <div class="qa"><div class="q">Cursor coute-t-il vraiment 20$/mois?<span class="plus">+</span></div><div class="a"><p>Cursor Pro commence a 20$/mois mais une utilisation intensive peut porter la facture a 60-200$/mois.</p></div></div>
  <div class="qa"><div class="q">Quel outil IA de coding est le moins cher?<span class="plus">+</span></div><div class="a"><p>GitHub Copilot a 10$/mois offre le meilleur rapport qualite-prix. Utilisez le calculateur ci-dessus pour votre usage specifique.</p></div></div>
</div></section>
<section class="sec"><h2>Calculateurs associes</h2><div class="tool-links">
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">Cout API LLM</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/fr/cout-fournisseur-auth.html" class="tool-link"><span class="ic">🔑</span><div><div class="tl-name">Cout Auth</div><div class="tl-desc">Clerk vs Auth0 vs Supabase</div></div></a>
  <a href="/fr/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Tous les calculateurs</div><div class="tl-desc">Retour a l'accueil</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/fr/">APICalculators</a> · Outils gratuits</span>
  <span>Prix estimatifs · verifiez avant de deployer</span>
</div></footer>
<script>{CODING_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'fr', 'cout-outil-ia-coding.html'), coding_fr)
print('✓ FR: cout-outil-ia-coding.html')

# ─────────────────────────────────────────────────────────────────────────────
# AI CODING TOOL — TR
# ─────────────────────────────────────────────────────────────────────────────
coding_tr = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>YZ Kodlama Araci Maliyet Hesaplayici 2026 — Cursor vs Copilot vs Claude Code</title>
<meta name="description" content="Yapay zeka kodlama araclarinin gercek maliyetini karsilastirin. Cursor vs GitHub Copilot vs Claude Code vs Windsurf. Ucretsiz, kayit gerekmez.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="TR"/>
<meta name="geo.placename" content="Turkey"/>
<link rel="canonical" href="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/ki-coding-tool-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-outil-ia-coding.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<meta property="og:locale" content="tr_TR"/>
<meta property="og:title" content="YZ Kodlama Araci Maliyet Hesaplayici 2026 — Cursor vs Copilot vs Claude Code">
<meta property="og:url" content="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Cursor gercekten aylik $20 mi?","acceptedAnswer":{{"@type":"Answer","text":"Cursor Pro $20/ay'dan baslar ancak yogun kullanim faturayi $60-200/ay'a cikarabilir."}}}},{{"@type":"Question","name":"2026'da en ucuz YZ kodlama araci hangisi?","acceptedAnswer":{{"@type":"Answer","text":"GitHub Copilot $10/ay ile hafif-orta kullanicilar icin en iyi degeri sunar. Hesaplayiciyi kullanin kendi durumunuzu gorun."}}}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/tr/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/tr/">Hesaplayicilar</a><a href="/tr/blog/">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Haziran 2026 · Guncel Fiyatlar</span>
  <h1 class="ph"><span class="em">YZ Kodlama Araci</span> Maliyet Hesaplayici</h1>
  <p class="intro">Cursor $20/ay diyor. Faturaniz $180 gosterdi. Cursor, GitHub Copilot, Claude Code ve Windsurf icin gercek kullanim patternize gore ne odeyeceginizi hesaplayin.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>💻 YZ Kodlama Araci Maliyet Hesaplayici</h2><p>Kullanim tipini secin · Sonuclar aninda guncellenir</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="usage">Gunluk kullanim yogunlugu</label>
        <select class="sel" id="usage">
          <option value="light">Hafif (1-2 saat/gun)</option>
          <option value="medium" selected>Orta (2-4 saat/gun)</option>
          <option value="heavy">Yogun (4+ saat/gun, ajan)</option>
        </select></div>
      <div class="field"><label for="type">Kullanim tipi</label>
        <select class="sel" id="type">
          <option value="complete">Sadece kod tamamlama</option>
          <option value="chat" selected>Tamamlama + chat</option>
          <option value="agent">Ajan gorevleri</option>
          <option value="all">Hepsi</option>
        </select></div>
      <div class="field"><label for="team">Ekip buyuklugu</label>
        <select class="sel" id="team">
          <option value="1" selected>Bireysel (1 kisi)</option>
          <option value="3">Kucuk ekip (3)</option>
          <option value="5">Kucuk ekip (5)</option>
          <option value="10">Orta ekip (10)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Tahmini aylik maliyet — en ucuzdan pahaliya</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<div class="callout warn"><div class="cl">Gizli Maliyet Uyarisi</div><p>Cursor Pro ($20) limit asiminda otomatik Pro+ ($60) veya Ultra ($200)'e gececer. Claude Code API kullanimi yogun oturumda $15+ ekleyebilir.</p></div>
<section class="sec">
  <h2>Gercek Aylik Maliyet: Fiyat Sayfalarinin Gostermedigini</h2>
  <table class="ptable">
    <thead><tr><th>Arac</th><th>Liste Fiyati</th><th>Hafif Kullanici</th><th>Yogun Kullanici</th><th>10 Kisilik Ekip</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GitHub Copilot</strong><span class="badge">TAHMIN EDILEBILIR</span></td><td class="mono">$10/ay</td><td class="mono">$10</td><td class="mono">$19</td><td class="mono">$190</td></tr>
      <tr><td><strong>Windsurf</strong></td><td class="mono">$15/ay</td><td class="mono">$15</td><td class="mono">$30-60</td><td class="mono">$300</td></tr>
      <tr><td><strong>Cursor</strong></td><td class="mono">$20/ay</td><td class="mono">$20</td><td class="mono">$60-200</td><td class="mono">$400+</td></tr>
      <tr><td><strong>Claude Code</strong></td><td class="mono">$20/ay</td><td class="mono">$20</td><td class="mono">$100-200</td><td class="mono">$200-1.000</td></tr>
    </tbody>
  </table>
</section>
<section class="sec"><h2>Sik Sorulan Sorular</h2><div class="faq">
  <div class="qa"><div class="q">Cursor gercekten $20/ay mi?<span class="plus">+</span></div><div class="a"><p>Cursor Pro $20/ay'dan baslar ancak yogun kullanim faturayi $60-200/ay'a cikarabilir. Pro+ ($60) veya Ultra ($200) kademeye gectigi oluyor.</p></div></div>
  <div class="qa"><div class="q">2026'da en ucuz YZ kodlama araci hangisi?<span class="plus">+</span></div><div class="a"><p>GitHub Copilot $10/ay ile hafif-orta kullanicilar icin en iyi deger. Yukaridaki hesaplayiciyi kullanarak kendi durumunuzu goruntuleyin.</p></div></div>
</div></section>
<section class="sec"><h2>Ilgili Hesaplayicilar</h2><div class="tool-links">
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Maliyeti</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/tr/kimlik-dogrulama-maliyet.html" class="tool-link"><span class="ic">🔑</span><div><div class="tl-name">Auth Maliyet</div><div class="tl-desc">Clerk vs Auth0 vs Supabase</div></div></a>
  <a href="/tr/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Tum Hesaplayicilar</div><div class="tl-desc">Ana sayfaya don</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/tr/">APICalculators</a> · Ucretsiz infra maliyet araclari</span>
  <span>Fiyatlar tahmindir · gonderiminizden once dogrulayin</span>
</div></footer>
<script>{CODING_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'tr', 'yapay-zeka-kodlama-arac-maliyeti.html'), coding_tr)
print('✓ TR: yapay-zeka-kodlama-arac-maliyeti.html')

# ─────────────────────────────────────────────────────────────────────────────
# AUTH PROVIDER — EN
# ─────────────────────────────────────────────────────────────────────────────
auth_faq_schema = '''{
  "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":"Is Clerk free?","acceptedAnswer":{"@type":"Answer","text":"Clerk is free up to 10,000 MAU. After that, it costs $0.02 per MAU. At 100,000 users that is $1,825/month - significantly more than Supabase Auth ($25/month)."}},
    {"@type":"Question","name":"What is the cheapest auth provider in 2026?","acceptedAnswer":{"@type":"Answer","text":"Supabase Auth is the cheapest at scale: 50,000 free MAUs then $0.00325/MAU. At 100K users it costs ~$25/month."}},
    {"@type":"Question","name":"Clerk vs Auth0 - which is better?","acceptedAnswer":{"@type":"Answer","text":"Clerk wins for developer experience and Next.js/React apps. Auth0 wins for enterprise compliance, SAML SSO, and complex B2B requirements."}},
    {"@type":"Question","name":"Does this auth cost calculator include SSO pricing?","acceptedAnswer":{"@type":"Answer","text":"Yes. Select Enterprise feature tier to include SSO/SAML pricing. Auth0 and WorkOS are optimized for enterprise SSO; Clerk charges extra for SSO connections."}}
  ]
}'''

auth_en = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Auth Provider Cost Calculator 2026 — Clerk vs Auth0 vs Supabase Auth</title>
<meta name="description" content="Calculate your true auth costs by MAU. Clerk vs Auth0 vs Supabase Auth vs Firebase. At 100K users the difference is $1,800 vs $25/month. Free, no signup.">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://apicalculators.com/auth-provider-cost.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/auth-provider-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/auth-anbieter-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-fournisseur-auth.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/auth-provider-cost.html"/>
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US"/>
<meta property="og:title" content="Auth Provider Cost Calculator 2026 — Clerk vs Auth0 vs Supabase Auth">
<meta property="og:description" content="At 100K users: Clerk $1,825/mo vs Supabase $25/mo. Calculate yours free.">
<meta property="og:url" content="https://apicalculators.com/auth-provider-cost.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<meta name="twitter:title" content="Auth Provider Cost Calculator 2026 — Clerk vs Auth0 vs Supabase">
<meta name="twitter:description" content="At 100K MAU: Clerk $1,825/mo vs Supabase $25/mo. Find your number.">
<meta name="twitter:image" content="https://apicalculators.com/twitter-image.png">
<script type="application/ld+json">{auth_faq_schema}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Auth Provider Cost Calculator 2026","applicationCategory":"DeveloperApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}},"url":"https://apicalculators.com/auth-provider-cost.html"}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"}},{{"@type":"ListItem","position":2,"name":"Auth Provider Cost Calculator 2026"}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/">Calculators</a><a href="/blog/">Blog</a><a href="/about.html">About</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> June 2026 · Updated Pricing</span>
  <h1 class="ph"><span class="em">Auth Provider</span> Cost Calculator</h1>
  <p class="intro">At 100K monthly active users, Clerk costs $1,825/month and Supabase Auth costs $25/month. Same authentication. 73x price difference. Find your number before you scale.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔑 Authentication Cost Calculator</h2><p>Enter your MAU · Select feature tier · Compare all providers instantly</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="mau">Monthly Active Users (MAU)</label>
        <input class="inp" id="mau" type="number" value="10000" min="0" step="1000"></div>
      <div class="field"><label for="tier">Feature requirements</label>
        <select class="sel" id="tier">
          <option value="basic">Basic (email + social login)</option>
          <option value="mid" selected>Standard (MFA + organizations)</option>
          <option value="enterprise">Enterprise (SSO + SAML + compliance)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Monthly cost — sorted cheapest first</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>

<section class="sec">
  <h2>The $1,800 vs $25 Problem</h2>
  <p class="sh-sub">Same authentication. Wildly different pricing at scale.</p>
  <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Clerk and Supabase Auth both let users sign in with email, Google, and GitHub. Both handle sessions, JWTs, and user management. At 1,000 users they cost the same: $0. At 100,000 users, Clerk charges $1,825/month ($0.02/MAU after 10K free). Supabase charges $25/month ($0.00325/MAU after 50K free).</p>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>Free MAU</th><th>Rate after free</th><th>10K MAU</th><th>50K MAU</th><th>100K MAU</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Supabase Auth</strong><span class="badge">CHEAPEST</span></td><td class="mono">50,000</td><td class="mono">$0.00325</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$25</td></tr>
      <tr><td><strong>WorkOS</strong></td><td class="mono">1,000,000</td><td class="mono">$0.001</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$0</td></tr>
      <tr><td><strong>Firebase Auth</strong></td><td class="mono">50,000</td><td class="mono">$0.0055</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$275</td></tr>
      <tr><td><strong>Clerk</strong></td><td class="mono">10,000</td><td class="mono">$0.02</td><td class="mono">$0</td><td class="mono">$800</td><td class="mono">$1,825</td></tr>
      <tr><td><strong>Auth0 (Okta)</strong></td><td class="mono">7,500</td><td class="mono">$0.07</td><td class="mono">$175</td><td class="mono">$2,975</td><td class="mono">$5,000+</td></tr>
    </tbody>
  </table>
</section>

<section class="sec">
  <h2>When to Choose Each Provider</h2>
  <p class="sh-sub">The cheapest option is not always the right option.</p>
  <div class="callout tip"><div class="cl">Supabase Auth</div><p>Best if you are already using Supabase for your database. Auth is essentially included. No pre-built UI — you build login forms yourself with their SDK.</p></div>
  <div class="callout tip"><div class="cl">Clerk</div><p>Best developer experience. Pre-built React/Next.js components, organizations, multi-session. Worth the cost below 10K MAU (free). Gets expensive fast after that.</p></div>
  <div class="callout tip"><div class="cl">WorkOS</div><p>Best for enterprise B2B. 1M MAU free, then $0.001/MAU. Built for SSO-first products. Overkill for B2C apps.</p></div>
  <div class="callout warn"><div class="cl">Auth0 warning</div><p>Auth0's per-MAU pricing becomes extremely expensive at scale. The 7,500 free MAU limit is the lowest of all providers compared here.</p></div>
</section>

<div class="aff-box"><p>Start building with auth included:</p><div class="btns">
  <a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">⚡ Supabase — 50K MAU free</a>
  <a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">🔐 Clerk — 10K MAU free</a>
</div></div>

<section class="sec"><h2>Frequently Asked Questions</h2><div class="faq">
  <div class="qa"><div class="q">Is Clerk free?<span class="plus">+</span></div><div class="a"><p>Clerk is free up to 10,000 MAU. After that, it costs $0.02 per MAU. At 100,000 users that is $1,825/month — significantly more than alternatives like Supabase Auth ($25/month).</p></div></div>
  <div class="qa"><div class="q">What is the cheapest auth provider in 2026?<span class="plus">+</span></div><div class="a"><p>Supabase Auth is the cheapest at scale: 50,000 free MAUs then $0.00325/MAU. At 100K users it costs ~$25/month. If you are already using Supabase for your database, auth is essentially free.</p></div></div>
  <div class="qa"><div class="q">Clerk vs Auth0 — which is better?<span class="plus">+</span></div><div class="a"><p>Clerk wins for developer experience and Next.js/React apps. Auth0 wins for enterprise compliance, SAML SSO, and complex B2B requirements. For most indie developers and startups, Clerk or Supabase Auth is the better choice.</p></div></div>
  <div class="qa"><div class="q">Does this auth cost calculator include SSO pricing?<span class="plus">+</span></div><div class="a"><p>Yes. Select Enterprise feature tier in the calculator to include SSO/SAML pricing. Auth0 and WorkOS are optimized for enterprise SSO; Clerk charges extra for SSO connections.</p></div></div>
</div></section>

<section class="sec"><h2>Related Calculators</h2><div class="tool-links">
  <a href="/ai-coding-tool-cost.html" class="tool-link"><span class="ic">💻</span><div><div class="tl-name">AI Coding Tool Cost</div><div class="tl-desc">Cursor vs Copilot vs Claude Code</div></div></a>
  <a href="/vector-db-cost.html" class="tool-link"><span class="ic">🗄️</span><div><div class="tl-name">Vector DB Cost</div><div class="tl-desc">Pinecone vs Supabase vs Qdrant</div></div></a>
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Cost</div><div class="tl-desc">GPT-4o, Claude, Gemini pricing</div></div></a>
  <a href="/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">All Calculators</div><div class="tl-desc">12 free infra cost tools</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/">APICalculators</a> · Free infra cost tools</span>
  <span>Prices are estimates · verify before you ship</span>
</div></footer>
<script>{AUTH_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'auth-provider-cost.html'), auth_en)
print('✓ EN: auth-provider-cost.html')

# ─────────────────────────────────────────────────────────────────────────────
# AUTH PROVIDER — DE
# ─────────────────────────────────────────────────────────────────────────────
auth_de = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Auth-Anbieter Kostenrechner 2026 — Clerk vs Auth0 vs Supabase</title>
<meta name="description" content="Berechnen Sie Ihre Auth-Kosten nach MAU. Bei 100K Nutzern: Clerk $1.800/Monat vs Supabase $25/Monat. Kostenlos, keine Anmeldung.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="DE"/>
<meta name="geo.placename" content="Germany"/>
<link rel="canonical" href="https://apicalculators.com/de/auth-anbieter-kosten.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/auth-provider-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/auth-anbieter-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-fournisseur-auth.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/auth-provider-cost.html"/>
<meta property="og:locale" content="de_DE"/>
<meta property="og:title" content="Auth-Anbieter Kostenrechner 2026 — Clerk vs Auth0 vs Supabase">
<meta property="og:url" content="https://apicalculators.com/de/auth-anbieter-kosten.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Ist Clerk kostenlos?","acceptedAnswer":{{"@type":"Answer","text":"Clerk ist bis zu 10.000 MAU kostenlos. Danach kostet es $0,02 pro MAU. Bei 100.000 Nutzern sind das $1.825/Monat."}}}},{{"@type":"Question","name":"Welcher Auth-Anbieter ist 2026 am guenstigsten?","acceptedAnswer":{{"@type":"Answer","text":"Supabase Auth ist bei Skalierung am guenstigsten: 50.000 kostenlose MAUs, dann $0,00325/MAU. Bei 100K Nutzern kostet es ca. $25/Monat."}}}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/de/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/de/">Rechner</a><a href="/de/blog/">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Juni 2026 · Aktuelle Preise</span>
  <h1 class="ph"><span class="em">Auth-Anbieter</span> Kostenrechner</h1>
  <p class="intro">Bei 100K monatlich aktiven Nutzern kostet Clerk $1.825/Monat und Supabase Auth $25/Monat. Gleiche Authentifizierung. 73-facher Preisunterschied. Finden Sie Ihre Zahl.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔑 Authentifizierungs-Kostenrechner</h2><p>MAU eingeben · Funktionsstufe waehlen · Alle Anbieter sofort vergleichen</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="mau">Monatlich aktive Nutzer (MAU)</label>
        <input class="inp" id="mau" type="number" value="10000" min="0" step="1000"></div>
      <div class="field"><label for="tier">Funktionsanforderungen</label>
        <select class="sel" id="tier">
          <option value="basic">Basis (E-Mail + Social Login)</option>
          <option value="mid" selected>Standard (MFA + Organisationen)</option>
          <option value="enterprise">Enterprise (SSO + SAML + Compliance)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Monatliche Kosten — guenstigste zuerst</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<section class="sec">
  <h2>Das $1.800 vs $25 Problem</h2>
  <table class="ptable">
    <thead><tr><th>Anbieter</th><th>Kostenlose MAU</th><th>Rate danach</th><th>10K MAU</th><th>50K MAU</th><th>100K MAU</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Supabase Auth</strong><span class="badge">GUENSTIGSTE</span></td><td class="mono">50.000</td><td class="mono">$0,00325</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$25</td></tr>
      <tr><td><strong>Firebase Auth</strong></td><td class="mono">50.000</td><td class="mono">$0,0055</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$275</td></tr>
      <tr><td><strong>Clerk</strong></td><td class="mono">10.000</td><td class="mono">$0,02</td><td class="mono">$0</td><td class="mono">$800</td><td class="mono">$1.825</td></tr>
      <tr><td><strong>Auth0 (Okta)</strong></td><td class="mono">7.500</td><td class="mono">$0,07</td><td class="mono">$175</td><td class="mono">$2.975</td><td class="mono">$5.000+</td></tr>
    </tbody>
  </table>
</section>
<div class="aff-box"><p>Jetzt starten — Auth inklusive:</p><div class="btns">
  <a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU kostenlos</a>
  <a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU kostenlos</a>
</div></div>
<section class="sec"><h2>Haeufig gestellte Fragen</h2><div class="faq">
  <div class="qa"><div class="q">Ist Clerk kostenlos?<span class="plus">+</span></div><div class="a"><p>Clerk ist bis zu 10.000 MAU kostenlos. Danach kostet es $0,02 pro MAU. Bei 100.000 Nutzern sind das $1.825/Monat — deutlich mehr als Supabase Auth ($25/Monat).</p></div></div>
  <div class="qa"><div class="q">Welcher Auth-Anbieter ist am guenstigsten?<span class="plus">+</span></div><div class="a"><p>Supabase Auth: 50.000 kostenlose MAUs, dann $0,00325/MAU. Bei 100K Nutzern ca. $25/Monat.</p></div></div>
</div></section>
<section class="sec"><h2>Verwandte Rechner</h2><div class="tool-links">
  <a href="/de/ki-coding-tool-kosten.html" class="tool-link"><span class="ic">💻</span><div><div class="tl-name">KI Coding Tool Kosten</div><div class="tl-desc">Cursor vs Copilot vs Claude Code</div></div></a>
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Kosten</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/de/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Alle Rechner</div><div class="tl-desc">Zurueck zur Uebersicht</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/de/">APICalculators</a></span>
  <span>Preise sind Schaetzungen</span>
</div></footer>
<script>{AUTH_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'de', 'auth-anbieter-kosten.html'), auth_de)
print('✓ DE: auth-anbieter-kosten.html')

# ─────────────────────────────────────────────────────────────────────────────
# AUTH PROVIDER — FR
# ─────────────────────────────────────────────────────────────────────────────
auth_fr = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Calculateur Cout Authentification 2026 — Clerk vs Auth0 vs Supabase</title>
<meta name="description" content="Calculez vos vrais couts d'auth par MAU. A 100K utilisateurs: Clerk 1800$/mois vs Supabase 25$/mois. Gratuit, sans inscription.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="FR"/>
<meta name="geo.placename" content="France"/>
<link rel="canonical" href="https://apicalculators.com/fr/cout-fournisseur-auth.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/auth-provider-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/auth-anbieter-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-fournisseur-auth.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/auth-provider-cost.html"/>
<meta property="og:locale" content="fr_FR"/>
<meta property="og:title" content="Calculateur Cout Authentification 2026 — Clerk vs Auth0 vs Supabase">
<meta property="og:url" content="https://apicalculators.com/fr/cout-fournisseur-auth.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/fr/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/fr/">Calculateurs</a><a href="/fr/blog/">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Juin 2026 · Prix mis a jour</span>
  <h1 class="ph"><span class="em">Fournisseur Auth</span> — Calculateur de Cout</h1>
  <p class="intro">A 100K MAU, Clerk coute 1 825$/mois et Supabase Auth 25$/mois. Meme authentification. 73x d'ecart de prix. Trouvez votre chiffre avant de scaler.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔑 Calculateur de Cout d'Authentification</h2><p>Entrez votre MAU · Selectionnez le niveau de fonctionnalites · Comparez instantanement</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="mau">Utilisateurs actifs mensuels (MAU)</label>
        <input class="inp" id="mau" type="number" value="10000" min="0" step="1000"></div>
      <div class="field"><label for="tier">Besoins en fonctionnalites</label>
        <select class="sel" id="tier">
          <option value="basic">Basique (email + connexion sociale)</option>
          <option value="mid" selected>Standard (MFA + organisations)</option>
          <option value="enterprise">Entreprise (SSO + SAML + conformite)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Cout mensuel — du moins cher au plus cher</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<section class="sec">
  <h2>Le probleme 1 800$ vs 25$</h2>
  <table class="ptable">
    <thead><tr><th>Fournisseur</th><th>MAU gratuits</th><th>Tarif apres</th><th>10K MAU</th><th>50K MAU</th><th>100K MAU</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Supabase Auth</strong><span class="badge">LE MOINS CHER</span></td><td class="mono">50 000</td><td class="mono">$0,00325</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$25</td></tr>
      <tr><td><strong>Firebase Auth</strong></td><td class="mono">50 000</td><td class="mono">$0,0055</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$275</td></tr>
      <tr><td><strong>Clerk</strong></td><td class="mono">10 000</td><td class="mono">$0,02</td><td class="mono">$0</td><td class="mono">$800</td><td class="mono">$1 825</td></tr>
      <tr><td><strong>Auth0 (Okta)</strong></td><td class="mono">7 500</td><td class="mono">$0,07</td><td class="mono">$175</td><td class="mono">$2 975</td><td class="mono">$5 000+</td></tr>
    </tbody>
  </table>
</section>
<div class="aff-box"><p>Commencer avec l'auth incluse:</p><div class="btns">
  <a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU gratuits</a>
  <a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU gratuits</a>
</div></div>
<section class="sec"><h2>Questions frequentes</h2><div class="faq">
  <div class="qa"><div class="q">Clerk est-il gratuit?<span class="plus">+</span></div><div class="a"><p>Clerk est gratuit jusqu'a 10 000 MAU. Ensuite, il coute 0,02$/MAU. A 100 000 utilisateurs, cela represente 1 825$/mois.</p></div></div>
  <div class="qa"><div class="q">Quel est le fournisseur d'auth le moins cher?<span class="plus">+</span></div><div class="a"><p>Supabase Auth: 50 000 MAUs gratuits puis 0,00325$/MAU. A 100K utilisateurs, environ 25$/mois.</p></div></div>
</div></section>
<section class="sec"><h2>Calculateurs associes</h2><div class="tool-links">
  <a href="/fr/cout-outil-ia-coding.html" class="tool-link"><span class="ic">💻</span><div><div class="tl-name">Cout Outils IA Coding</div><div class="tl-desc">Cursor vs Copilot vs Claude Code</div></div></a>
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">Cout API LLM</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/fr/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Tous les calculateurs</div><div class="tl-desc">Retour a l'accueil</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/fr/">APICalculators</a></span>
  <span>Prix estimatifs</span>
</div></footer>
<script>{AUTH_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'fr', 'cout-fournisseur-auth.html'), auth_fr)
print('✓ FR: cout-fournisseur-auth.html')

# ─────────────────────────────────────────────────────────────────────────────
# AUTH PROVIDER — TR
# ─────────────────────────────────────────────────────────────────────────────
auth_tr = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>Kimlik Dogrulama Maliyet Hesaplayici 2026 — Clerk vs Auth0 vs Supabase</title>
<meta name="description" content="MAU bazli gercek kimlik dogrulama maliyetinizi hesaplayin. 100K kullanicida: Clerk $1.800/ay vs Supabase $25/ay. Ucretsiz, kayit gerekmez.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="TR"/>
<meta name="geo.placename" content="Turkey"/>
<link rel="canonical" href="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/auth-provider-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/auth-anbieter-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-fournisseur-auth.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/auth-provider-cost.html"/>
<meta property="og:locale" content="tr_TR"/>
<meta property="og:title" content="Kimlik Dogrulama Maliyet Hesaplayici 2026 — Clerk vs Auth0 vs Supabase">
<meta property="og:url" content="https://apicalculators.com/tr/kimlik-dogrulama-maliyet.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Clerk ucretsiz mi?","acceptedAnswer":{{"@type":"Answer","text":"Clerk 10.000 MAU'ya kadar ucretsiz. Sonrasinda MAU basina $0,02. 100.000 kullanicida $1.825/ay."}}}},{{"@type":"Question","name":"2026'da en ucuz kimlik dogrulama saglayicisi hangisi?","acceptedAnswer":{{"@type":"Answer","text":"Supabase Auth olcekte en ucuz: 50.000 ucretsiz MAU, sonra $0,00325/MAU. 100K kullanicida yaklasik $25/ay tutar."}}}}]}}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="/tr/" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="/tr/">Hesaplayicilar</a><a href="/tr/blog/">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> Haziran 2026 · Guncel Fiyatlar</span>
  <h1 class="ph"><span class="em">Kimlik Dogrulama</span> Maliyet Hesaplayici</h1>
  <p class="intro">100K aylik aktif kullanicida Clerk $1.825/ay, Supabase Auth $25/ay tutar. Ayni kimlik dogrulama. 73 kat fiyat farki. Olceklenmeden once sayinizi ogrenin.</p>
</section>
<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔑 Kimlik Dogrulama Maliyet Hesaplayici</h2><p>MAU girin · Ozellik seviyesi secin · Tum saglayicilari aninda karsilastirin</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="mau">Aylik Aktif Kullanici (MAU)</label>
        <input class="inp" id="mau" type="number" value="10000" min="0" step="1000"></div>
      <div class="field"><label for="tier">Ozellik gereksinimleri</label>
        <select class="sel" id="tier">
          <option value="basic">Temel (e-posta + sosyal giris)</option>
          <option value="mid" selected>Standart (MFA + organizasyon)</option>
          <option value="enterprise">Kurumsal (SSO + SAML + uyumluluk)</option>
        </select></div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Aylik maliyet — en ucuzdan pahaliya</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>
<section class="sec">
  <h2>$1.800 vs $25 Farki</h2>
  <table class="ptable">
    <thead><tr><th>Saglayici</th><th>Ucretsiz MAU</th><th>Sonraki oran</th><th>10K MAU</th><th>50K MAU</th><th>100K MAU</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Supabase Auth</strong><span class="badge">EN UCUZ</span></td><td class="mono">50.000</td><td class="mono">$0,00325</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$25</td></tr>
      <tr><td><strong>Firebase Auth</strong></td><td class="mono">50.000</td><td class="mono">$0,0055</td><td class="mono">$0</td><td class="mono">$0</td><td class="mono">$275</td></tr>
      <tr><td><strong>Clerk</strong></td><td class="mono">10.000</td><td class="mono">$0,02</td><td class="mono">$0</td><td class="mono">$800</td><td class="mono">$1.825</td></tr>
      <tr><td><strong>Auth0 (Okta)</strong></td><td class="mono">7.500</td><td class="mono">$0,07</td><td class="mono">$175</td><td class="mono">$2.975</td><td class="mono">$5.000+</td></tr>
    </tbody>
  </table>
</section>
<div class="aff-box"><p>Auth dahil baslayin:</p><div class="btns">
  <a href="[SUPABASE_AFFILIATE_LINK]" rel="sponsored noopener" target="_blank" class="aff-btn">Supabase — 50K MAU ucretsiz</a>
  <a href="[CLERK_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">Clerk — 10K MAU ucretsiz</a>
</div></div>
<section class="sec"><h2>Sik Sorulan Sorular</h2><div class="faq">
  <div class="qa"><div class="q">Clerk ucretsiz mi?<span class="plus">+</span></div><div class="a"><p>Clerk 10.000 MAU'ya kadar ucretsiz. Sonrasinda MAU basina $0,02. 100.000 kullanicida $1.825/ay - Supabase Auth'dan ($25/ay) cok daha pahali.</p></div></div>
  <div class="qa"><div class="q">En ucuz kimlik dogrulama saglayicisi hangisi?<span class="plus">+</span></div><div class="a"><p>Supabase Auth: 50.000 ucretsiz MAU, sonra $0,00325/MAU. 100K kullanicida yaklasik $25/ay.</p></div></div>
</div></section>
<section class="sec"><h2>Ilgili Hesaplayicilar</h2><div class="tool-links">
  <a href="/tr/yapay-zeka-kodlama-arac-maliyeti.html" class="tool-link"><span class="ic">💻</span><div><div class="tl-name">YZ Kodlama Araci</div><div class="tl-desc">Cursor vs Copilot vs Claude Code</div></div></a>
  <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Maliyeti</div><div class="tl-desc">GPT-4o, Claude, Gemini</div></div></a>
  <a href="/tr/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">Tum Hesaplayicilar</div><div class="tl-desc">Ana sayfaya don</div></div></a>
</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/tr/">APICalculators</a></span>
  <span>Fiyatlar tahmindir</span>
</div></footer>
<script>{AUTH_JS}</script>
</body></html>"""

write(os.path.join(BASE, 'tr', 'kimlik-dogrulama-maliyet.html'), auth_tr)
print('✓ TR: kimlik-dogrulama-maliyet.html')
print('\nAll calc pages done.')
