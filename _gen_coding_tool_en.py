#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

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
.tool-result.best::before{content:"BEST VALUE";font-family:'Cascadia Code','Consolas',monospace;font-size:9px;color:var(--lime);letter-spacing:.1em;display:block;margin-bottom:4px}
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
footer a{color:var(--muted)}.footer a:hover{color:var(--lime)}"""

SCHEMA = '''{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Is Cursor really $20/month?","acceptedAnswer":{"@type":"Answer","text":"Cursor Pro starts at $20/month but heavy agentic usage can push bills to $60-200/month. The Pro plan has usage limits; exceeding them triggers Pro+ ($60) or Ultra ($200) tier pricing."}},
    {"@type":"Question","name":"Which AI coding tool is cheapest in 2026?","acceptedAnswer":{"@type":"Answer","text":"GitHub Copilot at $10/month offers the best value for light-to-medium users. For heavy agentic work, Claude Code Max 5x ($100/month) or Cursor Pro ($20/month with limits) compete."}},
    {"@type":"Question","name":"Is Claude Code free?","acceptedAnswer":{"@type":"Answer","text":"Claude Code has a limited free tier. The Pro plan is $20/month, Max 5x is $100/month, and Max 20x is $200/month. Heavy API usage through Claude Code can exceed subscription costs significantly."}},
    {"@type":"Question","name":"Cursor vs GitHub Copilot - which is better for teams?","acceptedAnswer":{"@type":"Answer","text":"Copilot Business ($19/seat) offers predictable team billing. Cursor Business ($40/seat) has stronger IDE integration but higher cost. For teams over 10, Copilot usually wins on total cost."}}
  ]
}'''

SCHEMA2 = '{"@context":"https://schema.org","@type":"SoftwareApplication","name":"AI Coding Tool Cost Calculator 2026","applicationCategory":"DeveloperApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":"https://apicalculators.com/ai-coding-tool-cost.html"}'

SCHEMA3 = '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"APICalculators","item":"https://apicalculators.com"},{"@type":"ListItem","position":2,"name":"AI Coding Tool Cost Calculator 2026"}]}'

JS = """
const TOOLS = {
  copilot:  { name:'GitHub Copilot', light:10,  medium:10,  heavy:19,  biz:19,  note:'Predictable flat pricing' },
  cursor:   { name:'Cursor',         light:20,  medium:20,  heavy:80,  biz:40,  note:'$20-200 depending on usage' },
  claude:   { name:'Claude Code',    light:20,  medium:20,  heavy:120, biz:100, note:'$20-200 depending on tasks' },
  windsurf: { name:'Windsurf',       light:15,  medium:15,  heavy:45,  biz:30,  note:'Credits deplete on heavy use' },
  tabnine:  { name:'Tabnine',        light:12,  medium:12,  heavy:12,  biz:39,  note:'Fixed price, no overages' },
  bolt:     { name:'Bolt.new',       light:20,  medium:20,  heavy:50,  biz:50,  note:'Token-based, can exceed plan' },
  v0:       { name:'v0 by Vercel',   light:20,  medium:20,  heavy:50,  biz:50,  note:'Token-based credits' }
};

function calc() {
  const usage = document.getElementById('usage').value;
  const type  = document.getElementById('type').value;
  const team  = parseInt(document.getElementById('team').value) || 1;
  const res   = document.getElementById('results');

  let multiplier = 1;
  if (type === 'agent') multiplier = 2.5;
  else if (type === 'all') multiplier = 3;
  else if (type === 'chat') multiplier = 1.2;

  const rows = Object.entries(TOOLS).map(([k,t]) => {
    let base = usage === 'light' ? t.light : usage === 'medium' ? t.medium : t.heavy;
    if (usage === 'heavy' && (k === 'cursor' || k === 'claude')) base = Math.min(base * multiplier, k==='cursor'?200:200);
    const total = base * team;
    return { key:k, name:t.name, per:base, total, note:t.note };
  }).sort((a,b) => a.total - b.total);

  const bestVal = rows[0].total;
  res.innerHTML = rows.map((r,i) => `
    <div class="tool-result${i===0?' best':''}">
      <div>
        <div class="tname">${r.name}</div>
        <div class="tnote">${r.note}</div>
      </div>
      <div style="text-align:right">
        <div class="tprice">$${r.total.toLocaleString()}/mo</div>
        ${team>1?`<div class="tnote">$${r.per}/seat</div>`:''}
      </div>
    </div>`).join('');
}

document.querySelectorAll('.sel,.inp').forEach(el => el.addEventListener('change', calc));
calc();

