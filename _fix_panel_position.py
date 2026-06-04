#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move panels 05-10 from outside .calc div to inside (before closing </div>)."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

TARGETS = {
    'de': os.path.join(BASE, 'de', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'index.html'),
}

for lang, path in TARGETS.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # ── Find where pay panel ends ──────────────────────────────────────────────
    pay_pos = c.find('id="pay"')
    pay_end = c.find('</section>', pay_pos) + len('</section>')

    # The NEXT </div> after pay section closes .calc div
    calc_close_pos = c.find('</div>', pay_end)
    print(f'{lang}: pay ends at {pay_end}, calc </div> at {calc_close_pos}')
    print(f'  Between: {repr(c[pay_end:pay_end+80])}')

    # ── Find panels 05-10 block ────────────────────────────────────────────────
    cloud_pos = c.find('<section class="panel" id="cloud"')
    agent_pos = c.find('id="agent"')
    agent_end = c.find('</section>', agent_pos) + len('</section>')

    # Start from comment if exists
    comment_pos = c.rfind('<!-- PANEL 5', 0, cloud_pos)
    if comment_pos != -1 and comment_pos > cloud_pos - 200:
        block_start = comment_pos
    else:
        # Start from newline before cloud section
        block_start = cloud_pos

    panels_block = '\n\n' + c[block_start:agent_end].strip()
    print(f'{lang}: panels block {block_start}-{agent_end} ({len(panels_block)} chars)')

    # ── Remove panels block from current location ──────────────────────────────
    # Include preceding newlines
    pre_start = block_start
    while pre_start > 0 and c[pre_start-1] in '\n\r ':
        pre_start -= 1
    c2 = c[:pre_start] + '\n' + c[agent_end:]

    # ── Recalculate positions in c2 ────────────────────────────────────────────
    pay_pos2 = c2.find('id="pay"')
    pay_end2 = c2.find('</section>', pay_pos2) + len('</section>')
    calc_close2 = c2.find('</div>', pay_end2)
    print(f'{lang}: after removal, calc </div> at {calc_close2}')
    print(f'  Between: {repr(c2[pay_end2:pay_end2+80])}')

    # ── Insert panels before calc closing </div> ───────────────────────────────
    c_fixed = c2[:calc_close2] + panels_block + '\n\n' + c2[calc_close2:]

    # ── Simple verification ────────────────────────────────────────────────────
    cloud_in = c_fixed.find('id="cloud"')
    calc_close_in = c_fixed.find('</div>', c_fixed.find('</section>', c_fixed.find('id="agent"')) + 10)
    # The panels should be before the adslot
    adslot_in = c_fixed.find('class="adslot"')
    cloud_before_ad = cloud_in < adslot_in
    print(f'{lang}: cloud before adslot: {cloud_before_ad} (cloud={cloud_in}, adslot={adslot_in})')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c_fixed)
    print(f'{lang}: saved ({len(c_fixed)} chars)\n')

print('Done.')
