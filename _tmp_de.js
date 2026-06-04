
(function(){var dd=document.getElementById('langDD'),btn=document.getElementById('langBtn'),hamb=document.getElementById('hamb'),mm=document.getElementById('mobileMenu');btn.addEventListener('click',function(e){e.stopPropagation();dd.classList.toggle('open');btn.setAttribute('aria-expanded',dd.classList.contains('open'));});document.addEventListener('click',function(){dd.classList.remove('open');btn.setAttribute('aria-expanded','false');});hamb.addEventListener('click',function(){var o=mm.classList.toggle('open');hamb.classList.toggle('open',o);hamb.setAttribute('aria-expanded',o);});mm.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){mm.classList.remove('open');hamb.classList.remove('open');});});})();
const LLM=[{id:"gpt-4o",name:"GPT-4o",in:2.50,out:10.00},{id:"gpt-4o-mini",name:"GPT-4o mini",in:0.15,out:0.60},{id:"o1",name:"OpenAI o1",in:15.00,out:60.00},{id:"claude-sonnet",name:"Claude 3.5 Sonnet",in:3.00,out:15.00},{id:"claude-haiku",name:"Claude 3.5 Haiku",in:0.80,out:4.00},{id:"claude-opus",name:"Claude 3 Opus",in:15.00,out:75.00},{id:"gemini-pro",name:"Gemini 1.5 Pro",in:1.25,out:5.00},{id:"gemini-flash",name:"Gemini 1.5 Flash",in:0.075,out:0.30}];
const VEC=[{id:"pinecone",name:"Pinecone (Serverless)",base:0,storagePerGB:0.33,queryPerMillion:16.00},{id:"supabase",name:"Supabase (pgvector)",base:25,storagePerGB:0.125,queryPerMillion:0},{id:"qdrant",name:"Qdrant Cloud",base:0,storagePerGB:9.00,queryPerMillion:0},{id:"weaviate",name:"Weaviate Cloud",base:25,storagePerGB:0.50,queryPerMillion:10.00}];
const IMG=[{id:"dalle3-std",name:"DALL·E 3 · 1024 Standard",unit:0.040},{id:"dalle3-hd",name:"DALL·E 3 · 1024 HD",unit:0.080},{id:"dalle3-wide",name:"DALL·E 3 · 1792 HD",unit:0.120},{id:"sdxl",name:"Stable Diffusion XL (API)",unit:0.009},{id:"sd3",name:"Stable Diffusion 3",unit:0.035},{id:"flux",name:"Flux.1 Pro (API)",unit:0.050}];
const PAY=[{id:"stripe",name:"Stripe",rate:0.029,fixed:0.30,note:"2,9% + $0,30"},{id:"paddle",name:"Paddle",rate:0.050,fixed:0.50,note:"5% + $0,50 · MoR"},{id:"lemon",name:"Lemon Squeezy",rate:0.050,fixed:0.50,note:"5% + $0,50 · MoR"},{id:"paypal",name:"PayPal",rate:0.0349,fixed:0.49,note:"3,49% + $0,49"}];
const $=id=>document.getElementById(id);
const num=v=>{const n=parseFloat(String(v).replace(/,/g,''));return isNaN(n)?0:n;};
const fmt$=v=>{if(v===0)return"$0";if(v<0.01)return"$"+v.toFixed(5);if(v<1)return"$"+v.toFixed(3);if(v<1000)return"$"+v.toFixed(2);return"$"+Math.round(v).toLocaleString("de-DE");};
const big$=v=>{if(v>=1000)return"$"+Math.round(v).toLocaleString("de-DE");if(v>=1)return"$"+v.toFixed(2);if(v>0)return"$"+v.toFixed(4);return"$0";};
const intf=v=>Math.round(v).toLocaleString("de-DE");
document.querySelectorAll('.tab').forEach(t=>{t.addEventListener('click',()=>{document.querySelectorAll('.tab').forEach(x=>{x.classList.remove('on');x.setAttribute('aria-selected','false');});document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));t.classList.add('on');t.setAttribute('aria-selected','true');$(t.dataset.tab).classList.add('on');});});
LLM.forEach(m=>{const o=document.createElement('option');o.value=m.id;o.textContent=`${m.name} — $${m.in}/$${m.out} pro 1M`;$('llmModel').appendChild(o);});
let llmDays=30;
$('llmPeriod').addEventListener('click',e=>{if(!e.target.dataset.v)return;[...$('llmPeriod').children].forEach(b=>b.classList.remove('on'));e.target.classList.add('on');llmDays=+e.target.dataset.v;calcLLM();});
function calcLLM(){const m=LLM.find(x=>x.id===$('llmModel').value);const inTok=num($('llmIn').value),outTok=num($('llmOut').value),req=num($('llmReq').value);const inCostReq=inTok/1e6*m.in,outCostReq=outTok/1e6*m.out;const perReq=inCostReq+outCostReq;const reqTotal=req*llmDays;const total=perReq*reqTotal;const totalTok=(inTok+outTok)*reqTotal;$('llmTotal').textContent=big$(total);$('llmPer').textContent=llmDays===1?"— pro Tag":llmDays===30?"— pro Monat":"— pro Jahr";$('llmPrice').textContent=`$${m.in} / $${m.out}`;$('llmPerReq').textContent=fmt$(perReq);$('llmInCost').textContent=fmt$(inCostReq*reqTotal);$('llmOutCost').textContent=fmt$(outCostReq*reqTotal);$('llmTok').textContent=intf(totalTok)+" Token";}
['llmModel','llmIn','llmOut','llmReq'].forEach(id=>$(id).addEventListener('input',calcLLM));
VEC.forEach(p=>{const o=document.createElement('option');o.value=p.id;o.textContent=p.name;$('vecProvider').appendChild(o);});
function calcVec(){const p=VEC.find(x=>x.id===$('vecProvider').value);const n=num($('vecCount').value),d=num($('vecDim').value),q=num($('vecQ').value);const bytes=n*d*4*1.5;const gb=bytes/(1024**3);const storeCost=gb*p.storagePerGB;const qCost=q/1e6*p.queryPerMillion;const total=p.base+storeCost+qCost;$('vecTotal').textContent=big$(total);$('vecName').textContent="— "+p.name;$('vecStore').textContent=gb<1?(gb*1024).toFixed(1)+" MB":gb.toFixed(2)+" GB";$('vecStoreCost').textContent=fmt$(storeCost);$('vecQCost').textContent=p.queryPerMillion?fmt$(qCost):"inklusive";$('vecBase').textContent=p.base?fmt$(p.base)+" /Mo":"keine Grundgebühr";}
['vecProvider','vecCount','vecDim','vecQ'].forEach(id=>$(id).addEventListener('input',calcVec));
IMG.forEach(m=>{const o=document.createElement('option');o.value=m.id;o.textContent=`${m.name} — $${m.unit}/Bild`;$('imgModel').appendChild(o);});
function calcImg(){const m=IMG.find(x=>x.id===$('imgModel').value);const c=num($('imgCount').value),v=Math.max(1,num($('imgVar').value));const totalImg=c*v;const total=totalImg*m.unit;$('imgTotal').textContent=big$(total);$('imgName').textContent="— "+m.name;$('imgUnit').textContent=fmt$(m.unit);$('imgGen').textContent=intf(totalImg)+" Bilder";$('imgK').textContent=fmt$(m.unit*1000);}
['imgModel','imgCount','imgVar'].forEach(id=>$(id).addEventListener('input',calcImg));
function calcPay(){const rev=num($('payRev').value),tx=num($('payTx').value);$('payAvg').value=tx>0?"$"+(rev/tx).toFixed(2):"$0.00";const rows=PAY.map(p=>{const fee=rev*p.rate+tx*p.fixed;return {...p,fee,net:rev-fee,pct:rev>0?fee/rev*100:0};}).sort((a,b)=>a.fee-b.fee);const max=Math.max(...rows.map(r=>r.fee),1);$('payCmp').innerHTML=rows.map((r,i)=>`<div class="cmpitem${i===0?' best':''}"><div class="cmptop"><span class="name">${r.name}${i===0?'<span class="badge">AM GÜNSTIGSTEN</span>':''}</span><span class="amt">${fmt$(r.fee)}</span></div><div class="bar"><i style="width:${(r.fee/max*100).toFixed(1)}%"></i></div><div class="cmpmeta">${r.note} · effektiv ${r.pct.toFixed(2)}% · netto ${fmt$(r.net)}</div></div>`).join('');}
['payRev','payTx'].forEach(id=>$(id).addEventListener('input',calcPay));
document.querySelectorAll('.qa').forEach(qa=>{qa.querySelector('.q').addEventListener('click',()=>{const open=qa.classList.contains('open');document.querySelectorAll('.qa').forEach(x=>{x.classList.remove('open');x.querySelector('.a').style.maxHeight=null;});if(!open){qa.classList.add('open');qa.querySelector('.a').style.maxHeight=qa.querySelector('.a').scrollHeight+'px';}});});
calcLLM();calcVec();calcImg();calcPay();