document.querySelectorAll('.qa .q').forEach(q => {
  q.addEventListener('click', () => {
    const qa = q.parentElement;
    const open = qa.classList.toggle('open');
    q.querySelector('.a-box, .a') && (q.nextElementSibling.style.maxHeight = open ? '300px' : '0');
    const a = qa.querySelector('.a');
    if(a) a.style.maxHeight = open ? '300px' : '0';
  });
});
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<title>AI Coding Tool Cost Calculator 2026 — Cursor vs Copilot vs Claude Code</title>
<meta name="description" content="Free calculator to compare real AI coding tool costs. Cursor vs GitHub Copilot vs Claude Code vs Windsurf. Find your true monthly bill. No signup.">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://apicalculators.com/ai-coding-tool-cost.html">
<link rel="alternate" hreflang="en" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<link rel="alternate" hreflang="de" href="https://apicalculators.com/de/ki-coding-tool-kosten.html"/>
<link rel="alternate" hreflang="fr" href="https://apicalculators.com/fr/cout-outil-ia-coding.html"/>
<link rel="alternate" hreflang="tr" href="https://apicalculators.com/tr/yapay-zeka-kodlama-arac-maliyeti.html"/>
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com/ai-coding-tool-cost.html"/>
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US"/>
<meta property="og:title" content="AI Coding Tool Cost Calculator 2026 — Cursor vs Copilot vs Claude Code">
<meta property="og:description" content="Free calculator to compare real AI coding tool costs. Cursor vs GitHub Copilot vs Claude Code vs Windsurf.">
<meta property="og:url" content="https://apicalculators.com/ai-coding-tool-cost.html">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@apicalculators">
<meta name="twitter:creator" content="@apicalculators">
<meta name="twitter:title" content="AI Coding Tool Cost Calculator 2026 — Cursor vs Copilot vs Claude Code">
<meta name="twitter:description" content="Compare real monthly costs for AI coding tools. No pricing page surprises.">
<meta name="twitter:image" content="https://apicalculators.com/twitter-image.png">
<script type="application/ld+json">{SCHEMA}</script>
<script type="application/ld+json">{SCHEMA2}</script>
<script type="application/ld+json">{SCHEMA3}</script>
<style>{CSS}</style>
</head>
<body>
<header class="nav">
  <div class="wrap nav-in">
    <a href="/" class="logo">API<b>Calculators</b></a>
    <nav class="nav-r"><a href="/">Calculators</a><a href="/blog/">Blog</a><a href="/about.html">About</a></nav>
  </div>
</header>

<section class="hero wrap">
  <span class="chip"><span class="dot"></span> June 2026 · Updated Pricing</span>
  <h1 class="ph"><span class="em">AI Coding Tool</span> Cost Calculator</h1>
  <p class="intro">Cursor says $20/month. Your bill says $180. Find out what you'll actually pay for Cursor, GitHub Copilot, Claude Code, and Windsurf based on your real usage pattern.</p>
</section>

<div class="wrap">
<div class="calc-shell" id="calc">
  <div class="calc-header">
    <h2>💻 AI Coding Tool Cost Calculator</h2>
    <p>Select usage pattern · Results update live</p>
  </div>
  <div class="calc-body">
    <div>
      <div class="field">
        <label for="usage">Daily usage intensity</label>
        <select class="sel" id="usage">
          <option value="light">Light (1-2 hours/day)</option>
          <option value="medium" selected>Medium (2-4 hours/day)</option>
          <option value="heavy">Heavy (4+ hours/day, agents)</option>
        </select>
      </div>
      <div class="field">
        <label for="type">Primary use case</label>
        <select class="sel" id="type">
          <option value="complete">Code completion only</option>
          <option value="chat" selected>Completion + chat</option>
          <option value="agent">Agentic tasks</option>
          <option value="all">Everything (completion + chat + agents)</option>
        </select>
      </div>
      <div class="field">
        <label for="team">Team size</label>
        <select class="sel" id="team">
          <option value="1" selected>Individual (1 person)</option>
          <option value="3">Small team (3)</option>
          <option value="5">Small team (5)</option>
          <option value="10">Medium team (10)</option>
          <option value="20">Medium team (20)</option>
          <option value="50">Large team (50+)</option>
        </select>
      </div>
    </div>
    <div>
      <div style="font-family:'Cascadia Code','Consolas',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Estimated monthly cost — sorted cheapest first</div>
      <div class="result-grid" id="results"></div>
    </div>
  </div>
</div>

<div class="callout warn">
  <div class="cl">⚠ Hidden cost warning</div>
  <p>Cursor Pro ($20) auto-upgrades to Pro+ ($60) or Ultra ($200) when you hit limits. Claude Code API usage can add $15+ per heavy session. Always monitor your billing dashboard.</p>
</div>

<section class="sec">
  <h2>True Monthly Cost: What the Pricing Pages Don't Show</h2>
  <p class="sh-sub">Headline price vs real bill at different usage levels.</p>
  <table class="ptable">
    <thead><tr><th>Tool</th><th>Listed Price</th><th>Light User</th><th>Heavy User</th><th>Team of 10</th></tr></thead>
    <tbody>
      <tr class="best"><td><strong>GitHub Copilot</strong><span class="badge">PREDICTABLE</span></td><td class="mono">$10/mo</td><td class="mono">$10</td><td class="mono">$19</td><td class="mono">$190</td></tr>
      <tr><td><strong>Windsurf</strong></td><td class="mono">$15/mo</td><td class="mono">$15</td><td class="mono">$30-60</td><td class="mono">$300</td></tr>
      <tr><td><strong>Cursor</strong></td><td class="mono">$20/mo</td><td class="mono">$20</td><td class="mono">$60-200</td><td class="mono">$400+</td></tr>
      <tr><td><strong>Claude Code</strong></td><td class="mono">$20/mo</td><td class="mono">$20</td><td class="mono">$100-200</td><td class="mono">$200-1,000</td></tr>
      <tr><td><strong>Tabnine</strong></td><td class="mono">$12/mo</td><td class="mono">$12</td><td class="mono">$12</td><td class="mono">$390</td></tr>
    </tbody>
  </table>
