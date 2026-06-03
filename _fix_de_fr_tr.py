#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert 6 new panels + JS into DE/FR/TR index files."""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# Read the panels from EN index (already generated correctly)
en_path = os.path.join(BASE, 'index.html')
with open(en_path, 'r', encoding='utf-8') as f:
    en = f.read()

# Extract panels 5-10 from EN
panel_start = en.find('<!-- PANEL 5: Cloud VPS -->')
panel_end   = en.find('\n<!-- AD: IN-CONTENT -->')
if panel_start == -1 or panel_end == -1:
    print("Could not extract panels from EN. Searching differently...")
    panel_start = en.find('id="cloud"') - 50
    panel_end   = en.rfind('</section>') + len('</section>')

panels_html = en[panel_start:panel_end]
print(f"Extracted {len(panels_html)} chars of panel HTML")

# Extract JS for new tools from EN
js_start = en.find('/* ===== CLOUD VPS =====')
js_end   = en.find('</script>', js_start)
if js_start == -1:
    print("JS not found in EN")
    sys.exit(1)
new_js = en[js_start:js_end]
print(f"Extracted {len(new_js)} chars of JS")

LANGS = ['de', 'fr', 'tr']

for lang in LANGS:
    path = os.path.join(BASE, lang, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    if 'id="cloud"' in c:
        print(f"{lang}: panels already present, skipping")
        continue

    # Find insertion point: after last </section> (end of pay panel)
    # The structure is: </section>\n</div>\n\n<div
    last_section = c.rfind('</section>')
    if last_section == -1:
        print(f"{lang}: no </section> found!")
        continue

    # Insert panels after last </section>
    insert_pos = last_section + len('</section>')
    c = c[:insert_pos] + '\n' + panels_html + c[insert_pos:]
    print(f"{lang}: panels inserted at pos {insert_pos}")

    # Insert JS before last </script>
    if '/* ===== CLOUD VPS =====' not in c:
        last_script = c.rfind('</script>')
        if last_script == -1:
            print(f"{lang}: no </script> found!")
            continue
        c = c[:last_script] + '\n' + new_js + '\n' + c[last_script:]
        print(f"{lang}: JS inserted")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"{lang}: DONE")

print("All done.")