/* ===== CLOUD VPS ===== */
const CLOUD_PRICES = {
  vultr:        {1:{1:6},2:{4:24},4:{8:48},8:{16:96}},
  digitalocean: {1:{1:6},2:{4:24},4:{8:48},8:{16:96}},
  hetzner:      {2:{4:4.5},4:{8:8.5},8:{16:17}},
  linode:       {1:{1:5},2:{4:18}},
};
const CLOUD_PROVIDERS = [
  {id:'vultr',    name:'Vultr'},
  {id:'digitalocean', name:'DigitalOcean'},
  {id:'hetzner',  name:'Hetzner'},
  {id:'linode',   name:'Linode'},
];
function calcCloud(){
  var cpu=parseInt(document.getElementById('cloudCpu').value);
  var ram=parseInt(document.getElementById('cloudRam').value);
  var cnt=parseInt(document.getElementById('cloudCount').value)||1;
  var results=[];
  CLOUD_PROVIDERS.forEach(function(p){
    var tier=CLOUD_PRICES[p.id]||{};
    // find cheapest plan meeting requirements
    var best=null;
    Object.keys(tier).forEach(function(c){
      if(parseInt(c)>=cpu){
        Object.keys(tier[c]).forEach(function(r){
          if(parseInt(r)>=ram){
            var price=tier[c][r];
            if(!best||price<best.price) best={price:price,cpu:c,ram:r};
          }
        });
      }
    });
    if(best) results.push({name:p.name,price:best.price*cnt,cpu:best.cpu,ram:best.ram});
  });
  if(!results.length){document.getElementById('cloudTotal').textContent='N/A';return;}
  results.sort(function(a,b){return a.price-b.price;});
  var cheapest=results[0];
    var cheapestName = cheapest.name;
  document.getElementById('cloudTotal').textContent = '$' + cheapest.price.toFixed(2);
  document.getElementById('cloudPer').textContent   = 'per month — cheapest: ' + cheapestName;

  // Contextual Vultr CTA
  var ctaBox = document.getElementById('cloudVultrCta');
  if (ctaBox) {
    var isVultr = cheapestName === 'Vultr';
    ctaBox.style.display = 'block';
    ctaBox.innerHTML = isVultr
      ? '<div class="vcta vcta-win"><div class="vcta-icon">V</div><div class="vcta-body">'
        + '<div class="vcta-title">Deploy on Vultr — cheapest for your spec</div>'
        + '<div class="vcta-sub">Vultr matches your spec at the lowest price. Start with free credits.</div>'
        + '<a href="https://www.vultr.com/?ref=9904709" rel="sponsored nofollow" target="_blank" '
        + 'class="vcta-btn" onclick="trackAffiliateClick(\'vultr_calc\')">Deploy on Vultr →</a>'
        + '<span class="vcta-note">Affiliate link · You get $300 free credits</span></div></div>'
      : '<div class="vcta vcta-near"><div class="vcta-icon">V</div><div class="vcta-body">'
        + '<div class="vcta-title">Compare on Vultr</div>'
        + '<div class="vcta-sub">Vultr is close — compare plans before deciding.</div>'
        + '<a href="https://www.vultr.com/?ref=9904709" rel="sponsored nofollow" target="_blank" '
        + 'class="vcta-btn vcta-btn-sm" onclick="trackAffiliateClick(\'vultr_calc\')">Deploy on Vultr →</a>'
        + '</div></div>';
  }
  var cmp=document.getElementById('cloudCmp');
  cmp.innerHTML='';
  results.forEach(function(r){
    var row=document.createElement('div');row.className='brow'+(r===cheapest?' hl':'');
    row.innerHTML='<span>'+r.name+' ('+r.cpu+'vCPU/'+r.ram+'GB)</span><b>$'+r.price.toFixed(2)+'/mo</b>';
    cmp.appendChild(row);
  });
}
['cloudCpu','cloudRam','cloudCount'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcCloud),el.addEventListener('input',calcCloud);
});

