#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate remaining dedicated pages — Stripe, API Gateway, STT, Image + DE/FR/TR."""
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'
VULTR = 'https://www.vultr.com/?ref=9904710-9J'

# Execute full _gen_pages to get all shared functions and HTML fragments
_src = open(os.path.join(BASE, '_gen_pages.py'), encoding='utf-8').read()
# Remove the final write block so it doesn't re-write files
_src_no_write = _src.split('# ── Write all pages')[0]
exec(compile(_src_no_write, '_gen_pages.py', 'exec'), globals())
pages = []  # reset pages list

pages = []

# ── 7. API Gateway Cost (/api-gateway-cost.html) ─────────────────────────────
gw_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🔀 API Gateway Cost Calculator</h2>
    <p>Select provider · Enter request volume and transfer · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="gwProvider">Provider</label>
        <select class="sel" id="gwProvider">
          <option value="aws">AWS API Gateway</option>
          <option value="cf">Cloudflare Workers</option>
          <option value="kong">Kong Konnect</option>
        </select></div>
      <div class="field"><label for="gwReqs">Requests / month (millions)</label>
        <input class="inp" id="gwReqs" type="number" value="10" min="0" step="0.5"></div>
      <div class="field"><label for="gwTransfer">Data transfer out (GB/month)</label>
        <input class="inp" id="gwTransfer" type="number" value="50" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="gwTotal">$0</div>
      <div class="per" id="gwPer">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Request cost</span><b id="gwReqCost">—</b></div>
        <div class="brow"><span>Transfer cost</span><b id="gwXferCost">—</b></div>
        <div class="brow hl"><span>Annual estimate</span><b id="gwAnnual">—</b></div>
      </div>
    </div>
  </div>
</div>"""

gw_calc_js = """
const GW_PRICES = {
  aws: {per_m:3.50, per_gb:0.09,  label:'AWS API Gateway',  free_m:0},
  cf:  {per_m:0.50, per_gb:0.00,  label:'Cloudflare Workers',free_m:10},
  kong:{per_m:2.00, per_gb:0.05,  label:'Kong Konnect',     free_m:0},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
function calcGateway(){
  const prov=$('gwProvider').value;
  const p=GW_PRICES[prov];
  const reqs=Math.max(0,num($('gwReqs').value)-p.free_m);
  const xfer=num($('gwTransfer').value);
  const req_cost=reqs*p.per_m;
  const xfer_cost=xfer*p.per_gb;
  const total=req_cost+xfer_cost;
  $('gwTotal').textContent=big$(total);
  $('gwPer').textContent='per month — '+p.label;
  $('gwReqCost').textContent=big$(req_cost);
  $('gwXferCost').textContent=big$(xfer_cost);
  $('gwAnnual').textContent=big$(total*12);
}
['gwProvider','gwReqs','gwTransfer'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcGateway),el.addEventListener('input',calcGateway);
});
calcGateway();
"""

gw_sections = """
<section class="sec">
  <h2>API Gateway Pricing 2026</h2>
  <p class="sh-sub">Monthly cost for 10M requests · 50 GB transfer.</p>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>Requests</th><th>Transfer</th><th>Free tier</th><th>10M req / 50GB</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Cloudflare Workers</strong><span class="badge">CHEAPEST</span></td><td class="mono">$0.50/M</td><td class="mono">Free</td><td>10M req/day (free plan)</td><td class="mono">$0</td></tr>
      <tr><td><strong>Kong Konnect</strong></td><td class="mono">$2.00/M</td><td class="mono">$0.05/GB</td><td>1M req/mo</td><td class="mono">$20.50</td></tr>
      <tr><td><strong>AWS API Gateway</strong></td><td class="mono">$3.50/M</td><td class="mono">$0.09/GB</td><td>1M calls/mo (12 mo)</td><td class="mono">$39.50</td></tr>
    </tbody>
  </table>
  <div class="callout info"><div class="cl">⚠ AWS hidden cost</div><p>AWS API Gateway at $3.50/M often doubles your Lambda bill. A Lambda function at $3.47/month for 10M invocations + API Gateway at $35 = $38.47 total. Cloudflare Workers ($5/mo Paid plan) is often far cheaper for simple APIs.</p></div>
</section>""" + aff_block("Deploy your API Gateway:", [("[CLOUDFLARE_AFFILIATE_LINK]", "🔶 Cloudflare Workers")])

gw_faqs = [
    ("How much does AWS API Gateway cost?", "$3.50 per million API calls after the free tier (1M calls/month for 12 months). Plus $0.09/GB data transfer. For 10M calls/month: ~$31.50 requests + transfer costs."),
    ("Is Cloudflare Workers cheaper than AWS API Gateway?", "Yes, significantly. Cloudflare Workers free plan: 100K requests/day. Paid plan ($5/mo): 10M requests included, then $0.50/M. For 10M requests with no transfer cost vs AWS at $35, Cloudflare is 7× cheaper."),
    ("Do I need an API Gateway with AWS Lambda?", "Not necessarily. Lambda Function URLs (free) expose Lambda directly over HTTPS. API Gateway adds routing, rate limiting, auth, and usage plans. For simple APIs, skip API Gateway and save $3.50/M."),
    ("What is the difference between API Gateway and load balancer?", "API Gateway handles HTTP request routing, auth, rate limiting, and API versioning. Load balancers distribute traffic across servers. For serverless APIs use API Gateway; for traditional servers use ALB ($0.008/LCU-hour, often cheaper than API Gateway)."),
]

gw_related = related_tools([
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Lambda behind your gateway'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Self-host Kong or Nginx'),
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'LLM API behind your gateway'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'Agent pipeline with gateway'),
])

pages.append((
    os.path.join(BASE, 'api-gateway-cost.html'),
    page('en', 'https://apicalculators.com/api-gateway-cost.html',
         'API Gateway Pricing Calculator 2026 — AWS vs Cloudflare vs Kong',
         'Free API gateway cost calculator. Compare AWS API Gateway, Cloudflare Workers, and Kong pricing. Enter request volume → get exact monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/api-gateway-cost.html'),
          ('x-default','https://apicalculators.com/api-gateway-cost.html')],
         None,
         'June 2026 · API Gateway pricing',
         '<span class="em">API Gateway</span> Cost Calculator',
         'Compare AWS API Gateway, Cloudflare Workers, and Kong Konnect pricing. Enter request volume and data transfer → see exact monthly cost.',
         gw_calc_html, gw_calc_js, gw_sections, gw_faqs, '', gw_related)
))

# ── 8. STT/TTS API Cost (/stt-tts-api-cost.html) ─────────────────────────────
stt_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🎙️ STT / TTS API Cost Calculator</h2>
    <p>Select provider · Enter volume · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="sttModel">Provider / Model</label>
        <select class="sel" id="sttModel">
          <optgroup label="Speech-to-Text (STT)">
            <option value="whisper">OpenAI Whisper ($0.006/min)</option>
            <option value="deepgram">Deepgram Nova-2 ($0.0043/min)</option>
            <option value="google-stt">Google STT ($0.024/min)</option>
          </optgroup>
          <optgroup label="Text-to-Speech (TTS)">
            <option value="openai-tts">OpenAI TTS ($0.015/1K chars)</option>
            <option value="openai-tts-hd">OpenAI TTS HD ($0.030/1K chars)</option>
            <option value="elevenlabs">ElevenLabs ($0.330/1K chars)</option>
            <option value="google-tts">Google TTS ($0.016/1K chars)</option>
          </optgroup>
        </select></div>
      <div class="field"><label for="sttVol" id="sttVolLabel">Minutes / month</label>
        <input class="inp" id="sttVol" type="number" value="10000" min="0"></div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="sttTotal">$0</div>
      <div class="per" id="sttPer">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Rate</span><b id="sttRate">—</b></div>
        <div class="brow hl"><span>Annual estimate</span><b id="sttAnnual">—</b></div>
      </div>
    </div>
  </div>
</div>"""

