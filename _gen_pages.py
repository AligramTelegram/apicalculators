#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate dedicated calculator landing pages — Section 5."""
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

VULTR = 'https://www.vultr.com/?ref=9904710-9J'

# ── Shared CSS ─────────────────────────────────────────────────────────────────
CSS = """
:root{--bg:#0a0c10;--bg2:#0c0f15;--surface:#12161d;--surface2:#161b24;--border:#1d2530;--border2:#27313e;--text:#e8edf1;--muted:#8b97a4;--lime:#b8ff2e;--cyan:#4dd6ff;--amber:#ffb24d;--shadow:0 24px 60px -20px rgba(0,0,0,.7)}
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
.seg{display:flex;gap:6px}.seg button{flex:1;background:var(--bg);border:1px solid var(--border2);color:var(--muted);border-radius:9px;padding:9px;font-size:13px;font-weight:600;cursor:pointer;font-family:-apple-system,system-ui,sans-serif;transition:all .15s}
.seg button.on{background:var(--lime);color:#06210a;border-color:var(--lime)}
.result{background:radial-gradient(120% 120% at 100% 0%,rgba(184,255,46,.07),transparent 55%),var(--surface2);border:1px solid var(--border2);border-radius:16px;padding:22px;position:relative;overflow:hidden}
.result::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--lime),var(--cyan))}
.rlabel{font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.big{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:clamp(34px,7vw,50px);line-height:1;margin:8px 0 4px;color:var(--lime)}
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
.callout{border-radius:12px;padding:16px 20px;margin:20px 0;border-left:3px solid}.callout p{margin:0;color:#cdd6dd;font-size:14px}
.callout .cl{font-family:'Cascadia Code','Consolas',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;font-weight:700}
.callout.tip{background:rgba(184,255,46,.07);border-color:var(--lime)}.callout.tip .cl{color:var(--lime)}
.callout.info{background:rgba(77,214,255,.08);border-color:var(--cyan)}.callout.info .cl{color:var(--cyan)}
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
footer a{color:var(--muted)}.footer a:hover{color:var(--lime)}
"""

FAQ_JS = """
document.querySelectorAll('.qa').forEach(qa=>{
  qa.querySelector('.q').addEventListener('click',()=>{
    const open=qa.classList.contains('open');
    document.querySelectorAll('.qa').forEach(x=>{x.classList.remove('open');x.querySelector('.a').style.maxHeight=null;});
    if(!open){qa.classList.add('open');qa.querySelector('.a').style.maxHeight=qa.querySelector('.a').scrollHeight+'px';}
  });
});
"""

def nav(home_url='/'):
    return f"""<header class="nav">
  <div class="wrap nav-in">
    <a href="{home_url}" class="logo">API<b>Calculators</b></a>
    <nav class="nav-r"><a href="{home_url}">Calculators</a><a href="{home_url}blog/">Blog</a><a href="{home_url}about.html">About</a></nav>
  </div>
</header>"""

def footer(home_url='/'):
    return f"""<footer><div class="wrap foot-in">
  <span>© 2026 <a href="{home_url}">APICalculators</a> · Free infra cost tools</span>
  <span>Prices are estimates · verify before you ship</span>
</div></footer>"""

def faq_accordion(faqs):
    items = ''
    for q, a in faqs:
        items += f'<div class="qa"><div class="q">{q}<span class="plus">+</span></div><div class="a"><p>{a}</p></div></div>\n'
    return f'<div class="faq">{items}</div>'

def related_tools(tools):
    cards = ''
    for url, icon, name, desc in tools:
        cards += f'<a href="{url}" class="tool-link"><span class="ic">{icon}</span><div><div class="tl-name">{name}</div><div class="tl-desc">{desc}</div></div></a>\n'
    return f'<div class="tool-links">{cards}</div>'

def aff_block(headline, btns):
    b = ''.join(f'<a href="{url}" rel="sponsored" target="_blank" class="aff-btn">{label}</a>' for url, label in btns)
    return f'<div class="aff-box"><p>{headline}</p><div class="btns">{b}</div></div>'

def page(lang, canonical, title, desc, og_locale, hreflangs, geo, chip_text,
         h1_html, intro, calc_html, calc_js,
         sections_html, faq_items, schema_extra, related, home_url='/'):

    hl_tags = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{u}" />' for l, u in hreflangs)
    geo_tags = f'<meta name="geo.region" content="{geo[0]}" />\n<meta name="geo.placename" content="{geo[1]}" />' if geo else ''

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]
    }, ensure_ascii=False)

    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "url": canonical
    }, ensure_ascii=False)

    breadcrumb_parts = [
        {"@type": "ListItem", "position": 1, "name": "APICalculators", "item": "https://apicalculators.com"},
        {"@type": "ListItem", "position": 2, "name": title},
    ]
    breadcrumb_schema = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": breadcrumb_parts}, ensure_ascii=False)

    faq_accordion_html = faq_accordion(faq_items)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
{hl_tags}
<meta property="og:type" content="website">
<meta property="og:locale" content="{og_locale}" />
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://apicalculators.com/twitter-image.png">
{geo_tags}
<script type="application/ld+json">{faq_schema}</script>
<script type="application/ld+json">{article_schema}</script>
<script type="application/ld+json">{breadcrumb_schema}</script>
{schema_extra}
<style>{CSS}</style>
</head>
<body>
{nav(home_url)}
<section class="hero wrap">
  <span class="chip"><span class="dot"></span> {chip_text}</span>
  <h1 class="ph">{h1_html}</h1>
  <p class="intro">{intro}</p>
</section>
<div class="wrap">
{calc_html}
{sections_html}
<section class="sec">
  <h2>Frequently Asked Questions</h2>
  {faq_accordion_html}
</section>
<section class="sec">
  <h2>Related Calculators</h2>
  {related}
</section>
</div>
{footer(home_url)}
<script>
{FAQ_JS}
{calc_js}
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════════════════
# PAGE DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

pages = []  # (filepath, html)

# ── 1. LLM Cost Calculator (/llm-cost-calculator.html) ────────────────────────
llm_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🤖 LLM API Cost Calculator</h2>
    <p>Select model · Enter token volume · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="llmModel">Model</label>
        <select class="sel" id="llmModel">
          <option value="gpt4o">GPT-4o — $2.50/$10.00 per 1M</option>
          <option value="gpt4omini">GPT-4o mini — $0.15/$0.60 per 1M</option>
          <option value="o1">OpenAI o1 — $15.00/$60.00 per 1M</option>
          <option value="sonnet">Claude 3.5 Sonnet — $3.00/$15.00 per 1M</option>
          <option value="haiku">Claude 3.5 Haiku — $0.80/$4.00 per 1M</option>
          <option value="opus">Claude 3 Opus — $15.00/$75.00 per 1M</option>
          <option value="gempro">Gemini 1.5 Pro — $1.25/$5.00 per 1M</option>
          <option value="flash">Gemini 1.5 Flash — $0.075/$0.30 per 1M</option>
        </select></div>
      <div class="row2">
        <div class="field"><label for="llmIn">Input tokens / request</label>
          <input class="inp" id="llmIn" type="number" value="1500" min="0"></div>
        <div class="field"><label for="llmOut">Output tokens / request</label>
          <input class="inp" id="llmOut" type="number" value="500" min="0"></div>
      </div>
      <div class="field"><label for="llmReq">Requests / day</label>
        <input class="inp" id="llmReq" type="number" value="333" min="0"></div>
      <div class="field"><label>Period</label>
        <div class="seg" id="llmPeriod">
          <button data-v="1">Day</button><button class="on" data-v="30">Month</button><button data-v="365">Year</button>
        </div></div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated cost</div>
      <div class="big" id="llmTotal">$0</div>
      <div class="per" id="llmPer">— per month</div>
      <div class="breakdown">
        <div class="brow"><span>Input / output per 1M tokens</span><b id="llmPrice">—</b></div>
        <div class="brow"><span>Cost per request</span><b id="llmPerReq">—</b></div>
        <div class="brow"><span>Input cost</span><b id="llmInCost">—</b></div>
        <div class="brow"><span>Output cost</span><b id="llmOutCost">—</b></div>
        <div class="brow hl"><span>Total tokens</span><b id="llmTok">—</b></div>
      </div>
    </div>
  </div>
