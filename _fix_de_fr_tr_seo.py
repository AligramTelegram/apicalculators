#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

# ─────────────────────────────────────────────────────────────────────────────
# DE
# ─────────────────────────────────────────────────────────────────────────────
de = os.path.join(BASE, 'de', 'index.html')
c = read(de)

# H1 — keyword ekle
c = c.replace(
    '<h1 class="h">Kennen Sie Ihre <span class="em">Infra-Kosten</span><br>bevor es die Rechnung tut.</h1>',
    '<h1 class="h">Kostenlose <span class="em">LLM &amp; API Kostenrechner</span> — Kennen Sie Ihre Infra-Kosten bevor die Rechnung kommt.</h1>'
)

# Hero tagpill — 10 → 12
c = c.replace('10 Rechner', '12 Rechner')
c = c.replace('2026-Preise · 12 Rechner', '2026-Preise · 12 Rechner')  # idempotent

# Meta description — kısalt + 12 araç
c = c.replace(
    'content="Kostenlose Echtzeit-Rechner für LLM-Token, Vektordatenbanken, Cloud VPS, Serverless (AWS Lambda), STT/TTS, API-Gateway, Embeddings, KI-Agenten und Zahlungsgebühren."',
    'content="Kostenlose KI-Infrastruktur-Kostenrechner. LLM, Vektordatenbank, Serverless, Auth, KI-Coding-Tools und mehr. 12 Rechner, kein Login, laeuft im Browser."'
)

# Meta keywords — KI-Coding + Auth hinzufuegen
c = c.replace(
    'content="LLM Kostenrechner, AWS Lambda Rechner, Cloud VPS Vergleich, Embedding API Kosten, STT TTS API Kosten, API Gateway Rechner, KI Agent Kosten"',
    'content="LLM Kostenrechner, AWS Lambda Rechner, Cloud VPS Vergleich, Embedding API Kosten, STT TTS API Kosten, API Gateway Rechner, KI Agent Kosten, KI Coding Tool Kosten, Auth Anbieter Kostenrechner, Clerk vs Supabase Preise, Cursor vs Copilot Kosten"'
)

# aggregateRating — ratingCount:150 -> reviewCount:127 consistent
c = c.replace(
    '"ratingCount":"150"',
    '"reviewCount":"127","bestRating":"5","worstRating":"1"'
)

write(de, c)
print('✓ DE: H1, tagpill, desc, keywords, rating fixed')

# ─────────────────────────────────────────────────────────────────────────────
# FR
# ─────────────────────────────────────────────────────────────────────────────
fr = os.path.join(BASE, 'fr', 'index.html')
c = read(fr)

# H1
c = c.replace(
    'Connaissez vos <span class="em">coûts d\'infra</span><br>avant la facture.',
    'Calculateurs <span class="em">LLM &amp; API Gratuits</span> — Connaissez vos coûts avant la facture.'
)
# Alternate H1 form
c = c.replace(
    'Connaissez vos <span class="em">coûts d\'infra</span> avant la facture.',
    'Calculateurs <span class="em">LLM &amp; API Gratuits</span> — Connaissez vos coûts avant la facture.'
)

# Hero tagpill
c = c.replace('10 calculatrices', '12 calculatrices')

# Meta description — 180 → ~155
c = c.replace(
    'content="Calculatrices gratuites en temps réel pour tokens LLM, bases vectorielles, cloud VPS, serverless (AWS Lambda), STT/TTS, API gateway, embeddings, agents IA et frais de paiement."',
    'content="Calculateurs gratuits pour LLM, base vectorielle, serverless, auth et outils IA. 12 calculateurs, sans inscription, 100% dans votre navigateur."'
)

# Meta keywords — add new tools
c = c.replace(
    'content="calculatrice LLM, calculateur AWS Lambda, comparaison cloud VPS, coût API embedding, coût STT TTS, calculateur API gateway, coût agent IA"',
    'content="calculatrice LLM, calculateur AWS Lambda, comparaison cloud VPS, coût API embedding, coût STT TTS, calculateur API gateway, coût agent IA, cout outil IA coding, calculateur fournisseur auth, Clerk vs Supabase prix, Cursor vs Copilot cout"'
)

write(fr, c)
print('✓ FR: H1, tagpill, desc, keywords fixed')

# ─────────────────────────────────────────────────────────────────────────────
# TR
# ─────────────────────────────────────────────────────────────────────────────
tr = os.path.join(BASE, 'tr', 'index.html')
c = read(tr)

# H1
old_h1_tr = c[c.find('<h1'):c.find('</h1>')+5]
c = c.replace(
    old_h1_tr,
    '<h1 class="h">Ücretsiz <span class="em">LLM &amp; API Maliyet Hesaplayıcıları</span> — Faturadan Önce Altyapı Maliyetinizi Bilin.</h1>'
)

# Hero tagpill
c = c.replace('10 hesaplayıcı', '12 hesaplayıcı')

# Meta description — 159 → ~158 (biraz genişlet)
c = c.replace(
    'content="LLM token, vektör veritabanı, cloud VPS, serverless, STT/TTS, API gateway, embedding, YZ ajan ve ödeme ücretleri için ücretsiz gerçek zamanlı hesaplayıcılar."',
    'content="Ücretsiz YZ altyapı maliyet hesaplayıcıları. LLM, vektör DB, serverless, auth ve YZ kodlama araçları dahil 12 hesaplayıcı. Kayıt gerekmez, tarayıcıda çalışır."'
)

# Meta keywords — add new tools
c = c.replace(
    'content="LLM maliyet hesaplayıcı, AWS Lambda hesaplayıcı, cloud VPS karşılaştırma, embedding API maliyet, STT TTS fiyat, API gateway maliyet, YZ ajan maliyet"',
    'content="LLM maliyet hesaplayıcı, AWS Lambda hesaplayıcı, cloud VPS karşılaştırma, embedding API maliyet, STT TTS fiyat, API gateway maliyet, YZ ajan maliyet, YZ kodlama aracı maliyet, kimlik dogrulama saglayici maliyet, Clerk vs Supabase fiyat, Cursor vs Copilot maliyet"'
)

write(tr, c)
print('✓ TR: H1, tagpill, desc, keywords fixed')

# ─────────────────────────────────────────────────────────────────────────────
# Verify
# ─────────────────────────────────────────────────────────────────────────────
print('\n--- Verification ---')
for lang, path in [('DE', de), ('FR', fr), ('TR', tr)]:
    c = read(path)
    title = re.search(r'<title>(.*?)</title>', c).group(1)
    desc  = re.search(r'<meta name="description" content="([^"]+)"', c).group(1)
    pill  = re.search(r'(\d+) (Rechner|calculatrices|hesaplayıcı)', c)
    print(f'\n{lang}:')
    print(f'  Title ({len(title)}): {title}')
    print(f'  Desc  ({len(desc)}): {desc[:80]}...')
    if pill:
        print(f'  Tagpill count: {pill.group(1)}')