stt_calc_js = """
const STT_RATES = {
  'whisper':      {type:'stt',rate:0.006,  label:'OpenAI Whisper'},
  'deepgram':     {type:'stt',rate:0.0043, label:'Deepgram Nova-2'},
  'google-stt':   {type:'stt',rate:0.024,  label:'Google STT'},
  'openai-tts':   {type:'tts',rate:0.015,  label:'OpenAI TTS'},
  'openai-tts-hd':{type:'tts',rate:0.030,  label:'OpenAI TTS HD'},
  'elevenlabs':   {type:'tts',rate:0.330,  label:'ElevenLabs'},
  'google-tts':   {type:'tts',rate:0.016,  label:'Google TTS'},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
function calcStt(){
  const key=$('sttModel').value;
  const p=STT_RATES[key];
  const vol=num($('sttVol').value);
  const total=p.type==='stt'?vol*p.rate:(vol/1000)*p.rate;
  const lbl=$('sttVolLabel');
  lbl.textContent=p.type==='stt'?'Minutes / month':'Characters / month (thousands)';
  $('sttTotal').textContent=big$(total);
  $('sttPer').textContent='per month — '+p.label;
  $('sttRate').textContent=p.type==='stt'?'$'+p.rate+'/min':'$'+p.rate+'/1K chars';
  $('sttAnnual').textContent=big$(total*12);
}
$('sttModel').addEventListener('change',calcStt);
$('sttVol').addEventListener('input',calcStt);
calcStt();
"""

stt_sections = """
<section class="sec">
  <h2>STT/TTS API Pricing 2026</h2>
  <table class="ptable">
    <thead><tr><th>Provider</th><th>Type</th><th>Price</th><th>Quality</th><th>10K min / 1M chars</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Deepgram Nova-2</strong><span class="badge">CHEAPEST STT</span></td><td>STT</td><td class="mono">$0.0043/min</td><td>Excellent</td><td class="mono">$43</td></tr>
      <tr><td><strong>OpenAI Whisper</strong></td><td>STT</td><td class="mono">$0.006/min</td><td>Excellent</td><td class="mono">$60</td></tr>
      <tr><td><strong>Google STT</strong></td><td>STT</td><td class="mono">$0.024/min</td><td>Good</td><td class="mono">$240</td></tr>
      <tr class="best"><td><strong>OpenAI TTS</strong><span class="badge">CHEAPEST TTS</span></td><td>TTS</td><td class="mono">$0.015/1K chars</td><td>Good</td><td class="mono">$15</td></tr>
      <tr><td><strong>Google TTS</strong></td><td>TTS</td><td class="mono">$0.016/1K chars</td><td>Good</td><td class="mono">$16</td></tr>
      <tr><td><strong>ElevenLabs</strong></td><td>TTS</td><td class="mono">$0.330/1K chars</td><td>Best</td><td class="mono">$330</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Self-host Whisper</div><p>OpenAI Whisper is open source. Self-hosting on a $6/mo Hetzner CX22 handles ~5K minutes/month at near-zero cost. For over 50K min/month, self-hosting saves $300+/mo.</p></div>
</section>""" + aff_block("Try the best TTS API:", [("[ELEVENLABS_AFFILIATE_LINK]", "🎙️ Try ElevenLabs free")])

stt_faqs = [
    ("How much does OpenAI Whisper API cost?", "$0.006 per minute of audio transcribed. For 10,000 minutes/month: $60. Self-hosting Whisper (open source) on your own server costs near $0 at the same volume."),
    ("Is ElevenLabs worth the premium price?", "ElevenLabs at $0.330/1K chars is 20× more expensive than OpenAI TTS ($0.015). The quality and naturalness is significantly better — worth it for customer-facing voice, audiobooks, or brand voice. For internal tools, OpenAI TTS is sufficient."),
    ("What is the cheapest TTS API in 2026?", "OpenAI TTS at $0.015 per 1,000 characters. Google TTS is similar at $0.016. For large volumes, Azure Neural TTS or Amazon Polly can be cheaper. Self-hosting Coqui TTS or Bark eliminates API costs entirely."),
    ("How many characters per minute of speech?", "Approximately 800–1,000 characters per minute of spoken text (at normal speaking pace). A 10-minute podcast script ≈ 9,000 characters ≈ $0.135 with OpenAI TTS."),
]

stt_related = related_tools([
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Add LLM to your voice pipeline'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'Full voice agent cost'),
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Run STT/TTS on Lambda'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Self-host Whisper'),
])

pages.append((
    os.path.join(BASE, 'stt-tts-api-cost.html'),
    page('en', 'https://apicalculators.com/stt-tts-api-cost.html',
         'STT & TTS API Cost Calculator 2026 — Whisper vs ElevenLabs vs Google',
         'Free speech-to-text and text-to-speech API cost calculator. Compare Whisper, Deepgram, ElevenLabs, and Google pricing. Enter volume → get monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/stt-tts-api-cost.html'),
          ('x-default','https://apicalculators.com/stt-tts-api-cost.html')],
         None,
         'June 2026 · STT/TTS API pricing',
         '<span class="em">STT &amp; TTS API</span> Cost Calculator',
         'Compare Whisper, Deepgram, ElevenLabs, OpenAI TTS, and Google pricing. Enter minutes or characters → see exact monthly cost. Free, no signup.',
         stt_calc_html, stt_calc_js, stt_sections, stt_faqs, '', stt_related)
))

# ── 9. Stripe vs Paddle Calculator (/stripe-vs-paddle-calculator.html) ────────
pay_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>💳 Payment Fee Calculator</h2>
    <p>Enter revenue and transaction count · Compare processors instantly</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="payRev">Monthly revenue ($)</label>
        <input class="inp" id="payRev" type="number" value="10000" min="0"></div>
      <div class="field"><label for="payTx">Transactions / month</label>
        <input class="inp" id="payTx" type="number" value="200" min="0"></div>
      <div class="field"><label>Avg transaction value</label>
        <input class="inp" id="payAvg" type="text" value="$50.00" readonly style="opacity:.6"></div>
    </div>
    <div class="result" style="overflow:visible">
      <div class="rlabel">Fee comparison</div>
      <div id="payCmp" style="display:flex;flex-direction:column;gap:8px;margin-top:10px"></div>
    </div>
  </div>
</div>"""

pay_calc_js = """
const PAY = [
  {id:'stripe', name:'Stripe',        rate:0.029, fixed:0.30, note:'2.9% + $0.30'},
  {id:'paddle', name:'Paddle',        rate:0.050, fixed:0.50, note:'5% + $0.50 · MoR'},
  {id:'lemon',  name:'Lemon Squeezy', rate:0.050, fixed:0.50, note:'5% + $0.50 · MoR'},
  {id:'paypal', name:'PayPal',        rate:0.0349,fixed:0.49, note:'3.49% + $0.49'},
];
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const fmt$=v=>{if(v===0)return'$0';if(v<1)return'$'+v.toFixed(3);if(v<1000)return'$'+v.toFixed(2);return'$'+Math.round(v).toLocaleString('en-US');};
function calcPay(){
  const rev=num($('payRev').value),tx=num($('payTx').value);
  $('payAvg').value=tx>0?'$'+(rev/tx).toFixed(2):'$0.00';
  const rows=PAY.map(p=>{
    const fee=rev*p.rate+tx*p.fixed;
    return {...p,fee,net:rev-fee,pct:rev>0?fee/rev*100:0};
  }).sort((a,b)=>a.fee-b.fee);
  const max=Math.max(...rows.map(r=>r.fee),1);
  $('payCmp').innerHTML=rows.map((r,i)=>`
    <div style="background:var(--surface);border:1px solid var(--border${i===0?'2':''});border-radius:10px;padding:12px 14px;${i===0?'border-color:rgba(184,255,46,.3)':''}">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-weight:700">${r.name}${i===0?'<span class="badge" style="margin-left:8px">CHEAPEST</span>':''}</span>
        <span style="font-family:monospace;color:var(--lime)">${fmt$(r.fee)}</span>
      </div>
      <div style="background:var(--bg);border-radius:4px;height:6px;margin-bottom:6px">
        <div style="background:${i===0?'var(--lime)':'var(--border2)'};height:6px;border-radius:4px;width:${(r.fee/max*100).toFixed(1)}%"></div>
      </div>
      <div style="font-size:12px;color:var(--muted)">${r.note} · ${r.pct.toFixed(2)}% effective · net ${fmt$(r.net)}</div>
    </div>`).join('');
}
['payRev','payTx'].forEach(id=>$(id).addEventListener('input',calcPay));
calcPay();
"""

pay_sections = """
<section class="sec">
  <h2>Stripe vs Paddle vs Lemon Squeezy Fees</h2>
  <p class="sh-sub">True cost comparison — raw fees only, excluding tax handling.</p>
  <table class="ptable">
    <thead><tr><th>Processor</th><th>Rate</th><th>Fixed fee</th><th>Tax handling</th><th>MoR</th><th>$10K MRR fee</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Stripe</strong><span class="badge">LOWEST RATE</span></td><td class="mono">2.9%</td><td class="mono">$0.30</td><td>You handle (Stripe Tax extra)</td><td>No</td><td class="mono">~$350</td></tr>
      <tr><td><strong>PayPal</strong></td><td class="mono">3.49%</td><td class="mono">$0.49</td><td>You handle</td><td>No</td><td class="mono">~$447</td></tr>
      <tr><td><strong>Paddle</strong></td><td class="mono">5%</td><td class="mono">$0.50</td><td>Handled (global VAT)</td><td>Yes</td><td class="mono">~$600</td></tr>
      <tr><td><strong>Lemon Squeezy</strong></td><td class="mono">5%</td><td class="mono">$0.50</td><td>Handled (global VAT)</td><td>Yes</td><td class="mono">~$600</td></tr>
    </tbody>
  </table>
  <div class="callout info"><div class="cl">ℹ What is a Merchant of Record?</div><p>A Merchant of Record (MoR) is the legal entity that processes payment and handles all tax obligations globally. Paddle and Lemon Squeezy collect VAT/sales tax in 100+ countries automatically. Stripe requires you to use Stripe Tax ($0.50 per transaction) or handle tax yourself.</p></div>
  <div class="callout tip"><div class="cl">💡 Break-even point</div><p>Paddle's 5% beats Stripe at MRR above ~$15K when adding Stripe Tax ($0.50/tx) and accounting for international card fees (1.5% extra). Below $15K MRR: Stripe is cheaper. Above $15K MRR with global customers: Paddle or Lemon Squeezy saves tax headaches.</p></div>