</div>"""

llm_calc_js = """
const LLM_PRICES = {
  gpt4o:    {name:'GPT-4o',         in:2.50,  out:10.00},
  gpt4omini:{name:'GPT-4o mini',    in:0.15,  out:0.60},
  o1:       {name:'OpenAI o1',      in:15.00, out:60.00},
  sonnet:   {name:'Claude 3.5 Sonnet',in:3.00,out:15.00},
  haiku:    {name:'Claude 3.5 Haiku',in:0.80, out:4.00},
  opus:     {name:'Claude 3 Opus',  in:15.00, out:75.00},
  gempro:   {name:'Gemini 1.5 Pro', in:1.25,  out:5.00},
  flash:    {name:'Gemini 1.5 Flash',in:0.075,out:0.30},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const fmt$=v=>{if(v===0)return'$0';if(v<0.01)return'$'+v.toFixed(5);if(v<1)return'$'+v.toFixed(3);if(v<1000)return'$'+v.toFixed(2);return'$'+Math.round(v).toLocaleString('en-US');};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
const intf=v=>Math.round(v).toLocaleString('en-US');
let llmDays=30;
$('llmPeriod').addEventListener('click',e=>{
  if(!e.target.dataset.v)return;
  [...$('llmPeriod').children].forEach(b=>b.classList.remove('on'));
  e.target.classList.add('on');llmDays=+e.target.dataset.v;calcLLM();
});
function calcLLM(){
  const m=LLM_PRICES[$('llmModel').value];
  const inTok=num($('llmIn').value),outTok=num($('llmOut').value),req=num($('llmReq').value);
  const inCostReq=inTok/1e6*m.in,outCostReq=outTok/1e6*m.out;
  const perReq=inCostReq+outCostReq;
  const reqTotal=req*llmDays;
  const total=perReq*reqTotal;
  $('llmTotal').textContent=big$(total);
  $('llmPer').textContent=llmDays===1?'— per day':llmDays===30?'— per month':'— per year';
  $('llmPrice').textContent='$'+m.in+' / $'+m.out;
  $('llmPerReq').textContent=fmt$(perReq);
  $('llmInCost').textContent=fmt$(inCostReq*reqTotal);
  $('llmOutCost').textContent=fmt$(outCostReq*reqTotal);
  $('llmTok').textContent=intf((inTok+outTok)*reqTotal)+' tok';
}
['llmModel','llmIn','llmOut','llmReq'].forEach(id=>$(id).addEventListener('input',calcLLM));
calcLLM();
"""

llm_sections = """
<section class="sec">
  <h2>2026 LLM API Pricing Table</h2>
  <p class="sh-sub">All prices in USD per 1 million tokens, pay-as-you-go, June 2026.</p>
  <table class="ptable">
    <thead><tr><th>Model</th><th>Input / 1M</th><th>Output / 1M</th><th>Context</th><th>Best for</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GPT-4o mini</strong><span class="badge">CHEAPEST</span></td><td class="mono">$0.15</td><td class="mono">$0.60</td><td class="mono">128K</td><td>High-volume tasks</td></tr>
      <tr><td><strong>Gemini 1.5 Flash</strong></td><td class="mono">$0.075</td><td class="mono">$0.30</td><td class="mono">1M</td><td>Ultra-high volume</td></tr>
      <tr><td><strong>Claude 3.5 Haiku</strong></td><td class="mono">$0.80</td><td class="mono">$4.00</td><td class="mono">200K</td><td>Quality on a budget</td></tr>
      <tr><td><strong>GPT-4o</strong></td><td class="mono">$2.50</td><td class="mono">$10.00</td><td class="mono">128K</td><td>General flagship</td></tr>
      <tr><td><strong>Claude 3.5 Sonnet</strong></td><td class="mono">$3.00</td><td class="mono">$15.00</td><td class="mono">200K</td><td>Coding & reasoning</td></tr>
      <tr><td><strong>Gemini 1.5 Pro</strong></td><td class="mono">$1.25</td><td class="mono">$5.00</td><td class="mono">1M</td><td>Long context tasks</td></tr>
      <tr><td><strong>OpenAI o1</strong></td><td class="mono">$15.00</td><td class="mono">$60.00</td><td class="mono">200K</td><td>Hard reasoning</td></tr>
      <tr><td><strong>Claude 3 Opus</strong></td><td class="mono">$15.00</td><td class="mono">$75.00</td><td class="mono">200K</td><td>Most capable Claude</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 50% off with Batch API</div><p>OpenAI, Anthropic, and Google all offer batch processing at 50% discount for async workloads (up to 24h latency). Zero quality difference.</p></div>
</section>
<section class="sec">
  <h2>Real-World Cost Examples</h2>
  <p class="sh-sub">Monthly cost for common production workloads.</p>
  <table class="ptable">
    <thead><tr><th>Workload</th><th>Volume</th><th>GPT-4o mini</th><th>GPT-4o</th><th>Claude Sonnet</th></tr></thead>
    <tbody>
      <tr><td>Customer support bot</td><td>10K req/day · 1K+300 tok</td><td class="mono best">$4.05</td><td class="mono">$82.50</td><td class="mono">$97.50</td></tr>
      <tr><td>Document summarizer</td><td>1K docs/day · 4K+800 tok</td><td class="mono best">$9.36</td><td class="mono">$204</td><td class="mono">$246</td></tr>
      <tr><td>Code review assistant</td><td>500 req/day · 3K+1K tok</td><td class="mono best">$9.45</td><td class="mono">$195</td><td class="mono">$247.50</td></tr>
      <tr><td>RAG Q&A system</td><td>5K req/day · 2K+500 tok</td><td class="mono best">$22.50</td><td class="mono">$450</td><td class="mono">$562.50</td></tr>
    </tbody>
  </table>
</section>""" + aff_block("Ready to build? Start with free cloud credits:", [(VULTR, "☁️ $300 Vultr credit"), ("[DIGITALOCEAN_AFFILIATE_LINK]", "🌊 $200 DigitalOcean")])

llm_faqs = [
    ("How much does GPT-4o cost per 1 million tokens?", "GPT-4o costs $2.50 per million input tokens and $10.00 per million output tokens (pay-as-you-go, June 2026)."),
    ("What is the cheapest LLM API in 2026?", "Gemini 1.5 Flash at $0.075/$0.30 per million tokens is the cheapest capable model. GPT-4o mini ($0.15/$0.60) is the cheapest OpenAI option."),
    ("How much does Claude 3.5 Sonnet cost?", "Claude 3.5 Sonnet costs $3.00 per million input tokens and $15.00 per million output tokens via the Anthropic API."),
    ("How do I reduce LLM API costs?", "Use cheaper models (GPT-4o mini vs GPT-4o is 16× cheaper). Enable Batch API for 50% off async workloads. Cache repeated prompts. Trim system prompts. Set max_tokens explicitly."),
    ("What is a token in LLM pricing?", "A token is roughly 4 characters or 0.75 words. A 1,000-word document is approximately 1,333 tokens. Most LLM APIs charge separately for input (prompt) and output (completion) tokens."),
]

llm_related = related_tools([
    ('/vector-db-cost.html', '🗄️', 'Vector DB Cost', 'Pinecone vs Supabase vs Qdrant'),
    ('/embedding-api-cost.html', '🔢', 'Embedding API Cost', 'OpenAI vs Cohere vs Voyage'),
    ('/ai-agent-cost-calculator.html', '🤖', 'AI Agent Cost', 'Multi-step pipeline pricing'),
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Lambda vs Vercel vs Cloudflare'),
])

pages.append((
    os.path.join(BASE, 'llm-cost-calculator.html'),
    page('en', 'https://apicalculators.com/llm-cost-calculator.html',
         'LLM API Cost Calculator 2026 — GPT-4o, Claude & Gemini Pricing',
         'Free LLM cost calculator. Compare GPT-4o, Claude 3.5, Gemini pricing instantly. Enter token volume → get exact monthly cost. No signup.',
         'en_US',
         [('en','https://apicalculators.com/llm-cost-calculator.html'),
          ('de','https://apicalculators.com/de/llm-kostenrechner.html'),
          ('fr','https://apicalculators.com/fr/calculateur-cout-llm.html'),
          ('tr','https://apicalculators.com/tr/llm-maliyet-hesaplayici.html'),
          ('x-default','https://apicalculators.com/llm-cost-calculator.html')],
         None,
         'June 2026 · Updated LLM pricing',
         '<span class="em">LLM API Cost</span> Calculator',
         'Compare GPT-4o, Claude 3.5 Sonnet, Gemini, and 5 more models. Enter your token volume and request count — see exact monthly costs. Free, no signup, runs in your browser.',
         llm_calc_html, llm_calc_js, llm_sections, llm_faqs, '', llm_related)
))

# ── 2. AWS Lambda Calculator (/aws-lambda-calculator.html) ────────────────────
lambda_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>⚡ Serverless Cost Calculator</h2>
    <p>Select provider · Enter invocations and duration · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="slProvider">Provider</label>
        <select class="sel" id="slProvider">
          <option value="lambda">AWS Lambda</option>
          <option value="cf">Cloudflare Workers</option>
          <option value="vercel">Vercel Functions</option>
          <option value="gcp">Google Cloud Functions</option>
        </select></div>
      <div class="field"><label for="slInvoke">Invocations / month (millions)</label>
        <input class="inp" id="slInvoke" type="number" value="10" min="0" step="0.1"></div>
      <div class="row2">
        <div class="field"><label for="slDuration">Avg duration (ms)</label>
          <input class="inp" id="slDuration" type="number" value="200" min="1"></div>
        <div class="field"><label for="slMemory">Memory (GB)</label>
          <select class="sel" id="slMemory">
            <option value="0.128">128 MB</option>
            <option value="0.256" selected>256 MB</option>
            <option value="0.512">512 MB</option>
            <option value="1">1 GB</option>
            <option value="2">2 GB</option>
          </select></div>
      </div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="slTotal">$0</div>
      <div class="per" id="slPer">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Invocation cost</span><b id="slInvCost">—</b></div>
        <div class="brow"><span>Compute cost</span><b id="slCompCost">—</b></div>
        <div class="brow hl"><span>Annual estimate</span><b id="slAnnual">—</b></div>
      </div>
    </div>
  </div>
</div>"""

lambda_calc_js = """
const SL_PRICES = {
  lambda:{inv:0.0000002,gb_sec:0.0000166725,free_inv:1000000,free_gb:400000,label:'AWS Lambda'},
  cf:    {inv:0.0000003,gb_sec:0.000012,    free_inv:1000000,free_gb:0,     label:'Cloudflare Workers'},
  vercel:{inv:0.0000004,gb_sec:0.000018,    free_inv:0,      free_gb:0,     label:'Vercel Functions'},
  gcp:   {inv:0.0000004,gb_sec:0.0000250,   free_inv:2000000,free_gb:400000,label:'GCP Cloud Functions'},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
function calcServerless(){
  const prov=$('slProvider').value;
  const p=SL_PRICES[prov];
  const inv=num($('slInvoke').value)*1e6;
  const dur=num($('slDuration').value);
  const mem=num($('slMemory').value);
  const billable_inv=Math.max(0,inv-p.free_inv);
  const gb_sec=inv*(dur/1000)*mem;
  const billable_gb=Math.max(0,gb_sec-p.free_gb);
  const inv_cost=billable_inv*p.inv;
  const comp_cost=billable_gb*p.gb_sec;
  const total=inv_cost+comp_cost;
  $('slTotal').textContent=big$(total);
  $('slPer').textContent='per month ('+p.label+')';
  $('slInvCost').textContent=big$(inv_cost);
  $('slCompCost').textContent=big$(comp_cost);
  $('slAnnual').textContent=big$(total*12);
}
['slProvider','slInvoke','slDuration','slMemory'].forEach(id=>$(id).addEventListener('change',calcServerless));
['slInvoke','slDuration'].forEach(id=>$(id).addEventListener('input',calcServerless));
calcServerless();
"""

lambda_sections = """
<section class="sec">
  <h2>Serverless Pricing Comparison 2026</h2>
  <p class="sh-sub">Monthly cost for 10M invocations · 256MB · 200ms avg duration.</p>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>Free tier</th><th>Invocation price</th><th>Compute price</th><th>10M inv / 200ms / 256MB</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>AWS Lambda</strong><span class="badge">MOST POPULAR</span></td><td class="mono">1M inv/mo + 400K GB-s</td><td class="mono">$0.20/M</td><td class="mono">$0.0000166725/GB-s</td><td class="mono">$3.47</td></tr>
      <tr><td><strong>Cloudflare Workers</strong></td><td class="mono">1M req/day (free plan)</td><td class="mono">$0.30/M (paid)</td><td class="mono">$0.012/M GB-s</td><td class="mono">$2.70</td></tr>
      <tr><td><strong>Vercel Functions</strong></td><td class="mono">100K GB-s/mo</td><td class="mono">$0.40/M</td><td class="mono">$0.018/GB-s</td><td class="mono">$4.00</td></tr>
      <tr><td><strong>GCP Cloud Functions</strong></td><td class="mono">2M inv/mo + 400K GB-s</td><td class="mono">$0.40/M</td><td class="mono">$0.0000250/GB-s</td><td class="mono">$3.20</td></tr>
    </tbody>
  </table>
  <div class="callout info"><div class="cl">⚠ Hidden costs</div><p>AWS API Gateway adds $3.50/M requests — often doubling your Lambda bill. CloudWatch Logs add $0.50/GB. NAT Gateway in VPC adds $0.045/GB. Factor these in for real-world costs.</p></div>
</section>
<section class="sec">
  <h2>When to Choose Lambda vs Alternatives</h2>
  <table class="ptable">
    <thead><tr><th>Use case</th><th>Best choice</th><th>Reason</th></tr></thead>
    <tbody>
      <tr><td>REST API · under 30ms</td><td>Cloudflare Workers</td><td>Edge execution, no cold start</td></tr>
      <tr><td>REST API · 100ms–500ms</td><td class="best">AWS Lambda</td><td>Free tier, mature ecosystem</td></tr>
      <tr><td>Heavy compute · 1–5s</td><td class="best">AWS Lambda</td><td>Up to 10GB memory, 15min timeout</td></tr>
      <tr><td>Next.js / React SSR</td><td>Vercel Functions</td><td>Zero-config deployment</td></tr>
      <tr><td>Event-driven batch</td><td class="best">AWS Lambda</td><td>Native integration with SQS, SNS, S3</td></tr>
    </tbody>
  </table>
</section>""" + aff_block("Deploy serverless today — free tiers available:", [("[VERCEL_AFFILIATE_LINK]", "▲ Deploy on Vercel"), ("[CLOUDFLARE_AFFILIATE_LINK]", "🔶 Cloudflare Workers")])

lambda_faqs = [
    ("How much does AWS Lambda cost per million requests?", "After the free tier (1M/month), Lambda costs $0.20 per million invocations plus compute. A 256MB function at 200ms avg = ~$3.47/month for 10M invocations total."),
    ("Is Cloudflare Workers cheaper than Lambda?", "For short-duration (under 30ms) high-frequency APIs, yes. Workers at $0.30/M beats Lambda. For longer compute (500ms+) or when you need AWS integrations, Lambda is often better value."),
    ("What is the AWS Lambda free tier?", "1 million free invocations per month + 400,000 GB-seconds of compute per month, forever (not just 12-month trial). Enough for ~2M requests at 256MB/200ms."),
    ("Does Lambda have cold starts?", "Yes. Cold starts add 100–500ms latency for the first request after a function is idle. Mitigation: Provisioned Concurrency ($0.0000041271/GB-s), keeping functions warm with scheduled pings, or choosing Cloudflare Workers (no cold starts)."),
    ("What is the maximum timeout for AWS Lambda?", "15 minutes (900 seconds). For longer workloads use AWS Step Functions or ECS Fargate instead."),
]

lambda_related = related_tools([
    ('/api-gateway-cost.html', '🔀', 'API Gateway Cost', 'AWS vs Cloudflare vs Kong pricing'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS Comparison', 'When VPS beats serverless'),
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Run LLMs on your serverless infra'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'Multi-step pipeline pricing'),
])

pages.append((
    os.path.join(BASE, 'aws-lambda-calculator.html'),
    page('en', 'https://apicalculators.com/aws-lambda-calculator.html',
         'AWS Lambda Cost Calculator 2026 — Free Serverless Pricing Tool',
         'Free AWS Lambda cost calculator. Compare Lambda vs Cloudflare Workers vs Vercel Functions. Enter invocations and duration → get exact monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/aws-lambda-calculator.html'),
          ('de','https://apicalculators.com/de/aws-lambda-rechner.html'),
          ('fr','https://apicalculators.com/fr/calculateur-cout-llm.html'),
          ('tr','https://apicalculators.com/tr/aws-lambda-maliyet.html'),
          ('x-default','https://apicalculators.com/aws-lambda-calculator.html')],
         None,
         'June 2026 · Official AWS Lambda pricing',
         '<span class="em">AWS Lambda</span> Cost Calculator',
         'Compare Lambda, Cloudflare Workers, Vercel, and GCP Functions pricing. Enter invocations, duration, memory → see exact monthly bills. Free, no signup.',
         lambda_calc_html, lambda_calc_js, lambda_sections, lambda_faqs, '', lambda_related)
))

