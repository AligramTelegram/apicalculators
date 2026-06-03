#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 6 new calculator tools to EN/DE/FR/TR index pages."""

import re, os

# ── New tab buttons (appended after tab-04) ──────────────────────────────────
NEW_TABS_EN = """    <button class="tab" role="tab" aria-selected="false" aria-controls="cloud" data-tab="cloud"><span class="ic">&#9729;&#65039;</span> Cloud VPS <span class="num">05</span></button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="stt" data-tab="stt"><span class="ic">&#127897;&#65039;</span> STT / TTS <span class="num">06</span></button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="serverless" data-tab="serverless"><span class="ic">&#9889;</span> Serverless <span class="num">07</span></button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="gateway" data-tab="gateway"><span class="ic">&#128256;</span> API Gateway <span class="num">08</span></button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="embedding" data-tab="embedding"><span class="ic">&#129710;</span> Embeddings <span class="num">09</span></button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="agent" data-tab="agent"><span class="ic">&#129302;</span> AI Agent <span class="num">10</span></button>"""

# ── Localised tab labels ──────────────────────────────────────────────────────
TAB_LABELS = {
    "de": ["Cloud VPS", "STT / TTS", "Serverless", "API-Gateway", "Embeddings", "KI-Agent"],
    "fr": ["Cloud VPS", "STT / TTS", "Serverless", "API Gateway", "Embeddings", "Agent IA"],
    "tr": ["Cloud VPS", "STT / TTS", "Serverless", "API Gateway", "Embeddings", "YZ Ajan"],
}

def make_tabs(labels):
    ids = ["cloud","stt","serverless","gateway","embedding","agent"]
    nums = ["05","06","07","08","09","10"]
    icons = ["&#9729;&#65039;","&#127897;&#65039;","&#9889;","&#128256;","&#129710;","&#129302;"]
    lines = []
    for label, id_, num, icon in zip(labels, ids, nums, icons):
        lines.append(
            f'    <button class="tab" role="tab" aria-selected="false" '
            f'aria-controls="{id_}" data-tab="{id_}">'
            f'<span class="ic">{icon}</span> {label} <span class="num">{num}</span></button>'
        )
    return "\n".join(lines)