</section>"""

pay_faqs = [
    ("Is Stripe cheaper than Paddle for SaaS?", "At raw fee level yes (2.9% vs 5%). But adding Stripe Tax ($0.50/tx for VAT), international card fees (1.5%), and chargeback costs puts the break-even at $12–18K MRR. Below that Stripe is cheaper; above that Paddle is often cheaper total."),
    ("What is a Merchant of Record?", "A Merchant of Record (MoR) is the legal entity that processes payment and handles all tax obligations. Paddle and Lemon Squeezy are MoRs — they collect VAT/sales tax globally. Stripe is not a MoR; you are responsible for tax compliance."),
    ("Does Stripe work in Turkey?", "Yes, Stripe supports Turkey. You can accept TRY payments and international cards. Note: Stripe Tax applies for VAT in EU countries. Turkish customers paying in TRY may incur FX conversion fees."),
    ("What is Lemon Squeezy vs Paddle?", "Both are Merchant of Record platforms at 5% + $0.50. Lemon Squeezy is newer with a simpler UI and stronger developer experience. Paddle has been around longer with more enterprise features. Both handle global VAT automatically."),
]

pay_related = related_tools([
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Full SaaS stack cost'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Infrastructure cost for your SaaS'),
    ('/aws-lambda-calculator.html', '⚡', 'Serverless Cost', 'Backend cost for your SaaS'),
    ('/embedding-api-cost.html', '🔢', 'Embedding Cost', 'AI feature cost for your SaaS'),
])

pages.append((
    os.path.join(BASE, 'stripe-vs-paddle-calculator.html'),
    page('en', 'https://apicalculators.com/stripe-vs-paddle-calculator.html',
         'Stripe vs Paddle vs Lemon Squeezy Fee Calculator 2026',
         'Free payment processor fee calculator. Compare Stripe, Paddle, Lemon Squeezy, and PayPal fees. Enter monthly revenue → see exact costs and net revenue.',
         'en_US',
         [('en','https://apicalculators.com/stripe-vs-paddle-calculator.html'),
          ('x-default','https://apicalculators.com/stripe-vs-paddle-calculator.html')],
         None,
         'June 2026 · Payment processor pricing',
         'Stripe vs <span class="em">Paddle</span> Fee Calculator',
         'Compare Stripe, Paddle, Lemon Squeezy, and PayPal fees side by side. Enter your monthly revenue → see exact fees, effective rate, and net revenue.',
         pay_calc_html, pay_calc_js, pay_sections, pay_faqs, '', pay_related)
))

# ── 10. AI Image Cost (/ai-image-cost-calculator.html) ────────────────────────
img_calc_html = """
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>🎨 AI Image Generation Cost Calculator</h2>
    <p>Select model · Enter volume · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field"><label for="imgModel">Model</label>
        <select class="sel" id="imgModel">
          <option value="dalle3std">DALL·E 3 · 1024 standard ($0.040/img)</option>
          <option value="dalle3hd">DALL·E 3 · 1024 HD ($0.080/img)</option>
          <option value="dalle3wide">DALL·E 3 · 1792 HD ($0.120/img)</option>
          <option value="sdxl">Stable Diffusion XL API ($0.009/img)</option>
          <option value="flux">Flux.1 Pro API ($0.050/img)</option>
          <option value="midjourney">Midjourney Basic ($10/mo ≈ $0.050/img)</option>
        </select></div>
      <div class="row2">
        <div class="field"><label for="imgCount">Generations / day</label>
          <input class="inp" id="imgCount" type="number" value="100" min="0"></div>
        <div class="field"><label for="imgVar">Variants per prompt</label>
          <input class="inp" id="imgVar" type="number" value="2" min="1" max="10"></div>
      </div>
    </div>
    <div class="result">
      <div class="rlabel">Estimated monthly cost</div>
      <div class="big" id="imgTotal">$0</div>
      <div class="per" id="imgName">per month</div>
      <div class="breakdown">
        <div class="brow"><span>Price per image</span><b id="imgUnit">—</b></div>
        <div class="brow"><span>Images per month</span><b id="imgGen">—</b></div>
        <div class="brow hl"><span>Cost per 1,000 images</span><b id="imgK">—</b></div>
      </div>
    </div>
  </div>
</div>"""

img_calc_js = """
const IMG_PRICES = {
  dalle3std: {name:'DALL·E 3 Standard',unit:0.040},
  dalle3hd:  {name:'DALL·E 3 HD',     unit:0.080},
  dalle3wide:{name:'DALL·E 3 Wide HD', unit:0.120},
  sdxl:      {name:'SDXL API',         unit:0.009},
  flux:      {name:'Flux.1 Pro',       unit:0.050},
  midjourney:{name:'Midjourney Basic', unit:0.050},
};
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const big$=v=>{if(v>=1000)return'$'+Math.round(v).toLocaleString('en-US');if(v>=1)return'$'+v.toFixed(2);if(v>0)return'$'+v.toFixed(4);return'$0';};
const fmt$=v=>{if(v===0)return'$0';if(v<0.01)return'$'+v.toFixed(4);if(v<1)return'$'+v.toFixed(3);return'$'+v.toFixed(2);};
const intf=v=>Math.round(v).toLocaleString('en-US');
function calcImg(){
  const m=IMG_PRICES[$('imgModel').value];
  const c=num($('imgCount').value);
  const v=Math.max(1,num($('imgVar').value));
  const total_per_day=c*v;
  const total=total_per_day*30*m.unit;
  $('imgTotal').textContent=big$(total);
  $('imgName').textContent='per month — '+m.name;
  $('imgUnit').textContent=fmt$(m.unit);
  $('imgGen').textContent=intf(total_per_day*30)+' images';
  $('imgK').textContent=fmt$(m.unit*1000);
}
['imgModel','imgCount','imgVar'].forEach(id=>{
  const el=$(id);if(el)el.addEventListener('change',calcImg),el.addEventListener('input',calcImg);
});
calcImg();
"""

img_sections = """
<section class="sec">
  <h2>AI Image Generation Pricing 2026</h2>
  <p class="sh-sub">Cost per image. API pricing unless noted.</p>
  <table class="ptable">
    <thead><tr><th>Model</th><th>Price / image</th><th>Quality</th><th>API?</th><th>1,000 images</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Stable Diffusion XL</strong><span class="badge">CHEAPEST API</span></td><td class="mono">$0.009</td><td>Good</td><td>Yes</td><td class="mono">$9</td></tr>
      <tr><td><strong>DALL·E 3 Standard</strong></td><td class="mono">$0.040</td><td>Excellent</td><td>Yes</td><td class="mono">$40</td></tr>
      <tr><td><strong>Flux.1 Pro</strong></td><td class="mono">$0.050</td><td>Excellent</td><td>Yes</td><td class="mono">$50</td></tr>
      <tr><td><strong>Midjourney Basic</strong></td><td class="mono">~$0.050</td><td>Excellent</td><td>No (Discord)</td><td class="mono">$50</td></tr>
      <tr><td><strong>DALL·E 3 HD</strong></td><td class="mono">$0.080</td><td>Best</td><td>Yes</td><td class="mono">$80</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Self-host for scale</div><p>Running SDXL on a $0.50/hr GPU spot instance (Hetzner, Vultr) generates ~500 images/hour. At 10,000 images/day: self-hosting costs ~$10/day vs $90 with SDXL API. Break-even at ~5,000 images/month.</p></div>