# ── 3. Vector DB Cost (/vector-db-cost.html) ──────────────────────────────────
vec_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🗄️ Vector Database Cost Calculator</h2>
    <p>Select provider · Enter vector count and queries · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="vecProvider">Provider</label>
        <select class="sel" id="vecProvider">
          <option value="pinecone">Pinecone (Serverless)</option>
          <option value="supabase">Supabase pgvector</option>
          <option value="qdrant">Qdrant Cloud</option>
          <option value="weaviate">Weaviate Cloud</option>
        </select></div>
      <div class="row2">
        <div class="field"><label for="vecCount">Vectors (thousands)</label>
          <input class="inp" id="vecCount" type="number" value="1000" min="1"></div>
        <div class="field"><label for="vecDim">Dimensions</label>
          <select class="sel" id="vecDim">
            <option value="384">384 (MiniLM)</option>
            <option value="768">768 (BERT)</option>
            <option value="1536" selected>1536 (OpenAI)</option>
            <option value="3072">3072 (text-3-large)</option>
          </select></div>
      </div>
      <div class="field"><label for="vecQ">Queries / month (thousands)</label>
        <input class="inp" id="vecQ" type="number" value="100" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="vecTotal">$0</div>
      <div class="per" id="vecName">— select provider</div>
      <div class="breakdown">
        <div class="brow"><span>Storage size</span><b id="vecStore">—</b></div>
        <div class="brow"><span>Storage cost</span><b id="vecStoreCost">—</b></div>
        <div class="brow"><span>Query cost</span><b id="vecQCost">—</b></div>
        <div class="brow hl"><span>Base fee</span><b id="vecBase">—</b></div>
      </div>
    </div>
  </div>
