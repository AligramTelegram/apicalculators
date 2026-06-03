#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace DigitalOcean affiliate CTAs with Vultr across all 4 lang index files."""
import re, os
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE  = r'C:\Users\muham\Desktop\APICalculators'
FILES = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

VULTR_URL = 'https://www.vultr.com/?ref=9904710-9J'

# CTA text per lang
CTA_TEXT = {
    'index.html':    'Get $300 free credits at Vultr',
    'de/index.html': '$300 Gratisguthaben bei Vultr',
    'fr/index.html': 'Obtenez $300 de credits gratuits sur Vultr',
    'tr/index.html': "Vultr'da $300 ucretsiz kredi",
}

# Affiliate onclick text replacement
ONCLICK_OLD = "trackAffiliateClick('digitalocean')"
ONCLICK_NEW = "trackAffiliateClick('vultr')"

for path in FILES:
    if not os.path.exists(path):
        print(f'SKIP {path}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    key = path.replace(BASE + os.sep, '').replace('\\', '/')
    cta_label = CTA_TEXT.get(key, CTA_TEXT['index.html'])

    # 1) Replace href with Vultr URL (DO href)
    c = re.sub(
        r'https://www\.digitalocean\.com/\?refcode=[^"&]+[^"]*',
        VULTR_URL,
        c
    )

    # 2) Replace CTA button text (various lang patterns)
    c = re.sub(
        r'Deploy with \$200 DigitalOcean credits',
        'Get $300 free credits at Vultr',
        c
    )
    c = re.sub(
        r'200 USD Cloud-Guthaben erhalten',
        '$300 Gratisguthaben bei Vultr',
        c
    )
    c = re.sub(
        r'Obtenez 200 USD de cr[^<"]+',
        'Obtenez $300 de credits sur Vultr',
        c
    )
    c = re.sub(
        r'\$200 [Üu]cretsiz Bulut Kredisi Al',
        "Vultr'da $300 ucretsiz kredi",
        c
    )

    # 3) Replace DO emoji/icon with Vultr V icon
    c = c.replace('>&#127754;</span>', '>V</span>')  # wave emoji -> V
    c = re.sub(r'><span class="em">🌊</span>', '><span class="em" style="font-weight:900">V</span>', c)

    # 4) Replace onclick tracker
    c = c.replace(ONCLICK_OLD, ONCLICK_NEW)

    # 5) Replace affiliate_cta_do text in any hardcoded strings
    c = re.sub(
        r'affiliate_cta_do.*?(?=<)',
        '',
        c
    )

    # 6) Replace "200 USD" / "$200" references near DigitalOcean
    c = re.sub(r'\$200 Free Cloud Credits', '$300 Free Cloud Credits at Vultr', c)
    c = re.sub(r'200 USD Cloud-Guthaben erhalten', '$300 Vultr Guthaben', c)

    # 7) Clean up any remaining digitalocean.com refs that didn't match
    c = re.sub(
        r'https?://www\.digitalocean\.com[^\s"]*',
        VULTR_URL,
        c
    )

    # 8) Replace "DigitalOcean" brand name in button labels
    c = re.sub(r'DigitalOcean(?!\s+credits\s+→)', 'Vultr', c)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    hits = c.count('vultr')
    do_left = c.lower().count('digitalocean')
    print(f'OK {key}: vultr_refs={hits}, do_remaining={do_left}')

print('Done.')
