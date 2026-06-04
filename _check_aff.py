import sys, re
sys.stdout.reconfigure(encoding='utf-8')
import os
BASE = r'C:\Users\muham\Desktop\APICalculators'

for lang in ['en', 'de', 'fr', 'tr']:
    path = os.path.join(BASE, lang, 'index.html') if lang != 'en' else os.path.join(BASE, 'index.html')
    c = open(path, encoding='utf-8').read()
    ctacount = c.count('affiliate-cta')
    vultr = c.count('ref=9904710')
    print(f'{lang}/index.html: {ctacount} CTA blocks, {vultr} vultr links')