</section>""" + aff_block("GPU hosting for self-hosted image generation:", [(VULTR, "☁️ $300 Vultr credit (GPU servers)")])

img_faqs = [
    ("How much does DALL·E 3 cost?", "DALL·E 3 via OpenAI API: $0.040 per standard 1024×1024 image, $0.080 per HD image, $0.120 per 1792×1024 HD image. For 1,000 standard images: $40."),
    ("Is Midjourney cheaper than DALL·E 3?", "Midjourney Basic ($10/mo) gives ~200 images/month at $0.05 each. DALL·E 3 standard at $0.040 is slightly cheaper per image with API access. For programmatic use, DALL·E 3 or SDXL are better since Midjourney has no official API."),
    ("What is the cheapest AI image generator?", "SDXL via Replicate/API at $0.009/image is cheapest managed API. Self-hosting SDXL on a spot GPU is cheaper at scale (~$0.002–0.005/image). Midjourney has no API; DALL·E 3 is cheapest quality-tier API option."),
    ("Does Midjourney have an API?", "No official API as of 2026. Midjourney requires Discord interaction. For programmatic image generation, use DALL·E 3 (OpenAI API), Stable Diffusion (Replicate/fal.ai), or Flux (Replicate)."),
]

img_related = related_tools([
    ('/llm-cost-calculator.html', '🤖', 'LLM API Cost', 'Text generation costs'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS', 'Self-host image generation'),
    ('/embedding-api-cost.html', '🔢', 'Embedding Cost', 'Image embedding cost'),
    ('/ai-agent-cost-calculator.html', '⛓️', 'AI Agent Cost', 'Multi-modal agent cost'),
])

pages.append((
    os.path.join(BASE, 'ai-image-cost-calculator.html'),
    page('en', 'https://apicalculators.com/ai-image-cost-calculator.html',
         'AI Image Generation Cost Calculator 2026 — DALL·E 3 vs Stable Diffusion vs Flux',
         'Free AI image generation cost calculator. Compare DALL·E 3, Stable Diffusion, Flux, and Midjourney pricing. Enter volume → see exact monthly cost.',
         'en_US',
         [('en','https://apicalculators.com/ai-image-cost-calculator.html'),
          ('x-default','https://apicalculators.com/ai-image-cost-calculator.html')],
         None,
         'June 2026 · AI image pricing',
         '<span class="em">AI Image</span> Cost Calculator',
         'Compare DALL·E 3, Stable Diffusion XL, Flux.1, and Midjourney pricing. Enter daily generation volume → see exact monthly cost. Free, no signup.',
         img_calc_html, img_calc_js, img_sections, img_faqs, '', img_related)
))

# ══════════════════════════════════════════════════════════════════════════════
# DE PAGES
# ══════════════════════════════════════════════════════════════════════════════

# ── DE LLM Kostenrechner (/de/llm-kostenrechner.html) ─────────────────────────
de_llm_calc_html = llm_calc_html.replace('🤖 LLM API Cost Calculator','🤖 LLM API Kostenrechner').replace('Select model · Enter token volume · Results update live','Modell wählen · Token-Volumen eingeben · Ergebnisse aktualisieren sich live').replace('Input tokens / request','Eingabe-Token / Anfrage').replace('Output tokens / request','Ausgabe-Token / Anfrage').replace('Requests / day','Anfragen / Tag').replace('Day','Tag').replace('Month','Monat').replace('Year','Jahr').replace('Estimated cost','Geschätzte Kosten').replace('Input / output per 1M tokens','Preis Eingabe / Ausgabe / 1M Token').replace('Cost per request','Kosten pro Anfrage').replace('Input cost','Eingabekosten').replace('Output cost','Ausgabekosten').replace('Total tokens','Token gesamt')

de_llm_sections = """
<section class="sec">
  <h2>LLM API Preise 2026</h2>
  <p class="sh-sub">Alle Preise in USD pro 1 Million Token, Pay-as-you-go, Juni 2026.</p>
  <table class="ptable">
    <thead><tr><th>Modell</th><th>Eingabe / 1M</th><th>Ausgabe / 1M</th><th>Kontext</th><th>Beste für</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GPT-4o mini</strong><span class="badge">GÜNSTIGSTE</span></td><td class="mono">$0.15</td><td class="mono">$0.60</td><td class="mono">128K</td><td>Hochvolumen-Aufgaben</td></tr>
      <tr><td><strong>Gemini 1.5 Flash</strong></td><td class="mono">$0.075</td><td class="mono">$0.30</td><td class="mono">1M</td><td>Ultra-Hochvolumen</td></tr>
      <tr><td><strong>Claude 3.5 Haiku</strong></td><td class="mono">$0.80</td><td class="mono">$4.00</td><td class="mono">200K</td><td>Qualität im Budget</td></tr>
      <tr><td><strong>GPT-4o</strong></td><td class="mono">$2.50</td><td class="mono">$10.00</td><td class="mono">128K</td><td>Allgemeines Flaggschiff</td></tr>
      <tr><td><strong>Claude 3.5 Sonnet</strong></td><td class="mono">$3.00</td><td class="mono">$15.00</td><td class="mono">200K</td><td>Coding &amp; Reasoning</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Wechselkurs EUR/USD</div><p>Alle LLM APIs berechnen in USD. Beim aktuellen Kurs (~1,08) kostet GPT-4o mini ~0,14 € / 1M Token (Eingabe). Planen Sie einen Puffer für Kursschwankungen ein.</p></div>
