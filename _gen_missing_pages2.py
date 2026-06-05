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

FAQ_JS="""document.querySelectorAll('.qa .q').forEach(q=>{q.addEventListener('click',()=>{const qa=q.parentElement,open=qa.classList.toggle('open');const a=qa.querySelector('.a');if(a)a.style.maxHeight=open?'300px':'0';});});"""

def t(lang,de,fr,tr,en=''):
    return {'de':de,'fr':fr,'tr':tr,'en':en if en else de}.get(lang,en or de)

def make_page(lang,html_lang,og_locale,geo_region,geo_place,nav_home,nav_blog,nav_label,
              title,desc,canonical,en_url,chip,h1_html,intro,calc_html,calc_js,
              table_html,faq_items,related_links,schema_faq,schema_name):
    faq_schema=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in schema_faq]},ensure_ascii=False)
    app_schema=json.dumps({"@context":"https://schema.org","@type":"SoftwareApplication","name":schema_name,"applicationCategory":"DeveloperApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":canonical},ensure_ascii=False)
    bread=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"},{"@type":"ListItem","position":2,"name":schema_name}]},ensure_ascii=False)
    faq_html='\n'.join(f'<div class="qa"><div class="q">{q}<span class="plus">+</span></div><div class="a"><p>{a}</p></div></div>' for q,a in faq_items)
    rel_html='\n'.join(f'<a href="{u}" class="tool-link"><span class="ic">{ic}</span><div><div class="tl-name">{n}</div><div class="tl-desc">{d}</div></div></a>' for u,ic,n,d in related_links)
    rel_title=t(lang,'Verwandte Rechner','Calculateurs associes','Ilgili Hesaplayicilar','Related Calculators')
    price_note=t(lang,'Preise sind Schaetzungen','Prix estimatifs','Fiyatlar tahmindir','Prices are estimates')
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
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<script type="application/ld+json">{faq_schema}</script>
<script type="application/ld+json">{app_schema}</script>
<script type="application/ld+json">{bread}</script>
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
<section class="sec"><h2>FAQ</h2><div class="faq">{faq_html}</div></section>
<section class="sec"><h2>{rel_title}</h2><div class="tool-links">{rel_html}</div></section>
</div>
<footer><div class="wrap foot-in">
  <span>© 2026 <a href="{nav_home}">APICalculators</a></span>
  <span>{price_note}</span>