</section>

<section class="sec">
  <h2>When Does Cursor Cost More Than Copilot?</h2>
  <p class="sh-sub">The crossover point depends entirely on how you use agentic features.</p>
  <p style="color:var(--muted);font-size:15px;margin-bottom:16px">Cursor Pro's $20/month plan includes a limited number of "fast requests." Once you exceed this quota — typically within a few days for power users running agent loops — Cursor automatically bumps you to Pro+ at $60/month. Run multi-file refactors or long agent sessions daily and you'll hit Ultra at $200/month.</p>
  <p style="color:var(--muted);font-size:15px;margin-bottom:16px">GitHub Copilot Business at $19/seat has no usage-based overages. For teams that want predictable billing, Copilot wins. For individual developers who primarily use autocomplete and occasional chat, Cursor Pro at $20 is competitive.</p>
  <div class="callout tip">
    <div class="cl">💡 Hybrid strategy</div>
    <p>Use Copilot ($10/mo) for daily autocomplete + Claude Code Pro ($20/mo) for agent tasks. Total: $30/mo vs Cursor Ultra at $200/mo. Same capability, 85% cheaper.</p>
  </div>
</section>

<div class="aff-box">
  <p>Start with the best value option:</p>
  <div class="btns">
    <a href="[GITHUB_COPILOT_AFFILIATE]" rel="sponsored noopener" target="_blank" class="aff-btn">🐙 Try GitHub Copilot — $10/mo</a>
    <a href="[WINDSURF_REFERRAL]" rel="sponsored noopener" target="_blank" class="aff-btn">🌊 Try Windsurf free</a>
  </div>
</div>

<section class="sec">
  <h2>Frequently Asked Questions</h2>
  <div class="faq">
    <div class="qa"><div class="q">Is Cursor really $20/month?<span class="plus">+</span></div><div class="a"><p>Cursor Pro starts at $20/month but heavy agentic usage can push bills to $60-200/month. The Pro plan has usage limits; exceeding them triggers Pro+ ($60) or Ultra ($200) tier pricing.</p></div></div>
    <div class="qa"><div class="q">Which AI coding tool is cheapest in 2026?<span class="plus">+</span></div><div class="a"><p>GitHub Copilot at $10/month offers the best value for light-to-medium users. For heavy agentic work, Claude Code Max 5x ($100/month) or Cursor Pro ($20/month with limits) compete. Use the calculator above for your specific usage.</p></div></div>
    <div class="qa"><div class="q">Is Claude Code free?<span class="plus">+</span></div><div class="a"><p>Claude Code has a limited free tier. The Pro plan is $20/month, Max 5x is $100/month, and Max 20x is $200/month. Heavy API usage through Claude Code can exceed subscription costs significantly.</p></div></div>
    <div class="qa"><div class="q">Cursor vs GitHub Copilot — which is better for teams?<span class="plus">+</span></div><div class="a"><p>Copilot Business ($19/seat) offers predictable team billing. Cursor Business ($40/seat) has stronger IDE integration but higher cost. For teams over 10, Copilot usually wins on total cost.</p></div></div>
  </div>
</section>

<section class="sec">
  <h2>Related Calculators</h2>
  <div class="tool-links">
    <a href="/llm-cost-calculator.html" class="tool-link"><span class="ic">🤖</span><div><div class="tl-name">LLM API Cost</div><div class="tl-desc">GPT-4o, Claude, Gemini pricing</div></div></a>
    <a href="/auth-provider-cost.html" class="tool-link"><span class="ic">🔑</span><div><div class="tl-name">Auth Provider Cost</div><div class="tl-desc">Clerk vs Auth0 vs Supabase</div></div></a>
    <a href="/api-gateway-cost.html" class="tool-link"><span class="ic">🔀</span><div><div class="tl-name">API Gateway Cost</div><div class="tl-desc">AWS vs Cloudflare pricing</div></div></a>
    <a href="/" class="tool-link"><span class="ic">🧮</span><div><div class="tl-name">All Calculators</div><div class="tl-desc">10 free infra cost tools</div></div></a>
  </div>
</section>
</div>

<footer><div class="wrap foot-in">
  <span>© 2026 <a href="/">APICalculators</a> · Free infra cost tools</span>
  <span>Prices are estimates · verify before you ship</span>
</div></footer>
<script>{JS}</script>
</body>
</html>"""

path = os.path.join(BASE, 'ai-coding-tool-cost.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'✓ Created: ai-coding-tool-cost.html')
