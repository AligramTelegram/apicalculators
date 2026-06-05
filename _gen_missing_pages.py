#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json
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
.row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.result{background:radial-gradient(120% 120% at 100% 0%,rgba(184,255,46,.07),transparent 55%),var(--surface2);border:1px solid var(--border2);border-radius:16px;padding:22px;position:relative;overflow:hidden}
.result::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--lime),var(--cyan))}
.rlabel{font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.big{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:clamp(34px,7vw,50px);line-height:1;margin:4px 0;color:var(--lime)}
.per{color:var(--muted);font-size:13px;margin-bottom:14px}
.breakdown{border-top:1px solid var(--border);padding-top:13px;display:flex;flex-direction:column;gap:9px}
.brow{display:flex;justify-content:space-between;font-size:13px}.brow span{color:var(--muted)}.brow b{font-family:'Cascadia Code','Consolas',monospace}
.brow.hl b{color:var(--lime)}.brow.amber b{color:var(--amber)}
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
footer{border-top:1px solid var(--border);padding:26px 0;font-family:'Cascadia Code','Consolas',monospace;font-size:12px;color:var(--muted)}
.foot-in{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
footer a{color:var(--muted)}"""

FAQ_JS = """document.querySelectorAll('.qa .q').forEach(q=>{
  q.addEventListener('click',()=>{
    const qa=q.parentElement,open=qa.classList.toggle('open');
    const a=qa.querySelector('.a');if(a)a.style.maxHeight=open?'300px':'0';
  });
});"""

def page(lang, html_lang, title, desc, canonical, en_url, og_locale, geo_region, geo_place,
         chip, h1_html, intro, calc_html, calc_js, table_h2, table_sub, table_html,
         faq_items, related_links, nav_home, nav_blog, nav_label, footer_home,
         schema_faq, schema_app_name):

    hreflang = f'''<link rel="alternate" hreflang="{lang}" href="{canonical}"/>
<link rel="alternate" hreflang="en" href="{en_url}"/>
<link rel="alternate" hreflang="x-default" href="{en_url}"/>'''

    faq_schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in schema_faq
    ]}, ensure_ascii=False)

    app_schema = json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication",
        "name":schema_app_name,"applicationCategory":"DeveloperApplication","operatingSystem":"Web",
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":canonical}, ensure_ascii=False)

    bread_schema = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"},
        {"@type":"ListItem","position":2,"name":schema_app_name}
    ]}, ensure_ascii=False)

    faq_html = '\n'.join(f'<div class="qa"><div class="q">{q}<span class="plus">+</span></div><div class="a"><p>{a}</p></div></div>' for q,a in faq_items)
    related_html = '\n'.join(f'<a href="{u}" class="tool-link"><span class="ic">{ic}</span><div><div class="tl-name">{n}</div><div class="tl-desc">{d}</div></div></a>' for u,ic,n,d in related_links)

    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="{geo_region}"/>
<meta name="geo.placename" content="{geo_place}"/>
<link rel="canonical" href="{canonical}">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:locale" content="{og_locale}"/>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://apicalculators.com/twitter-image.png">
<script type="application/ld+json">{faq_schema}</script>
<script type="application/ld+json">{app_schema}</script>
<script type="application/ld+json">{bread_schema}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a href="{nav_home}" class="logo">API<b>Calculators</b></a>
  <nav class="nav-r"><a href="{nav_home}">{nav_label}</a><a href="{nav_blog}">Blog</a></nav>
</div></header>
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> {chip}</span>
  <h1 class="ph">{h1_html}</h1>
  <p class="intro">{intro}</p>
</section>
<div class="wrap">
{calc_html}
<section class="sec">
  <h2>{table_h2}</h2>
  <p class="sh-sub">{table_sub}</p>
  {table_html}
</section>
<section class="sec">
  <h2>FAQ</h2>
  <div class="faq">{faq_html}</div>
</section>
<section class="sec">
  <h2>{'Related Calculators' if lang=='en' else 'Verwandte Rechner' if lang=='de' else 'Calculateurs associes' if lang=='fr' else 'Ilgili Hesaplayicilar'}</h2>
  <div class="tool-links">{related_html}</div>
</section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="{nav_home}">APICalculators</a></span>
  <span>{'Prices are estimates' if lang=='en' else 'Preise sind Schaetzungen' if lang=='de' else 'Prix estimatifs' if lang=='fr' else 'Fiyatlar tahmindir'}</span>
</div></footer>
<script>{FAQ_JS}</script>
<script>{calc_js}</script>
</body></html>"""

# ══════════════════════════════════════════════════════════════════════════════
# TOOL DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

PAGES_TO_CREATE = []

# ── 1. AWS Lambda — FR only ───────────────────────────────────────────────────
PAGES_TO_CREATE.append(dict(
    path='fr/calculateur-cout-aws-lambda.html',
    lang='fr', html_lang='fr', og_locale='fr_FR', geo_region='FR', geo_place='France',
    title='Calculateur Cout AWS Lambda 2026 — Serverless Pricing',
    desc='Calculateur gratuit AWS Lambda. Comparez Lambda, Cloudflare Workers et Vercel Functions. Entrez vos invocations et obtenez le cout mensuel exact.',
    canonical='https://apicalculators.com/fr/calculateur-cout-aws-lambda.html',
    en_url='https://apicalculators.com/aws-lambda-calculator.html',
    chip='Juin 2026 · Prix mis a jour',
    h1_html='<span class="em">AWS Lambda</span> Calculateur de Cout',
    intro='Comparez AWS Lambda, Cloudflare Workers et Vercel Functions. Entrez votre volume d\'invocations et obtenez le cout mensuel exact. Gratuit, sans inscription.',
    calc_html='''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>⚡ Calculateur AWS Lambda</h2><p>Selectionnez plateforme · Entrez invocations · Resultats en temps reel</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="slProv">Plateforme</label>
        <select class="sel" id="slProv">
          <option value="lambda">AWS Lambda</option>
          <option value="cf">Cloudflare Workers</option>
          <option value="vercel">Vercel Functions</option>
          <option value="gcp">GCP Cloud Functions</option>
        </select></div>
      <div class="field"><label for="slInv">Invocations / mois</label>
        <input class="inp" id="slInv" type="number" value="1000000" min="0"></div>
      <div class="field"><label for="slDur">Duree moy. (ms)</label>
        <input class="inp" id="slDur" type="number" value="150" min="1"></div>
      <div class="field"><label for="slMem">Memoire</label>
        <select class="sel" id="slMem">
          <option value="0.125">128 MB</option>
          <option value="0.25" selected>256 MB</option>
          <option value="0.5">512 MB</option>
          <option value="1">1024 MB</option>
        </select></div>
    </div>
    <div class="result">
      <div class="rlabel">Cout mensuel estime</div>
      <div class="big" id="slTotal">$0</div>
      <div class="per" id="slPer">— par mois</div>
      <div class="breakdown">
        <div class="brow"><span>Cout invocation</span><b id="slInvCost">—</b></div>
        <div class="brow"><span>Cout calcul (Go-sec)</span><b id="slComp">—</b></div>
        <div class="brow hl"><span>Estimation annuelle</span><b id="slAnn">—</b></div>
      </div>
    </div>
  </div>
</div>''',
    calc_js='''
const SL={lambda:{inv:0.20,gb:0.0000166667,free_inv:1e6,free_gb:400000},cf:{inv:0.30,gb:0,free_inv:1e7,free_gb:0},vercel:{inv:0,gb:0,free_inv:1e6,free_gb:0},gcp:{inv:0.40,gb:0.0000025,free_inv:2e6,free_gb:400000}};
function calcSl(){
  var p=document.getElementById('slProv').value;
  var inv=parseFloat(document.getElementById('slInv').value)||0;
  var dur=parseFloat(document.getElementById('slDur').value)||1;
  var mem=parseFloat(document.getElementById('slMem').value)||0.25;
  var pr=SL[p];
  var billInv=Math.max(0,inv-pr.free_inv);
  var gbSec=inv*(dur/1000)*mem;
  var billGb=Math.max(0,gbSec-pr.free_gb);
  var invCost=billInv/1e6*pr.inv;
  var gbCost=billGb*pr.gb;
  var total=invCost+gbCost;
  document.getElementById('slTotal').textContent='$'+total.toFixed(2);
  document.getElementById('slInvCost').textContent='$'+invCost.toFixed(4);
  document.getElementById('slComp').textContent='$'+gbCost.toFixed(4);
  document.getElementById('slAnn').textContent='$'+(total*12).toFixed(2);
}
['slProv','slInv','slDur','slMem'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcSl);el.addEventListener('change',calcSl);}});
calcSl();''',
    table_h2='Comparaison Serverless 2026',
    table_sub='Tous les prix en USD, par million d\'invocations.',
    table_html='''<table class="ptable"><thead><tr><th>Plateforme</th><th>Invocations</th><th>Calcul</th><th>Gratuit</th></tr></thead><tbody>
<tr class="best"><td><strong>Cloudflare Workers</strong><span class="badge">LE MOINS CHER</span></td><td class="mono">$0.30/M</td><td class="mono">inclus</td><td class="mono">10M/mois</td></tr>
<tr><td><strong>AWS Lambda</strong></td><td class="mono">$0.20/M</td><td class="mono">$0.0000167/Go-sec</td><td class="mono">1M/mois</td></tr>
<tr><td><strong>Vercel Functions</strong></td><td class="mono">inclus</td><td class="mono">inclus</td><td class="mono">1M/mois</td></tr>
<tr><td><strong>GCP Cloud Functions</strong></td><td class="mono">$0.40/M</td><td class="mono">$0.0000025/Go-sec</td><td class="mono">2M/mois</td></tr>
</tbody></table>''',
    faq_items=[
        ('Combien coute AWS Lambda par million de requetes?','Apres le tier gratuit (1M/mois), Lambda coute $0.20 par million d\'invocations plus les couts de calcul. Une fonction 256MB a 200ms = ~$3.47/mois pour 10M invocations.'),
        ('Cloudflare Workers est-il moins cher que Lambda?','Pour les courtes durees (moins de 30ms) a haute frequence oui. Workers a $0.30/M bat Lambda. Pour les calculs plus longs ou les integrations AWS, Lambda est souvent meilleur.'),
    ],
    schema_faq=[
        ('Combien coute AWS Lambda par million d\'invocations?','Apres le tier gratuit (1M/mois): $0.20/M invocations plus $0.0000167/Go-sec de calcul.'),
        ('Cloudflare Workers est-il moins cher que Lambda?','Pour les fonctions courtes (moins de 30ms) oui. Workers a $0.30/M est plus avantageux pour les APIs a haute frequence.'),
    ],
    schema_app_name='Calculateur Cout AWS Lambda 2026',
    related_links=[
        ('/llm-cost-calculator.html','🤖','Cout API LLM','GPT-4o, Claude, Gemini'),
        ('/vector-db-cost.html','🗄️','Cout Base Vectorielle','Pinecone vs Supabase'),
        ('/api-gateway-cost.html','🔀','Cout API Gateway','AWS vs Cloudflare'),
        ('/fr/','🧮','Tous les calculateurs','Retour accueil'),
    ],
    nav_home='/fr/', nav_blog='/fr/blog/', nav_label='Calculateurs', footer_home='APICalculators',
))

# ── 2. Cloud VPS — TR only ────────────────────────────────────────────────────
PAGES_TO_CREATE.append(dict(
    path='tr/bulut-vps-maliyet.html',
    lang='tr', html_lang='tr', og_locale='tr_TR', geo_region='TR', geo_place='Turkey',
    title='Bulut VPS Maliyet Karsilastirmasi 2026 — Hetzner vs DigitalOcean vs Vultr',
    desc='Ucretsiz bulut VPS maliyet hesaplayicisi. Hetzner, Vultr ve DigitalOcean fiyatlarini karsilastirin. Sunucu ozelliklerini girin, anlik maliyet alin.',
    canonical='https://apicalculators.com/tr/bulut-vps-maliyet.html',
    en_url='https://apicalculators.com/cloud-vps-comparison.html',
    chip='Haziran 2026 · Guncel Fiyatlar',
    h1_html='<span class="em">Bulut VPS</span> Maliyet Karsilastirmasi',
    intro='Hetzner, Vultr, DigitalOcean ve Linode VPS fiyatlarini karsilastirin. Sunucu ozelliklerini secin, anlik aylik maliyeti gorun. Ucretsiz, kayit gerekmez.',
    calc_html='''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>☁️ Bulut VPS Maliyet Hesaplayici</h2><p>Sunucu ozellikleri secin · Sonuclar aninda guncellenir</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="cpu">vCPU</label>
        <select class="sel" id="cpu"><option value="1">1 vCPU</option><option value="2" selected>2 vCPU</option><option value="4">4 vCPU</option><option value="8">8 vCPU</option></select></div>
      <div class="field"><label for="ram">RAM</label>
        <select class="sel" id="ram"><option value="1">1 GB</option><option value="4" selected>4 GB</option><option value="8">8 GB</option><option value="16">16 GB</option></select></div>
      <div class="field"><label for="cnt">Sunucu sayisi</label>
        <input class="inp" id="cnt" type="number" value="1" min="1"></div>
    </div>
    <div class="result">
      <div class="rlabel">Tahmini aylik maliyet</div>
      <div class="big" id="cloudTotal">$0</div>
      <div class="per" id="cloudPer">— aylik</div>
      <div class="breakdown" id="cloudCmp"></div>
    </div>
  </div>
</div>''',
    calc_js='''
var CLOUD=[
  {name:'Hetzner',prices:{'1-1':3.29,'2-4':6.49,'4-8':13.49,'8-16':27.49}},
  {name:'Vultr',prices:{'1-1':6,'2-4':24,'4-8':48,'8-16':96}},
  {name:'DigitalOcean',prices:{'1-1':8,'2-4':24,'4-8':48,'8-16':96}},
  {name:'Linode',prices:{'1-1':5,'2-4':20,'4-8':40,'8-16':80}},
];
function calcCloud(){
  var cpu=document.getElementById('cpu').value;
  var ram=document.getElementById('ram').value;
  var cnt=parseInt(document.getElementById('cnt').value)||1;
  var key=cpu+'-'+ram;
  var total=0,best=null;
  var rows=CLOUD.map(function(p){var pr=(p.prices[key]||0)*cnt;if(best===null||pr<best)best=pr;return{name:p.name,pr:pr};});
  rows.sort(function(a,b){return a.pr-b.pr;});
  document.getElementById('cloudTotal').textContent='$'+rows[0].pr.toFixed(2);
  document.getElementById('cloudCmp').innerHTML=rows.map(function(r,i){
    return '<div class="brow'+(i===0?' hl':'')+'"><span>'+r.name+'</span><b>$'+r.pr.toFixed(2)+'/ay</b></div>';
  }).join('');
}
['cpu','ram','cnt'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('change',calcCloud);el.addEventListener('input',calcCloud);}});
calcCloud();''',
    table_h2='VPS Fiyat Karsilastirmasi 2026',
    table_sub='2 vCPU / 4 GB RAM icin tipik fiyatlar.',
    table_html='''<table class="ptable"><thead><tr><th>Saglayici</th><th>2vCPU/4GB</th><th>4vCPU/8GB</th><th>Egress</th><th>Lokasyon</th></tr></thead><tbody>
<tr class="best"><td><strong>Hetzner</strong><span class="badge">EN UCUZ</span></td><td class="mono">€5.29</td><td class="mono">€13.49</td><td class="mono">20TB ucretsiz</td><td>DE/FI</td></tr>
<tr><td><strong>Linode/Akamai</strong></td><td class="mono">$20</td><td class="mono">$40</td><td class="mono">4TB ucretsiz</td><td>Global</td></tr>
<tr><td><strong>Vultr</strong></td><td class="mono">$24</td><td class="mono">$48</td><td class="mono">3TB ucretsiz</td><td>32 lokasyon</td></tr>
<tr><td><strong>DigitalOcean</strong></td><td class="mono">$24</td><td class="mono">$48</td><td class="mono">$0.01/GB</td><td>Global</td></tr>
</tbody></table>''',
    faq_items=[
        ('Hetzner DigitalOcean\'dan ucuz mu?','Evet — 3-5 kat daha ucuz. Hetzner CX22 (2 vCPU/4GB) €5.29/ay, DigitalOcean $24/ay.'),
        ('Kucuk SaaS icin hangi VPS?','EU kitlasi icin Hetzner. Global erisim icin Vultr (32 lokasyon). Managed Postgres gerekiyorsa DigitalOcean.'),
    ],
    schema_faq=[
        ('Hetzner DigitalOcean\'dan ucuz mu?','Evet — 3-5 kat daha ucuz. Hetzner CX22 (2 vCPU/4GB) €5.29/ay iken DigitalOcean $24/ay.'),
        ('En iyi VPS saglayicisi hangisi?','EU icin Hetzner, global icin Vultr, managed veritabani gerekiyorsa DigitalOcean.'),
    ],
    schema_app_name='Bulut VPS Maliyet Karsilastirmasi 2026',
    related_links=[
        ('/llm-cost-calculator.html','🤖','LLM API Maliyeti','GPT-4o, Claude, Gemini'),
        ('/tr/aws-lambda-maliyet.html','⚡','AWS Lambda Maliyet','Serverless fiyatlandirma'),
        ('/embedding-api-cost.html','🔢','Embedding API Maliyeti','OpenAI vs Cohere'),
        ('/tr/','🧮','Tum Hesaplayicilar','Ana sayfaya don'),
    ],
    nav_home='/tr/', nav_blog='/tr/blog/', nav_label='Hesaplayicilar', footer_home='APICalculators',
))

# ── HELPER: generic calc page for vector/embedding/gateway/stt/agent/image/stripe ──

def make_vector_page(lang, html_lang, og_locale, geo_region, geo_place, nav_home, nav_blog, nav_label, path,
    title, desc, canonical, en_url, chip, h1_html, intro, table_h2, table_sub, faq_items, schema_faq, related_links):

    calc_html = '''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🗄️ ''' + ('Vector DB' if lang=='en' else 'Vektordatenbank' if lang=='de' else 'Base Vectorielle' if lang=='fr' else 'Vektor DB') + ''' Kostenrechner</h2><p>''' + ('Provider · Vectors · Queries' if lang=='en' else 'Anbieter · Vektoren · Abfragen' if lang=='de' else 'Fournisseur · Vecteurs · Requetes' if lang=='fr' else 'Saglayici · Vektor · Sorgu') + '''</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="vecProv">''' + ('Provider' if lang=='en' else 'Anbieter' if lang=='de' else 'Fournisseur' if lang=='fr' else 'Saglayici') + '''</label>
        <select class="sel" id="vecProv">
          <option value="pinecone">Pinecone Serverless</option>
          <option value="supabase">Supabase pgvector</option>
          <option value="qdrant">Qdrant Cloud</option>
          <option value="weaviate">Weaviate Cloud</option>
        </select></div>
      <div class="row2">
        <div class="field"><label for="vecCount">''' + ('Vectors' if lang=='en' else 'Vektoren' if lang=='de' else 'Vecteurs' if lang=='fr' else 'Vektor sayisi') + '''</label>
          <input class="inp" id="vecCount" type="number" value="1000000" min="0"></div>
        <div class="field"><label for="vecDim">Dimensions</label>
          <input class="inp" id="vecDim" type="number" value="1536" min="1"></div>
      </div>
      <div class="field"><label for="vecQ">''' + ('Queries / month' if lang=='en' else 'Abfragen / Monat' if lang=='de' else 'Requetes / mois' if lang=='fr' else 'Sorgu / ay') + '''</label>
        <input class="inp" id="vecQ" type="number" value="2000000" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">''' + ('Estimated monthly cost' if lang=='en' else 'Gesch. Monatskosten' if lang=='de' else 'Cout mensuel estime' if lang=='fr' else 'Tahmini aylik maliyet') + '''</div>
      <div class="big" id="vecTotal">$0</div>
      <div class="per" id="vecName">—</div>
      <div class="breakdown">
        <div class="brow"><span>''' + ('Storage cost' if lang=='en' else 'Speicherkosten' if lang=='de' else 'Cout stockage' if lang=='fr' else 'Depolama maliyeti') + '''</span><b id="vecStore">—</b></div>
        <div class="brow"><span>''' + ('Query cost' if lang=='en' else 'Abfragekosten' if lang=='de' else 'Cout requetes' if lang=='fr' else 'Sorgu maliyeti') + '''</span><b id="vecQCost">—</b></div>
        <div class="brow hl"><span>''' + ('Annual estimate' if lang=='en' else 'Jahresschaetzung' if lang=='de' else 'Estimation annuelle' if lang=='fr' else 'Yillik tahmin') + '''</span><b id="vecAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

    calc_js = '''
var VEC={pinecone:{base:0,storPerGB:0.33,queryPerM:16},supabase:{base:25,storPerGB:0.125,queryPerM:0},qdrant:{base:0,storPerGB:0.10,queryPerM:0.04},weaviate:{base:0,storPerGB:0.05,queryPerM:0.05}};
function calcVec(){
  var p=VEC[document.getElementById('vecProv').value];
  var n=parseFloat(document.getElementById('vecCount').value)||0;
  var d=parseFloat(document.getElementById('vecDim').value)||1536;
  var q=parseFloat(document.getElementById('vecQ').value)||0;
  var bytes=n*d*4*1.5;var gb=bytes/(1024*1024*1024);
  var store=gb*p.storPerGB;
  var qcost=q/1e6*p.queryPerM;
  var total=p.base+store+qcost;
  document.getElementById('vecTotal').textContent='$'+total.toFixed(2);
  document.getElementById('vecName').textContent='— '+document.getElementById('vecProv').value;
  document.getElementById('vecStore').textContent='$'+store.toFixed(2);
  document.getElementById('vecQCost').textContent=p.queryPerM?'$'+qcost.toFixed(2):'included';
  document.getElementById('vecAnn').textContent='$'+(total*12).toFixed(2);
}
['vecProv','vecCount','vecDim','vecQ'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcVec);el.addEventListener('change',calcVec);}});
calcVec();'''

    table_html = '''<table class="ptable"><thead><tr><th>''' + ('Provider' if lang=='en' else 'Anbieter' if lang=='de' else 'Fournisseur' if lang=='fr' else 'Saglayici') + '''</th><th>1M Vectors</th><th>10M Vectors</th><th>''' + ('Free tier' if lang=='en' else 'Kostenlos' if lang=='de' else 'Gratuit' if lang=='fr' else 'Ucretsiz') + '''</th></tr></thead><tbody>