# ── 6 new panels (HTML) ───────────────────────────────────────────────────────
def make_panels(lang="en"):
    L = {
        "en": {
            "cloud_h": "Cloud VPS &amp; Database Cost Comparison",
            "cloud_d": "Compare Vultr, DigitalOcean, Hetzner server costs. Keyword: <em>cloud VPS cost comparison</em>.",
            "cloud_cpu": "vCPU cores", "cloud_ram": "RAM", "cloud_srv": "Servers",
            "stt_h": "STT &amp; TTS API Cost Calculator",
            "stt_d": "Estimate Whisper, ElevenLabs, Google Speech costs. Keyword: <em>speech to text API cost</em>.",
            "stt_vol": "Audio minutes / month",
            "sl_h": "Serverless Compute Cost Calculator",
            "sl_d": "AWS Lambda, Vercel, Cloudflare Workers. Keyword: <em>AWS Lambda cost calculator</em>.",
            "sl_inv": "Invocations / month", "sl_dur": "Avg duration (ms)", "sl_mem": "Memory",
            "gw_h": "API Gateway Traffic Cost Calculator",
            "gw_d": "AWS API GW, Cloudflare, Kong costs. Keyword: <em>API gateway pricing calculator</em>.",
            "gw_req": "Requests (millions/month)", "gw_xf": "Data transfer out (GB)",
            "emb_h": "Embedding API Cost Calculator",
            "emb_d": "OpenAI, Cohere, Voyage AI embedding costs. Keyword: <em>embedding API cost</em>.",
            "emb_tok": "Tokens / month (millions)", "emb_doc": "Documents",
            "ag_h": "AI Agent Multi-Model Cost Estimator",
            "ag_d": "Multi-step agent pipeline cost per run. Keyword: <em>AI agent cost calculator</em>.",
            "ag_runs": "Agent runs / month",
            "step1":"Step 1 — Planner","step2":"Step 2 — Worker","step3":"Step 3 — Summariser",
            "per_run":"Cost per run","annual":"Annual estimate",
            "inv_cost":"Invocation cost","comp_cost":"Compute cost (GB-sec)",
            "req_cost":"Request cost","xfer_cost":"Transfer cost",
            "rate":"Rate / 1M tokens","per_doc":"Tokens / document",
        },
        "de": {
            "cloud_h": "Cloud VPS &amp; Datenbank Kostenvergleich",
            "cloud_d": "Vultr, DigitalOcean, Hetzner Vergleich. Keyword: <em>Cloud VPS Kostenvergleich</em>.",
            "cloud_cpu": "vCPU-Kerne", "cloud_ram": "RAM", "cloud_srv": "Server",
            "stt_h": "STT &amp; TTS API Kostenrechner",
            "stt_d": "Whisper, ElevenLabs, Google Speech. Keyword: <em>Speech-to-Text API Kosten</em>.",
            "stt_vol": "Audio-Minuten / Monat",
            "sl_h": "Serverless Compute Kostenrechner",
            "sl_d": "AWS Lambda, Vercel, CF Workers. Keyword: <em>AWS Lambda Kostenrechner</em>.",
            "sl_inv": "Aufrufe / Monat", "sl_dur": "Ø Dauer (ms)", "sl_mem": "Arbeitsspeicher",
            "gw_h": "API-Gateway Traffic Kostenrechner",
            "gw_d": "AWS API GW, Cloudflare, Kong. Keyword: <em>API Gateway Preisrechner</em>.",
            "gw_req": "Anfragen (Millionen/Monat)", "gw_xf": "Datentransfer out (GB)",
            "emb_h": "Embedding API Kostenrechner",
            "emb_d": "OpenAI, Cohere, Voyage AI Embedding-Kosten. Keyword: <em>Embedding API Kosten</em>.",
            "emb_tok": "Token / Monat (Millionen)", "emb_doc": "Dokumente",
            "ag_h": "KI-Agent Multi-Modell Kostenrechner",
            "ag_d": "Mehrstufige Agent-Pipeline. Keyword: <em>KI Agent Kosten</em>.",
            "ag_runs": "Agent-Läufe / Monat",
            "step1":"Schritt 1 — Planer","step2":"Schritt 2 — Arbeiter","step3":"Schritt 3 — Zusammenfassung",
            "per_run":"Kosten pro Lauf","annual":"Jahresschätzung",
            "inv_cost":"Aufrufkosten","comp_cost":"Rechenkosten (GB-Sek)",
            "req_cost":"Anfragekosten","xfer_cost":"Transferkosten",
            "rate":"Preis / 1M Token","per_doc":"Token / Dokument",
        },
        "fr": {
            "cloud_h": "Comparaison Coûts Cloud VPS &amp; Base de Données",
            "cloud_d": "Vultr, DigitalOcean, Hetzner. Keyword: <em>comparaison cloud VPS</em>.",
            "cloud_cpu": "Cœurs vCPU", "cloud_ram": "RAM", "cloud_srv": "Serveurs",
            "stt_h": "Calculatrice API STT &amp; TTS",
            "stt_d": "Whisper, ElevenLabs, Google Speech. Keyword: <em>coût API speech-to-text</em>.",
            "stt_vol": "Minutes audio / mois",
            "sl_h": "Calculatrice Coûts Serverless",
            "sl_d": "AWS Lambda, Vercel, CF Workers. Keyword: <em>calculateur coût AWS Lambda</em>.",
            "sl_inv": "Invocations / mois", "sl_dur": "Durée moy. (ms)", "sl_mem": "Mémoire",
            "gw_h": "Calculatrice Coûts API Gateway",
            "gw_d": "AWS API GW, Cloudflare, Kong. Keyword: <em>calculateur prix API gateway</em>.",
            "gw_req": "Requêtes (millions/mois)", "gw_xf": "Transfert sortant (Go)",
            "emb_h": "Calculatrice API Embedding",
            "emb_d": "OpenAI, Cohere, Voyage AI. Keyword: <em>coût API embedding</em>.",
            "emb_tok": "Tokens / mois (millions)", "emb_doc": "Documents",
            "ag_h": "Estimateur Coûts Agent IA Multi-Modèle",
            "ag_d": "Pipeline agent multi-étapes. Keyword: <em>coût agent IA</em>.",
            "ag_runs": "Exécutions agent / mois",
            "step1":"Étape 1 — Planificateur","step2":"Étape 2 — Travailleur","step3":"Étape 3 — Résumeur",
            "per_run":"Coût par exécution","annual":"Estimation annuelle",
            "inv_cost":"Coût invocations","comp_cost":"Coût calcul (Go-sec)",
            "req_cost":"Coût requêtes","xfer_cost":"Coût transfert",
            "rate":"Tarif / 1M tokens","per_doc":"Tokens / document",
        },
        "tr": {
            "cloud_h": "Bulut VPS &amp; Veritabanı Maliyet Karşılaştırması",
            "cloud_d": "Vultr, DigitalOcean, Hetzner karşılaştırması. Keyword: <em>bulut VPS maliyet karşılaştırma</em>.",
            "cloud_cpu": "vCPU çekirdek", "cloud_ram": "RAM", "cloud_srv": "Sunucu sayısı",
            "stt_h": "STT &amp; TTS API Maliyet Hesaplayıcı",
            "stt_d": "Whisper, ElevenLabs, Google Speech. Keyword: <em>konuşma tanıma API maliyet</em>.",
            "stt_vol": "Ses dakikası / ay",
            "sl_h": "Serverless Hesaplama Maliyet Hesaplayıcı",
            "sl_d": "AWS Lambda, Vercel, CF Workers. Keyword: <em>AWS Lambda maliyet hesaplayıcı</em>.",
            "sl_inv": "Çağrı / ay", "sl_dur": "Ort. süre (ms)", "sl_mem": "Bellek",
            "gw_h": "API Gateway Trafik Maliyet Hesaplayıcı",
            "gw_d": "AWS API GW, Cloudflare, Kong. Keyword: <em>API gateway fiyat hesaplayıcı</em>.",
            "gw_req": "İstek sayısı (milyon/ay)", "gw_xf": "Veri transferi (GB)",
            "emb_h": "Embedding API Maliyet Hesaplayıcı",
            "emb_d": "OpenAI, Cohere, Voyage AI. Keyword: <em>embedding API maliyeti</em>.",
            "emb_tok": "Token / ay (milyon)", "emb_doc": "Belge sayısı",
            "ag_h": "YZ Ajan Çoklu Model Maliyet Tahmincisi",
            "ag_d": "Çok adımlı ajan pipeline maliyeti. Keyword: <em>YZ ajan maliyeti</em>.",
            "ag_runs": "Ajan çalıştırma / ay",
            "step1":"Adım 1 — Planlayıcı","step2":"Adım 2 — Çalışan","step3":"Adım 3 — Özetleyici",
            "per_run":"Çalıştırma başı maliyet","annual":"Yıllık tahmin",
            "inv_cost":"Çağrı maliyeti","comp_cost":"Hesaplama maliyeti",
            "req_cost":"İstek maliyeti","xfer_cost":"Transfer maliyeti",
            "rate":"Fiyat / 1M token","per_doc":"Token / belge",
        },
    }
    t = L.get(lang, L["en"])

    stt_options = {
        "en": [
            ('whisper','OpenAI Whisper — $0.006/min'),
            ('google-stt','Google STT — $0.024/min'),
            ('deepgram','Deepgram Nova-2 — $0.0043/min'),
            ('openai-tts','OpenAI TTS — $15/1M chars'),
            ('openai-tts-hd','OpenAI TTS HD — $30/1M chars'),
            ('elevenlabs','ElevenLabs — $330/1M chars'),
            ('google-tts','Google TTS — $16/1M chars'),
        ],
        "de": [
            ('whisper','OpenAI Whisper — $0,006/Min'),
            ('google-stt','Google STT — $0,024/Min'),
            ('deepgram','Deepgram Nova-2 — $0,0043/Min'),
            ('openai-tts','OpenAI TTS — $15/1M Zeichen'),
            ('openai-tts-hd','OpenAI TTS HD — $30/1M Zeichen'),
            ('elevenlabs','ElevenLabs — $330/1M Zeichen'),
            ('google-tts','Google TTS — $16/1M Zeichen'),
        ],
        "fr": [
            ('whisper','OpenAI Whisper — $0,006/min'),
            ('google-stt','Google STT — $0,024/min'),
            ('deepgram','Deepgram Nova-2 — $0,0043/min'),
            ('openai-tts','OpenAI TTS — $15/1M cars'),
            ('openai-tts-hd','OpenAI TTS HD — $30/1M cars'),
            ('elevenlabs','ElevenLabs — $330/1M cars'),
            ('google-tts','Google TTS — $16/1M cars'),
        ],
        "tr": [
            ('whisper','OpenAI Whisper — $0,006/dak'),
            ('google-stt','Google STT — $0,024/dak'),
            ('deepgram','Deepgram Nova-2 — $0,0043/dak'),
            ('openai-tts','OpenAI TTS — $15/1M karakter'),
            ('openai-tts-hd','OpenAI TTS HD — $30/1M karakter'),
            ('elevenlabs','ElevenLabs — $330/1M karakter'),
            ('google-tts','Google TTS — $16/1M karakter'),
        ],
    }

    stt_opts_html = ""
    stt_grp = {
        "en": ("Speech-to-Text (STT)", "Text-to-Speech (TTS)"),
        "de": ("Spracherk. (STT)", "Sprachsynth. (TTS)"),
        "fr": ("Reconnaissance vocale (STT)", "Synthèse vocale (TTS)"),
        "tr": ("Konuşma Tanıma (STT)", "Metin Seslendirme (TTS)"),
    }
    g = stt_grp.get(lang, stt_grp["en"])
    opts = stt_options.get(lang, stt_options["en"])
    stt_opts_html = f'<optgroup label="{g[0]}">\n'
    for v,lbl in opts[:3]:
        stt_opts_html += f'            <option value="{v}">{lbl}</option>\n'
    stt_opts_html += f'          </optgroup>\n          <optgroup label="{g[1]}">\n'
    for v,lbl in opts[3:]:
        stt_opts_html += f'            <option value="{v}">{lbl}</option>\n'
    stt_opts_html += '          </optgroup>'

    mem_labels = {
        "en": ["128 MB","256 MB","512 MB","1024 MB"],
        "de": ["128 MB","256 MB","512 MB","1024 MB"],
        "fr": ["128 Mo","256 Mo","512 Mo","1024 Mo"],
        "tr": ["128 MB","256 MB","512 MB","1024 MB"],
    }
    mems = mem_labels.get(lang, mem_labels["en"])

    gw_opts = {
        "en": [("aws","AWS API Gateway — $3.50/M req"),("cf","Cloudflare Workers — $0.50/M req"),("kong","Kong Cloud — $2.00/M req")],
        "de": [("aws","AWS API Gateway — $3,50/Mio. Anf."),("cf","Cloudflare Workers — $0,50/Mio. Anf."),("kong","Kong Cloud — $2,00/Mio. Anf.")],
        "fr": [("aws","AWS API Gateway — $3,50/M req"),("cf","Cloudflare Workers — $0,50/M req"),("kong","Kong Cloud — $2,00/M req")],
        "tr": [("aws","AWS API Gateway — $3,50/M istek"),("cf","Cloudflare Workers — $0,50/M istek"),("kong","Kong Cloud — $2,00/M istek")],
    }
    gw_html = "\n".join(f'            <option value="{v}">{lbl}</option>' for v,lbl in gw_opts.get(lang, gw_opts["en"]))

    emb_opts = [
        ("text3small","OpenAI text-3-small — $0.020/1M"),
        ("text3large","OpenAI text-3-large — $0.130/1M"),
        ("ada002","OpenAI ada-002 — $0.100/1M"),
        ("cohere","Cohere embed-v3 — $0.100/1M"),
        ("voyage","Voyage AI large-2 — $0.120/1M"),
        ("jina","Jina AI v3 — $0.018/1M"),
    ]
    emb_html = "\n".join(f'            <option value="{v}">{lbl}</option>' for v,lbl in emb_opts)

    ag_m_opts = {
        "en": [
            ("Step 1 — Planner / Router", [("gpt4omini","GPT-4o mini"),("haiku","Claude 3.5 Haiku"),("flash","Gemini Flash")], "gpt4omini"),
            ("Step 2 — Main Worker",      [("gpt4o","GPT-4o"),("sonnet","Claude 3.5 Sonnet"),("gempro","Gemini Pro")], "gpt4o"),
            ("Step 3 — Summariser",       [("gpt4omini","GPT-4o mini"),("flash","Gemini Flash"),("haiku","Claude Haiku")], "gpt4omini"),
        ],
        "de": [
            ("Schritt 1 — Planer", [("gpt4omini","GPT-4o mini"),("haiku","Claude 3.5 Haiku"),("flash","Gemini Flash")], "gpt4omini"),
            ("Schritt 2 — Arbeiter",[("gpt4o","GPT-4o"),("sonnet","Claude 3.5 Sonnet"),("gempro","Gemini Pro")], "gpt4o"),
            ("Schritt 3 — Zusammenfassung",[("gpt4omini","GPT-4o mini"),("flash","Gemini Flash"),("haiku","Claude Haiku")], "gpt4omini"),
        ],
        "fr": [
            ("Étape 1 — Planificateur",[("gpt4omini","GPT-4o mini"),("haiku","Claude 3.5 Haiku"),("flash","Gemini Flash")], "gpt4omini"),
            ("Étape 2 — Travailleur", [("gpt4o","GPT-4o"),("sonnet","Claude 3.5 Sonnet"),("gempro","Gemini Pro")], "gpt4o"),
            ("Étape 3 — Résumeur",    [("gpt4omini","GPT-4o mini"),("flash","Gemini Flash"),("haiku","Claude Haiku")], "gpt4omini"),
        ],
        "tr": [
            ("Adım 1 — Planlayıcı",[("gpt4omini","GPT-4o mini"),("haiku","Claude 3.5 Haiku"),("flash","Gemini Flash")], "gpt4omini"),
            ("Adım 2 — Çalışan",   [("gpt4o","GPT-4o"),("sonnet","Claude 3.5 Sonnet"),("gempro","Gemini Pro")], "gpt4o"),
            ("Adım 3 — Özetleyici",[("gpt4omini","GPT-4o mini"),("flash","Gemini Flash"),("haiku","Claude Haiku")], "gpt4omini"),
        ],
    }
    ids_ag = ["agM1","agM2","agM3"]
    ag_selects = ""
    for (lbl, opts_ag, default), id_ in zip(ag_m_opts.get(lang, ag_m_opts["en"]), ids_ag):
        ag_selects += f'        <label class="lbl">{lbl}</label>\n'
        ag_selects += f'        <select class="sel" id="{id_}">\n'
        for v,lbl2 in opts_ag:
            sel = ' selected' if v == default else ''
            ag_selects += f'          <option value="{v}"{sel}>{lbl2}</option>\n'
        ag_selects += '        </select>\n'

    return f'''
  <!-- PANEL 5: Cloud VPS -->
  <section class="panel" id="cloud" role="tabpanel">
    <div class="panel-head">
      <h2>{t["cloud_h"]}</h2>
      <p class="pdesc">{t["cloud_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
        <label class="lbl" for="cloudCpu">{t["cloud_cpu"]}</label>
        <select class="sel" id="cloudCpu">
          <option value="1">1 vCPU</option><option value="2" selected>2 vCPU</option>
          <option value="4">4 vCPU</option><option value="8">8 vCPU</option>
        </select>
        <label class="lbl" for="cloudRam">{t["cloud_ram"]}</label>
        <select class="sel" id="cloudRam">
          <option value="1">1 GB</option><option value="4" selected>4 GB</option>
          <option value="8">8 GB</option><option value="16">16 GB</option>
        </select>
        <label class="lbl" for="cloudCount">{t["cloud_srv"]}</label>
        <input class="inp" id="cloudCount" type="number" value="1" min="1">
      </div>
      <div class="result">
        <div class="big" id="cloudTotal">$0</div>
        <div class="per" id="cloudPer">—</div>
        <div class="breakdown" id="cloudCmp"></div>
      </div>
    </div>
  </section>

  <!-- PANEL 6: STT/TTS -->
  <section class="panel" id="stt" role="tabpanel">
    <div class="panel-head">
      <h2>{t["stt_h"]}</h2>
      <p class="pdesc">{t["stt_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
        <label class="lbl" for="sttModel">Provider</label>
        <select class="sel" id="sttModel">
          {stt_opts_html}
        </select>
        <label class="lbl" for="sttVol">{t["stt_vol"]}</label>
        <input class="inp" id="sttVol" type="number" value="10000" min="0">
      </div>
      <div class="result">
        <div class="big" id="sttTotal">$0</div>
        <div class="per" id="sttPer">—</div>
        <div class="breakdown">
          <div class="brow"><span>{t["rate"]}</span><b id="sttRate">—</b></div>
          <div class="brow hl"><span>{t["annual"]}</span><b id="sttAnnual">—</b></div>
        </div>
      </div>
    </div>
  </section>

  <!-- PANEL 7: Serverless -->
  <section class="panel" id="serverless" role="tabpanel">
    <div class="panel-head">
      <h2>{t["sl_h"]}</h2>
      <p class="pdesc">{t["sl_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
        <label class="lbl" for="slProvider">Platform</label>
        <select class="sel" id="slProvider">
          <option value="lambda">AWS Lambda</option>
          <option value="vercel">Vercel Functions</option>
          <option value="cf">Cloudflare Workers</option>
          <option value="gcp">GCP Cloud Functions</option>
        </select>
        <label class="lbl" for="slInvoke">{t["sl_inv"]}</label>
        <input class="inp" id="slInvoke" type="number" value="1000000" min="0">
        <label class="lbl" for="slDuration">{t["sl_dur"]}</label>
        <input class="inp" id="slDuration" type="number" value="150" min="1">
        <label class="lbl" for="slMemory">{t["sl_mem"]}</label>
        <select class="sel" id="slMemory">
          <option value="0.125">{mems[0]}</option>
          <option value="0.25" selected>{mems[1]}</option>
          <option value="0.5">{mems[2]}</option>
          <option value="1">{mems[3]}</option>
        </select>
      </div>
      <div class="result">
        <div class="big" id="slTotal">$0</div>
        <div class="per" id="slPer">—</div>
        <div class="breakdown">
          <div class="brow"><span>{t["inv_cost"]}</span><b id="slInvCost">—</b></div>
          <div class="brow"><span>{t["comp_cost"]}</span><b id="slCompCost">—</b></div>
          <div class="brow hl"><span>{t["annual"]}</span><b id="slAnnual">—</b></div>
        </div>
      </div>
    </div>
  </section>

  <!-- PANEL 8: API Gateway -->
  <section class="panel" id="gateway" role="tabpanel">
    <div class="panel-head">
      <h2>{t["gw_h"]}</h2>
      <p class="pdesc">{t["gw_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
        <label class="lbl" for="gwProvider">Provider</label>
        <select class="sel" id="gwProvider">
{gw_html}
        </select>
        <label class="lbl" for="gwReqs">{t["gw_req"]}</label>
        <input class="inp" id="gwReqs" type="number" value="10" min="0" step="0.1">
        <label class="lbl" for="gwTransfer">{t["gw_xf"]}</label>
        <input class="inp" id="gwTransfer" type="number" value="50" min="0">
      </div>
      <div class="result">
        <div class="big" id="gwTotal">$0</div>
        <div class="per" id="gwPer">—</div>
        <div class="breakdown">
          <div class="brow"><span>{t["req_cost"]}</span><b id="gwReqCost">—</b></div>
          <div class="brow"><span>{t["xfer_cost"]}</span><b id="gwXferCost">—</b></div>
          <div class="brow hl"><span>{t["annual"]}</span><b id="gwAnnual">—</b></div>
        </div>
      </div>
    </div>
  </section>

  <!-- PANEL 9: Embedding -->
  <section class="panel" id="embedding" role="tabpanel">
    <div class="panel-head">
      <h2>{t["emb_h"]}</h2>
      <p class="pdesc">{t["emb_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
        <label class="lbl" for="embModel">Model</label>
        <select class="sel" id="embModel">
{emb_html}
        </select>
        <label class="lbl" for="embTokens">{t["emb_tok"]}</label>
        <input class="inp" id="embTokens" type="number" value="100" min="0">
        <label class="lbl" for="embDocs">{t["emb_doc"]}</label>
        <input class="inp" id="embDocs" type="number" value="500000" min="0">
      </div>
      <div class="result">
        <div class="big" id="embTotal">$0</div>
        <div class="per" id="embPer">—</div>
        <div class="breakdown">
          <div class="brow"><span>{t["rate"]}</span><b id="embRate">—</b></div>
          <div class="brow"><span>{t["per_doc"]}</span><b id="embPerDoc">—</b></div>
          <div class="brow hl"><span>{t["annual"]}</span><b id="embAnnual">—</b></div>
        </div>
      </div>
    </div>
  </section>

  <!-- PANEL 10: AI Agent -->
  <section class="panel" id="agent" role="tabpanel">
    <div class="panel-head">
      <h2>{t["ag_h"]}</h2>
      <p class="pdesc">{t["ag_d"]}</p>
    </div>
    <div class="panel-body">
      <div class="inputs">
{ag_selects}        <label class="lbl" for="agRuns">{t["ag_runs"]}</label>
        <input class="inp" id="agRuns" type="number" value="5000" min="1">
      </div>
      <div class="result">
        <div class="big" id="agTotal">$0</div>
        <div class="per" id="agPer">—</div>
        <div class="breakdown">
          <div class="brow"><span>{t["per_run"]}</span><b id="agPerRun">—</b></div>
          <div class="brow"><span>{t["step1"]}</span><b id="agS1">—</b></div>
          <div class="brow"><span>{t["step2"]}</span><b id="agS2">—</b></div>
          <div class="brow"><span>{t["step3"]}</span><b id="agS3">—</b></div>
          <div class="brow hl"><span>{t["annual"]}</span><b id="agAnnual">—</b></div>
        </div>
      </div>
    </div>
  </section>
'''

