import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\Users\muham\Desktop\APICalculators\index.html', encoding='utf-8').read()

# Find ALL tabs to understand panel IDs
tabs = re.findall(r'data-tab="#([^"]+)"', c)
print('Tabs:', tabs)

# Find sections with class panel
panels = re.findall(r'<section[^>]+id="([^"]+)"', c)
print('All section IDs:', panels)

# Check blog post for existing affiliate links
bc = open(r'C:\Users\muham\Desktop\APICalculators\blog\cloud-vps-cost-comparison-2026.html', encoding='utf-8').read()
print('\ncloud-vps vultr link:', 'ref=9904710' in bc)
# Show context around vultr
idx = bc.find('ref=9904710')
if idx > 0:
    print('Context:', bc[idx-100:idx+150])