<tr class="best"><td><strong>Supabase pgvector</strong><span class="badge">''' + ('CHEAPEST' if lang=='en' else 'GUENSTIGSTE' if lang=='de' else 'LE MOINS CHER' if lang=='fr' else 'EN UCUZ') + '''</span></td><td class="mono">$25</td><td class="mono">$25</td><td class="mono">50K MAU ''' + ('included' if lang=='en' else 'inkl.' if lang=='de' else 'inclus' if lang=='fr' else 'dahil') + '''</td></tr>
<tr><td><strong>Qdrant Cloud</strong></td><td class="mono">~$10</td><td class="mono">~$100</td><td class="mono">1GB ''' + ('free' if lang=='en' else 'kostenlos' if lang=='de' else 'gratuit' if lang=='fr' else 'ucretsiz') + '''</td></tr>
<tr><td><strong>Pinecone</strong></td><td class="mono">~$20</td><td class="mono">~$200</td><td class="mono">100K ''' + ('vectors' if lang=='en' else 'Vektoren' if lang=='de' else 'vecteurs' if lang=='fr' else 'vektor') + '''</td></tr>
<tr><td><strong>Weaviate Cloud</strong></td><td class="mono">~$25</td><td class="mono">~$250</td><td class="mono">Sandbox</td></tr>
</tbody></table>'''

    return page(lang=lang, html_lang=html_lang, title=title, desc=desc, canonical=canonical, en_url=en_url,
        og_locale=og_locale, geo_region=geo_region, geo_place=geo_place, chip=chip,
        h1_html=h1_html, intro=intro, calc_html=calc_html, calc_js=calc_js,
        table_h2=table_h2, table_sub=table_sub, table_html=table_html,
        faq_items=faq_items, related_links=related_links, nav_home=nav_home,
        nav_blog=nav_blog, nav_label=nav_label, footer_home='APICalculators',
        schema_faq=schema_faq, schema_app_name=title)

# Vector DB — DE
PAGES_TO_CREATE.append({'path':'de/vektordatenbank-kosten.html','_fn':'vector','lang':'de',
    'html_lang':'de','og_locale':'de_DE','geo_region':'DE','geo_place':'Germany',
    'nav_home':'/de/','nav_blog':'/de/blog/','nav_label':'Rechner',
    'title':'Vektordatenbank Kosten 2026 — Pinecone vs Supabase vs Qdrant',
    'desc':'Kostenloser Vektordatenbank Kostenrechner. Pinecone, Supabase pgvector, Qdrant und Weaviate vergleichen. Vektoranzahl eingeben und Monatskosten erhalten.',
    'canonical':'https://apicalculators.com/de/vektordatenbank-kosten.html',
    'en_url':'https://apicalculators.com/vector-db-cost.html',
    'chip':'Juni 2026 · Aktuelle Preise',
    'h1_html':'<span class="em">Vektordatenbank</span> Kosten 2026',
    'intro':'Pinecone, Supabase pgvector, Qdrant und Weaviate Preise vergleichen. Vektoranzahl und Abfragevolumen eingeben — exakte Monatskosten erhalten.',
    'table_h2':'Vektordatenbank Preisvergleich 2026','table_sub':'Preise in USD pro Monat, Stand Juni 2026.',
    'faq_items':[('Was ist die guenstigste Vektordatenbank 2026?','Supabase pgvector bei $25/Monat (50K Vektoren kostenlos). Fuer 50M+ Vektoren: selbst gehostetes Qdrant auf Spot-VMs bei $150-300/Monat.'),
        ('Wie viel kostet Pinecone fuer 1 Million Vektoren?','Ca. $20/Monat. Speicher ~$3, plus $16 pro Million Leseoperationen.')],
    'schema_faq':[('Guenstigste Vektordatenbank 2026?','Supabase pgvector $25/Monat. Fuer grosse Skalierung: Qdrant self-hosted.'),
        ('Pinecone Kosten fuer 1M Vektoren?','Ca. $20/Monat — $3 Speicher plus $16/M Leseoperationen.')],
    'related_links':[('/llm-cost-calculator.html','🤖','LLM API Kosten','GPT-4o, Claude, Gemini'),('/embedding-api-cost.html','🔢','Embedding API Kosten','OpenAI vs Cohere'),('/de/','🧮','Alle Rechner','Uebersicht')]})

# Vector DB — FR
PAGES_TO_CREATE.append({'path':'fr/cout-base-vectorielle.html','_fn':'vector','lang':'fr',
    'html_lang':'fr','og_locale':'fr_FR','geo_region':'FR','geo_place':'France',
    'nav_home':'/fr/','nav_blog':'/fr/blog/','nav_label':'Calculateurs',
    'title':'Cout Base de Donnees Vectorielle 2026 — Pinecone vs Supabase vs Qdrant',
    'desc':'Calculateur gratuit de cout de base vectorielle. Comparez Pinecone, Supabase pgvector, Qdrant et Weaviate. Entrez le nombre de vecteurs et obtenez le cout mensuel.',
    'canonical':'https://apicalculators.com/fr/cout-base-vectorielle.html',
    'en_url':'https://apicalculators.com/vector-db-cost.html',
    'chip':'Juin 2026 · Prix mis a jour',
    'h1_html':'<span class="em">Base Vectorielle</span> — Calculateur de Cout',
    'intro':'Comparez Pinecone, Supabase pgvector, Qdrant et Weaviate. Entrez votre volume de vecteurs et de requetes pour obtenir le cout mensuel exact.',
    'table_h2':'Comparaison Bases Vectorielles 2026','table_sub':'Prix en USD par mois, juin 2026.',
    'faq_items':[('Quelle est la base vectorielle la moins chere en 2026?','Supabase pgvector a $25/mois (50K vecteurs gratuits). Pour 50M+ vecteurs: Qdrant auto-heberge sur VMs spot a $150-300/mois.'),
        ('Combien coute Pinecone pour 1 million de vecteurs?','Environ $20/mois. Stockage ~$3, plus $16 par million d\'operations de lecture.')],
    'schema_faq':[('Base vectorielle la moins chere 2026?','Supabase pgvector $25/mois. Pour grande echelle: Qdrant auto-heberge.'),
        ('Cout Pinecone pour 1M vecteurs?','~$20/mois — $3 stockage plus $16/M operations lecture.')],
    'related_links':[('/llm-cost-calculator.html','🤖','Cout API LLM','GPT-4o, Claude, Gemini'),('/embedding-api-cost.html','🔢','Cout API Embedding','OpenAI vs Cohere'),('/fr/','🧮','Tous les calculateurs','Accueil')]})

# Vector DB — TR
PAGES_TO_CREATE.append({'path':'tr/vektor-veritabani-maliyet.html','_fn':'vector','lang':'tr',
    'html_lang':'tr','og_locale':'tr_TR','geo_region':'TR','geo_place':'Turkey',
    'nav_home':'/tr/','nav_blog':'/tr/blog/','nav_label':'Hesaplayicilar',
    'title':'Vektor Veritabani Maliyet Karsilastirmasi 2026 — Pinecone vs Supabase vs Qdrant',
    'desc':'Ucretsiz vektor veritabani maliyet hesaplayicisi. Pinecone, Supabase pgvector, Qdrant ve Weaviate fiyatlarini karsilastirin.',
    'canonical':'https://apicalculators.com/tr/vektor-veritabani-maliyet.html',
    'en_url':'https://apicalculators.com/vector-db-cost.html',
    'chip':'Haziran 2026 · Guncel Fiyatlar',
    'h1_html':'<span class="em">Vektor Veritabani</span> Maliyet Karsilastirmasi',
    'intro':'Pinecone, Supabase pgvector, Qdrant ve Weaviate fiyatlarini karsilastirin. Vektor sayisi ve sorgu hacmini girin, aylik maliyeti aninda gorun.',
    'table_h2':'Vektor Veritabani Fiyat Karsilastirmasi 2026','table_sub':'USD cinsinden aylik fiyatlar, Haziran 2026.',
    'faq_items':[('2026\'da en ucuz vektor veritabani hangisi?','Supabase pgvector $25/ay (50K vektor ucretsiz). 50M+ vektor icin: spot VM\'lerde Qdrant $150-300/ay.'),
        ('1 milyon vektor icin Pinecone ne kadar?','Yaklasik $20/ay. Depolama ~$3, arti $16/M okuma islemi.')],
    'schema_faq':[('En ucuz vektor veritabani 2026?','Supabase pgvector $25/ay. Buyuk olcek icin Qdrant self-hosted.'),
        ('Pinecone 1M vektor maliyeti?','~$20/ay — $3 depolama arti $16/M okuma.')],
    'related_links':[('/llm-cost-calculator.html','🤖','LLM API Maliyeti','GPT-4o, Claude, Gemini'),('/embedding-api-cost.html','🔢','Embedding API Maliyeti','OpenAI vs Cohere'),('/tr/','🧮','Tum Hesaplayicilar','Ana sayfa')]})

# ── Generate and write all pages ──────────────────────────────────────────────
created = 0
for p in PAGES_TO_CREATE:
    path = os.path.join(BASE, p['path'].replace('/', os.sep))
    if p.get('_fn') == 'vector':
        html = make_vector_page(
            lang=p['lang'], html_lang=p['html_lang'], og_locale=p['og_locale'],
            geo_region=p['geo_region'], geo_place=p['geo_place'],
            nav_home=p['nav_home'], nav_blog=p['nav_blog'], nav_label=p['nav_label'],
            path=path, title=p['title'], desc=p['desc'],
            canonical=p['canonical'], en_url=p['en_url'], chip=p['chip'],
            h1_html=p['h1_html'], intro=p['intro'],
            table_h2=p['table_h2'], table_sub=p['table_sub'],
            faq_items=p['faq_items'], schema_faq=p['schema_faq'],
            related_links=p['related_links']
        )
    else:
        html = page(
            lang=p['lang'], html_lang=p['html_lang'], title=p['title'], desc=p['desc'],
            canonical=p['canonical'], en_url=p['en_url'], og_locale=p['og_locale'],
            geo_region=p['geo_region'], geo_place=p['geo_place'], chip=p['chip'],
            h1_html=p['h1_html'], intro=p['intro'], calc_html=p['calc_html'],
            calc_js=p['calc_js'], table_h2=p['table_h2'], table_sub=p['table_sub'],
            table_html=p['table_html'], faq_items=p['faq_items'],
            related_links=p['related_links'], nav_home=p['nav_home'],
            nav_blog=p['nav_blog'], nav_label=p['nav_label'],
            footer_home=p['footer_home'], schema_faq=p['schema_faq'],
            schema_app_name=p['schema_app_name']
        )
    write(path, html)
    print(f'✓ {p["path"]}')
    created += 1

print(f'\nBatch 1: {created} pages created')