</section>""" + aff_block("Jetzt deployen — kostenlose Credits:", [(VULTR, "☁️ $300 Vultr-Guthaben"), ("[HETZNER_AFFILIATE_LINK]", "🇩🇪 Hetzner — günstigstes EU")])

de_llm_faqs = [
    ("Wie viel kostet die GPT-4o API?", "GPT-4o kostet $2,50 pro Million Eingabe-Token und $10,00 pro Million Ausgabe-Token (Pay-as-you-go, Juni 2026). Beim EUR/USD-Kurs von ~1,08 entspricht das ca. €2,31 und €9,26."),
    ("Was ist das günstigste LLM in 2026?", "Gemini 1.5 Flash bei $0,075/$0,30 pro Million Token ist das günstigste leistungsfähige Modell. GPT-4o mini ($0,15/$0,60) ist die günstigste OpenAI-Option."),
    ("Wie kann ich LLM API-Kosten senken?", "Günstigere Modelle verwenden (GPT-4o mini ist 16× günstiger als GPT-4o). Batch API für 50% Rabatt bei asynchronen Aufgaben aktivieren. Häufige Anfragen cachen. System-Prompts kürzen."),
    ("Warum sind LLM-Preise in USD?", "Alle großen LLM-Anbieter (OpenAI, Anthropic, Google) berechnen in USD. EUR-Nutzer tragen das Wechselkursrisiko. Europäische Alternativen wie Mistral AI (Paris) bieten teilweise EUR-Abrechnung."),
]

de_llm_related = related_tools([
    ('/de/', '🧮', 'Alle Rechner', 'Zurück zur Übersicht'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS Vergleich', 'Hetzner vs DigitalOcean'),
    ('/vector-db-cost.html', '🗄️', 'Vektordatenbank Kosten', 'Pinecone vs Supabase'),
    ('/embedding-api-cost.html', '🔢', 'Embedding API Kosten', 'OpenAI vs Cohere'),
])

pages.append((
    os.path.join(BASE, 'de', 'llm-kostenrechner.html'),
    page('de', 'https://apicalculators.com/de/llm-kostenrechner.html',
         'LLM API Kostenrechner 2026 — GPT-4o, Claude & Gemini Preise',
         'Kostenloser LLM API Kostenrechner. GPT-4o, Claude 3.5, Gemini Preise vergleichen. Token-Volumen eingeben → exakte Monatskosten erhalten.',
         'de_DE',
         [('de','https://apicalculators.com/de/llm-kostenrechner.html'),
          ('en','https://apicalculators.com/llm-cost-calculator.html'),
          ('x-default','https://apicalculators.com/llm-cost-calculator.html')],
         ('DE', 'Germany'),
         'Juni 2026 · Aktuelle LLM Preise',
         '<span class="em">LLM API</span> Kostenrechner',
         'GPT-4o, Claude 3.5 Sonnet, Gemini und 5 weitere Modelle vergleichen. Token-Volumen eingeben — exakte Monatskosten sofort sehen. Kostenlos, ohne Anmeldung.',
         de_llm_calc_html, llm_calc_js, de_llm_sections, de_llm_faqs, '', de_llm_related,
         home_url='/de/')
))

# ── DE Cloud VPS Kostenvergleich (/de/cloud-vps-kostenvergleich.html) ──────────
de_vps_sections = """
<section class="sec">
  <h2>Cloud VPS Preisvergleich 2026</h2>
  <p class="sh-sub">Einstiegs- und Mittelklasse-Pläne, pro Monat. Hetzner in EUR, andere in USD.</p>
  <table class="ptable">
    <thead><tr><th>Anbieter</th><th>2 vCPU / 4 GB</th><th>4 vCPU / 8 GB</th><th>Kostenloses Egress</th><th>Standorte</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Hetzner</strong><span class="badge">GÜNSTIGSTES EU</span></td><td class="mono">€4,50/mo</td><td class="mono">€8,50/mo</td><td class="mono">20 TB/mo</td><td>DE, FI, US, SG</td></tr>
      <tr><td><strong>Linode / Akamai</strong></td><td class="mono">$18/mo</td><td class="mono">$36/mo</td><td class="mono">1 TB/mo</td><td>11 Regionen</td></tr>
      <tr><td><strong>DigitalOcean</strong></td><td class="mono">$18/mo</td><td class="mono">$36/mo</td><td class="mono">2 TB/mo</td><td>15 Regionen</td></tr>
      <tr><td><strong>Vultr</strong></td><td class="mono">$24/mo</td><td class="mono">$48/mo</td><td class="mono">3 TB/mo</td><td>32 Regionen</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 DSGVO &amp; Datenschutz</div><p>Hetzner betreibt alle deutschen Rechenzentren in Deutschland (Nürnberg, Falkenstein). Für DSGVO-konforme Datenhaltung ist Hetzner DE die erste Wahl — Daten verlassen nie die EU.</p></div>
</section>""" + aff_block("Server heute deployen:", [(VULTR, "🖥️ $300 Vultr-Guthaben"), ("[HETZNER_AFFILIATE_LINK]", "🇩🇪 Hetzner — günstigstes EU")])

de_vps_faqs = [
    ("Ist Hetzner günstiger als DigitalOcean?", "Ja — 3–5× günstiger für EU-Specs. Hetzner CX22 (2 vCPU/4 GB) kostet €4,50/mo vs DigitalOcean $18/mo. Kompromiss: weniger globale Standorte (4 vs 15 Regionen)."),
    ("Ist Hetzner DSGVO-konform?", "Ja. Hetzner betreibt alle deutschen Rechenzentren ausschließlich in Deutschland (Nürnberg, Falkenstein) und Finnland. Als deutsches Unternehmen unterliegt Hetzner deutschem Datenschutzrecht und der DSGVO."),
    ("Welcher VPS ist am besten für deutschsprachige SaaS?", "Hetzner ist die erste Wahl: günstigste Preise, DSGVO-konform, deutsches Unternehmen, niedrige Latenz für DACH-Nutzer. DigitalOcean für verwaltete Datenbanken, Vultr für globale Reichweite."),
    ("Wie viel kostet ein Cloud-Server pro Monat?", "Einstieg (1 vCPU/1GB): €3–6/mo. Mittelklasse (2 vCPU/4GB): €4,50 (Hetzner) bis $24 (Vultr). Produktion (4 vCPU/8GB): €8,50 (Hetzner) bis $48 (Vultr). Hetzner ist konstant 3–5× günstiger für EU."),
]

de_vps_calc = vps_calc_html.replace('🖥️ Cloud VPS Cost Comparison','🖥️ Cloud VPS Kostenvergleich').replace('Select specs · See cheapest provider · Results update live','Specs wählen · Günstigsten Anbieter sehen · Ergebnisse live').replace('Number of servers','Anzahl Server').replace('Cheapest monthly cost','Günstigste Monatskosten')

pages.append((
    os.path.join(BASE, 'de', 'cloud-vps-kostenvergleich.html'),
    page('de', 'https://apicalculators.com/de/cloud-vps-kostenvergleich.html',
         'Cloud VPS Kostenvergleich 2026 — Hetzner vs DigitalOcean vs Vultr',
         'Kostenloser Cloud VPS Preisvergleich. Hetzner, DigitalOcean, Vultr und Linode vergleichen. Specs wählen → günstigsten Anbieter sofort sehen.',
         'de_DE',
         [('de','https://apicalculators.com/de/cloud-vps-kostenvergleich.html'),
          ('en','https://apicalculators.com/cloud-vps-comparison.html'),
          ('x-default','https://apicalculators.com/cloud-vps-comparison.html')],
         ('DE', 'Germany'),
         'Juni 2026 · VPS Preise',
         'Cloud VPS <span class="em">Kostenvergleich</span>',
         'Hetzner, DigitalOcean, Vultr und Linode VPS-Preise vergleichen. CPU und RAM-Anforderungen wählen — günstigsten Anbieter sofort sehen. Kostenlos.',
         de_vps_calc, vps_calc_js, de_vps_sections, de_vps_faqs, '', de_llm_related,
         home_url='/de/')
))

# ── DE AWS Lambda Rechner (/de/aws-lambda-rechner.html) ───────────────────────
de_lambda_calc = lambda_calc_html.replace('⚡ Serverless Cost Calculator','⚡ Serverless Kostenrechner').replace('Select provider · Enter invocations and duration · Results update live','Anbieter wählen · Aufrufe und Dauer eingeben · Ergebnisse live').replace('Invocations / month (millions)','Aufrufe / Monat (Millionen)').replace('Avg duration (ms)','Ø Dauer (ms)').replace('Estimated monthly cost','Geschätzte Monatskosten').replace('Invocation cost','Aufruf-Kosten').replace('Compute cost','Rechenkosten').replace('Annual estimate','Jährliche Schätzung')

de_lambda_sections = """
<section class="sec">
  <h2>Serverless Preisvergleich 2026</h2>
  <p class="sh-sub">Monatskosten für 10M Aufrufe · 256MB · 200ms Ø-Dauer.</p>
  <table class="ptable">
    <thead><tr><th>Anbieter</th><th>Kostenloses Tier</th><th>Aufrufpreis</th><th>Rechenpreis</th><th>10M Aufrufe / 200ms</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>AWS Lambda</strong><span class="badge">BELIEBTESTE</span></td><td class="mono">1M Aufrufe/mo</td><td class="mono">$0,20/M</td><td class="mono">$0,0000167/GB-s</td><td class="mono">$3,47</td></tr>
      <tr><td><strong>Cloudflare Workers</strong></td><td class="mono">1M Req/Tag (kostenlos)</td><td class="mono">$0,30/M</td><td class="mono">$0,012/M GB-s</td><td class="mono">$2,70</td></tr>
      <tr><td><strong>Google Cloud Functions</strong></td><td class="mono">2M Aufrufe/mo</td><td class="mono">$0,40/M</td><td class="mono">$0,000025/GB-s</td><td class="mono">$3,20</td></tr>
    </tbody>
  </table>
  <div class="callout info"><div class="cl">⚠ Versteckte Kosten</div><p>AWS API Gateway kostet $3,50/M Anfragen — verdoppelt oft die Lambda-Rechnung. CloudWatch Logs kosten $0,50/GB. Diese Posten im Budget berücksichtigen.</p></div>
