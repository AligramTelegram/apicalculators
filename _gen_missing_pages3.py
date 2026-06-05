#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def write(path, c):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

CSS=open(os.path.join(BASE,'de','llm-kostenrechner.html'),encoding='utf-8').read()
CSS=CSS[CSS.find('<style>')+7:CSS.find('</style>')]
FAQ_JS="document.querySelectorAll('.qa .q').forEach(q=>{q.addEventListener('click',()=>{const qa=q.parentElement,open=qa.classList.toggle('open');const a=qa.querySelector('.a');if(a)a.style.maxHeight=open?'300px':'0';});});"

def t(lang,de,fr,tr):
    return {'de':de,'fr':fr,'tr':tr}.get(lang,de)

def make_page(lang,html_lang,og_locale,geo_region,geo_place,nav_home,nav_blog,nav_label,
              title,desc,canonical,en_url,chip,h1_html,intro,calc_html,calc_js,
              table_html,faq_items,related_links,schema_faq,schema_name):
    fs=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in schema_faq]},ensure_ascii=False)
    ap=json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication","name":schema_name,"applicationCategory":"DeveloperApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":canonical},ensure_ascii=False)
    br=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"},{"@type":"ListItem","position":2,"name":schema_name}]},ensure_ascii=False)
    fh='\n'.join(f'<div class="qa"><div class="q">{q}<span class="plus">+</span></div><div class="a"><p>{a}</p></div></div>' for q,a in faq_items)
    rh='\n'.join(f'<a href="{u}" class="tool-link"><span class="ic">{ic}</span><div><div class="tl-name">{n}</div><div class="tl-desc">{d}</div></div></a>' for u,ic,n,d in related_links)
    rel_t=t(lang,'Verwandte Rechner','Calculateurs associes','Ilgili Hesaplayicilar')
    pnote=t(lang,'Preise sind Schaetzungen','Prix estimatifs','Fiyatlar tahmindir')
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=5.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="{geo_region}"/>
<meta name="geo.placename" content="{geo_place}"/>
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{lang}" href="{canonical}"/>
<link rel="alternate" hreflang="en" href="{en_url}"/>
<link rel="alternate" hreflang="x-default" href="{en_url}"/>
<meta property="og:type" content="website">
<meta property="og:locale" content="{og_locale}"/>
<meta property="og:title" content="{title}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{fs}</script>
<script type="application/ld+json">{ap}</script>
<script type="application/ld+json">{br}</script>
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
{table_html}
<section class="sec"><h2>FAQ</h2><div class="faq">{fh}</div></section>
<section class="sec"><h2>{rel_t}</h2><div class="tool-links">{rh}</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="{nav_home}">APICalculators</a></span>
  <span>{pnote}</span>
