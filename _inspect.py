import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\Users\muham\Desktop\APICalculators\index.html', encoding='utf-8').read()
panels = [(m.start(), m.group(1)) for m in re.finditer(r'<section class="panel" id="([^"]+)"', c)]
print('Panels:', [p[1] for p in panels])
print('affiliate-cta exists:', 'affiliate-cta' in c)
print('vultr ref:', 'ref=9904710' in c)

# Show end of one panel to understand structure
for pos, pid in panels[:2]:
    end = c.find('</section>', pos)
    print(f'\n--- Panel "{pid}" tail ---')
    print(c[end-300:end+10])
