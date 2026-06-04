#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all DE/FR/TR issues: h2 titles, pdesc, partner CTA button text."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── 1. h2 title translations ───────────────────────────────────────────────────
H2 = {
    'Cloud VPS &amp; Database Cost Comparison': {
        'de': 'Cloud VPS &amp; Datenbank Kostenvergleich',
        'fr': 'Comparaison des coûts Cloud VPS &amp; Base de données',
        'tr': 'Bulut VPS &amp; Veritabanı Maliyet Karşılaştırması',
    },
    'STT &amp; TTS API Cost Calculator': {
        'de': 'STT &amp; TTS API Kostenrechner',
        'fr': 'Calculateur de coûts API STT &amp; TTS',
        'tr': 'STT &amp; TTS API Maliyet Hesaplayıcı',
    },
    'Serverless Compute Cost Calculator': {
        'de': 'Serverless Compute Kostenrechner',
        'fr': 'Calculateur de coûts Serverless',
        'tr': 'Sunucusuz Hesaplama Maliyet Hesaplayıcı',
    },
    'API Gateway Traffic Cost Calculator': {
        'de': 'API Gateway Traffic Kostenrechner',
        'fr': 'Calculateur de coûts trafic API Gateway',
        'tr': 'API Gateway Trafik Maliyet Hesaplayıcı',
    },
    'Embedding API Cost Calculator': {
        'de': 'Embedding API Kostenrechner',
        'fr': 'Calculateur de coûts API Embedding',
        'tr': 'Embedding API Maliyet Hesaplayıcı',
    },
    'AI Agent Multi-Model Cost Estimator': {
        'de': 'KI-Agent Multi-Modell Kostenschätzer',
        'fr': 'Estimateur de coûts Agent IA Multi-Modèle',
        'tr': 'YZ Ajan Çok-Model Maliyet Tahmincisi',
    },
}

# ── 2. pdesc translations (EN leaked text → local) ────────────────────────────
PDESC = {
    'de': {
        'Compare Vultr, DigitalOcean, Hetzner server costs. Keyword: <em>cloud VPS cost comparison</em>.':
            'Vultr, Hetzner, DigitalOcean und Linode VPS-Preise 2026 vergleichen. Keyword: <em>Cloud VPS Kostenvergleich</em>.',
        'Compare Whisper, ElevenLabs, Google Speech and OpenAI TTS API costs. Cost per minute for STT, per 1000 chars for TTS. Keyword: <em>speech to text API cost</em>.':
            'Whisper, ElevenLabs, Google Speech und OpenAI TTS API-Kosten vergleichen. Keyword: <em>Spracherkennung API Kosten</em>.',
        'Calculate AWS Lambda, Vercel Functions, Cloudflare Workers monthly cost. Price tables at 1M, 10M, 100M invocations. Keyword: <em>AWS Lambda cost calculator</em>.':
            'AWS Lambda, Vercel Functions und Cloudflare Workers Kosten 2026 berechnen. Keyword: <em>AWS Lambda Kosten Rechner</em>.',
        'Calculate AWS API Gateway, Cloudflare, Kong monthly costs. Price per million requests, data transfer fees included. Keyword: <em>API gateway pricing calculator</em>.':
            'AWS API Gateway, Cloudflare Workers und Kong Cloud Preise 2026 vergleichen. Keyword: <em>API Gateway Preisrechner</em>.',
        'Estimate OpenAI, Cohere, Voyage AI embedding costs. Price per 1M tokens for all models. Keyword: <em>embedding API cost calculator</em>.':
            'OpenAI, Cohere, Voyage AI und Jina AI Embedding-Kosten 2026 vergleichen. Keyword: <em>Embedding API Kosten</em>.',
        'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.':
            'KI-Agent-Pipeline-Gesamtkosten pro Lauf berechnen. Planner, Worker und Summariser wählen. Keyword: <em>KI Agent Kosten Rechner</em>.',
    },
    'fr': {
        'Compare Vultr, DigitalOcean, Hetzner server costs. Keyword: <em>cloud VPS cost comparison</em>.':
            'Comparez les prix VPS Hetzner, Vultr et DigitalOcean en 2026. Keyword: <em>comparaison cloud VPS</em>.',
        'Compare Whisper, ElevenLabs, Google Speech and OpenAI TTS API costs. Cost per minute for STT, per 1000 chars for TTS. Keyword: <em>speech to text API cost</em>.':
            'Comparez Whisper, ElevenLabs, Google Speech et OpenAI TTS en 2026. Keyword: <em>coût API speech to text</em>.',
        'Calculate AWS Lambda, Vercel Functions, Cloudflare Workers monthly cost. Price tables at 1M, 10M, 100M invocations. Keyword: <em>AWS Lambda cost calculator</em>.':
            'Calculez les coûts AWS Lambda, Vercel Functions et Cloudflare Workers en 2026. Keyword: <em>calculateur coût AWS Lambda</em>.',
        'Calculate AWS API Gateway, Cloudflare, Kong monthly costs. Price per million requests, data transfer fees included. Keyword: <em>API gateway pricing calculator</em>.':
            'Comparez AWS API Gateway, Cloudflare Workers et Kong Cloud en 2026. Keyword: <em>calculateur prix API gateway</em>.',
        'Estimate OpenAI, Cohere, Voyage AI embedding costs. Price per 1M tokens for all models. Keyword: <em>embedding API cost calculator</em>.':
            "Comparez OpenAI text-embedding-3-small, Cohere et Voyage AI en 2026. Keyword: <em>coût API embedding</em>.",
        'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.':
            "Calculez le coût réel des pipelines d'agents IA en 2026. Keyword: <em>calculateur coût agent IA</em>.",
    },
    'tr': {
        'Compare Vultr, DigitalOcean, Hetzner server costs. Keyword: <em>cloud VPS cost comparison</em>.':
            "Hetzner, Vultr ve DigitalOcean VPS fiyatlarını 2026'da karşılaştırın. Keyword: <em>bulut VPS maliyet karşılaştırması</em>.",
        'Compare Whisper, ElevenLabs, Google Speech and OpenAI TTS API costs. Cost per minute for STT, per 1000 chars for TTS. Keyword: <em>speech to text API cost</em>.':
            'Whisper, ElevenLabs, Google Speech ve OpenAI TTS API maliyetleri 2026. Keyword: <em>konuşma tanıma API maliyeti</em>.',
        'Calculate AWS Lambda, Vercel Functions, Cloudflare Workers monthly cost. Price tables at 1M, 10M, 100M invocations. Keyword: <em>AWS Lambda cost calculator</em>.':
            "AWS Lambda, Vercel Functions ve Cloudflare Workers maliyetlerini 2026'da hesaplayın. Keyword: <em>AWS Lambda maliyet hesaplayıcı</em>.",
        'Calculate AWS API Gateway, Cloudflare, Kong monthly costs. Price per million requests, data transfer fees included. Keyword: <em>API gateway pricing calculator</em>.':
            "AWS API Gateway, Cloudflare Workers ve Kong Cloud fiyatlarını 2026'da karşılaştırın. Keyword: <em>API gateway fiyat hesaplayıcı</em>.",
        'Estimate OpenAI, Cohere, Voyage AI embedding costs. Price per 1M tokens for all models. Keyword: <em>embedding API cost calculator</em>.':
            'OpenAI, Cohere, Voyage AI ve Jina AI embedding maliyetleri 2026. Keyword: <em>embedding API maliyet hesaplayıcı</em>.',
        'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.':
            "YZ ajan pipeline'larının gerçek maliyetini 2026'da hesaplayın. Keyword: <em>yapay zeka ajan maliyet hesaplayıcı</em>.",
    },
}