</div>"""

vec_calc_js = """
const VEC_PROVIDERS = {
  pinecone:{name:'Pinecone',      base:0,  storagePerGB:0.33, queryPerMillion:16.00},
  supabase:{name:'Supabase',      base:25, storagePerGB:0.125,queryPerMillion:0},
  qdrant:  {name:'Qdrant Cloud',  base:0,  storagePerGB:9.00, queryPerMillion:0},
  weaviate:{name:'Weaviate Cloud',base:25, storagePerGB:0.50, queryPerMillion:10.00},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const fmt$=v=>{if(v===0)return'$0';if(v<0.01)return'$'+v.toFixed(4);if(v<1)return'$'+v.toFixed(3);if(v<1000)return'$'+v.toFixed(2);return'$'+Math.round(v).toLocaleString('en-US');};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
function calcVec(){
  const prov=$('vecProvider').value;
  const p=VEC_PROVIDERS[prov];
  const n=num($('vecCount').value)*1000;
  const d=num($('vecDim').value);
  const q=num($('vecQ').value)*1000;
  const bytes=n*d*4*1.5;
  const gb=bytes/(1024**3);
  const storeCost=gb*p.storagePerGB;
  const qCost=q/1e6*p.queryPerMillion;
  const total=p.base+storeCost+qCost;
  $('vecTotal').textContent=big$(total);
  $('vecName').textContent='— '+p.name;
  $('vecStore').textContent=gb<1?(gb*1024).toFixed(1)+' MB':gb.toFixed(2)+' GB';
  $('vecStoreCost').textContent=fmt$(storeCost);
  $('vecQCost').textContent=p.queryPerMillion?fmt$(qCost):'included';
  $('vecBase').textContent=p.base?fmt$(p.base)+' /mo':'no base fee';
}
['vecProvider','vecCount','vecDim','vecQ'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcVec),el.addEventListener('input',calcVec);
});
calcVec();
"""

vec_sections = """
<section class="sec">
  <h2>Vector Database Pricing 2026</h2>
  <p class="sh-sub">Comparison for 1M vectors · 1536 dimensions · 100K queries/month.</p>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>Free tier</th><th>Storage</th><th>Queries</th><th>1M vec / 100K q</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Supabase pgvector</strong><span class="badge">BEST VALUE</span></td><td>500MB + 2 projects</td><td class="mono">$0.125/GB</td><td>Included</td><td class="mono">~$27</td></tr>
      <tr><td><strong>Qdrant Cloud</strong></td><td>1GB storage</td><td class="mono">$9.00/GB</td><td>Included</td><td class="mono">~$54</td></tr>
      <tr><td><strong>Weaviate Cloud</strong></td><td>1 sandbox cluster</td><td class="mono">$0.50/GB</td><td class="mono">$10/M</td><td class="mono">~$28</td></tr>
      <tr><td><strong>Pinecone Serverless</strong></td><td>100K vectors</td><td class="mono">$0.33/GB</td><td class="mono">$16/M RU</td><td class="mono">~$20</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Self-host Qdrant</div><p>Qdrant on a $6/mo Hetzner VPS handles 1–5M vectors easily. Total cost: ~$6–10/mo vs $50+ on managed cloud. Requires ops knowledge.</p></div>