/* ===== STT / TTS ===== */
const STT_RATES = {
  'whisper':     {type:'stt',rate:0.006},
  'google-stt':  {type:'stt',rate:0.024},
  'deepgram':    {type:'stt',rate:0.0043},
  'openai-tts':  {type:'tts',rate:0.015},
  'openai-tts-hd':{type:'tts',rate:0.030},
  'elevenlabs':  {type:'tts',rate:0.330},
  'google-tts':  {type:'tts',rate:0.016},
};
function calcStt(){
  var model=document.getElementById('sttModel').value;
  var vol=parseFloat(document.getElementById('sttVol').value)||0;
  var p=STT_RATES[model];if(!p)return;
  var total=p.type==='stt'?vol*p.rate:(vol/1000)*p.rate;
  document.getElementById('sttTotal').textContent='$'+total.toFixed(2);
  document.getElementById('sttPer').textContent='per month';
  document.getElementById('sttRate').textContent=p.type==='stt'?'$'+p.rate+'/min':'$'+p.rate+'/1K chars';
  document.getElementById('sttAnnual').textContent='$'+(total*12).toFixed(2);
}
['sttModel','sttVol'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcStt),el.addEventListener('input',calcStt);
});

/* ===== SERVERLESS ===== */
const SL_PRICES = {
  lambda:{inv:0.0000002, gb_sec:0.0000166725, free_inv:1000000, free_gb:400000},
  vercel:{inv:0.0000004, gb_sec:0.000018,     free_inv:0,       free_gb:0},
  cf:    {inv:0.0000003, gb_sec:0.000012,     free_inv:1000000, free_gb:0},
  gcp:   {inv:0.0000004, gb_sec:0.0000250,    free_inv:2000000, free_gb:400000},
};
function calcServerless(){
  var prov=document.getElementById('slProvider').value;
  var inv=parseFloat(document.getElementById('slInvoke').value)||0;
  var dur=parseFloat(document.getElementById('slDuration').value)||0;
  var mem=parseFloat(document.getElementById('slMemory').value)||0.25;
  var p=SL_PRICES[prov];if(!p)return;
  var billable_inv=Math.max(0,inv-p.free_inv);
  var gb_sec=inv*(dur/1000)*mem;
  var billable_gb=Math.max(0,gb_sec-p.free_gb);
  var inv_cost=billable_inv*p.inv;
  var comp_cost=billable_gb*p.gb_sec;
  var total=inv_cost+comp_cost;
  document.getElementById('slTotal').textContent='$'+total.toFixed(4);
  document.getElementById('slPer').textContent='per month';
  document.getElementById('slInvCost').textContent='$'+inv_cost.toFixed(4);
  document.getElementById('slCompCost').textContent='$'+comp_cost.toFixed(4);
  document.getElementById('slAnnual').textContent='$'+(total*12).toFixed(2);
}
['slProvider','slInvoke','slDuration','slMemory'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcServerless),el.addEventListener('input',calcServerless);
});

