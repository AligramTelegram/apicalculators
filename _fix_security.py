#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security fixes:
1. Add rel="noopener noreferrer" to all target="_blank" external links
2. Update vercel.json CSP: add frame-ancestors + upgrade-insecure-requests
"""
import sys, os, re, glob, json
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

def read(path): return open(path, encoding='utf-8').read()
def write(path, c):
    with open(path, 'w', encoding='utf-8') as f: f.write(c)

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1: Add noopener to ALL target="_blank" links
# Rules:
#   - sponsored links:  rel="sponsored" → rel="sponsored noopener"
#   - nofollow links:   rel="nofollow"  → rel="nofollow noopener noreferrer"
#   - no rel at all:    target="_blank" → add rel="noopener noreferrer"
#   - already has noopener: skip
# ══════════════════════════════════════════════════════════════════════════════

all_html = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
all_html = [f for f in all_html if 'node_modules' not in f]

fixed_files = 0
fixed_links = 0

for path in all_html:
    c = read(path)
    original = c

    def fix_blank_link(m):
        tag = m.group(0)
        if 'noopener' in tag:
            return tag  # already fixed

        # Extract existing rel value
        rel_match = re.search(r'\brel=["\']([^"\']*)["\']', tag)
        if rel_match:
            existing_rel = rel_match.group(1)
            # Add noopener (and noreferrer for non-sponsored)
            if 'sponsored' in existing_rel:
                new_rel = existing_rel.strip() + ' noopener'
            else:
                new_rel = existing_rel.strip() + ' noopener noreferrer'
            new_tag = tag[:rel_match.start()] + f'rel="{new_rel}"' + tag[rel_match.end():]
        else:
            # No rel at all — insert rel="noopener noreferrer" before target="_blank"
            new_tag = tag.replace('target="_blank"', 'rel="noopener noreferrer" target="_blank"')

        return new_tag

    # Match all <a ...> tags that contain target="_blank"
    c = re.sub(r'<a\b[^>]*target="_blank"[^>]*>', fix_blank_link, c)

    if c != original:
        write(path, c)
        fixed_files += 1
        # Count how many links were changed
        orig_count = len(re.findall(r'target="_blank"', original))
        new_noopener = len(re.findall(r'noopener', c))
        fixed_links += orig_count

print(f'✓ noopener fix: {fixed_files} files updated')

# Verify
sample_issues = 0
for path in all_html[:20]:
    c = read(path)
    blanks = re.findall(r'<a[^>]+target="_blank"[^>]*>', c)
    for tag in blanks:
        if 'noopener' not in tag:
            sample_issues += 1
            print(f'  STILL MISSING: {tag[:80]} in {os.path.relpath(path, BASE)}')
print(f'  Verification (20 sample files): {sample_issues} remaining issues')

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2: vercel.json — improve CSP
# Add: frame-ancestors 'self' + upgrade-insecure-requests
# ══════════════════════════════════════════════════════════════════════════════

vercel_path = os.path.join(BASE, 'vercel.json')
c = read(vercel_path)
data = json.loads(c)

for rule in data.get('headers', []):
    for header in rule.get('headers', []):
        if header['key'] == 'Content-Security-Policy':
            csp = header['value']
            changed = False

            # Add frame-ancestors if missing
            if 'frame-ancestors' not in csp:
                csp = csp.rstrip(';') + "; frame-ancestors 'self';"
                changed = True
                print("✓ CSP: added frame-ancestors 'self'")

            # Add upgrade-insecure-requests if missing
            if 'upgrade-insecure-requests' not in csp:
                csp = csp.rstrip(';') + ' upgrade-insecure-requests;'
                changed = True
                print('✓ CSP: added upgrade-insecure-requests')

            # Ensure adsbygoogle connect-src (needed for AdSense reporting)
            if 'googleads.g.doubleclick.net' not in csp and 'connect-src' in csp:
                csp = csp.replace(
                    'connect-src ',
                    'connect-src https://googleads.g.doubleclick.net https://adservice.google.com '
                )
                changed = True
                print('✓ CSP: added AdSense connect-src domains')

            if changed:
                header['value'] = csp

# Write back with proper formatting
with open(vercel_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('✓ vercel.json updated')

# ══════════════════════════════════════════════════════════════════════════════
# VERIFY
# ══════════════════════════════════════════════════════════════════════════════
print('\n--- VERIFICATION ---')
c = read(vercel_path)
data = json.loads(c)
for rule in data.get('headers', []):
    for h in rule.get('headers', []):
        if h['key'] == 'Content-Security-Policy':
            csp = h['value']
            for check in ['frame-ancestors', 'upgrade-insecure-requests', "object-src 'none'"]:
                print(f'  {"✓" if check in csp else "✗"} {check}')

print('\nDone.')