</section>""" + aff_block("Start building your vector search:", [("[SUPABASE_AFFILIATE_LINK]", "⚡ Build on Supabase"), ("[PINECONE_AFFILIATE_LINK]", "🌲 Try Pinecone free")])

vec_faqs = [
    ("What is the cheapest vector database in 2026?", "For under 5M vectors: Supabase pgvector at $25/month (queries included). For 50M+ vectors: self-hosted Qdrant on spot VMs at $150–300/month. Pinecone Serverless is cheapest for very small (under 100K) with the free tier."),
    ("How much does Pinecone cost for 1 million vectors?", "Approximately $15–30/month depending on query volume. Storage ~$3 for 1536-dim vectors, plus $16 per million read units. At 100K queries/month expect ~$20."),
    ("Is pgvector as good as Pinecone?", "For most production workloads yes. pgvector in Supabase or RDS supports HNSW indexing, IVFFlat, and handles millions of vectors well. Pinecone has better managed scaling and dedicated infrastructure for very high query rates."),
    ("How many vectors can Qdrant handle?", "Qdrant Cloud handles hundreds of millions of vectors. Self-hosted Qdrant on a 16GB RAM server can store ~10M 1536-dim vectors in memory, or 50M+ with memory-mapped storage (slower queries)."),
    ("What is a vector dimension?", "Dimensions are the size of each embedding vector. OpenAI text-embedding-3-small produces 1536-dim vectors. Larger dimensions = more storage and cost. You can reduce OpenAI embeddings to 256 or 512 dimensions with minimal quality loss."),
]

vec_related = related_tools([
    ('/embedding-api-cost.html', '🔢', 'Embedding API Cost', 'Cost to generate your vectors'),
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Full AI stack cost'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Self-host your vector DB'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'RAG pipeline total cost'),
])

pages.append((
    os.path.join(BASE, 'vector-db-cost.html'),
    page('en', 'https://apicalculators.com/vector-db-cost.html',
         'Vector Database Cost Comparison 2026 — Pinecone vs Supabase vs Qdrant',
         'Free vector database cost calculator. Compare Pinecone, Supabase pgvector, Qdrant, and Weaviate pricing. Enter vector count → get exact monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/vector-db-cost.html'),
          ('x-default','https://apicalculators.com/vector-db-cost.html')],
         None,
         'June 2026 · Vector DB pricing',
         '<span class="em">Vector Database</span> Cost Comparison',
         'Compare Pinecone, Supabase pgvector, Qdrant, and Weaviate costs. Enter your vector count, dimensions, and query volume — see exact monthly prices.',
         vec_calc_html, vec_calc_js, vec_sections, vec_faqs, '', vec_related)
))

# ── 4. Cloud VPS Comparison (/cloud-vps-comparison.html) ──────────────────────
vps_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🖥️ Cloud VPS Cost Comparison</h2>
    <p>Select specs · See cheapest provider · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="row2">
        <div class="field"><label for="cloudCpu">vCPU</label>
          <select class="sel" id="cloudCpu">
            <option value="1">1 vCPU</option>
            <option value="2" selected>2 vCPU</option>
            <option value="4">4 vCPU</option>
            <option value="8">8 vCPU</option>
          </select></div>
        <div class="field"><label for="cloudRam">RAM</label>
          <select class="sel" id="cloudRam">
            <option value="1">1 GB</option>
            <option value="4" selected>4 GB</option>
            <option value="8">8 GB</option>
            <option value="16">16 GB</option>
          </select></div>
      </div>
      <div class="field"><label for="cloudCount">Number of servers</label>
        <input class="inp" id="cloudCount" type="number" value="1" min="1"></div>
    </div>
    <div class="result">
      <div class="rlabel">Cheapest monthly cost</div>
      <div class="big" id="cloudTotal">$0</div>
      <div class="per" id="cloudPer">per month</div>
      <div class="breakdown" id="cloudCmp"></div>
    </div>
  </div>
</div>"""

