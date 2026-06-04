#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix: translate new panel h2+pdesc titles in DE/FR/TR, fix partner CTA button text."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── Partner CTA button text fixes ─────────────────────────────────────────────
PARTNER_CTA_OLD = '$200 DigitalOcean kredisiyle başla'
PARTNER_CTA_NEW_TR = '$300 Vultr kredisiyle başla'

PARTNER_CTA_OLD_DE = '$200 DigitalOcean-Guthaben starten'  # may vary
PARTNER_CTA_NEW_DE = '$300 Vultr-Guthaben starten'

PARTNER_CTA_OLD_FR = '$200 de crédit DigitalOcean'
PARTNER_CTA_NEW_FR = '$300 de crédit Vultr'

# ── Panel h2 translations ──────────────────────────────────────────────────────
H2_TRANSLATIONS = {
    # EN source → {lang: translation}
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
        'de': 'KI-Agent Multi-Model Kostenschätzer',
        'fr': 'Estimateur de coûts Agent IA Multi-Modèle',
        'tr': 'YZ Ajan Çok-Model Maliyet Tahmincisi',
    },
}

# ── Panel pdesc fixes (EN text in DE/FR/TR) ────────────────────────────────────
PDESC_FIXES = {
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
            'Gesamtkosten von KI-Agent-Pipelines pro Lauf berechnen. Planner, Worker und Summariser-Modelle wählen. Keyword: <em>KI Agent Kosten Rechner</em>.',
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
            'Comparez OpenAI text-embedding-3-small, Cohere et Voyage AI en 2026. Keyword: <em>coût API embedding</em>.',
        'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.':
            'Calculez le coût réel des pipelines d\'agents IA en 2026. Keyword: <em>calculateur coût agent IA</em>.',
    },
    'tr': {
        'Compare Vultr, DigitalOcean, Hetzner server costs. Keyword: <em>cloud VPS cost comparison</em>.':
            'Hetzner, Vultr ve DigitalOcean VPS fiyatlarını 2026\'da karşılaştırın. Keyword: <em>bulut VPS maliyet karşılaştırması</em>.',
        'Compare Whisper, ElevenLabs, Google Speech and OpenAI TTS API costs. Cost per minute for STT, per 1000 chars for TTS. Keyword: <em>speech to text API cost</em>.':
            'Whisper, ElevenLabs, Google Speech ve OpenAI TTS API maliyetleri 2026. Keyword: <em>konuşma tanıma API maliyeti</em>.',
        'Calculate AWS Lambda, Vercel Functions, Cloudflare Workers monthly cost. Price tables at 1M, 10M, 100M invocations. Keyword: <em>AWS Lambda cost calculator</em>.':
            'AWS Lambda, Vercel Functions ve Cloudflare Workers maliyetlerini 2026\'da hesaplayın. Keyword: <em>AWS Lambda maliyet hesaplayıcı</em>.',
        'Calculate AWS API Gateway, Cloudflare, Kong monthly costs. Price per million requests, data transfer fees included. Keyword: <em>API gateway pricing calculator</em>.':
            'AWS API Gateway, Cloudflare Workers ve Kong Cloud fiyatlarını 2026\'da karşılaştırın. Keyword: <em>API gateway fiyat hesaplayıcı</em>.',
        'Estimate OpenAI, Cohere, Voyage AI embedding costs. Price per 1M tokens for all models. Keyword: <em>embedding API cost calculator</em>.':
            'OpenAI, Cohere, Voyage AI ve Jina AI embedding maliyetleri 2026. Keyword: <em>embedding API maliyet hesaplayıcı</em>.',
        'Calculate multi-step agent pipeline total cost per run. Choose planner, worker, summariser models. Keyword: <em>AI agent cost calculator</em>.':
            'YZ ajan pipeline\'larının gerçek maliyetini 2026\'da hesaplayın. Keyword: <em>yapay zeka ajan maliyet hesaplayıcı</em>.',
    },
}

# ── Partner CTA button text per lang ──────────────────────────────────────────
# Find the Vultr partner button text (old DO text → new Vultr text)
PARTNER_FIXES = {
    'de': [
        # Various possible DE strings from _vultr_cta.py
        ('DigitalOcean', '$300 Vultr-Guthaben starten'),  # catch-all for DE CTA
    ],
    'fr': [
        ('DigitalOcean', '$300 de crédit Vultr'),
    ],
    'tr': [
        ('$200 DigitalOcean kredisiyle başla', '$300 Vultr kredisi ile başla'),
    ],
}

TARGETS = {
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in TARGETS.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    original = c

    # 1. Fix h2 titles
    for en_h2, translations in H2_TRANSLATIONS.items():
        if en_h2 in c:
            c = c.replace(f'<h2>{en_h2}</h2>', f'<h2>{translations[lang]}</h2>')
            print(f'{lang}: h2 fixed → {translations[lang][:40]}...')

    # 2. Fix pdesc text
    for en_pdesc, local_pdesc in PDESC_FIXES[lang].items():
        if en_pdesc in c:
            c = c.replace(en_pdesc, local_pdesc)
            print(f'{lang}: pdesc fixed')

    # 3. Fix partner CTA button text
    # Find the Vultr partner link and fix its display text
    import re
    # Pattern: the anchor tag for partner Vultr CTA
    def fix_cta_text(content, lang):
        # Find <a ... href="https://www.vultr.com/?ref=9904710-9J">...</a>
        pattern = r'(<a [^>]*href="https://www\.vultr\.com/\?ref=9904710-9J"[^>]*>)(.*?)(</a>)'
        def replacer(m):
            prefix = m.group(1)
            inner = m.group(2)
            suffix = m.group(3)
            vultr_labels = {
                'de': '<span class="em" style="font-weight:900;color:#1557c0">V</span> $300 Vultr-Guthaben · Jetzt starten <span class="arr">↗</span>',
                'fr': '<span class="em" style="font-weight:900;color:#1557c0">V</span> $300 crédit Vultr · Démarrer <span class="arr">↗</span>',
                'tr': '<span class="em" style="font-weight:900;color:#1557c0">V</span> $300 Vultr kredisi · Başla <span class="arr">↗</span>',
            }
            return prefix + vultr_labels[lang] + suffix
        new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        if new_content != content:
            print(f'{lang}: partner CTA button text fixed')
        return new_content

    c = fix_cta_text(c, lang)

    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'{lang}: saved ✓\n')
    else:
        print(f'{lang}: no changes needed\n')

print('All translation fixes done.')