</section>""" + aff_block("Serverless heute deployen:", [("[VERCEL_AFFILIATE_LINK]", "▲ Auf Vercel deployen"), ("[CLOUDFLARE_AFFILIATE_LINK]", "🔶 Cloudflare Workers")])

de_lambda_faqs = [
    ("Was kostet AWS Lambda pro Million Aufrufe?", "Nach dem kostenlosen Tier (1M/Monat) kostet Lambda $0,20 pro Million Aufrufe plus Rechenkosten. Eine 256MB-Funktion bei 200ms Ø = ~$3,47/Monat für 10M Aufrufe."),
    ("Ist Cloudflare Workers günstiger als Lambda?", "Für kurze Laufzeiten (unter 30ms) bei hoher Frequenz ja. Workers bei $0,30/M schlägt Lambda. Für längere Berechnungen (500ms+) oder AWS-Integrationen ist Lambda oft besser."),
    ("Was ist das AWS Lambda Free Tier?", "1 Million kostenlose Aufrufe pro Monat + 400.000 GB-Sekunden Rechenzeit, dauerhaft (kein 12-Monats-Trial). Reicht für ~2M Aufrufe bei 256MB/200ms."),
    ("Hat Lambda Cold Starts?", "Ja. Cold Starts fügen 100–500ms Latenz beim ersten Aufruf nach Inaktivität hinzu. Gegenmaßnahmen: Provisioned Concurrency, Warmup-Pings oder Cloudflare Workers (keine Cold Starts)."),
]

pages.append((
    os.path.join(BASE, 'de', 'aws-lambda-rechner.html'),
    page('de', 'https://apicalculators.com/de/aws-lambda-rechner.html',
         'AWS Lambda Kostenrechner 2026 — Serverless Kosten berechnen',
         'Kostenloser AWS Lambda Kostenrechner. Lambda, Cloudflare Workers und Vercel Functions vergleichen. Aufrufe eingeben → exakte Monatskosten erhalten.',
         'de_DE',
         [('de','https://apicalculators.com/de/aws-lambda-rechner.html'),
          ('en','https://apicalculators.com/aws-lambda-calculator.html'),
          ('x-default','https://apicalculators.com/aws-lambda-calculator.html')],
         ('DE', 'Germany'),
         'Juni 2026 · AWS Lambda Preise',
         '<span class="em">AWS Lambda</span> Kostenrechner',
         'Lambda, Cloudflare Workers, Vercel und GCP Functions Preise vergleichen. Aufrufe, Dauer, Speicher eingeben — exakte Monatskosten sofort sehen.',
         de_lambda_calc, lambda_calc_js, de_lambda_sections, de_lambda_faqs, '', de_llm_related,
         home_url='/de/')
))

# ══════════════════════════════════════════════════════════════════════════════
# FR PAGES
# ══════════════════════════════════════════════════════════════════════════════

fr_llm_calc = llm_calc_html.replace('🤖 LLM API Cost Calculator','🤖 Calculateur de coût API LLM').replace('Select model · Enter token volume · Results update live','Choisir le modèle · Entrer le volume de tokens · Résultats en temps réel').replace('Input tokens / request','Tokens d\'entrée / requête').replace('Output tokens / request','Tokens de sortie / requête').replace('Requests / day','Requêtes / jour').replace('Day','Jour').replace('Month','Mois').replace('Year','Année').replace('Estimated cost','Coût estimé').replace('Input / output per 1M tokens','Prix entrée / sortie / 1M tokens').replace('Cost per request','Coût par requête').replace('Input cost','Coût d\'entrée').replace('Output cost','Coût de sortie').replace('Total tokens','Tokens totaux')

fr_llm_sections = """
<section class="sec">
  <h2>Tarifs API LLM 2026</h2>
  <p class="sh-sub">Prix en USD par million de tokens, pay-as-you-go, juin 2026.</p>
  <table class="ptable">
    <thead><tr><th>Modèle</th><th>Entrée / 1M</th><th>Sortie / 1M</th><th>Contexte</th><th>Meilleur pour</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GPT-4o mini</strong><span class="badge">MOINS CHER</span></td><td class="mono">$0,15</td><td class="mono">$0,60</td><td class="mono">128K</td><td>Haut volume</td></tr>
      <tr><td><strong>Gemini 1.5 Flash</strong></td><td class="mono">$0,075</td><td class="mono">$0,30</td><td class="mono">1M</td><td>Ultra-haut volume</td></tr>
      <tr><td><strong>Claude 3.5 Haiku</strong></td><td class="mono">$0,80</td><td class="mono">$4,00</td><td class="mono">200K</td><td>Qualité économique</td></tr>
      <tr><td><strong>GPT-4o</strong></td><td class="mono">$2,50</td><td class="mono">$10,00</td><td class="mono">128K</td><td>Usage général</td></tr>
      <tr><td><strong>Mistral Large</strong></td><td class="mono">$2,00</td><td class="mono">$6,00</td><td class="mono">128K</td><td>Alternative européenne</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 Alternative française : Mistral AI</div><p>Mistral AI (Paris) propose des modèles compétitifs avec facturation en EUR. Mistral Large ($2/$6 per 1M) et Mistral Small ($0.20/$0.60) sont d'excellentes alternatives européennes à OpenAI.</p></div>
</section>""" + aff_block("Déployez maintenant — crédits offerts :", [(VULTR, "☁️ $300 crédit Vultr"), ("[HETZNER_AFFILIATE_LINK]", "🇩🇪 Hetzner — moins cher EU")])

fr_llm_faqs = [
    ("Quel est le coût de l'API GPT-4o ?", "GPT-4o coûte $2,50 par million de tokens d'entrée et $10,00 par million de tokens de sortie (pay-as-you-go, juin 2026). Au taux EUR/USD de ~1,08, cela représente environ €2,31 et €9,26."),
    ("Quelle est l'API LLM la moins chère en 2026 ?", "Gemini 1.5 Flash à $0,075/$0,30 par million de tokens est la moins chère. GPT-4o mini ($0,15/$0,60) est l'option OpenAI la moins chère. Mistral Small ($0,20/$0,60) est la meilleure alternative européenne."),
    ("Comment réduire les coûts d'API LLM ?", "Utiliser des modèles moins chers (GPT-4o mini est 16× moins cher que GPT-4o). Activer le Batch API pour 50% de réduction sur les charges asynchrones. Mettre en cache les requêtes fréquentes. Réduire les system prompts."),
    ("Existe-t-il des API LLM françaises ?", "Oui. Mistral AI (Paris) propose des modèles compétitifs : Mistral Small ($0,20/$0,60), Mistral Large ($2/$6), facturable en EUR. Alternative souveraine à OpenAI/Anthropic avec données traitées en UE."),
]

fr_llm_related = related_tools([
    ('/fr/', '🧮', 'Tous les calculateurs', 'Retour à l\'accueil'),
    ('/cloud-vps-comparison.html', '🖥️', 'Comparateur VPS', 'Hetzner vs DigitalOcean'),
    ('/vector-db-cost.html', '🗄️', 'Coût base vectorielle', 'Pinecone vs Supabase'),
    ('/embedding-api-cost.html', '🔢', 'Coût embeddings', 'OpenAI vs Cohere'),
])

pages.append((
    os.path.join(BASE, 'fr', 'calculateur-cout-llm.html'),
    page('fr', 'https://apicalculators.com/fr/calculateur-cout-llm.html',
         'Calculateur de coût API LLM 2026 — GPT-4o, Claude & Gemini',
         'Calculateur gratuit de coût API LLM. Comparer GPT-4o, Claude 3.5, Gemini et Mistral. Entrer le volume de tokens → obtenir le coût mensuel exact.',
         'fr_FR',
         [('fr','https://apicalculators.com/fr/calculateur-cout-llm.html'),
          ('en','https://apicalculators.com/llm-cost-calculator.html'),
          ('x-default','https://apicalculators.com/llm-cost-calculator.html')],
         ('FR', 'France'),
         'Juin 2026 · Tarifs LLM actualisés',
         'Calculateur de coût <span class="em">API LLM</span>',
         'Comparez GPT-4o, Claude 3.5, Gemini 1.5 Flash et Mistral. Entrez le volume de tokens — coût mensuel exact instantané. Gratuit, sans inscription.',
         fr_llm_calc, llm_calc_js, fr_llm_sections, fr_llm_faqs, '', fr_llm_related,
         home_url='/fr/')
))

# ── FR VPS Comparateur (/fr/comparateur-vps-cloud.html) ──────────────────────
fr_vps_sections = """
<section class="sec">
  <h2>Comparatif VPS Cloud 2026</h2>
  <p class="sh-sub">Plans entrée et milieu de gamme, par mois.</p>
  <table class="ptable">
    <thead><tr><th>Fournisseur</th><th>2 vCPU / 4 Go</th><th>4 vCPU / 8 Go</th><th>Egress inclus</th><th>Régions</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>Hetzner</strong><span class="badge">MOINS CHER EU</span></td><td class="mono">€4,50/mo</td><td class="mono">€8,50/mo</td><td class="mono">20 To/mo</td><td>DE, FI, US, SG</td></tr>
      <tr><td><strong>OVHcloud</strong></td><td class="mono">€7,00/mo</td><td class="mono">€14,00/mo</td><td class="mono">Illimité</td><td>FR, DE, UK, CA</td></tr>
      <tr><td><strong>DigitalOcean</strong></td><td class="mono">$18/mo</td><td class="mono">$36/mo</td><td class="mono">2 To/mo</td><td>15 régions</td></tr>
      <tr><td><strong>Vultr</strong></td><td class="mono">$24/mo</td><td class="mono">$48/mo</td><td class="mono">3 To/mo</td><td>32 régions</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 OVHcloud — option française</div><p>OVHcloud (Roubaix) est l'alternative souveraine française. Données hébergées en France, conformité RGPD native, facturation en EUR. €7/mo pour 2 vCPU/4Go vs €4,50 chez Hetzner — prime de ~55% pour la souveraineté française.</p></div>
