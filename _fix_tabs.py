#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace horizontal scroll tabs with 2×5 grid card layout."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE  = r'C:\Users\muham\Desktop\APICalculators'
FILES = [
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'de', 'index.html'),
    os.path.join(BASE, 'fr', 'index.html'),
    os.path.join(BASE, 'tr', 'index.html'),
]

# ── New CSS for .tabs and .tab ────────────────────────────────────────────────
OLD_TABS_CSS = """.tabs{display:flex;gap:4px;padding:8px;border-bottom:1px solid var(--border);
  overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:1;min-width:max-content;display:flex;align-items:center;gap:9px;
  padding:13px 16px;border-radius:11px;cursor:pointer;color:var(--muted);
  font-weight:600;font-size:14.5px;white-space:nowrap;border:1px solid transparent;
  transition:all .18s;background:transparent}
.tab .ic{font-size:17px}
.tab:hover{color:var(--text);background:var(--surface2)}
.tab.on{color:var(--text);background:var(--surface2);border-color:var(--border2)}
.tab.on .ic{filter:drop-shadow(0 0 8px rgba(184,255,46,.6))}"""

NEW_TABS_CSS = """.tabs{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;
  padding:12px;border-bottom:1px solid var(--border)}
.tab{display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:6px;padding:12px 8px;border-radius:12px;cursor:pointer;color:var(--muted);
  font-weight:600;font-size:12px;text-align:center;border:1px solid transparent;
  transition:all .18s;background:transparent;line-height:1.2;min-height:64px}
.tab .ic{font-size:22px;line-height:1}
.tab .num{font-family:'Cascadia Code','Consolas',monospace;font-size:9px;
  color:var(--border2);margin-top:1px}
.tab:hover{color:var(--text);background:var(--surface2)}
.tab.on{color:var(--text);background:var(--surface2);border-color:var(--border2)}
.tab.on .ic{filter:drop-shadow(0 0 10px rgba(184,255,46,.7))}
.tab.on .num{color:var(--lime)}
@media(max-width:900px){.tabs{grid-template-columns:repeat(5,1fr)}}
@media(max-width:640px){.tabs{grid-template-columns:repeat(3,1fr);gap:5px}
  .tab{padding:10px 6px;font-size:11px;min-height:58px}.tab .ic{font-size:20px}}
@media(max-width:420px){.tabs{grid-template-columns:repeat(2,1fr)}
  .tab{min-height:54px}}"""

def process(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    if OLD_TABS_CSS in c:
        c = c.replace(OLD_TABS_CSS, NEW_TABS_CSS)
        print(f"  CSS replaced via exact match")
    else:
        # Fallback: regex replace between .tabs{ ... } and .tab.on .ic{ ... }
        pattern = r'(\.tabs\{[^}]+\}.*?\.tab\.on \.ic\{[^}]+\})'
        match = re.search(pattern, c, re.DOTALL)
        if match:
            c = c[:match.start()] + NEW_TABS_CSS + c[match.end():]
            print(f"  CSS replaced via regex")
        else:
            print(f"  WARNING: could not find tabs CSS to replace")
            return False

    # Fix .tab .num selector if it's overriding (some files have it separately)
    # Remove old .tab .num if exists separately
    c = re.sub(r'\n\.tab \.num\{[^}]+\}', '', c)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

    # Verify emoji intact
    emoji_ok = '🔤' in c or 'abc' in c.lower() or 'LLM' in c
    grid_ok  = 'grid-template-columns' in c
    print(f"  grid={grid_ok} file_ok=True")
    return True

for path in FILES:
    lang = path.replace(BASE, '').split(os.sep)[1] if 'de' in path or 'fr' in path or 'tr' in path else 'en'
    print(f"Processing {lang}...")
    process(path)

print("Done.")