/* ===== API GATEWAY ===== */
const GW_PRICES = {
  aws: {per_m:3.50,per_gb:0.09},
  cf:  {per_m:0.50,per_gb:0.00},
  kong:{per_m:2.00,per_gb:0.05},
};
function calcGateway(){
  var prov=document.getElementById('gwProvider').value;
  var reqs=parseFloat(document.getElementById('gwReqs').value)||0;
  var xfer=parseFloat(document.getElementById('gwTransfer').value)||0;
  var p=GW_PRICES[prov];if(!p)return;
  var req_cost=reqs*p.per_m;
  var xfer_cost=xfer*p.per_gb;
  var total=req_cost+xfer_cost;
  document.getElementById('gwTotal').textContent='$'+total.toFixed(2);
  document.getElementById('gwPer').textContent='per month';
  document.getElementById('gwReqCost').textContent='$'+req_cost.toFixed(2);
  document.getElementById('gwXferCost').textContent='$'+xfer_cost.toFixed(2);
  document.getElementById('gwAnnual').textContent='$'+(total*12).toFixed(2);
}
['gwProvider','gwReqs','gwTransfer'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcGateway),el.addEventListener('input',calcGateway);
});

/* ===== EMBEDDING ===== */
const EMB_PRICES = {
  text3small:0.020, text3large:0.130, ada002:0.100,
  cohere:0.100, voyage:0.120, jina:0.018,
};
function calcEmbedding(){
  var model=document.getElementById('embModel').value;
  var tokM=parseFloat(document.getElementById('embTokens').value)||0;
  var docs=parseFloat(document.getElementById('embDocs').value)||1;
  var rate=EMB_PRICES[model];if(rate===undefined)return;
  var total=tokM*rate;
  var tok_per_doc=docs>0?(tokM*1e6/docs).toFixed(0):'—';
  document.getElementById('embTotal').textContent='$'+total.toFixed(4);
  document.getElementById('embPer').textContent='per month';
  document.getElementById('embRate').textContent='$'+rate+'/1M';
  document.getElementById('embPerDoc').textContent=tok_per_doc+' tokens';
  document.getElementById('embAnnual').textContent='$'+(total*12).toFixed(2);
}
['embModel','embTokens','embDocs'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcEmbedding),el.addEventListener('input',calcEmbedding);
});