</section>""" + aff_block("Déployez votre serveur aujourd'hui :", [(VULTR, "🖥️ $300 crédit Vultr"), ("[HETZNER_AFFILIATE_LINK]", "🇩🇪 Hetzner — moins cher EU")])

fr_vps_faqs = [
    ("Hetzner est-il moins cher qu'OVHcloud ?", "Oui. Hetzner CX22 (2 vCPU/4 Go) à €4,50/mo vs OVHcloud à ~€7/mo. Hetzner est ~35% moins cher. OVHcloud offre plus de régions en France et une souveraineté des données 100% française."),
    ("OVHcloud est-il RGPD-conforme ?", "Oui. OVHcloud est une entreprise française, héberge les données en France, et est naturellement conforme au RGPD. Idéal pour les entreprises soumises à des obligations de localisation des données françaises."),
    ("Quel VPS pour une SaaS française ?", "Hetzner Frankfurt pour le rapport qualité-prix (moins cher + RGPD). OVHcloud pour la souveraineté française. DigitalOcean pour les services managés (Postgres, Redis). Vultr pour la portée mondiale."),
    ("Combien coûte un VPS cloud par mois ?", "Entrée (1 vCPU/1 Go) : €3–7/mo. Milieu de gamme (2 vCPU/4 Go) : €4,50 (Hetzner) à €7 (OVHcloud) à $24 (Vultr). Production (4 vCPU/8 Go) : €8,50 (Hetzner) à $48 (Vultr)."),
]

fr_vps_calc = vps_calc_html.replace('🖥️ Cloud VPS Cost Comparison','🖥️ Comparateur VPS Cloud').replace('Select specs · See cheapest provider · Results update live','Choisir les specs · Voir le fournisseur le moins cher · Résultats en temps réel').replace('Number of servers','Nombre de serveurs').replace('Cheapest monthly cost','Coût mensuel le moins cher')

pages.append((
    os.path.join(BASE, 'fr', 'comparateur-vps-cloud.html'),
    page('fr', 'https://apicalculators.com/fr/comparateur-vps-cloud.html',
         'Comparateur VPS Cloud 2026 — Hetzner vs OVHcloud vs DigitalOcean',
         'Comparateur gratuit de VPS cloud. Hetzner, OVHcloud, DigitalOcean, Vultr. Choisissez vos specs → voyez le fournisseur le moins cher instantanément.',
         'fr_FR',
         [('fr','https://apicalculators.com/fr/comparateur-vps-cloud.html'),
          ('en','https://apicalculators.com/cloud-vps-comparison.html'),
          ('x-default','https://apicalculators.com/cloud-vps-comparison.html')],
         ('FR', 'France'),
         'Juin 2026 · Tarifs VPS',
         'Comparateur <span class="em">VPS Cloud</span>',
         'Comparez Hetzner, OVHcloud, DigitalOcean et Vultr. Sélectionnez CPU et RAM — voyez le fournisseur le moins cher instantanément. Gratuit.',
         fr_vps_calc, vps_calc_js, fr_vps_sections, fr_vps_faqs, '', fr_llm_related,
         home_url='/fr/')
))

# ══════════════════════════════════════════════════════════════════════════════
# TR PAGES
# ══════════════════════════════════════════════════════════════════════════════

tr_llm_calc = llm_calc_html.replace('🤖 LLM API Cost Calculator','🤖 LLM API Maliyet Hesaplayıcı').replace('Select model · Enter token volume · Results update live','Model seç · Token hacmini gir · Sonuçlar anlık güncellenir').replace('Input tokens / request','Giriş token / istek').replace('Output tokens / request','Çıkış token / istek').replace('Requests / day','İstek / gün').replace('Day','Gün').replace('Month','Ay').replace('Year','Yıl').replace('Estimated cost','Tahmini maliyet').replace('Input / output per 1M tokens','Giriş / çıkış 1M token başı').replace('Cost per request','İstek başı maliyet').replace('Input cost','Giriş maliyeti').replace('Output cost','Çıkış maliyeti').replace('Total tokens','Toplam token')

tr_llm_sections = """
<section class="sec">
  <h2>LLM API Fiyatları 2026</h2>
  <p class="sh-sub">Tüm fiyatlar USD, 1 milyon token başına, pay-as-you-go, Haziran 2026.</p>
  <table class="ptable">
    <thead><tr><th>Model</th><th>Giriş / 1M</th><th>Çıkış / 1M</th><th>Bağlam</th><th>En iyi kullanım</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GPT-4o mini</strong><span class="badge">EN UCUZ</span></td><td class="mono">$0.15</td><td class="mono">$0.60</td><td class="mono">128K</td><td>Yüksek hacimli görevler</td></tr>
      <tr><td><strong>Gemini 1.5 Flash</strong></td><td class="mono">$0.075</td><td class="mono">$0.30</td><td class="mono">1M</td><td>Ultra-yüksek hacim</td></tr>
      <tr><td><strong>Claude 3.5 Haiku</strong></td><td class="mono">$0.80</td><td class="mono">$4.00</td><td class="mono">200K</td><td>Bütçeye uygun kalite</td></tr>
      <tr><td><strong>GPT-4o</strong></td><td class="mono">$2.50</td><td class="mono">$10.00</td><td class="mono">128K</td><td>Genel amaçlı</td></tr>
      <tr><td><strong>Claude 3.5 Sonnet</strong></td><td class="mono">$3.00</td><td class="mono">$15.00</td><td class="mono">200K</td><td>Kod ve muhakeme</td></tr>
    </tbody>
  </table>
  <div class="callout tip"><div class="cl">💡 USD/TRY döviz etkisi</div><p>Tüm LLM API'ları USD üzerinden fiyatlandırılır. Mevcut kurda (~32 TRY/USD) GPT-4o mini giriş tokenleri 1M için ~4,8 TL'ye karşılık gelir. Döviz dalgalanmalarına karşı bütçe payı bırakın.</p></div>