# ── JavaScript for 6 new calculators ─────────────────────────────────────────
NEW_JS = """
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
  document.getElementById('cloudTotal').textContent='$'+cheapest.price.toFixed(2);
  document.getElementById('cloudPer').textContent='per month (cheapest match: '+cheapest.name+')';
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
"""

# ── SEO meta updates ──────────────────────────────────────────────────────────
SEO_UPDATES = {
    "en": {
        "title": "LLM, Cloud VPS, Serverless & Embedding Cost Calculators | APICalculators",
        "desc":  "Free real-time cost calculators for LLM tokens, vector databases, cloud VPS, serverless (AWS Lambda), STT/TTS APIs, API gateway, embeddings, AI agents and payment fees. 10 tools, zero signup.",
        "kw":    "LLM cost calculator, AWS Lambda cost calculator, cloud VPS comparison, embedding API cost, STT TTS API pricing, API gateway pricing, AI agent cost, vector database pricing, payment processor fees",
        "hero_tag": "2026 pricing · 10 calculators · runs 100% in your browser",
        "hero_sub": "Real-time cost estimators for LLM tokens, vector DBs, cloud VPS, serverless, STT/TTS, API gateway, embeddings, AI agents and payment fees. Free, no signup.",
    },
    "de": {
        "title": "LLM, Cloud VPS, Serverless &amp; Embedding Kostenrechner | APICalculators",
        "desc":  "Kostenlose Echtzeit-Rechner für LLM-Token, Vektordatenbanken, Cloud VPS, Serverless (AWS Lambda), STT/TTS, API-Gateway, Embeddings, KI-Agenten und Zahlungsgebühren.",
        "kw":    "LLM Kostenrechner, AWS Lambda Rechner, Cloud VPS Vergleich, Embedding API Kosten, STT TTS API Kosten, API Gateway Rechner, KI Agent Kosten",
        "hero_tag": "2026 Preise · 10 Rechner · 100% im Browser",
        "hero_sub": "Echtzeit-Kostenrechner für LLM-Token, Vektordatenbanken, Cloud VPS, Serverless, STT/TTS, API-Gateway, Embeddings, KI-Agenten und Zahlungsgebühren.",
    },
    "fr": {
        "title": "Calculatrices LLM, Cloud VPS, Serverless &amp; Embeddings | APICalculators",
        "desc":  "Calculatrices gratuites en temps réel pour tokens LLM, bases vectorielles, cloud VPS, serverless (AWS Lambda), STT/TTS, API gateway, embeddings, agents IA et frais de paiement.",
        "kw":    "calculatrice LLM, calculateur AWS Lambda, comparaison cloud VPS, coût API embedding, coût STT TTS, calculateur API gateway, coût agent IA",
        "hero_tag": "Tarifs 2026 · 10 outils · 100% navigateur",
        "hero_sub": "Estimateurs de coûts en temps réel pour tokens LLM, bases vectorielles, cloud VPS, serverless, STT/TTS, API gateway, embeddings, agents IA et frais de paiement.",
    },
    "tr": {
        "title": "LLM, Cloud VPS, Serverless ve Embedding Maliyet Hesaplayıcıları | APICalculators",
        "desc":  "LLM token, vektör veritabanı, cloud VPS, serverless, STT/TTS, API gateway, embedding, YZ ajan ve ödeme ücretleri için ücretsiz gerçek zamanlı hesaplayıcılar.",
        "kw":    "LLM maliyet hesaplayıcı, AWS Lambda hesaplayıcı, cloud VPS karşılaştırma, embedding API maliyet, STT TTS fiyat, API gateway maliyet, YZ ajan maliyet",
        "hero_tag": "2026 fiyatları · 10 hesaplayıcı · 100% tarayıcıda",
        "hero_sub": "LLM token, vektör veritabanı, cloud VPS, serverless, STT/TTS, API gateway, embedding, YZ ajan ve ödeme ücretleri için gerçek zamanlı maliyet tahminleri.",
    },
}

