#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'
TODAY = '2026-06-05'

def read(p): return open(p, encoding='utf-8').read()
def write(p, c):
    with open(p, 'w', encoding='utf-8') as f: f.write(c)

NEW_LOCS = [
    'https://apicalculators.com/fr/calculateur-cout-aws-lambda.html',
    'https://apicalculators.com/tr/bulut-vps-maliyet.html',
    'https://apicalculators.com/de/vektordatenbank-kosten.html',
    'https://apicalculators.com/fr/cout-base-vectorielle.html',
    'https://apicalculators.com/tr/vektor-veritabani-maliyet.html',
    'https://apicalculators.com/de/embedding-api-kosten.html',
    'https://apicalculators.com/fr/cout-api-embedding.html',
    'https://apicalculators.com/tr/embedding-api-maliyet.html',
    'https://apicalculators.com/de/api-gateway-kosten.html',
    'https://apicalculators.com/fr/cout-api-gateway.html',
    'https://apicalculators.com/tr/api-gateway-maliyet.html',
    'https://apicalculators.com/de/stt-tts-api-kosten.html',
    'https://apicalculators.com/fr/cout-api-stt-tts.html',
    'https://apicalculators.com/tr/stt-tts-api-maliyet.html',
    'https://apicalculators.com/de/ki-agent-kostenrechner.html',
    'https://apicalculators.com/fr/cout-agent-ia.html',
    'https://apicalculators.com/tr/yz-ajan-maliyet.html',
    'https://apicalculators.com/de/ki-bildgenerierung-kosten.html',
    'https://apicalculators.com/fr/cout-generation-image-ia.html',
    'https://apicalculators.com/tr/yz-gorsel-uretim-maliyet.html',
    'https://apicalculators.com/de/stripe-vs-paddle-rechner.html',
    'https://apicalculators.com/fr/comparateur-stripe-paddle.html',
    'https://apicalculators.com/tr/stripe-vs-paddle-hesaplayici.html',
]

path = os.path.join(BASE, 'sitemap.xml')
c = read(path)
existing = set(re.findall(r'<loc>(.*?)</loc>', c))

inject = ''
added = 0
for loc in NEW_LOCS:
    if loc in existing:
        continue
    inject += f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>\n'''
    added += 1

c = c.replace('</urlset>', inject + '</urlset>')
write(path, c)

total = len(re.findall(r'<loc>', c))
print(f'✓ Added {added} URLs — total: {total}')