/* ===== AI AGENT ===== */
const AG_LLM = {
  gpt4o:    {in:2.50,out:10.00},
  gpt4omini:{in:0.15,out:0.60},
  sonnet:   {in:3.00,out:15.00},
  haiku:    {in:0.80,out:4.00},
  gempro:   {in:1.25,out:5.00},
  flash:    {in:0.075,out:0.30},
};
var AG_STEPS=[
  {model:'agM1',in_tok:500,out_tok:100},
  {model:'agM2',in_tok:3000,out_tok:800},
  {model:'agM3',in_tok:1500,out_tok:300},
];
function calcAgent(){
  var runs=parseFloat(document.getElementById('agRuns').value)||0;
  var step_costs=AG_STEPS.map(function(s){
    var m=document.getElementById(s.model).value;
    var p=AG_LLM[m];if(!p)return 0;
    return (s.in_tok/1e6)*p.in+(s.out_tok/1e6)*p.out;
  });
  var per_run=step_costs.reduce(function(a,b){return a+b;},0);
  var total=per_run*runs;
  document.getElementById('agTotal').textContent='$'+total.toFixed(2);
  document.getElementById('agPer').textContent='per month';
  document.getElementById('agPerRun').textContent='$'+per_run.toFixed(6);
  document.getElementById('agS1').textContent='$'+(step_costs[0]*runs).toFixed(2);
  document.getElementById('agS2').textContent='$'+(step_costs[1]*runs).toFixed(2);
  document.getElementById('agS3').textContent='$'+(step_costs[2]*runs).toFixed(2);
  document.getElementById('agAnnual').textContent='$'+(total*12).toFixed(2);
}
['agM1','agM2','agM3','agRuns'].forEach(function(id){
  var el=document.getElementById(id);if(el)el.addEventListener('change',calcAgent),el.addEventListener('input',calcAgent);
});

/* ===== INIT ALL NEW CALCULATORS ===== */
calcCloud();calcStt();calcServerless();calcGateway();calcEmbedding();calcAgent();

