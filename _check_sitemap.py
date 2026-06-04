#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# Collect all actual HTML files (relative paths with forward slashes)
actual = set()
for root, dirs, files in os.walk(BASE):
    # Skip hidden dirs and script dirs
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules']]
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), BASE)
            rel = rel.replace(os.sep, '/')
            actual.add(rel)

# Parse sitemap URLs
with open(os.path.join(BASE, 'sitemap.xml'), 'r', encoding='utf-8') as f:
    content = f.read()

urls = re.findall(r'<loc>https://apicalculators\.com(/[^<]*)</loc>', content)
missing = []
ok = []
for path in urls:
    if path == '/' or path.endswith('/'):
        file_path = path.lstrip('/') + 'index.html'
    else:
        file_path = path.lstrip('/')
    if file_path not in actual:
        missing.append((path, file_path))
    else:
        ok.append(path)

print(f'Total URLs: {len(urls)}')
print(f'OK: {len(ok)}')
print(f'MISSING ({len(missing)}):')
for url, fp in missing:
    print(f'  sitemap: {url}')
    print(f'  file:    {fp}  (NOT FOUND)')
