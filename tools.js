// tools.js — APICalculators.com pricing data + calculation functions
// All prices in USD (providers bill in USD; locale formatting handled by i18n.js)
// Updated: 2026-06-03

const PRICES = {
  llm: {
    "gpt-4o":            { label:"GPT-4o",             input: 2.50,  output: 10.00 },
    "gpt-4o-mini":       { label:"GPT-4o mini",        input: 0.15,  output: 0.60  },
    "o1":                { label:"OpenAI o1",           input: 15.00, output: 60.00 },
    "claude-3-5-sonnet": { label:"Claude 3.5 Sonnet",  input: 3.00,  output: 15.00 },
    "claude-3-5-haiku":  { label:"Claude 3.5 Haiku",   input: 0.80,  output: 4.00  },
    "claude-3-opus":     { label:"Claude 3 Opus",      input: 15.00, output: 75.00 },
    "gemini-1-5-pro":    { label:"Gemini 1.5 Pro",     input: 1.25,  output: 5.00  },
    "gemini-1-5-flash":  { label:"Gemini 1.5 Flash",   input: 0.075, output: 0.30  },
    "llama-3-70b":       { label:"Llama 3 70B (API)",  input: 0.59,  output: 0.79  },
  },

  image: {
    "dalle3-standard":   { label:"DALL·E 3 1024 Standard",  price: 0.040 },
    "dalle3-hd":         { label:"DALL·E 3 1024 HD",        price: 0.080 },
    "dalle3-1792":       { label:"DALL·E 3 1792 HD",        price: 0.120 },
    "sdxl-replicate":    { label:"SDXL via Replicate",      price: 0.006 },
    "sd3":               { label:"Stable Diffusion 3",      price: 0.035 },
    "flux-pro":          { label:"Flux.1 Pro (BFL API)",    price: 0.050 },
    "midjourney-basic":  { label:"Midjourney Basic (∕img)", price: 0.033 },
    "ideogram-v2":       { label:"Ideogram v2",             price: 0.080 },
  },

  cloud_vps: {
    vultr: {
      basic: { label:"Vultr 1 vCPU / 1GB",   cpu:1,  ram:1,  storage:25,  price:6    },
      std:   { label:"Vultr 2 vCPU / 4GB",   cpu:2,  ram:4,  storage:80,  price:24   },
      perf:  { label:"Vultr 4 vCPU / 8GB",   cpu:4,  ram:8,  storage:160, price:48   },
    },
    digitalocean: {
      basic: { label:"DO 1 vCPU / 1GB",  cpu:1,  ram:1,  storage:25,  price:6    },
      std:   { label:"DO 2 vCPU / 4GB",  cpu:2,  ram:4,  storage:80,  price:24   },
      perf:  { label:"DO 4 vCPU / 8GB",  cpu:4,  ram:8,  storage:160, price:48   },
    },
    hetzner: {
      basic: { label:"Hetzner CX22 2C/4G",  cpu:2, ram:4,  storage:40,  price:4.5  },
      std:   { label:"Hetzner CX32 4C/8G",  cpu:4, ram:8,  storage:80,  price:8.5  },
      perf:  { label:"Hetzner CX42 8C/16G", cpu:8, ram:16, storage:160, price:17   },
    },
    linode: {
      basic: { label:"Linode 1 vCPU / 1GB", cpu:1, ram:1,  storage:25,  price:5    },
      std:   { label:"Linode 2 vCPU / 4GB", cpu:2, ram:4,  storage:80,  price:18   },
    },
  },

  vector_db: {
    pinecone:  { label:"Pinecone (Serverless)", storage_per_gb:0.33,  query_per_M:16.0, min_mo:0   },
    qdrant:    { label:"Qdrant Cloud",          storage_per_gb:9.00,  query_per_M:0,    min_mo:0   },
    milvus:    { label:"Milvus (Zilliz Cloud)", storage_per_gb:0.30,  query_per_M:2.0,  min_mo:0   },
    weaviate:  { label:"Weaviate Cloud",        storage_per_gb:0.50,  query_per_M:10.0, min_mo:25  },
    supabase:  { label:"Supabase pgvector",     storage_per_gb:0.125, query_per_M:0,    min_mo:25  },
  },

  stt_tts: {
    "openai-whisper":    { type:"stt", label:"OpenAI Whisper",        per_min:0.006  },
    "google-stt":        { type:"stt", label:"Google STT Standard",   per_min:0.024  },
    "deepgram-nova":     { type:"stt", label:"Deepgram Nova-2",       per_min:0.0043 },
    "openai-tts":        { type:"tts", label:"OpenAI TTS Standard",   per_1k:0.015   },
    "openai-tts-hd":     { type:"tts", label:"OpenAI TTS HD",         per_1k:0.030   },
    "elevenlabs-starter":{ type:"tts", label:"ElevenLabs Starter",    per_1k:0.330   },
    "google-tts":        { type:"tts", label:"Google TTS Standard",   per_1k:0.016   },
  },

  serverless: {
    "aws-lambda":       { label:"AWS Lambda",         per_invoke:0.0000002,  per_gb_sec:0.0000166725 },
    "vercel-functions": { label:"Vercel Functions",   per_invoke:0.0000004,  per_gb_sec:0.000018     },
    "cf-workers":       { label:"Cloudflare Workers", per_invoke:0.0000003,  per_gb_sec:0.000012     },
    "gcp-functions":    { label:"GCP Cloud Functions",per_invoke:0.0000004,  per_gb_sec:0.000025     },
  },

  api_gateway: {
    "aws-api-gw":   { label:"AWS API Gateway",      per_M_req:3.50, per_gb:0.09 },
    "cloudflare":   { label:"Cloudflare (Workers)", per_M_req:0.50, per_gb:0.00 },
    "kong-cloud":   { label:"Kong Cloud",           per_M_req:2.00, per_gb:0.05 },
    "apigee":       { label:"Google Apigee",        per_M_req:3.00, per_gb:0.12 },
  },

  payment: {
    stripe:       { label:"Stripe",        pct:0.029, flat:0.30 },
    paddle:       { label:"Paddle",        pct:0.050, flat:0.50 },
    lemonsqueezy: { label:"Lemon Squeezy", pct:0.050, flat:0.50 },
    paypal:       { label:"PayPal",        pct:0.0349,flat:0.49 },
  },

  embedding: {
    "openai-text-3-small": { label:"OpenAI text-embedding-3-small", per_M:0.020 },
    "openai-text-3-large": { label:"OpenAI text-embedding-3-large", per_M:0.130 },
    "openai-ada-002":      { label:"OpenAI ada-002",                per_M:0.100 },
    "cohere-embed-v3":     { label:"Cohere embed-v3",               per_M:0.100 },
    "voyage-large-2":      { label:"Voyage AI large-2",             per_M:0.120 },
    "jina-embed-v3":       { label:"Jina AI v3",                    per_M:0.018 },
  },
};

