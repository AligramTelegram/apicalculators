import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\Users\muham\Desktop\APICalculators\blog\llm-api-cost-guide-2026.html', encoding='utf-8').read()
head = c[:c.find('</head>')]
print('Script in head:', 'pagead2.googlesyndication' in head)
print('Ad units:', c.count('class="adsbygoogle"'))
print('ad-top-content:', 'ad-top-content' in c)
print('ad-mid-content:', 'ad-mid-content' in c)
print('ad-bottom-content:', 'ad-bottom-content' in c)