vps_calc_js = """
const CLOUD_PRICES = {
  hetzner:      {2:{4:4.5},4:{8:8.5},8:{16:17}},
  vultr:        {1:{1:6},2:{4:24},4:{8:48},8:{16:96}},
  digitalocean: {1:{1:6},2:{4:18},4:{8:36},8:{16:72}},
  linode:       {1:{1:5},2:{4:18},4:{8:36}},
};
const PROVIDERS = [
  {id:'hetzner',name:'Hetzner'},
  {id:'vultr',name:'Vultr'},
  {id:'digitalocean',name:'DigitalOcean'},
  {id:'linode',name:'Linode'},
];
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);return'$0';};
function calcCloud(){
  const cpu=parseInt($('cloudCpu').value);
  const ram=parseInt($('cloudRam').value);
  const cnt=parseInt($('cloudCount').value)||1;
  const results=[];
  PROVIDERS.forEach(p=>{
    const tier=CLOUD_PRICES[p.id]||{};
    let best=null;
    Object.keys(tier).forEach(c=>{
      if(parseInt(c)>=cpu){
        Object.keys(tier[c]).forEach(r=>{
          if(parseInt(r)>=ram){
            const price=tier[c][r];
            if(!best||price<best.price) best={price,cpu:c,ram:r};
          }
        });
      }
    });
    if(best) results.push({name:p.name,price:best.price*cnt,cpu:best.cpu,ram:best.ram});
  });
  if(!results.length){$('cloudTotal').textContent='N/A';return;}
  results.sort((a,b)=>a.price-b.price);
  const cheapest=results[0];
  $('cloudTotal').textContent=big$(cheapest.price);
  $('cloudPer').textContent='per month — cheapest: '+cheapest.name;
  const cmp=$('cloudCmp');
  cmp.innerHTML='';
  results.forEach(r=>{
    const row=document.createElement('div');
    row.className='brow'+(r===cheapest?' hl':'');
    row.innerHTML='<span>'+r.name+' ('+r.cpu+'vCPU/'+r.ram+'GB)</span><b>$'+r.price.toFixed(2)+'/mo</b>';
    cmp.appendChild(row);
  });
}
['cloudCpu','cloudRam','cloudCount'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcCloud),el.addEventListener('input',calcCloud);
});
calcCloud();
"""

vps_sections = """
<section class="sec">
  <h2>Cloud VPS Pricing Comparison 2026</h2>
  <p class="sh-sub">Entry-level and mid-range plans, per month.</p>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>2 vCPU / 4 GB</th><th>4 vCPU / 8 GB</th><th>Egress free</th><th>Locations</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Hetzner</strong><span class="badge">CHEAPEST EU</span></td><td class="mono">€4.50/mo</td><td class="mono">€8.50/mo</td><td class="mono">20 TB/mo</td><td>DE, FI, US, SG</td></tr>
      <tr><td><strong>Linode / Akamai</strong></td><td class="mono">$18/mo</td><td class="mono">$36/mo</td><td class="mono">1 TB/mo</td><td>11 regions</td></tr>
      <tr><td><strong>DigitalOcean</strong></td><td class="mono">$18/mo</td><td class="mono">$36/mo</td><td class="mono">2 TB/mo</td><td>15 regions</td></tr>
      <tr><td><strong>Vultr</strong></td><td class="mono">$24/mo</td><td class="mono">$48/mo</td><td class="mono">3 TB/mo</td><td>32 regions</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Egress matters</div><p>Hetzner includes 20 TB/month free egress. DigitalOcean charges $0.01/GB after 2TB. At 10TB/month: Hetzner $0 extra, DigitalOcean $80 extra. Factor this into total cost.</p></div>
</section>
<section class="sec">
  <h2>Which VPS for Which Use Case?</h2>
  <table class="ptable">
    <thead><tr><th>Use case</th><th>Best choice</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td>EU SaaS (GDPR)</td><td class="best">Hetzner</td><td>Cheapest + EU data residency + GDPR compliant</td></tr>
      <tr><td>Global reach</td><td>Vultr</td><td>32 locations across 6 continents</td></tr>
      <tr><td>Managed databases</td><td>DigitalOcean</td><td>Managed Postgres, Redis, Kafka</td></tr>
      <tr><td>Budget dev server</td><td class="best">Hetzner</td><td>CX22 at €4.50 = best $/resource ratio</td></tr>
      <tr><td>TR audience (latency)</td><td>Hetzner / DO</td><td>Frankfurt or Amsterdam closest to Istanbul</td></tr>
    </tbody>
  </table>
</section>""" + aff_block("Deploy your server today:", [(VULTR, "🖥️ $300 Vultr credit"), ("[HETZNER_AFFILIATE_LINK]", "🇩🇪 Hetzner — cheapest EU"), ("[DIGITALOCEAN_AFFILIATE_LINK]", "🌊 $200 DigitalOcean")])

vps_faqs = [
    ("Is Hetzner cheaper than DigitalOcean?", "Yes — 3–5× cheaper for EU specs. Hetzner CX22 (2 vCPU/4 GB) is €4.50/mo vs DigitalOcean's $18/mo. Trade-off: fewer global locations (4 vs 15 regions)."),
    ("Which VPS is best for a small SaaS?", "Hetzner for EU audience (cheapest + GDPR). Vultr for global reach (32 locations). DigitalOcean if you need managed Postgres or Redis alongside compute."),
    ("How much does a cloud VPS cost per month?", "Entry-level (1 vCPU/1GB): $5–6/mo. Mid-range (2 vCPU/4GB): €4.50 (Hetzner) to $24 (Vultr). Production (4 vCPU/8GB): €8.50 (Hetzner) to $48 (Vultr). Hetzner is consistently 3–5× cheaper for EU."),
    ("What is egress pricing in cloud VPS?", "Egress is outbound bandwidth from your server to the internet. Hetzner includes 20TB/month free. DigitalOcean gives 2TB free then $0.01/GB. At 10TB/month egress: Hetzner adds $0, DigitalOcean adds $80 to your bill."),
    ("Is Vultr or DigitalOcean better?", "Vultr has 32 global locations (vs DO's 15) and is slightly more flexible. DigitalOcean has a more mature managed services ecosystem (Managed Kubernetes, Databases, App Platform). For pure compute, Vultr is often cheaper with $300 new account credit."),
]

vps_related = related_tools([
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Lambda vs VPS comparison'),
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Run LLMs on your VPS'),
    ('/api-gateway-cost.html', '🔀', 'API Gateway Cost', 'Add API gateway to your VPS'),
    ('/embedding-api-cost.html', '🔢', 'Embedding Cost', 'Self-host embedding models'),
])

pages.append((
    os.path.join(BASE, 'cloud-vps-comparison.html'),
    page('en', 'https://apicalculators.com/cloud-vps-comparison.html',
         'Cloud VPS Cost Comparison 2026 — Hetzner vs DigitalOcean vs Vultr',
         'Free cloud VPS cost comparison. Compare Hetzner, DigitalOcean, Vultr, and Linode pricing. Select your specs → see cheapest provider instantly.',
         'en_US',
         [('en','https://apicalculators.com/cloud-vps-comparison.html'),
          ('de','https://apicalculators.com/de/cloud-vps-kostenvergleich.html'),
          ('fr','https://apicalculators.com/fr/comparateur-vps-cloud.html'),
          ('x-default','https://apicalculators.com/cloud-vps-comparison.html')],
         None,
         'June 2026 · VPS pricing',
         '<span class="em">Cloud VPS</span> Cost Comparison',
         'Compare Hetzner, DigitalOcean, Vultr, and Linode VPS pricing. Select CPU and RAM requirements — see cheapest provider instantly. Free, no signup.',
         vps_calc_html, vps_calc_js, vps_sections, vps_faqs, '', vps_related)
))

