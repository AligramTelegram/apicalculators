#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean Python-only Vultr affiliate replacement.
No PowerShell Set-Content — avoids encoding corruption.
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE  = r'C:\Users\muham\Desktop\APICalculators'
FILES = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

VULTR_URL = 'https://www.vultr.com/?ref=9904710-9J'

CTA_LABELS = {
    'en': 'Get $300 free credits at Vultr',
    'de': '$300 Gratisguthaben bei Vultr',
    'fr': 'Obtenez $300 de crédits sur Vultr',
    'tr': "Vultr'da $300 ücretsiz kredi",
}

for lang, path in FILES.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1) Replace ALL DigitalOcean href URLs with Vultr
    c = re.sub(
        r'https?://www\.digitalocean\.com[^\s"]*',
        VULTR_URL,
        c
    )

    # 2) Replace CTA button labels (language-specific)
    c = re.sub(r'Deploy with \$200 DigitalOcean credits', CTA_LABELS['en'], c)
    c = re.sub(r'200 USD Cloud-Guthaben erhalten',        CTA_LABELS['de'], c)
    c = re.sub(r'Obtenez 200 USD de cr[éee][^\s<"]*[^<"]+', CTA_LABELS['fr'], c)
    c = re.sub(r'\$200 [ÜüU]cretsiz Bulut Kredisi Al',   CTA_LABELS['tr'], c)

    # 3) Replace affiliate onclick
    c = c.replace("trackAffiliateClick('digitalocean')", "trackAffiliateClick('vultr')")

    # 4) Fix DigitalOcean name in JS pricing data label (keep DO in pricing comparison)
    #    but ensure Cloud VPS calc shows 'DigitalOcean' not 'Vultr' for DO row
    c = c.replace("{id:'digitalocean', name:'Vultr'}", "{id:'digitalocean', name:'DigitalOcean'}")

    # 5) Replace wave emoji + DO brand text in button (emoji-safe replacement)
    c = c.replace(
        '<span class="em">🌊</span> Deploy with $200 DigitalOcean credits',
        f'<span class="em" style="font-weight:900;color:#1557c0">V</span> {CTA_LABELS[lang]}'
    )
    # Generic fallback for wave emoji without prior text
    c = c.replace('<span class="em">🌊</span>', '<span class="em" style="font-weight:900;color:#1557c0">V</span>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    # Verify
    do_refs = len(re.findall(r'digitalocean\.com', c))
    vultr_refs = len(re.findall(r'vultr\.com', c))
    emoji_ok = '🔤' in c  # check emoji integrity
    print(f"OK {lang}: vultr={vultr_refs} do_links={do_refs} emoji_intact={emoji_ok}")

print("Done. All files written as UTF-8.")
