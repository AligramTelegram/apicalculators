#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add contextual Vultr CTA to calcCloud() in all 4 lang index files."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE  = r'C:\Users\muham\Desktop\APICalculators'
FILES = {
    'en': os.path.join(BASE, 'index.html'),
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

# Localised CTA strings
CTA = {
    'en': {
        'vultr_win':  'Deploy on Vultr — cheapest for your spec',
        'other_win':  'Compare on Vultr',
        'sub_vultr':  'Vultr matches your spec at the lowest price. Start with free credits.',
        'sub_other':  'Vultr is close — compare plans before deciding.',
        'btn':        'Deploy on Vultr →',
        'note':       'Affiliate link · You get $300 free credits',
    },
    'de': {
        'vultr_win':  'Auf Vultr deployen — günstigstes Angebot',
        'other_win':  'Auf Vultr vergleichen',
        'sub_vultr':  'Vultr bietet die günstigste Konfiguration für Ihre Anforderungen.',
        'sub_other':  'Vultr liegt nah dran — Pläne vor der Entscheidung vergleichen.',
        'btn':        'Auf Vultr deployen →',
        'note':       'Affiliate-Link · Sie erhalten $300 Startguthaben',
    },
    'fr': {
        'vultr_win':  'Déployer sur Vultr — le moins cher',
        'other_win':  'Comparer sur Vultr',
        'sub_vultr':  'Vultr correspond à vos specs au prix le plus bas.',
        'sub_other':  'Vultr est proche — comparez avant de décider.',
        'btn':        'Déployer sur Vultr →',
        'note':       'Lien affilié · Vous recevez $300 de crédits',
    },
    'tr': {
        'vultr_win':  "Vultr'a Deploy Et — en ucuz seçenek",
        'other_win':  "Vultr'da Karşılaştır",
        'sub_vultr':  "Vultr, özellikleriniz için en düşük fiyatı sunuyor.",
        'sub_other':  "Vultr yakın — karar vermeden önce planları karşılaştırın.",
        'btn':        "Vultr'a Deploy Et →",
        'note':       'Affiliate link · $300 ücretsiz kredi alırsınız',
    },
}

# The old calcCloud footer line (no CTA)
OLD_FOOTER = "  document.getElementById('cloudPer').textContent='per month (cheapest match: '+cheapest.name+')';"

# New calcCloud results block with contextual Vultr CTA
NEW_RESULTS = r"""  var cheapestName = cheapest.name;
  document.getElementById('cloudTotal').textContent = '$' + cheapest.price.toFixed(2);
  document.getElementById('cloudPer').textContent   = 'per month — cheapest: ' + cheapestName;

  // Contextual Vultr CTA
  var ctaBox = document.getElementById('cloudVultrCta');
  if (ctaBox) {
    var isVultr = cheapestName === 'Vultr';
    ctaBox.style.display = 'block';
    ctaBox.innerHTML = isVultr
      ? '<div class="vcta vcta-win"><div class="vcta-icon">V</div><div class="vcta-body">'
        + '<div class="vcta-title">__VULTR_WIN__</div>'
        + '<div class="vcta-sub">__SUB_VULTR__</div>'
        + '<a href="https://www.vultr.com/?ref=9904709" rel="sponsored nofollow" target="_blank" '
        + 'class="vcta-btn" onclick="trackAffiliateClick(\'vultr_calc\')">__BTN__</a>'
        + '<span class="vcta-note">__NOTE__</span></div></div>'
      : '<div class="vcta vcta-near"><div class="vcta-icon">V</div><div class="vcta-body">'
        + '<div class="vcta-title">__OTHER_WIN__</div>'
        + '<div class="vcta-sub">__SUB_OTHER__</div>'
        + '<a href="https://www.vultr.com/?ref=9904709" rel="sponsored nofollow" target="_blank" '
        + 'class="vcta-btn vcta-btn-sm" onclick="trackAffiliateClick(\'vultr_calc\')">__BTN__</a>'
        + '</div></div>';
  }"""

# CSS to inject (once, before </style> in head)
VCTA_CSS = """
/* ── Vultr contextual CTA ─────────────────────────────────────── */
#cloudVultrCta{display:none;margin-top:14px}
.vcta{display:flex;gap:14px;align-items:flex-start;border-radius:12px;padding:16px 18px;border:1px solid var(--border2)}
.vcta-win{background:rgba(184,255,46,.06);border-color:rgba(184,255,46,.3)}
.vcta-near{background:var(--surface)}
.vcta-icon{width:38px;height:38px;border-radius:9px;background:#1557c0;display:grid;place-items:center;
  color:#fff;font-weight:900;font-size:17px;flex-shrink:0;margin-top:2px}
.vcta-body{flex:1;min-width:0}
.vcta-title{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:14px;margin-bottom:4px;color:var(--text)}
.vcta-sub{font-size:12.5px;color:var(--muted);margin-bottom:10px}
.vcta-btn{display:inline-flex;align-items:center;gap:6px;background:var(--lime);color:#06210a;
  padding:9px 15px;border-radius:9px;font-weight:700;font-size:13px;text-decoration:none;transition:opacity .15s}
.vcta-btn:hover{opacity:.85;text-decoration:none}
.vcta-btn-sm{background:var(--surface2);color:var(--text);border:1px solid var(--border2)}
.vcta-note{display:block;font-family:'Cascadia Code','Consolas',monospace;font-size:10px;color:var(--muted2);margin-top:7px}
"""

def process(path, lang):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    t = CTA[lang]

    # 1) Inject CSS before </style> (first occurrence in head)
    if '#cloudVultrCta' not in c:
        c = c.replace('</style>', VCTA_CSS + '</style>', 1)

    # 2) Add CTA div inside cloud panel result, after <div class="breakdown" id="cloudCmp"></div>
    OLD_CMP = '<div class="breakdown" id="cloudCmp"></div>'
    NEW_CMP = '<div class="breakdown" id="cloudCmp"></div>\n      <div id="cloudVultrCta"></div>'
    if 'cloudVultrCta' not in c:
        c = c.replace(OLD_CMP, NEW_CMP)

    # 3) Replace calcCloud JS footer with new results block + CTA logic
    localised = NEW_RESULTS \
        .replace('__VULTR_WIN__', t['vultr_win']) \
        .replace('__OTHER_WIN__', t['other_win']) \
        .replace('__SUB_VULTR__', t['sub_vultr']) \
        .replace('__SUB_OTHER__', t['sub_other']) \
        .replace('__BTN__', t['btn']) \
        .replace('__NOTE__', t['note']) \
        .replace("'per month'", f"'per month'")

    # Find and replace the old two-line footer in calcCloud
    OLD1 = "document.getElementById('cloudTotal').textContent='$'+cheapest.price.toFixed(2);"
    OLD2 = "document.getElementById('cloudPer').textContent='per month (cheapest match: '+cheapest.name+')';"

    if OLD1 in c and 'cloudVultrCta' not in c.split(OLD1)[1][:200]:
        # Replace both lines together
        old_block = OLD1 + '\n  ' + OLD2
        c = c.replace(old_block, localised)
    elif OLD1 in c:
        # Already partially replaced — just ensure CTA logic is there
        pass

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    has_cta  = 'cloudVultrCta' in c
    has_css  = '#cloudVultrCta' in c
    print(f'OK {lang}: cta_div={has_cta} cta_css={has_css}')

for lang, path in FILES.items():
    if os.path.exists(path):
        process(path, lang)

print('Done.')
