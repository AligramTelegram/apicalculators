#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add panel descriptions (pdesc) to all 6 new tool panels in 4 langs."""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

PDESC = {
    'cloud': {
        'en': 'Compare Vultr, DigitalOcean, Hetzner, and Linode server costs at your required specs. Keyword: <em>cloud VPS cost comparison</em>.',
        'de': 'Vultr, DigitalOcean, Hetzner und Linode VPS Preise 2026 im Vergleich. Keyword: <em>Cloud VPS Kostenvergleich</em>.',
        'fr': 'Comparez les prix VPS Hetzner, Vultr, DigitalOcean et Linode en 2026. Keyword: <em>comparaison cloud VPS</em>.',
        'tr': 'Hetzner, Vultr, DigitalOcean ve Linode VPS fiyatları 2026. Keyword: <em>bulut VPS maliyet karşılaştırması</em>.',
    },
    'stt': {
        'en': 'Compare Whisper, ElevenLabs, Google Speech and OpenAI TTS API costs. Cost per minute for STT, per 1000 chars for TTS. Keyword: <em>speech to text API cost</em>.',
        'de': 'Whisper, ElevenLabs, Google Speech und OpenAI TTS API-Kosten vergleichen. Keyword: <em>Spracherkennung API Kosten</em>.',
        'fr': 'Comparez les coûts Whisper, ElevenLabs, Google Speech et OpenAI TTS en 2026. Keyword: <em>coût API speech to text</em>.',
        'tr': 'Whisper, ElevenLabs, Google Speech ve OpenAI TTS API maliyetleri. Keyword: <em>konuşma tanıma API maliyeti</em>.',
    },
    'serverless': {
        'en': 'Calculate AWS Lambda, Vercel Functions, Cloudflare Workers monthly cost. Price tables at 1M, 10M, 100M invocations. Keyword: <em>AWS Lambda cost calculator</em>.',
        'de': 'AWS Lambda, Vercel Functions und Cloudflare Workers Kosten 2026 berechnen. Keyword: <em>AWS Lambda Kosten Rechner</em>.',
        'fr': 'Calculez les coûts AWS Lambda, Vercel Functions et Cloudflare Workers en 2026. Keyword: <em>calculateur coût AWS Lambda</em>.',
        'tr': 'AWS Lambda, Vercel Functions ve Cloudflare Workers maliyetlerini 2026\'da hesaplayın. Keyword: <em>AWS Lambda maliyet hesaplayıcı</em>.',
    },
    'gateway': {
        'en': 'Calculate AWS API Gateway, Cloudflare, Kong monthly costs. Price per million requests, data transfer fees included. Keyword: <em>API gateway pricing calculator</em>.',
        'de': 'AWS API Gateway, Cloudflare Workers und Kong Cloud Preise 2026 vergleichen. Keyword: <em>API Gateway Preisrechner</em>.',
        'fr': 'Comparez AWS API Gateway, Cloudflare Workers et Kong Cloud en 2026. Keyword: <em>calculateur prix API gateway</em>.',
        'tr': 'AWS API Gateway, Cloudflare Workers ve Kong Cloud fiyatlarını 2026\'da karşılaştırın. Keyword: <em>API gateway fiyat hesaplayıcı</em>.',
    },
    'embedding': {
        'en': 'Estimate OpenAI, Cohere, Voyage AI embedding costs. Price per 1M tokens for all models. Keyword: <em>embedding API cost calculator</em>.',
        'de': 'OpenAI, Cohere, Voyage AI und Jina AI Embedding-Kosten 2026 vergleichen. Keyword: <em>Embedding API Kosten</em>.',
        'fr': 'Comparez OpenAI text-embedding-3-small, Cohere embed-v3, Voyage AI et Jina AI en 2026. Keyword: <em>coût API embedding</em>.',
        'tr': 'OpenAI, Cohere, Voyage AI ve Jina AI embedding maliyetleri 2026. Keyword: <em>embedding API maliyet hesaplayıcı</em>.',
    },
    'agent': {
        'en': 'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.',
        'de': 'Berechnen Sie die Gesamtkosten von KI-Agent-Pipelines pro Lauf. Keyword: <em>KI Agent Kosten Rechner</em>.',
        'fr': 'Calculez le coût réel des pipelines d\'agents IA en 2026. Keyword: <em>calculateur coût agent IA</em>.',
        'tr': 'YZ ajan pipeline\'larının gerçek maliyetini 2026\'da hesaplayın. Keyword: <em>yapay zeka ajan maliyet hesaplayıcı</em>.',
    },
}

PANELS = ['cloud', 'stt', 'serverless', 'gateway', 'embedding', 'agent']
LANGS = ['en', 'de', 'fr', 'tr']

for lang in LANGS:
    path = os.path.join(BASE, 'index.html') if lang == 'en' else os.path.join(BASE, lang, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    changed = False
    for panel_id in PANELS:
        # Find panel opening: <section class="panel" id="[panel_id]"
        pattern = f'<section class="panel" id="{panel_id}"'
        if pattern not in c:
            print(f"{lang}: panel {panel_id} not found")
            continue

        # Find <h2> inside this panel
        panel_start = c.find(pattern)
        h2_start = c.find('<h2>', panel_start)
        h2_end   = c.find('</h2>', h2_start) + len('</h2>')

        # Check if pdesc already exists after </h2>
        after_h2 = c[h2_end:h2_end+200]
        if 'class="pdesc"' in after_h2:
            # Already has pdesc
            continue

        # Insert pdesc after </h2>
        pdesc_html = f'\n      <p class="pdesc">{PDESC[panel_id][lang]}</p>'
        c = c[:h2_end] + pdesc_html + c[h2_end:]
        print(f"{lang}/{panel_id}: pdesc added")
        changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"{lang}: saved")

    # Verify
    pdesc_count = c.count('class="pdesc"')
    print(f"{lang}: {pdesc_count} pdesc elements\n")

print("pdesc injection done.")