# ── 3. Partner CTA button replacement per lang ────────────────────────────────
PARTNER_CTA = {
    'de': {
        'old': 'Mit $200 DigitalOcean-Guthaben starten',
        'new': '$300 Vultr-Guthaben · Jetzt starten',
    },
    'fr': {
        'old': 'Démarrer avec $200 de crédits DigitalOcean',
        'new': '$300 de crédits Vultr · Démarrer maintenant',
    },
    'tr': {
        'old': '$200 DigitalOcean kredisiyle başla',
        'new': '$300 Vultr kredisi ile başla',
    },
}

TARGETS = {
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in TARGETS.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    fixes = []

    # Fix h2
    for en_h2, t in H2.items():
        old = f'<h2>{en_h2}</h2>'
        new = f'<h2>{t[lang]}</h2>'
        if old in c:
            c = c.replace(old, new)
            fixes.append(f'h2: {en_h2[:30]}')

    # Fix pdesc
    for en_p, local_p in PDESC[lang].items():
        if en_p in c:
            c = c.replace(en_p, local_p)
            fixes.append(f'pdesc: {en_p[:30]}')

    # Fix partner CTA button text
    cta = PARTNER_CTA[lang]
    if cta['old'] in c:
        c = c.replace(cta['old'], cta['new'])
        fixes.append(f'CTA: {cta["old"][:30]}')

    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'{lang}: {len(fixes)} fixes saved')
        for fx in fixes:
            print(f'  ✓ {fx}')
    else:
        print(f'{lang}: nothing changed (check strings match exactly)')

    # Verify
    leaked = sum(1 for line in c.split('\n') if 'class="pdesc"' in line and ('Compare ' in line or 'Calculate ' in line or 'Estimate ' in line))
    en_h2_leaked = sum(1 for h2, _ in H2.items() if h2 in c)
    print(f'  verify: EN pdesc leaked={leaked}, EN h2 leaked={en_h2_leaked}\n')

print('Done.')
