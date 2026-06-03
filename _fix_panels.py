#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copy the 6 new working calculator panels from EN index to DE/FR/TR.
EN is working. DE/FR/TR have tabs but broken/missing panels.
Strategy: extract panels 5-10 + JS from EN, replace in DE/FR/TR.
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# Read EN (source of truth)
with open(os.path.join(BASE, 'index.html'), 'r', encoding='utf-8') as f:
    en = f.read()

# ── Extract panels 5-10 from EN ───────────────────────────────────────────────
# Find start: <!-- PANEL 5: Cloud VPS -->
p5_start = en.find('<!-- PANEL 5: Cloud VPS -->')
if p5_start == -1:
    # fallback: find id="cloud"
    p5_start = en.find('<section class="panel" id="cloud"')
    p5_start = en.rfind('\n  ', 0, p5_start) + 1  # go back to section start

# Find end: last </section> before <!-- AD: IN-CONTENT -->
ad_marker = en.find('<!-- AD: IN-CONTENT -->')
p10_end = en.rfind('</section>', 0, ad_marker) + len('</section>')

new_panels_en = en[p5_start:p10_end]
print(f"Extracted {len(new_panels_en)} chars of panel HTML (panels 5-10)")

# ── Extract JS for new tools from EN ─────────────────────────────────────────
js_start = en.find('/* ===== CLOUD VPS =====')
js_end   = en.find('/* ===== INIT ALL NEW', js_start)
js_end   = en.find('\n', js_end + 100) + 1  # include init line
new_js_en = en[js_start:js_end]
print(f"Extracted {len(new_js_en)} chars of calculator JS")

# ── Process DE/FR/TR ─────────────────────────────────────────────────────────
TARGETS = {
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in TARGETS.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    original_len = len(c)
    changed = False

    # ── Step 1: Fix/insert panels ─────────────────────────────────────────────
    has_cloud = 'id="cloud"' in c
    has_cloud_panel = '<section class="panel" id="cloud"' in c

    if not has_cloud_panel:
        # Find insertion point: after the pay panel's last </section>
        # Pay panel ends with </section>, then </div> closes .calc div
        # We find the last </section> before the first </div> that closes .calc
        last_section = c.rfind('</section>')
        if last_section == -1:
            print(f"{lang}: ERROR - no </section> found")
            continue
        insert_pos = last_section + len('</section>')
        c = c[:insert_pos] + '\n\n' + new_panels_en + c[insert_pos:]
        print(f"{lang}: panels inserted")
        changed = True
    else:
        # Panels exist but might be wrong — replace from cloud to end of panels
        cloud_start = c.find('<section class="panel" id="cloud"')
        # go back to find the comment or newline before
        cloud_start_safe = c.rfind('\n', 0, cloud_start) + 1

        # Find end of panel 10 (agent)
        agent_end = c.find('</section>', c.find('id="agent"')) + len('</section>')
        if agent_end > len('</section>'):
            c = c[:cloud_start_safe] + new_panels_en + '\n' + c[agent_end:]
            print(f"{lang}: panels replaced")
            changed = True

    # ── Step 2: Fix/insert JS ─────────────────────────────────────────────────
    if '/* ===== CLOUD VPS =====' not in c:
        # Find last </script> tag
        last_script = c.rfind('</script>')
        if last_script != -1:
            c = c[:last_script] + '\n\n' + new_js_en + '\n\n' + c[last_script:]
            print(f"{lang}: JS inserted")
            changed = True
    else:
        # Replace existing JS block
        js_s = c.find('/* ===== CLOUD VPS =====')
        js_e = c.find('/* ===== INIT ALL NEW', js_s)
        js_e = c.find('\n', js_e + 100) + 1
        if js_e > js_s:
            c = c[:js_s] + new_js_en + c[js_e:]
            print(f"{lang}: JS replaced")
            changed = True

    # ── Step 3: Fix tab buttons to match EN exactly ───────────────────────────
    # Ensure tabs 05-10 exist with correct IDs
    tab_ids = ['cloud', 'stt', 'serverless', 'gateway', 'embedding', 'agent']
    missing_tabs = [tid for tid in tab_ids if f'data-tab="{tid}"' not in c]
    if missing_tabs:
        print(f"{lang}: WARNING - missing tabs: {missing_tabs}")
    else:
        print(f"{lang}: all tabs present")

    # ── Write ─────────────────────────────────────────────────────────────────
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"{lang}: saved ({len(c)} chars, was {original_len})")

    # Verify
    panels_count = c.count('role="tabpanel"')
    js_ok = '/* ===== CLOUD VPS =====' in c
    emoji_ok = '🔤' in c
    print(f"{lang}: panels={panels_count} js={js_ok} emoji={emoji_ok}\n")

print("All done.")