</div></footer>
<script>{FAQ_JS}</script>
<script>{calc_js}</script>
</body></html>"""

# ── EMBEDDING API ─────────────────────────────────────────────────────────────
EMB_JS="""
var EMB={text3small:0.020,text3large:0.130,ada002:0.100,cohere:0.100,voyage:0.120,jina:0.018};
var EMB_NAMES={text3small:'OpenAI text-3-small',text3large:'OpenAI text-3-large',ada002:'OpenAI ada-002',cohere:'Cohere embed-v3',voyage:'Voyage AI large-2',jina:'Jina AI v3'};
function calcEmb(){
  var m=document.getElementById('embM').value;
  var tok=parseFloat(document.getElementById('embTok').value)||0;
  var rate=EMB[m];
  var total=tok*rate;
  document.getElementById('embTotal').textContent='$'+total.toFixed(4);
  document.getElementById('embRate').textContent='$'+rate+'/1M';
  document.getElementById('embAnn').textContent='$'+(total*12).toFixed(2);
}
['embM','embTok'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcEmb);el.addEventListener('change',calcEmb);}});
calcEmb();"""

def emb_calc(lang):
    mod_label=t(lang,'Modell','Modele','Model')
    tok_label=t(lang,'Token / Monat (Mio.)','Tokens / mois (millions)','Token / ay (milyon)')
    est_label=t(lang,'Gesch. Kosten','Cout estime','Tahmini maliyet')
    rate_label=t(lang,'Preis / 1M Token','Tarif / 1M tokens','Oran / 1M token')
    ann_label=t(lang,'Jahresschaetzung','Estimation annuelle','Yillik tahmin')
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔢 {'Embedding API Kostenrechner' if lang=='de' else 'Calculateur Cout Embedding' if lang=='fr' else 'Embedding API Maliyet Hesaplayici'}</h2><p>{'Modell · Token · Ergebnis' if lang=='de' else 'Modele · Tokens · Resultat' if lang=='fr' else 'Model · Token · Sonuc'}</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="embM">{mod_label}</label>
        <select class="sel" id="embM">
          <option value="text3small">OpenAI text-3-small — $0.020/1M</option>
          <option value="text3large">OpenAI text-3-large — $0.130/1M</option>
          <option value="ada002">OpenAI ada-002 — $0.100/1M</option>
          <option value="cohere">Cohere embed-v3 — $0.100/1M</option>
          <option value="voyage">Voyage AI large-2 — $0.120/1M</option>
          <option value="jina">Jina AI v3 — $0.018/1M</option>
        </select></div>
      <div class="field"><label for="embTok">{tok_label}</label>
        <input class="inp" id="embTok" type="number" value="100" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">{est_label}</div>
      <div class="big" id="embTotal">$0</div>
      <div class="per">{"pro Monat" if lang=="de" else "par mois" if lang=="fr" else "aylik"}</div>
      <div class="breakdown">
        <div class="brow"><span>{rate_label}</span><b id="embRate">—</b></div>
        <div class="brow hl"><span>{ann_label}</span><b id="embAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

EMB_TABLE=lambda lang: f'''<section class="sec">
  <h2>{"Embedding API Preise 2026" if lang=="de" else "Prix API Embedding 2026" if lang=="fr" else "Embedding API Fiyatlari 2026"}</h2>
  <p class="sh-sub">{"USD pro 1 Million Token, Juni 2026" if lang=="de" else "USD par million de tokens, juin 2026" if lang=="fr" else "USD / 1 milyon token, Haziran 2026"}</p>
  <table class="ptable"><thead><tr><th>{"Modell" if lang=="de" else "Modele" if lang=="fr" else "Model"}</th><th>$/1M token</th><th>{"Dimensionen" if lang=="de" else "Dimensions" if lang=="fr" else "Boyut"}</th></tr></thead><tbody>
<tr class="best"><td><strong>Jina AI v3</strong><span class="badge">{"GUENSTIGSTE" if lang=="de" else "LE MOINS CHER" if lang=="fr" else "EN UCUZ"}</span></td><td class="mono">$0.018</td><td class="mono">1024</td></tr>
<tr><td><strong>OpenAI text-3-small</strong></td><td class="mono">$0.020</td><td class="mono">1536</td></tr>
<tr><td><strong>Cohere embed-v3</strong></td><td class="mono">$0.100</td><td class="mono">1024</td></tr>
<tr><td><strong>Voyage AI large-2</strong></td><td class="mono">$0.120</td><td class="mono">1536</td></tr>
<tr><td><strong>OpenAI text-3-large</strong></td><td class="mono">$0.130</td><td class="mono">3072</td></tr>
</tbody></table></section>'''

for lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/embedding-api-kosten.html',
     'Embedding API Kosten 2026 — OpenAI vs Cohere vs Voyage',
     'Kostenloser Embedding API Kostenrechner. OpenAI, Cohere, Voyage AI und Jina Preise vergleichen.',
     'https://apicalculators.com/de/embedding-api-kosten.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/cout-api-embedding.html',
     'Calculateur Cout API Embedding 2026 — OpenAI vs Cohere vs Voyage',
     'Calculateur gratuit de cout API embedding. Comparez OpenAI, Cohere, Voyage AI et Jina.',
     'https://apicalculators.com/fr/cout-api-embedding.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/embedding-api-maliyet.html',
     'Embedding API Maliyet Hesaplayici 2026 — OpenAI vs Cohere vs Voyage',
     'Ucretsiz embedding API maliyet hesaplayicisi. OpenAI, Cohere, Voyage AI ve Jina fiyatlarini karsilastirin.',
     'https://apicalculators.com/tr/embedding-api-maliyet.html'),
]:
    en_url='https://apicalculators.com/embedding-api-cost.html'
    chip=t(lang,'Juni 2026 · Aktuelle Preise','Juin 2026 · Prix mis a jour','Haziran 2026 · Guncel Fiyatlar')
    h1=t(lang,'<span class="em">Embedding API</span> Kostenrechner','<span class="em">Embedding API</span> — Calculateur de Cout','<span class="em">Embedding API</span> Maliyet Hesaplayici')
    intro=t(lang,'OpenAI, Cohere, Voyage AI und Jina Embedding-Kosten vergleichen. Token-Volumen eingeben und exakte Monatskosten erhalten.',
            'Comparez OpenAI, Cohere, Voyage AI et Jina pour vos embeddings. Entrez votre volume de tokens et obtenez le cout mensuel exact.',
            'OpenAI, Cohere, Voyage AI ve Jina embedding maliyetlerini karsilastirin. Token hacmini girin, aylik maliyeti gorun.')
    faq=[(t(lang,'Was ist das guenstigste Embedding-Modell 2026?','Quel est le modele embedding le moins cher en 2026?','2026\'da en ucuz embedding modeli hangisi?'),
          t(lang,'Jina AI v3 bei $0,018/1M Token ist das guenstigste. OpenAI text-3-small ($0,020/1M) ist die guenstigste OpenAI-Option.','Jina AI v3 a $0.018/1M tokens est le moins cher. OpenAI text-3-small ($0.020/1M) est la moins chere chez OpenAI.','Jina AI v3 $0.018/1M token ile en ucuz. OpenAI icinde text-3-small ($0.020/1M) en ucuz secenektir.')),
         (t(lang,'Was ist ein Embedding?','Qu\'est-ce qu\'un embedding?','Embedding nedir?'),
          t(lang,'Embeddings sind numerische Vektoren, die Text semantisch repraesentieren. Sie werden fuer RAG, Suche und Empfehlungssysteme verwendet.','Les embeddings sont des vecteurs numeriques representant semantiquement du texte. Utilises pour RAG, recherche et systemes de recommandation.','Embeddinglar, metni sayisal olarak temsil eden vektorlerdir. RAG, arama ve oneri sistemleri icin kullanilir.'))]
    rels=[('/vector-db-cost.html','🗄️',t(lang,'Vektordatenbank Kosten','Cout Base Vectorielle','Vektor DB Maliyeti'),'Pinecone vs Supabase'),
          ('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o, Claude'),
          (nav_home,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),t(lang,'Uebersicht','Accueil','Ana sayfa'))]
    schema_faq=[(f[0],f[1]) for f in faq]
    html=make_page(lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,title,desc,canonical,en_url,chip,h1,intro,
        emb_calc(lang),EMB_JS,EMB_TABLE(lang),faq,rels,schema_faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

# ── API GATEWAY ───────────────────────────────────────────────────────────────
GW_JS="""
var GW={aws:{req:3.50,xfer:0.09},cf:{req:0.50,xfer:0},kong:{req:2.00,xfer:0.05}};
function calcGw(){
  var p=GW[document.getElementById('gwProv').value];
  var req=parseFloat(document.getElementById('gwReqs').value)||0;
  var xfer=parseFloat(document.getElementById('gwXfer').value)||0;
  var reqCost=req*p.req;var xferCost=xfer*p.xfer;var total=reqCost+xferCost;
  document.getElementById('gwTotal').textContent='$'+total.toFixed(2);
  document.getElementById('gwReqCost').textContent='$'+reqCost.toFixed(2);
  document.getElementById('gwXferCost').textContent='$'+xferCost.toFixed(2);
  document.getElementById('gwAnn').textContent='$'+(total*12).toFixed(2);
}
['gwProv','gwReqs','gwXfer'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcGw);el.addEventListener('change',calcGw);}});
calcGw();"""

def gw_calc(lang):
    prov=t(lang,'Anbieter','Fournisseur','Saglayici')
    req=t(lang,'Anfragen (Mio./Monat)','Requetes (millions/mois)','Istek (milyon/ay)')
    xfer=t(lang,'Datenuebertragung (GB)','Transfert donnees (Go)','Veri transferi (GB)')
    est=t(lang,'Gesch. Kosten','Cout estime','Tahmini maliyet')
    rc=t(lang,'Anfragekosten','Cout requetes','Istek maliyeti')
    xc=t(lang,'Uebertragungskosten','Cout transfert','Transfer maliyeti')
    ann=t(lang,'Jahresschaetzung','Estimation annuelle','Yillik tahmin')
    title=t(lang,'API Gateway Kostenrechner','Calculateur Cout API Gateway','API Gateway Maliyet Hesaplayici')
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🔀 {title}</h2><p>{t(lang,"Anbieter · Anfragen · Ergebnis","Fournisseur · Requetes · Resultat","Saglayici · Istek · Sonuc")}</p></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="gwProv">{prov}</label>
        <select class="sel" id="gwProv">
          <option value="aws">AWS API Gateway — $3.50/M</option>
          <option value="cf">Cloudflare Workers — $0.50/M</option>
          <option value="kong">Kong Cloud — $2.00/M</option>
        </select></div>
      <div class="field"><label for="gwReqs">{req}</label>
        <input class="inp" id="gwReqs" type="number" value="10" min="0" step="0.1"></div>
      <div class="field"><label for="gwXfer">{xfer}</label>
        <input class="inp" id="gwXfer" type="number" value="50" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">{est}</div>
      <div class="big" id="gwTotal">$0</div>
      <div class="per">{"pro Monat" if lang=="de" else "par mois" if lang=="fr" else "aylik"}</div>
      <div class="breakdown">
        <div class="brow"><span>{rc}</span><b id="gwReqCost">—</b></div>
        <div class="brow"><span>{xc}</span><b id="gwXferCost">—</b></div>
        <div class="brow hl"><span>{ann}</span><b id="gwAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

GW_TABLE=lambda lang: f'''<section class="sec">
  <h2>{"API Gateway Preisvergleich 2026" if lang=="de" else "Comparaison API Gateway 2026" if lang=="fr" else "API Gateway Fiyat Karsilastirmasi 2026"}</h2>
  <table class="ptable"><thead><tr><th>{"Anbieter" if lang=="de" else "Fournisseur" if lang=="fr" else "Saglayici"}</th><th>$/M {"Anfragen" if lang=="de" else "requetes" if lang=="fr" else "istek"}</th><th>Egress</th></tr></thead><tbody>
<tr class="best"><td><strong>Cloudflare Workers</strong><span class="badge">{"GUENSTIGSTE" if lang=="de" else "LE MOINS CHER" if lang=="fr" else "EN UCUZ"}</span></td><td class="mono">$0.50</td><td class="mono">{"kostenlos" if lang=="de" else "gratuit" if lang=="fr" else "ucretsiz"}</td></tr>
<tr><td><strong>Kong Cloud</strong></td><td class="mono">$2.00</td><td class="mono">$0.05/GB</td></tr>
<tr><td><strong>AWS API Gateway</strong></td><td class="mono">$3.50</td><td class="mono">$0.09/GB</td></tr>
</tbody></table></section>'''

for lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/api-gateway-kosten.html',
     'API Gateway Kostenrechner 2026 — AWS vs Cloudflare vs Kong',
     'Kostenloser API Gateway Kostenrechner. AWS API Gateway, Cloudflare Workers und Kong vergleichen.',
     'https://apicalculators.com/de/api-gateway-kosten.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/cout-api-gateway.html',
     'Calculateur Cout API Gateway 2026 — AWS vs Cloudflare vs Kong',
     'Calculateur gratuit de cout API Gateway. Comparez AWS API Gateway, Cloudflare Workers et Kong.',
     'https://apicalculators.com/fr/cout-api-gateway.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/api-gateway-maliyet.html',
     'API Gateway Maliyet Hesaplayici 2026 — AWS vs Cloudflare vs Kong',
     'Ucretsiz API Gateway maliyet hesaplayicisi. AWS API Gateway, Cloudflare Workers ve Kong fiyatlarini karsilastirin.',
     'https://apicalculators.com/tr/api-gateway-maliyet.html'),
]:
    en_url='https://apicalculators.com/api-gateway-cost.html'
    chip=t(lang,'Juni 2026','Juin 2026','Haziran 2026')
    h1=t(lang,'<span class="em">API Gateway</span> Kostenrechner','<span class="em">API Gateway</span> — Calculateur de Cout','<span class="em">API Gateway</span> Maliyet Hesaplayici')
    intro=t(lang,'AWS API Gateway, Cloudflare Workers und Kong Traffic-Kosten vergleichen.',
            'Comparez AWS API Gateway, Cloudflare Workers et Kong pour vos couts de trafic.',
            'AWS API Gateway, Cloudflare Workers ve Kong trafik maliyetlerini karsilastirin.')
    faq=[(t(lang,'Was kostet AWS API Gateway pro Million Anfragen?','Combien coute AWS API Gateway par million de requetes?','AWS API Gateway 1 milyon istek icin ne kadar?'),
          t(lang,'$3,50 pro Million HTTP-Anfragen plus $0,09/GB Datenubertragung. Cloudflare Workers ist mit $0,50/M deutlich guenstiger.','$3.50 par million de requetes HTTP plus $0.09/Go de transfert. Cloudflare Workers est bien moins cher a $0.50/M.','$3.50/milyon HTTP istegi arti $0.09/GB veri transferi. Cloudflare Workers $0.50/M ile cok daha ucuz.'))]
    rels=[('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o, Claude'),
          ('/aws-lambda-calculator.html','⚡','AWS Lambda',t(lang,'Serverless Kosten','Cout serverless','Serverless maliyet')),
          (nav_home,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),'')]
    html=make_page(lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,title,desc,canonical,en_url,chip,h1,intro,
        gw_calc(lang),GW_JS,GW_TABLE(lang),faq,rels,faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

# ── STT/TTS ───────────────────────────────────────────────────────────────────
STT_JS="""
var STT={whisper:{rate:0.006,unit:'min'},gstt:{rate:0.024,unit:'min'},deepgram:{rate:0.0043,unit:'min'},openai_tts:{rate:15,unit:'1M_char'},openai_hd:{rate:30,unit:'1M_char'},elevenlabs:{rate:330,unit:'1M_char'},gtts:{rate:16,unit:'1M_char'}};
function calcStt(){
  var m=document.getElementById('sttM').value;
  var vol=parseFloat(document.getElementById('sttVol').value)||0;
  var pr=STT[m];var total=pr.unit==='min'?vol*pr.rate:vol/1e6*pr.rate;
  document.getElementById('sttTotal').textContent='$'+total.toFixed(2);
  document.getElementById('sttRate').textContent=pr.unit==='min'?'$'+pr.rate+'/min':'$'+pr.rate+'/1M chars';
  document.getElementById('sttAnn').textContent='$'+(total*12).toFixed(2);
}
['sttM','sttVol'].forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',calcStt);el.addEventListener('change',calcStt);}});
calcStt();"""

def stt_calc(lang):
    prov=t(lang,'Anbieter','Fournisseur','Saglayici')
    vol=t(lang,'Audiominuten / Monat','Minutes audio / mois','Ses dakikasi / ay')
    est=t(lang,'Gesch. Kosten','Cout estime','Tahmini maliyet')
    rate=t(lang,'Preis / Einheit','Tarif / unite','Birim fiyat')
    ann=t(lang,'Jahresschaetzung','Estimation annuelle','Yillik tahmin')
    title=t(lang,'STT & TTS API Kostenrechner','Calculateur Cout STT & TTS','STT & TTS API Maliyet Hesaplayici')
    return f'''<div class="calc-shell" id="calc">
  <div class="calc-header"><h2>🎙️ {title}</h2></div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="sttM">{prov}</label>
        <select class="sel" id="sttM">
          <optgroup label="STT"><option value="whisper">OpenAI Whisper — $0.006/min</option><option value="gstt">Google STT — $0.024/min</option><option value="deepgram">Deepgram Nova-2 — $0.0043/min</option></optgroup>
          <optgroup label="TTS"><option value="openai_tts">OpenAI TTS — $15/1M chars</option><option value="openai_hd">OpenAI TTS HD — $30/1M chars</option><option value="elevenlabs">ElevenLabs — $330/1M chars</option><option value="gtts">Google TTS — $16/1M chars</option></optgroup>
        </select></div>
      <div class="field"><label for="sttVol">{vol}</label>
        <input class="inp" id="sttVol" type="number" value="10000" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">{est}</div>
      <div class="big" id="sttTotal">$0</div>
      <div class="per">{"pro Monat" if lang=="de" else "par mois" if lang=="fr" else "aylik"}</div>
      <div class="breakdown">
        <div class="brow"><span>{rate}</span><b id="sttRate">—</b></div>
        <div class="brow hl"><span>{ann}</span><b id="sttAnn">—</b></div>
      </div>
    </div>
  </div>
</div>'''

STT_TABLE=lambda lang: f'''<section class="sec">
  <h2>{"STT & TTS Preise 2026" if lang=="de" else "Prix STT & TTS 2026" if lang=="fr" else "STT & TTS Fiyatlari 2026"}</h2>
  <table class="ptable"><thead><tr><th>{"Anbieter" if lang=="de" else "Fournisseur" if lang=="fr" else "Saglayici"}</th><th>{"Preis" if lang=="de" else "Prix" if lang=="fr" else "Fiyat"}</th><th>{"Typ" if lang=="de" else "Type" if lang=="fr" else "Tip"}</th></tr></thead><tbody>
<tr class="best"><td><strong>Deepgram Nova-2</strong><span class="badge">{"GUENSTIGSTE STT" if lang=="de" else "STT LE MOINS CHER" if lang=="fr" else "EN UCUZ STT"}</span></td><td class="mono">$0.0043/min</td><td>STT</td></tr>
<tr><td><strong>OpenAI Whisper</strong></td><td class="mono">$0.006/min</td><td>STT</td></tr>
<tr><td><strong>Google STT</strong></td><td class="mono">$0.024/min</td><td>STT</td></tr>
<tr><td><strong>OpenAI TTS</strong></td><td class="mono">$15/1M chars</td><td>TTS</td></tr>
<tr><td><strong>Google TTS</strong></td><td class="mono">$16/1M chars</td><td>TTS</td></tr>
<tr><td><strong>ElevenLabs</strong></td><td class="mono">$330/1M chars</td><td>TTS</td></tr>
</tbody></table></section>'''

for lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,path,title,desc,canonical in [
    ('de','de','de_DE','DE','Germany','/de/','/de/blog/','Rechner','de/stt-tts-api-kosten.html',
     'STT & TTS API Kosten 2026 — Whisper vs ElevenLabs vs Google',
     'Kostenloser STT/TTS API Kostenrechner. Whisper, ElevenLabs, Google Speech vergleichen.',
     'https://apicalculators.com/de/stt-tts-api-kosten.html'),
    ('fr','fr','fr_FR','FR','France','/fr/','/fr/blog/','Calculateurs','fr/cout-api-stt-tts.html',
     'Calculateur Cout STT & TTS 2026 — Whisper vs ElevenLabs vs Google',
     'Calculateur gratuit STT/TTS. Comparez Whisper, ElevenLabs et Google Speech.',
     'https://apicalculators.com/fr/cout-api-stt-tts.html'),
    ('tr','tr','tr_TR','TR','Turkey','/tr/','/tr/blog/','Hesaplayicilar','tr/stt-tts-api-maliyet.html',
     'STT & TTS API Maliyet 2026 — Whisper vs ElevenLabs vs Google',
     'Ucretsiz STT/TTS API maliyet hesaplayicisi. Whisper, ElevenLabs ve Google Speech fiyatlarini karsilastirin.',
     'https://apicalculators.com/tr/stt-tts-api-maliyet.html'),
]:
    en_url='https://apicalculators.com/stt-tts-api-cost.html'
    chip=t(lang,'Juni 2026','Juin 2026','Haziran 2026')
    h1=t(lang,'<span class="em">STT & TTS API</span> Kostenrechner','<span class="em">STT & TTS API</span> — Calculateur de Cout','<span class="em">STT & TTS API</span> Maliyet Hesaplayici')
    intro=t(lang,'Whisper, ElevenLabs, Google Speech und OpenAI TTS Kosten vergleichen.',
            'Comparez Whisper, ElevenLabs, Google Speech et OpenAI TTS.',
            'Whisper, ElevenLabs, Google Speech ve OpenAI TTS maliyetlerini karsilastirin.')
    faq=[(t(lang,'Was ist die guenstigste STT API 2026?','Quelle est l\'API STT la moins chere en 2026?','2026\'da en ucuz STT API hangisi?'),
          t(lang,'Deepgram Nova-2 bei $0,0043/Minute. OpenAI Whisper ($0,006/min) ist eine zuverlaessige Alternative.',
            'Deepgram Nova-2 a $0.0043/minute. OpenAI Whisper ($0.006/min) est une alternative fiable.',
            'Deepgram Nova-2 $0.0043/dakika. OpenAI Whisper ($0.006/dk) guvenilir bir alternatiftir.'))]
    rels=[('/llm-cost-calculator.html','🤖',t(lang,'LLM API Kosten','Cout API LLM','LLM API Maliyeti'),'GPT-4o'),
          ('/embedding-api-cost.html','🔢',t(lang,'Embedding API','Embedding API','Embedding API'),t(lang,'OpenAI vs Cohere','OpenAI vs Cohere','OpenAI vs Cohere')),
          (nav_home,'🧮',t(lang,'Alle Rechner','Tous les calculateurs','Tum Hesaplayicilar'),'')]
    html=make_page(lang,hl,og,geo_r,geo_p,nav_home,nav_blog,nav_label,title,desc,canonical,en_url,chip,h1,intro,
        stt_calc(lang),STT_JS,STT_TABLE(lang),faq,rels,faq,title)
    write(os.path.join(BASE,path.replace('/',os.sep)),html)
    print(f'✓ {path}')

print('\nBatch 2 done.')