# ── Process a file ────────────────────────────────────────────────────────────
def process_file(path, lang):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    seo = SEO_UPDATES[lang]

    # Title
    content = re.sub(r'<title>[^<]+</title>', f'<title>{seo["title"]}</title>', content)
    # Description
    content = re.sub(r'<meta name="description" content="[^"]*"',
                     f'<meta name="description" content="{seo["desc"]}"', content)
    # Keywords
    content = re.sub(r'<meta name="keywords" content="[^"]*"',
                     f'<meta name="keywords" content="{seo["kw"]}"', content)

    # Hero tagpill (EN only has this pattern; others may differ)
    # Replace calculator count in tagpill
    content = re.sub(r'\d+ calculators?', '10 calculators', content)
    content = re.sub(r'\d+ Rechner', '10 Rechner', content)
    content = re.sub(r'\d+ outils', '10 outils', content)
    content = re.sub(r'\d+ hesaplayıcı', '10 hesaplayıcı', content)

    # Add 6 new tabs after tab-04 (pay)
    tab_04_pattern = r'(<button[^>]+data-tab="pay"[^>]*>.*?</button>)'
    tabs_lang = make_tabs(TAB_LABELS.get(lang, ["Cloud VPS","STT/TTS","Serverless","API Gateway","Embeddings","AI Agent"]))
    if lang == "en":
        tabs_insert = NEW_TABS_EN
    else:
        tabs_insert = tabs_lang

    if 'data-tab="cloud"' not in content:
        content = re.sub(tab_04_pattern,
                         lambda m: m.group(0) + '\n' + tabs_insert,
                         content, flags=re.DOTALL)

    # Add 6 new panels before the AD: IN-CONTENT comment
    panels_html = make_panels(lang)
    ad_marker = '<!-- AD: IN-CONTENT -->'
    if 'id="cloud"' not in content and ad_marker in content:
        content = content.replace(ad_marker, panels_html + '\n' + ad_marker)

    # Add JS before </script> that contains the existing calc JS block
    # Find the last </script> before </body>
    js_marker = '/* ===== CLOUD VPS ====='
    if js_marker not in content:
        # Insert before last </script>
        content = content.replace('</script>\n</body>', NEW_JS + '\n</script>\n</body>', 1)
        # fallback: replace last occurrence
        if js_marker not in content:
            last_script = content.rfind('</script>')
            if last_script != -1:
                content = content[:last_script] + NEW_JS + '\n' + content[last_script:]

    return content

# ── File paths ────────────────────────────────────────────────────────────────
BASE = r'C:\Users\muham\Desktop\APICalculators'
FILES = {
    "en": os.path.join(BASE, 'index.html'),
    "de": os.path.join(BASE, 'de', 'index.html'),
    "fr": os.path.join(BASE, 'fr', 'index.html'),
    "tr": os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in FILES.items():
    if not os.path.exists(path):
        print(f"SKIP {path}")
        continue
    new_content = process_file(path, lang)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"OK {lang}: {path}")

print("Done. All 4 files updated.")
