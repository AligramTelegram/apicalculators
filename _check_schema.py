import re, sys
sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\Users\muham\Desktop\APICalculators\blog\llm-api-cost-guide-2026.html', encoding='utf-8').read()
schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
for i, s in enumerate(schemas):
    print(f'Schema {i+1}:', s[:300])
    print()