// ─── CALCULATION FUNCTIONS ─────────────────────────────────────────────────
const Calc = {
  llm(modelId, inputM, outputM) {
    const p = PRICES.llm[modelId];
    if (!p) return null;
    const inCost  = inputM  * p.input;
    const outCost = outputM * p.output;
    return { input: inCost, output: outCost, total: inCost + outCost, model: p.label };
  },

  llmFromTokens(modelId, inputTokens, outputTokens, requests = 1) {
    const inputM  = (inputTokens  * requests) / 1e6;
    const outputM = (outputTokens * requests) / 1e6;
    return this.llm(modelId, inputM, outputM);
  },

  image(modelId, count) {
    const p = PRICES.image[modelId];
    if (!p) return null;
    return { total: count * p.price, perImage: p.price, count, model: p.label };
  },

  vectorDb(providerId, vectors, dimensions, queriesPerMonth) {
    const p = PRICES.vector_db[providerId];
    if (!p) return null;
    const bytes      = vectors * dimensions * 4 * 1.5; // float32 + ~50% index overhead
    const gb         = bytes / (1024 ** 3);
    const storageCost = gb * p.storage_per_gb;
    const queryCost   = (queriesPerMonth / 1e6) * p.query_per_M;
    const total      = Math.max(p.min_mo, storageCost + queryCost);
    return { total, storageCost, queryCost, baseFee: p.min_mo, gb, provider: p.label };
  },

  sttTts(modelId, volume) {
    const p = PRICES.stt_tts[modelId];
    if (!p) return null;
    const total = p.type === 'stt' ? volume * p.per_min : (volume / 1000) * p.per_1k;
    return { total, type: p.type, model: p.label };
  },

  serverless(providerId, invocations, durationMs, memoryGB) {
    const p = PRICES.serverless[providerId];
    if (!p) return null;
    const gbSec    = invocations * (durationMs / 1000) * memoryGB;
    const invCost  = invocations * p.per_invoke;
    const compCost = gbSec       * p.per_gb_sec;
    return { total: invCost + compCost, invCost, compCost, gbSec, provider: p.label };
  },

  apiGateway(providerId, reqMillions, transferGB) {
    const p = PRICES.api_gateway[providerId];
    if (!p) return null;
    const reqCost  = reqMillions * p.per_M_req;
    const xferCost = transferGB  * p.per_gb;
    return { total: reqCost + xferCost, reqCost, xferCost, provider: p.label };
  },

  payment(providerId, revenue, avgTicket) {
    const p = PRICES.payment[providerId];
    if (!p) return null;
    const txns  = avgTicket > 0 ? revenue / avgTicket : 0;
    const fees  = revenue * p.pct + txns * p.flat;
    const net   = revenue - fees;
    const effPct = revenue > 0 ? (fees / revenue) * 100 : 0;
    return { fees, net, txns, effPct, provider: p.label };
  },

  embedding(modelId, tokensM) {
    const p = PRICES.embedding[modelId];
    if (!p) return null;
    return { total: tokensM * p.per_M, perM: p.per_M, tokensM, model: p.label };
  },

  // Multi-step AI agent pipeline
  agentChain(steps) {
    // steps: [{modelId, inputTokens, outputTokens}, ...]
    let total = 0;
    const breakdown = steps.map((s, i) => {
      const r = this.llmFromTokens(s.modelId, s.inputTokens, s.outputTokens, 1);
      if (r) total += r.total;
      return { step: i + 1, ...r };
    });
    return { total, breakdown };
  },

  // Helpers
  monthly(dailyCost)  { return dailyCost * 30;  },
  annual(monthlyCost) { return monthlyCost * 12; },
};

// Export for use as module or global
if (typeof window !== 'undefined') window.Calc = Calc, window.PRICES = PRICES;
if (typeof module !== 'undefined') module.exports = { PRICES, Calc };