# ── 5. Embedding API Cost (/embedding-api-cost.html) ─────────────────────────
emb_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🔢 Embedding API Cost Calculator</h2>
    <p>Select model · Enter token volume · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="embModel">Model</label>
        <select class="sel" id="embModel">
          <option value="text3small">OpenAI text-embedding-3-small</option>
          <option value="text3large">OpenAI text-embedding-3-large</option>
          <option value="ada002">OpenAI ada-002</option>
          <option value="cohere">Cohere embed-v3</option>
          <option value="voyage">Voyage AI voyage-2</option>
          <option value="jina">Jina Embeddings v2</option>
        </select></div>
      <div class="row2">
        <div class="field"><label for="embTokens">Tokens / month (millions)</label>
          <input class="inp" id="embTokens" type="number" value="10" min="0" step="0.1"></div>
        <div class="field"><label for="embDocs">Documents / month</label>
          <input class="inp" id="embDocs" type="number" value="100000" min="1"></div>
      </div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="embTotal">$0</div>
      <div class="per" id="embPer">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Price per 1M tokens</span><b id="embRate">—</b></div>
        <div class="brow"><span>Avg tokens per document</span><b id="embPerDoc">—</b></div>
        <div class="brow hl"><span>Annual estimate</span><b id="embAnnual">—</b></div>
      </div>
    </div>
  </div>
</div>"""

emb_calc_js = """
const EMB_PRICES = {
  text3small:{name:'text-embedding-3-small',rate:0.020,dim:1536},
  text3large:{name:'text-embedding-3-large',rate:0.130,dim:3072},
  ada002:    {name:'ada-002',               rate:0.100,dim:1536},
  cohere:    {name:'Cohere embed-v3',       rate:0.100,dim:1024},
  voyage:    {name:'Voyage AI voyage-2',    rate:0.120,dim:1024},
  jina:      {name:'Jina v2',              rate:0.018,dim:768},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
function calcEmbedding(){
  const key=$('embModel').value;
  const p=EMB_PRICES[key];
  const tokM=num($('embTokens').value);
  const docs=num($('embDocs').value)||1;
  const total=tokM*p.rate;
  const tok_per_doc=docs>0?((tokM*1e6)/docs).toFixed(0):'—';
  $('embTotal').textContent=big$(total);
  $('embPer').textContent='per month — '+p.name;
  $('embRate').textContent='$'+p.rate+'/1M';
  $('embPerDoc').textContent=tok_per_doc+' tokens';
  $('embAnnual').textContent=big$(total*12);
}
['embModel','embTokens','embDocs'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcEmbedding),el.addEventListener('input',calcEmbedding);
});
calcEmbedding();
"""

emb_sections = """
<section class="sec">
  <h2>Embedding API Pricing 2026</h2>
  <p class="sh-sub">Cost per million tokens, June 2026.</p>
  <table class="ptable">
    <thead><tr><th>Model</th><th>Price / 1M tokens</th><th>Dimensions</th><th>Best for</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Jina Embeddings v2</strong><span class="badge">CHEAPEST</span></td><td class="mono">$0.018</td><td class="mono">768</td><td>High-volume, cost-sensitive</td></tr>
      <tr><td><strong>OpenAI text-3-small</strong></td><td class="mono">$0.020</td><td class="mono">1536</td><td>Best quality/cost for most RAG</td></tr>
      <tr><td><strong>Cohere embed-v3</strong></td><td class="mono">$0.100</td><td class="mono">1024</td><td>Multilingual, enterprise</td></tr>
      <tr><td><strong>OpenAI ada-002</strong></td><td class="mono">$0.100</td><td class="mono">1536</td><td>Legacy, being phased out</td></tr>
      <tr><td><strong>Voyage AI voyage-2</strong></td><td class="mono">$0.120</td><td class="mono">1024</td><td>Code search, technical docs</td></tr>
      <tr><td><strong>OpenAI text-3-large</strong></td><td class="mono">$0.130</td><td class="mono">3072</td><td>Max quality, high-precision RAG</td></tr>
    </tbody>
  </table>
</section>""" + aff_block("Store your embeddings — start free:", [("[SUPABASE_AFFILIATE_LINK]", "⚡ Build on Supabase")])

emb_faqs = [
    ("How much does the OpenAI embedding API cost?", "text-embedding-3-small costs $0.020 per million tokens (cheapest OpenAI option). text-embedding-3-large costs $0.130/M. For 100K documents at ~300 tokens each (30M tokens), text-3-small costs $0.60 total."),
    ("What is the cheapest embedding API in 2026?", "Jina Embeddings v2 at $0.018/M tokens is cheapest. OpenAI text-3-small at $0.020/M is close and has excellent quality. For self-hosted, sentence-transformers (free) on a $6/mo Hetzner VPS is near-zero cost at scale."),
    ("What dimensions should I use for embeddings?", "1536 dimensions (OpenAI text-3-small default) works well for most RAG use cases. You can truncate OpenAI text-3-small to 512 or 256 dimensions with minimal quality loss and significant storage savings. Only use 3072-dim for very high-precision retrieval needs."),
    ("How many tokens per document for embeddings?", "Typical documents: 100-word paragraph ~133 tokens, 1-page document ~700 tokens, 10-page report ~7,000 tokens. Most embedding models have 8,191 token input limits — chunk longer documents."),
]

emb_related = related_tools([
    ('/vector-db-cost.html', '🗄️', 'Vector DB Cost', 'Store your embeddings'),
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Full RAG pipeline cost'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Self-host embedding models'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'Total agent pipeline cost'),
])

pages.append((
    os.path.join(BASE, 'embedding-api-cost.html'),
    page('en', 'https://apicalculators.com/embedding-api-cost.html',
         'Embedding API Cost Calculator 2026 — OpenAI vs Cohere vs Voyage',
         'Free embedding API cost calculator. Compare OpenAI text-embedding-3-small, Cohere, Voyage, and Jina pricing. Enter token volume → get monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/embedding-api-cost.html'),
          ('x-default','https://apicalculators.com/embedding-api-cost.html')],
         None,
         'June 2026 · Embedding API pricing',
         '<span class="em">Embedding API</span> Cost Calculator',
         'Compare OpenAI text-embedding-3-small, Cohere, Voyage AI, and Jina pricing. Enter token volume → see exact monthly cost. Free, no signup.',
         emb_calc_html, emb_calc_js, emb_sections, emb_faqs, '', emb_related)
))

# ── 6. AI Agent Cost Calculator (/ai-agent-cost-calculator.html) ──────────────
agent_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>⛓️ AI Agent Cost Calculator</h2>
    <p>Define your pipeline steps · Enter run volume · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label>Step 1 — Planner LLM</label>
        <select class="sel" id="agM1">
          <option value="gpt4omini">GPT-4o mini ($0.15/$0.60)</option>
          <option value="flash">Gemini 1.5 Flash ($0.075/$0.30)</option>
          <option value="gpt4o">GPT-4o ($2.50/$10.00)</option>
          <option value="sonnet">Claude 3.5 Sonnet ($3.00/$15.00)</option>
        </select></div>
      <div class="field"><label>Step 2 — Worker LLM</label>
        <select class="sel" id="agM2">
          <option value="gpt4o" selected>GPT-4o ($2.50/$10.00)</option>
          <option value="sonnet">Claude 3.5 Sonnet ($3.00/$15.00)</option>
          <option value="gpt4omini">GPT-4o mini ($0.15/$0.60)</option>
          <option value="haiku">Claude 3.5 Haiku ($0.80/$4.00)</option>
        </select></div>
      <div class="field"><label>Step 3 — Critic/Verifier LLM</label>
        <select class="sel" id="agM3">
          <option value="gpt4omini">GPT-4o mini ($0.15/$0.60)</option>
          <option value="haiku">Claude 3.5 Haiku ($0.80/$4.00)</option>
          <option value="gpt4o">GPT-4o ($2.50/$10.00)</option>
          <option value="sonnet">Claude 3.5 Sonnet ($3.00/$15.00)</option>
        </select></div>
      <div class="field"><label for="agRuns">Agent runs / month</label>
        <input class="inp" id="agRuns" type="number" value="1000" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="agTotal">$0</div>
      <div class="per" id="agPer">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Cost per agent run</span><b id="agPerRun">—</b></div>
        <div class="brow"><span>Step 1 (planner) total</span><b id="agS1">—</b></div>
        <div class="brow"><span>Step 2 (worker) total</span><b id="agS2">—</b></div>
        <div class="brow hl"><span>Step 3 (critic) total</span><b id="agS3">—</b></div>
        <div class="brow amber"><span>Annual estimate</span><b id="agAnnual">—</b></div>
      </div>
    </div>
  </div>
</div>"""