</div></footer>
<script>{FAQ_JS}</script>
<script>{calc_js}</script>
</body></html>"""

# ── AI AGENT ──────────────────────────────────────────────────────────────────
AG_JS="""
var AG_LLM={gpt4o:{in:2.50,out:10.00},gpt4omini:{in:0.15,out:0.60},sonnet:{in:3.00,out:15.00},haiku:{in:0.80,out:4.00},flash:{in:0.075,out:0.30}};
var STEPS=[{m:'agM1',in_tok:500,out_tok:100},{m:'agM2',in_tok:3000,out_tok:800},{m:'agM3',in_tok:1500,out_tok:300}];
function calcAg(){
  var runs=parseFloat(document.getElementById('agRuns').value)||0;
  var costs=STEPS.map(function(s){var m=AG_LLM[document.getElementById(s.m).value];return(s.in_tok/1e6)*m.in+(s.out_tok/1e6)*m.out;});
  var per=costs.reduce(function(a,b){return a+b;},0);
  var total=per*runs;
  document.getElementById('agTotal').textContent='$'+total.toFixed(2);
  document.getElementById('agPerRun').textContent='$'+per.toFixed(6);
  document.getElementById('agAnn').textContent='$'+(total*12).toFixed(2);
}
['agM1','agM2','agM3','agRuns'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcAg);el.addEventListener('change',calcAg);}});
calcAg();"""

def ag_calc(lang):
    runs=t(lang,'Aufrufe / Monat','Executions / mois','Calistirma / ay')
    s1=t(lang,'Schritt 1 — Planer / Router','Etape 1 — Planificateur','Adim 1 — Planlayici')
    s2=t(lang,'Schritt 2 — Hauptworker','Etape 2 — Travailleur principal','Adim 2 — Ana Iscisi')
    s3=t(lang,'Schritt 3 — Zusammenfasser','Etape 3 — Resumeur','Adim 3 — Ozetleyici')
    est=t(lang,'Gesch. Monatskosten','Cout mensuel estime','Tahmini aylik maliyet')
    per=t(lang,'Kosten pro Aufruf','Cout par execution','Calistirma basi maliyet')
    ann=t(lang,'Jahresschaetzung','Estimation annuelle','Yillik tahmin')
    hdr=t(lang,'KI-Agent Multi-Modell Kostenrechner','Calculateur Cout Agent IA Multi-Modele','YZ Ajan Cok-Model Maliyet Hesaplayici')
    opts='<option value="gpt4o">GPT-4o — $2.50/$10.00</option><option value="gpt4omini" selected>GPT-4o mini — $0.15/$0.60</option><option value="sonnet">Claude 3.5 Sonnet — $3.00/$15.00</option><option value="haiku">Claude 3.5 Haiku — $0.80/$4.00</option><option value="flash">Gemini Flash — $0.075/$0.30</option>'
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🤖 {hdr}</h2></div>
  <div class="calc-body">
    <div>
      <div class="field"><label>{s1}</label><select class="sel" id="agM1">{opts}</select></div>
      <div class="field"><label>{s2}</label><select class="sel" id="agM2">{opts}</select></div>
      <div class="field"><label>{s3}</label><select class="sel" id="agM3">{opts.replace('selected','').replace('gpt4omini','gpt4omini selected',1)}</select></div>
      <div class="field"><label for="agRuns">{runs}</label>
        <input class="inp" id="agRuns" type="number" value="10000" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">{est}</div>
      <div class="big" id="agTotal">$0</div>
      <div class="per">{"pro Monat" if lang=="de" else "par mois" if lang=="fr" else "aylik"}</div>
      <div class="breakdown">
        <div class="brow"><span>{per}</span><b id="agPerRun">—</b></div>
        <div class="brow hl"><span>{ann}</span><b id="agAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

AG_TABLE=lambda lang:f'''<section class="sec">
  <h2>{"KI-Agent Kosten nach Modell" if lang=="de" else "Couts Agent IA par Modele" if lang=="fr" else "YZ Ajan Maliyeti - Model Bazli"}</h2>
  <table class="ptable"><thead><tr><th>{"Modell" if lang=="de" else "Modele" if lang=="fr" else "Model"}</th><th>Input/1M</th><th>Output/1M</th></tr></thead><tbody>
<tr class="best"><td><strong>Gemini 1.5 Flash</strong><span class="badge">{"GUENSTIGSTE" if lang=="de" else "LE MOINS CHER" if lang=="fr" else "EN UCUZ"}</span></td><td class="mono">$0.075</td><td class="mono">$0.30</td></tr>
<tr><td><strong>GPT-4o mini</strong></td><td class="mono">$0.15</td><td class="mono">$0.60</td></tr>
<tr><td><strong>Claude 3.5 Haiku</strong></td><td class="mono">$0.80</td><td class="mono">$4.00</td></tr>
<tr><td><strong>GPT-4o</strong></td><td class="mono">$2.50</td><td class="mono">$10.00</td></tr>
<tr><td><strong>Claude 3.5 Sonnet</strong></td><td class="mono">$3.00</td><td class="mono">$15.00</td></tr>
</tbody></table></section>'''

for lang,hl,og,gr,gp,nh,nb,nl,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/ki-agent-kostenrechner.html',
     'KI-Agent Kostenrechner 2026 — Multi-Modell Pipeline',
     'Kostenloser KI-Agent Kostenrechner. Mehrstufige Pipeline-Kosten mit GPT-4o, Claude und Gemini berechnen.',
     'https://apicalculators.com/de/ki-agent-kostenrechner.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/cout-agent-ia.html',
     'Calculateur Cout Agent IA 2026 — Pipeline Multi-Modele',
     'Calculateur gratuit de cout agent IA. Estimez les couts de pipeline multi-etapes avec GPT-4o, Claude et Gemini.',
     'https://apicalculators.com/fr/cout-agent-ia.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/yz-ajan-maliyet.html',
     'YZ Ajan Maliyet Hesaplayici 2026 — Cok Modelli Pipeline',
     'Ucretsiz YZ ajan maliyet hesaplayicisi. GPT-4o, Claude ve Gemini ile cok asamali pipeline maliyetlerini hesaplayin.',
     'https://apicalculators.com/tr/yz-ajan-maliyet.html'),
]:
    en_url='https://apicalculators.com/ai-agent-cost-calculator.html'
    chip=t(lang,'Juni 2026','Juin 2026','Haziran 2026')
    h1=t(lang,'<span class="em">KI-Agent</span> Kostenrechner','<span class="em">Agent IA</span> — Calculateur de Cout','<span class="em">YZ Ajan</span> Maliyet Hesaplayici')
    intro=t(lang,'Mehrstufige KI-Agent-Pipeline-Kosten berechnen. GPT-4o, Claude und Gemini fuer jeden Schritt konfigurieren.',
            'Calculez les couts de votre pipeline agent IA multi-etapes. Configurez GPT-4o, Claude et Gemini pour chaque etape.',
            'Cok asamali YZ ajan pipeline maliyetlerini hesaplayin. Her adim icin GPT-4o, Claude ve Gemini yapilandirin.')
    faq=[(t(lang,'Wie viel kostet ein KI-Agent pro Aufruf?','Combien coute un agent IA par execution?','YZ ajan calistirma basi ne kadar?'),
          t(lang,'Abhaengig vom Modell-Mix. Ein 3-Schritt-Agent mit GPT-4o mini kostet ca. $0,000020 pro Aufruf. Bei 10M Aufrufen/Monat = $200.',
            'Selon le mix de modeles. Un agent 3 etapes avec GPT-4o mini coute ~$0.000020 par execution. A 10M executions/mois = $200.',
            'Model karisimina gore degisir. GPT-4o mini ile 3 asamali ajan yaklasik $0.000020/calistirma. 10M calistirma/ay = $200.'))]
    rels=[('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o, Claude'),
          ('/embedding-api-cost.html','🔢','Embedding API',t(lang,'Fuer RAG-Pipelines','Pour pipelines RAG','RAG pipeline icin')),
          (nh,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),'')]
    html=make_page(lang,hl,og,gr,gp,nh,nb,nl,title,desc,canonical,en_url,chip,h1,intro,ag_calc(lang),AG_JS,AG_TABLE(lang),faq,rels,faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

# ── AI IMAGE ──────────────────────────────────────────────────────────────────
IMG_JS="""
var IMG={dalle3_std:0.040,dalle3_hd:0.080,dalle2:0.020,sd:0.002,mj_basic:0.016,sd_ultra:0.008};
function calcImg(){
  var m=IMG[document.getElementById('imgM').value];
  var cnt=parseFloat(document.getElementById('imgCnt').value)||0;
  var vars=parseFloat(document.getElementById('imgVar').value)||1;
  var total=cnt*vars*m;
  document.getElementById('imgTotal').textContent='$'+total.toFixed(2);
  document.getElementById('imgUnit').textContent='$'+m+'/image';
  document.getElementById('imgAnn').textContent='$'+(total*12).toFixed(2);
}
['imgM','imgCnt','imgVar'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcImg);el.addEventListener('change',calcImg);}});
calcImg();"""

def img_calc(lang):
    mod=t(lang,'Modell / Qualitaet','Modele / Qualite','Model / Kalite')
    cnt=t(lang,'Bilder / Monat','Images / mois','Gorsel / ay')
    var=t(lang,'Variationen pro Prompt','Variations par prompt','Prompt basi varyasyon')
    est=t(lang,'Gesch. Monatskosten','Cout mensuel estime','Tahmini aylik maliyet')
    unit=t(lang,'Preis pro Bild','Prix par image','Gorsel basi fiyat')
    ann=t(lang,'Jahresschaetzung','Estimation annuelle','Yillik tahmin')
    hdr=t(lang,'KI-Bildgenerierung Kostenrechner','Calculateur Cout Generation Image IA','YZ Gorsel Uretim Maliyet Hesaplayici')
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🎨 {hdr}</h2></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="imgM">{mod}</label>
        <select class="sel" id="imgM">
          <option value="dalle3_std">DALL-E 3 Standard — $0.040/img</option>
          <option value="dalle3_hd">DALL-E 3 HD — $0.080/img</option>
          <option value="dalle2">DALL-E 2 — $0.020/img</option>
          <option value="mj_basic">Midjourney Basic — $0.016/img</option>
          <option value="sd_ultra">SD Ultra — $0.008/img</option>
          <option value="sd">Stable Diffusion API — $0.002/img</option>
        </select></div>
      <div class="field"><label for="imgCnt">{cnt}</label>
        <input class="inp" id="imgCnt" type="number" value="5000" min="0"></div>
      <div class="field"><label for="imgVar">{var}</label>
        <input class="inp" id="imgVar" type="number" value="1" min="1"></div>
    </div>
    <div class="result">
      <div class="rlabel">{est}</div>
      <div class="big" id="imgTotal">$0</div>
      <div class="per">{"pro Monat" if lang=="de" else "par mois" if lang=="fr" else "aylik"}</div>
      <div class="breakdown">
        <div class="brow"><span>{unit}</span><b id="imgUnit">—</b></div>
        <div class="brow hl"><span>{ann}</span><b id="imgAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

IMG_TABLE=lambda lang:f'''<section class="sec">
  <h2>{"KI-Bildgenerierung Preise 2026" if lang=="de" else "Prix Generation Image IA 2026" if lang=="fr" else "YZ Gorsel Uretim Fiyatlari 2026"}</h2>
  <table class="ptable"><thead><tr><th>{"Modell" if lang=="de" else "Modele" if lang=="fr" else "Model"}</th><th>$/{"Bild" if lang=="de" else "image" if lang=="fr" else "gorsel"}</th><th>1K {"Bilder" if lang=="de" else "images" if lang=="fr" else "gorsel"}</th></tr></thead><tbody>
<tr class="best"><td><strong>Stable Diffusion API</strong><span class="badge">{"GUENSTIGSTE" if lang=="de" else "LE MOINS CHER" if lang=="fr" else "EN UCUZ"}</span></td><td class="mono">$0.002</td><td class="mono">$2</td></tr>
<tr><td><strong>SD Ultra</strong></td><td class="mono">$0.008</td><td class="mono">$8</td></tr>
<tr><td><strong>Midjourney Basic</strong></td><td class="mono">$0.016</td><td class="mono">$16</td></tr>
<tr><td><strong>DALL-E 2</strong></td><td class="mono">$0.020</td><td class="mono">$20</td></tr>
<tr><td><strong>DALL-E 3 Standard</strong></td><td class="mono">$0.040</td><td class="mono">$40</td></tr>
<tr><td><strong>DALL-E 3 HD</strong></td><td class="mono">$0.080</td><td class="mono">$80</td></tr>
</tbody></table></section>'''

for lang,hl,og,gr,gp,nh,nb,nl,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/ki-bildgenerierung-kosten.html',
     'KI-Bildgenerierung Kosten 2026 — DALL-E 3 vs Stable Diffusion',
     'Kostenloser KI-Bildgenerierung Kostenrechner. DALL-E 3, Midjourney und Stable Diffusion vergleichen.',
     'https://apicalculators.com/de/ki-bildgenerierung-kosten.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/cout-generation-image-ia.html',
     'Calculateur Cout Generation Image IA 2026 — DALL-E 3 vs Stable Diffusion',
     'Calculateur gratuit de cout generation image IA. Comparez DALL-E 3, Midjourney et Stable Diffusion.',
     'https://apicalculators.com/fr/cout-generation-image-ia.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/yz-gorsel-uretim-maliyet.html',
     'YZ Gorsel Uretim Maliyet Hesaplayici 2026 — DALL-E 3 vs Stable Diffusion',
     'Ucretsiz YZ gorsel uretim maliyet hesaplayicisi. DALL-E 3, Midjourney ve Stable Diffusion fiyatlarini karsilastirin.',
     'https://apicalculators.com/tr/yz-gorsel-uretim-maliyet.html'),
]:
    en_url='https://apicalculators.com/ai-image-cost-calculator.html'
    chip=t(lang,'Juni 2026','Juin 2026','Haziran 2026')
    h1=t(lang,'<span class="em">KI-Bildgenerierung</span> Kostenrechner','<span class="em">Generation Image IA</span> — Calculateur','<span class="em">YZ Gorsel Uretim</span> Maliyet Hesaplayici')
    intro=t(lang,'DALL-E 3, Midjourney und Stable Diffusion Kosten vergleichen.',
            'Comparez DALL-E 3, Midjourney et Stable Diffusion pour vos couts de generation d\'images.',
            'DALL-E 3, Midjourney ve Stable Diffusion gorsel uretim maliyetlerini karsilastirin.')
    faq=[(t(lang,'Was ist das guenstigste Bildgenerierungsmodell 2026?','Quel est le modele de generation d\'image le moins cher en 2026?','2026\'da en ucuz gorsel uretim modeli hangisi?'),
          t(lang,'Stable Diffusion API bei $0,002/Bild. Fuer verwaltete Qualitaet: DALL-E 3 Standard ($0,040/Bild) oder Midjourney ($0,016/Bild).',
            'Stable Diffusion API a $0.002/image. Pour la qualite geree: DALL-E 3 Standard ($0.040/image) ou Midjourney ($0.016/image).',
            'Stable Diffusion API $0.002/gorsel. Yonetilen kalite icin: DALL-E 3 Standard ($0.040/gorsel) veya Midjourney ($0.016/gorsel).'))]
    rels=[('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o, Claude'),
          ('/embedding-api-cost.html','🔢','Embedding API',''),
          (nh,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),'')]
    html=make_page(lang,hl,og,gr,gp,nh,nb,nl,title,desc,canonical,en_url,chip,h1,intro,img_calc(lang),IMG_JS,IMG_TABLE(lang),faq,rels,faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

# ── STRIPE vs PADDLE ──────────────────────────────────────────────────────────
PAY_JS="""
var PAY={stripe:{pct:2.9,flat:0.30,intl:1.5,extra:0},paddle:{pct:5.0,flat:0,intl:0,extra:0},lemon:{pct:5.0,flat:0.50,intl:0,extra:0}};
function calcPay(){
  var rev=parseFloat(document.getElementById('payRev').value)||0;
  var tx=parseFloat(document.getElementById('payTx').value)||0;
  var avg=tx>0?rev/tx:0;
  document.getElementById('payAvg').value='$'+avg.toFixed(2);
  ['stripe','paddle','lemon'].forEach(function(k){
    var p=PAY[k];
    var fee=(rev*p.pct/100)+(tx*p.flat)+(rev*p.intl/100);
    document.getElementById(k+'Fee').textContent='$'+fee.toFixed(2);
    document.getElementById(k+'Pct').textContent=(fee/rev*100).toFixed(1)+'%';
  });
}
['payRev','payTx'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcPay);el.addEventListener('change',calcPay);}});
calcPay();"""

def pay_calc(lang):
    rev=t(lang,'Monatsumsatz (USD)','Chiffre d\'affaires mensuel (USD)','Aylik ciro (USD)')
    tx=t(lang,'Transaktionen / Monat','Transactions / mois','Islem / ay')
    avg=t(lang,'Ø Transaktionswert','Valeur moy. transaction','Ort. islem degeri')
    hdr=t(lang,'Stripe vs Paddle Gebuehrenrechner','Calculateur Frais Stripe vs Paddle','Stripe vs Paddle Ucret Hesaplayici')
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>💳 {hdr}</h2></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="payRev">{rev}</label>
        <input class="inp" id="payRev" type="number" value="25000" min="0"></div>
      <div class="field"><label for="payTx">{tx}</label>
        <input class="inp" id="payTx" type="number" value="800" min="0"></div>
      <div class="field"><label>{avg}</label>
        <input class="inp" id="payAvg" type="text" readonly value="$31.25" style="opacity:.7;cursor:default"></div>
    </div>
    <div class="result">
      <div class="rlabel">{"Gebuehren nach Anbieter" if lang=="de" else "Frais par fournisseur" if lang=="fr" else "Saglayici basi ucret"}</div>
      <div class="breakdown" style="margin-top:12px">
        <div class="brow hl"><span>Stripe</span><b><span id="stripeFee">—</span> (<span id="stripePct">—</span>)</b></div>
        <div class="brow"><span>Paddle</span><b><span id="paddleFee">—</span> (<span id="paddlePct">—</span>)</b></div>
        <div class="brow"><span>Lemon Squeezy</span><b><span id="lemonFee">—</span> (<span id="lemonPct">—</span>)</b></div>
      </div>
    </div>
  </div>
</div>'''

PAY_TABLE=lambda lang:f'''<section class="sec">
  <h2>{"Stripe vs Paddle Gebuehrenvergleich" if lang=="de" else "Comparaison Frais Stripe vs Paddle" if lang=="fr" else "Stripe vs Paddle Ucret Karsilastirmasi"}</h2>
  <table class="ptable"><thead><tr><th>{"Anbieter" if lang=="de" else "Fournisseur" if lang=="fr" else "Saglayici"}</th><th>{"Gebuehr" if lang=="de" else "Frais" if lang=="fr" else "Ucret"}</th><th>{"MoR?" if True else ""}</th></tr></thead><tbody>
<tr><td><strong>Stripe</strong></td><td class="mono">2.9% + $0.30</td><td>No</td></tr>
<tr><td><strong>Paddle</strong></td><td class="mono">5.0%</td><td>Yes</td></tr>
<tr><td><strong>Lemon Squeezy</strong></td><td class="mono">5.0% + $0.50</td><td>Yes</td></tr>
</tbody></table></section>'''

for lang,hl,og,gr,gp,nh,nb,nl,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/stripe-vs-paddle-rechner.html',
     'Stripe vs Paddle Gebuehrenrechner 2026 — SaaS Zahlungsgebuehren',
     'Kostenloser Stripe vs Paddle Gebuehrenrechner. Monatsumsatz eingeben und Zahlungsgebuehren vergleichen.',
     'https://apicalculators.com/de/stripe-vs-paddle-rechner.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/comparateur-stripe-paddle.html',
     'Comparateur Frais Stripe vs Paddle 2026 — Paiement SaaS',
     'Calculateur gratuit Stripe vs Paddle. Entrez votre chiffre d\'affaires et comparez les frais de paiement.',
     'https://apicalculators.com/fr/comparateur-stripe-paddle.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/stripe-vs-paddle-hesaplayici.html',
     'Stripe vs Paddle Ucret Hesaplayici 2026 — SaaS Odeme Ucretleri',
     'Ucretsiz Stripe vs Paddle ucret hesaplayicisi. Aylik cironuzu girin ve odeme ucretlerini karsilastirin.',
     'https://apicalculators.com/tr/stripe-vs-paddle-hesaplayici.html'),
]:
    en_url='https://apicalculators.com/stripe-vs-paddle-calculator.html'
    chip=t(lang,'Juni 2026','Juin 2026','Haziran 2026')
    h1=t(lang,'<span class="em">Stripe vs Paddle</span> Gebuehrenrechner','<span class="em">Stripe vs Paddle</span> — Calculateur de Frais','<span class="em">Stripe vs Paddle</span> Ucret Hesaplayici')
    intro=t(lang,'Stripe, Paddle und Lemon Squeezy Zahlungsgebuehren vergleichen. Monatsumsatz eingeben und exakte Gebuehren erhalten.',
            'Comparez les frais de Stripe, Paddle et Lemon Squeezy. Entrez votre CA mensuel et obtenez les frais exacts.',
            'Stripe, Paddle ve Lemon Squeezy odeme ucretlerini karsilastirin. Aylik cirozunu girin, kesin ucretleri gorun.')
    faq=[(t(lang,'Ist Stripe guenstiger als Paddle?','Stripe est-il moins cher que Paddle?','Stripe mi Paddle mi daha ucuz?'),
          t(lang,'Auf Gebuehrenebene ja (2,9% vs 5%), aber Paddle handelt als Merchant of Record und uebernimmt Steuern global.',
            'Au niveau des frais oui (2.9% vs 5%), mais Paddle agit comme Merchant of Record et gere les taxes globalement.',
            'Ucret bazinda evet (2.9% vs 5%), ancak Paddle Merchant of Record olarak global vergileri ustleniyor.'))]
    rels=[('/auth-provider-cost.html','🔑',t(lang,'Auth-Anbieter Kosten','Cout Fournisseur Auth','Auth Saglayici Maliyeti'),t(lang,'Clerk vs Supabase','Clerk vs Supabase','Clerk vs Supabase')),
          ('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o, Claude'),
          (nh,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),'')]
    html=make_page(lang,hl,og,gr,gp,nh,nb,nl,title,desc,canonical,en_url,chip,h1,intro,pay_calc(lang),PAY_JS,PAY_TABLE(lang),faq,rels,faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

print('\nBatch 3 done. All missing pages created.')