</section>""" + aff_block("Hemen deploy et — ücretsiz kredi:", [(VULTR, "☁️ $300 Vultr Kredisi"), ("[DIGITALOCEAN_AFFILIATE_LINK]", "🌊 $200 DigitalOcean")])

tr_llm_faqs = [
    ("GPT-4o API'si ne kadar tutar?", "GPT-4o, 1 milyon giriş tokeni için $2,50 ve 1 milyon çıkış tokeni için $10,00 tutar (pay-as-you-go, Haziran 2026). Mevcut USD/TRY kurunda (~32) bu sırasıyla ~80 TL ve ~320 TL'ye karşılık gelir."),
    ("2026'da en ucuz LLM API hangisi?", "Gemini 1.5 Flash ($0.075/$0.30 per 1M token) en ucuz yetenekli model. GPT-4o mini ($0.15/$0.60) en ucuz OpenAI seçeneği. Her ikisi de yüksek hacimli Türkiye projeleri için uygundur."),
    ("LLM API maliyetleri nasıl düşürülür?", "Daha ucuz modeller kullanın (GPT-4o mini, GPT-4o'dan 16× ucuz). Asenkron iş yükleri için Batch API ile %50 indirim alın. Sık tekrarlanan istekleri önbelleğe alın. Sistem prompt'larını kısaltın."),
    ("Türkiye'den OpenAI API kullanmak mümkün mü?", "Evet. OpenAI API, Türkiye'den kredi kartı veya PayPal ile erişilebilir. USD üzerinden faturalandırılır. Anthropic Claude API da Türkiye'den erişilebilir. Google Gemini API ayrı Google Cloud hesabı gerektirir."),
]

tr_llm_related = related_tools([
    ('/tr/', '🧮', 'Tüm hesaplayıcılar', 'Ana sayfaya dön'),
    ('/cloud-vps-comparison.html', '🖥️', 'Cloud VPS Karşılaştırma', 'Hetzner vs DigitalOcean'),
    ('/vector-db-cost.html', '🗄️', 'Vektör DB Maliyeti', 'Pinecone vs Supabase'),
    ('/embedding-api-cost.html', '🔢', 'Embedding API Maliyeti', 'OpenAI vs Cohere'),
])

pages.append((
    os.path.join(BASE, 'tr', 'llm-maliyet-hesaplayici.html'),
    page('tr', 'https://apicalculators.com/tr/llm-maliyet-hesaplayici.html',
         'LLM API Maliyet Hesaplayıcı 2026 — GPT-4o, Claude & Gemini Fiyatları',
         'Ücretsiz LLM maliyet hesaplayıcı. GPT-4o, Claude 3.5, Gemini fiyatlarını karşılaştırın. Token hacmini girin → aylık maliyeti anında görün.',
         'tr_TR',
         [('tr','https://apicalculators.com/tr/llm-maliyet-hesaplayici.html'),
          ('en','https://apicalculators.com/llm-cost-calculator.html'),
          ('x-default','https://apicalculators.com/llm-cost-calculator.html')],
         ('TR', 'Turkey'),
         'Haziran 2026 · Güncel LLM fiyatları',
         '<span class="em">LLM API</span> Maliyet Hesaplayıcı',
         'GPT-4o, Claude 3.5 Sonnet, Gemini ve daha fazlasını karşılaştırın. Token hacmini girin — aylık maliyeti anında görün. Ücretsiz, kayıt yok.',
         tr_llm_calc, llm_calc_js, tr_llm_sections, tr_llm_faqs, '', tr_llm_related,
         home_url='/tr/')
))

# ── TR AWS Lambda (/tr/aws-lambda-maliyet.html) ───────────────────────────────
tr_lambda_calc = lambda_calc_html.replace('⚡ Serverless Cost Calculator','⚡ Serverless Maliyet Hesaplayıcı').replace('Select provider · Enter invocations and duration · Results update live','Sağlayıcı seç · Çağrı ve süre gir · Sonuçlar anlık').replace('Invocations / month (millions)','Çağrı / ay (milyon)').replace('Avg duration (ms)','Ort. süre (ms)').replace('Estimated monthly cost','Tahmini aylık maliyet').replace('Invocation cost','Çağrı maliyeti').replace('Compute cost','Hesaplama maliyeti').replace('Annual estimate','Yıllık tahmin')

tr_lambda_sections = """
<section class="sec">
  <h2>Serverless Fiyat Karşılaştırması 2026</h2>
  <p class="sh-sub">10M çağrı · 256MB · 200ms ort. süre için aylık maliyet.</p>
  <table class="ptable">
    <thead><tr><th>Sağlayıcı</th><th>Ücretsiz tier</th><th>Çağrı fiyatı</th><th>Hesaplama</th><th>10M çağrı / 200ms</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>AWS Lambda</strong><span class="badge">EN POPÜLER</span></td><td class="mono">1M çağrı/ay</td><td class="mono">$0.20/M</td><td class="mono">$0.0000167/GB-s</td><td class="mono">$3.47</td></tr>
      <tr><td><strong>Cloudflare Workers</strong></td><td class="mono">1M istek/gün (ücretsiz)</td><td class="mono">$0.30/M</td><td class="mono">$0.012/M GB-s</td><td class="mono">$2.70</td></tr>
      <tr><td><strong>Google Cloud Functions</strong></td><td class="mono">2M çağrı/ay</td><td class="mono">$0.40/M</td><td class="mono">$0.000025/GB-s</td><td class="mono">$3.20</td></tr>
    </tbody>
  </table>
  <div class="callout info"><div class="cl">⚠ Gizli maliyetler</div><p>AWS API Gateway 1M istek başına $3.50 ekler — genellikle Lambda faturanızı ikiye katlar. CloudWatch Logs GB başına $0.50 tutar. Bütçenize bu kalemleri de ekleyin.</p></div>
</section>""" + aff_block("Serverless bugün deploy et:", [("[VERCEL_AFFILIATE_LINK]", "▲ Vercel'de yayınla"), ("[CLOUDFLARE_AFFILIATE_LINK]", "🔶 Cloudflare Workers")])

tr_lambda_faqs = [
    ("AWS Lambda milyon istek başına ne kadar tutar?", "Ücretsiz tier (1M/ay) sonrası Lambda, milyon çağrı başına $0.20 alır. Ayrıca hesaplama maliyeti eklenir. 256MB / 200ms ort. süre ile 10M çağrı = ~$3.47/ay."),
    ("Cloudflare Workers, Lambda'dan ucuz mu?", "Kısa süreli (30ms altı) yüksek frekanslı API'lar için evet. Workers $0.30/M ile Lambda'yı geçer. Daha uzun hesaplamalar (500ms+) veya AWS entegrasyonları için Lambda daha iyidir."),
    ("AWS Lambda'nın ücretsiz tier'ı nedir?", "Her ay kalıcı olarak 1 milyon ücretsiz çağrı + 400.000 GB-saniye hesaplama süresi (12 aylık deneme değil, kalıcı). 256MB/200ms ile ~2M isteği karşılar."),
    ("Lambda'nın cold start süresi ne kadar?", "İnaktiflikten sonraki ilk istekte 100–500ms gecikme oluşur. Çözüm: Provisioned Concurrency, warm-up ping'leri veya cold start'ı olmayan Cloudflare Workers kullanmak."),
]

pages.append((
    os.path.join(BASE, 'tr', 'aws-lambda-maliyet.html'),
    page('tr', 'https://apicalculators.com/tr/aws-lambda-maliyet.html',
         'AWS Lambda Maliyet Hesaplama 2026 — Serverless Türkiye',
         'Ücretsiz AWS Lambda maliyet hesaplayıcı. Lambda, Cloudflare Workers ve Vercel karşılaştırın. Çağrı sayısını girin → aylık maliyeti anında görün.',
         'tr_TR',
         [('tr','https://apicalculators.com/tr/aws-lambda-maliyet.html'),
          ('en','https://apicalculators.com/aws-lambda-calculator.html'),
          ('x-default','https://apicalculators.com/aws-lambda-calculator.html')],
         ('TR', 'Turkey'),
         'Haziran 2026 · AWS Lambda fiyatları',
         '<span class="em">AWS Lambda</span> Maliyet Hesaplama',
         'Lambda, Cloudflare Workers, Vercel ve GCP Functions fiyatlarını karşılaştırın. Çağrı sayısı, süre, bellek girin — aylık maliyet anında görünür.',
         tr_lambda_calc, lambda_calc_js, tr_lambda_sections, tr_lambda_faqs, '', tr_llm_related,
         home_url='/tr/')
))

# ── Write all pages ────────────────────────────────────────────────────────────
written = []
for path, html in pages:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    rel = path.replace(BASE, '').replace('\\', '/')
    written.append(rel)
    print(f'  Written: {rel} ({len(html):,} chars)')

print(f'\nTotal: {len(written)} pages written')