agent_calc_js = """
const AG_LLM = {
  gpt4o:    {in:2.50, out:10.00},
  gpt4omini:{in:0.15, out:0.60},
  sonnet:   {in:3.00, out:15.00},
  haiku:    {in:0.80, out:4.00},
  gempro:   {in:1.25, out:5.00},
  flash:    {in:0.075,out:0.30},
};
const AG_STEPS=[
  {model:'agM1',in_tok:500, out_tok:100},
  {model:'agM2',in_tok:3000,out_tok:800},
  {model:'agM3',in_tok:1500,out_tok:300},
];
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
const fmt$=v=>{if(v===0)return'$0';if(v<0.000001)return'$'+v.toFixed(8);if(v<0.01)return'$'+v.toFixed(6);return'$'+v.toFixed(4);};
function calcAgent(){
  const runs=num($('agRuns').value);
  const step_costs=AG_STEPS.map(s=>{
    const m=AG_LLM[$( s.model).value];if(!m)return 0;
    return (s.in_tok/1e6)*m.in+(s.out_tok/1e6)*m.out;
  });
  const per_run=step_costs.reduce((a,b)=>a+b,0);
  const total=per_run*runs;
  $('agTotal').textContent=big$(total);
  $('agPer').textContent='per month';
  $('agPerRun').textContent=fmt$(per_run);
  $('agS1').textContent=big$(step_costs[0]*runs);
  $('agS2').textContent=big$(step_costs[1]*runs);
  $('agS3').textContent=big$(step_costs[2]*runs);
  $('agAnnual').textContent=big$(total*12);
}
['agM1','agM2','agM3','agRuns'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcAgent),el.addEventListener('input',calcAgent);
});
calcAgent();
"""

agent_sections = """
<section class="sec">
  <h2>AI Agent Pipeline Cost Breakdown</h2>
  <p class="sh-sub">Typical 3-step agent: planner → worker → critic. Monthly cost for 1,000 runs.</p>
  <table class="ptable">
    <thead><tr><th>Pipeline</th><th>Step 1 (Planner)</th><th>Step 2 (Worker)</th><th>Step 3 (Critic)</th><th>Cost / 1K runs</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Budget</strong><span class="badge">CHEAPEST</span></td><td>Flash</td><td>GPT-4o mini</td><td>GPT-4o mini</td><td class="mono">~$0.80</td></tr>
      <tr><td><strong>Balanced</strong></td><td>GPT-4o mini</td><td>GPT-4o</td><td>GPT-4o mini</td><td class="mono">~$27</td></tr>
      <tr><td><strong>High Quality</strong></td><td>GPT-4o</td><td>Claude Sonnet</td><td>GPT-4o</td><td class="mono">~$95</td></tr>
      <tr><td><strong>Maximum</strong></td><td>Claude Sonnet</td><td>Claude Sonnet</td><td>Claude Sonnet</td><td class="mono">~$185</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Mix models strategically</div><p>Use cheap models (Flash, GPT-4o mini) for planning and verification. Reserve expensive models (GPT-4o, Claude Sonnet) only for the main worker step. This cuts costs 5–10× with minimal quality loss.</p></div>
</section>""" + aff_block("Deploy your AI agent infrastructure:", [(VULTR, "☁️ $300 Vultr credit"), ("[DIGITALOCEAN_AFFILIATE_LINK]", "🌊 $200 DigitalOcean")])

agent_faqs = [
    ("How much does an AI agent cost per run?", "A 3-step agent (planner + worker + critic) with GPT-4o mini costs ~$0.0008 per run. With GPT-4o for the worker step: ~$0.027 per run. For 1,000 runs/month: $0.80 to $27 depending on model choice."),
    ("What is the cheapest LLM for AI agents?", "Gemini 1.5 Flash ($0.075/$0.30 per 1M tokens) and GPT-4o mini ($0.15/$0.60) are cheapest. Use Flash for planning/verification steps and GPT-4o or Claude Sonnet only for the main reasoning step."),
    ("How do I reduce AI agent costs?", "Use cheap models for routing, planning, and verification. Cache repeated tool calls. Limit max steps per agent run. Use streaming to detect early termination. Set hard token limits per step."),
    ("What is an AI agent pipeline?", "A multi-step LLM workflow where each step uses an LLM call: (1) Planner decides what to do, (2) Worker executes tasks (often with tool use), (3) Critic checks the result. Total cost = sum of all LLM calls per run × number of runs."),
]

agent_related = related_tools([
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Per-model pricing'),
    ('/embedding-api-cost.html', '🔢', 'Embedding Cost', 'RAG component cost'),
    ('/vector-db-cost.html', '🗄️', 'Vector DB Cost', 'Agent memory storage'),
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Run agents on Lambda'),
])

pages.append((
    os.path.join(BASE, 'ai-agent-cost-calculator.html'),
    page('en', 'https://apicalculators.com/ai-agent-cost-calculator.html',
         'AI Agent Cost Calculator 2026 — Multi-Model Pipeline Pricing',
         'Free AI agent cost calculator. Estimate multi-step LLM pipeline costs for GPT-4o, Claude, Gemini agents. Enter run volume → see monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/ai-agent-cost-calculator.html'),
          ('x-default','https://apicalculators.com/ai-agent-cost-calculator.html')],
         None,
         'June 2026 · AI agent pricing',
         '<span class="em">AI Agent</span> Cost Calculator',
         'Estimate multi-step AI agent pipeline costs. Configure planner, worker, and critic LLMs — see exact cost per run and monthly totals. Free, no signup.',
         agent_calc_html, agent_calc_js, agent_sections, agent_faqs, '', agent_related)
))

# ── Write all pages ────────────────────────────────────────────────────────────
written = []
for path, html in pages:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    written.append(os.path.basename(path))
    print(f'  Written: {os.path.basename(path)} ({len(html):,} chars)')

print(f'\nTotal: {len(written)} pages written')
