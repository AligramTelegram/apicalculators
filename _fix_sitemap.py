#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\muham\Desktop\APICalculators\sitemap.xml'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all </urlset> occurrences first, then add one at the end
content = content.replace('</urlset>', '')

# Strip trailing whitespace/newlines then add proper closing
content = content.rstrip() + '\n</urlset>\n'

# Validate: count <url> vs </url>
url_open = content.count('<url>')
url_close = content.count('</url>')
print(f"<url> count: {url_open}")
print(f"</url> count: {url_close}")
print(f"</urlset> count: {content.count('</urlset>')}")

if url_open != url_close:
    print("WARNING: mismatched url tags!")
else:
    print("OK: url tags balanced")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("sitemap.xml fixed.")
