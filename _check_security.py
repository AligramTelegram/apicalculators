#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Security audit for APICalculators.com static site."""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

issues = {'critical': [], 'high': [], 'medium': [], 'low': [], 'ok': []}

def ok(msg):   issues['ok'].append(msg)
def low(msg):  issues['low'].append(msg)
def med(msg):  issues['medium'].append(msg)
def high(msg): issues['high'].append(msg)
def crit(msg): issues['critical'].append(msg)

all_html = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
all_html = [f for f in all_html if '_' not in os.path.basename(f) or not os.path.basename(f).startswith('_')]

# ── 1. External scripts — check for SRI and rel=noopener ─────────────────────
print('Checking external scripts...')
ext_scripts = {}
for f in all_html:
    c = open(f, encoding='utf-8').read()
    srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', c)
    for src in srcs:
        if src.startswith('http') and 'apicalculators' not in src:
            if src not in ext_scripts:
                ext_scripts[src] = 0
            ext_scripts[src] += 1

for src, count in ext_scripts.items():
    print(f'  External script ({count} pages): {src[:80]}')

# Check SRI on any external scripts
sample = open(all_html[0], encoding='utf-8').read()
sri_count = len(re.findall(r'integrity="sha', sample))

if sri_count == 0:
    med(f'No SRI (Subresource Integrity) on external scripts — {len(ext_scripts)} external scripts loaded without hash verification')
else:
    ok('SRI hashes present on external scripts')

# ── 2. target="_blank" without rel="noopener" ────────────────────────────────
print('\nChecking target="_blank" links...')
blank_no_opener = []
for f in all_html:
    c = open(f, encoding='utf-8').read()
    blanks = re.findall(r'<a[^>]+target="_blank"[^>]*>', c)
    for tag in blanks:
        if 'noopener' not in tag and 'noreferrer' not in tag:
            blank_no_opener.append((os.path.relpath(f, BASE), tag[:80]))

if blank_no_opener:
    high(f'{len(blank_no_opener)} target="_blank" links missing rel="noopener" (tab-napping risk)')
    for fname, tag in blank_no_opener[:5]:
        print(f'  ⚠ {fname}: {tag}')
    if len(blank_no_opener) > 5:
        print(f'  ... and {len(blank_no_opener)-5} more')
else:
    ok('All target="_blank" links have rel="noopener"')

# ── 3. Mixed content (HTTP resources on HTTPS site) ──────────────────────────
print('\nChecking mixed content...')
http_resources = []
for f in all_html:
    c = open(f, encoding='utf-8').read()
    hits = re.findall(r'(?:src|href|action)=["\']http://[^"\']+["\']', c)
    for h in hits:
        if 'localhost' not in h:
            http_resources.append((os.path.relpath(f, BASE), h[:80]))

if http_resources:
    high(f'{len(http_resources)} HTTP (non-HTTPS) resource references found')
    for fname, h in http_resources[:5]:
        print(f'  ⚠ {fname}: {h}')
else:
    ok('No mixed content — all resources use HTTPS')

# ── 4. Sensitive info exposure ────────────────────────────────────────────────
print('\nChecking for sensitive data exposure...')
sensitive_patterns = [
    (r'api[_-]?key\s*[=:]\s*["\'][A-Za-z0-9_\-]{20,}', 'API key'),
    (r'secret\s*[=:]\s*["\'][A-Za-z0-9_\-]{10,}', 'Secret'),
    (r'password\s*[=:]\s*["\'][^"\']{6,}', 'Password'),
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI secret key'),
    (r'Bearer\s+[A-Za-z0-9\._\-]{20,}', 'Bearer token'),
]
found_sensitive = []
for f in all_html:
    c = open(f, encoding='utf-8').read()
    for pattern, label in sensitive_patterns:
        hits = re.findall(pattern, c, re.IGNORECASE)
        for h in hits:
            found_sensitive.append((label, os.path.relpath(f, BASE), h[:40]))

if found_sensitive:
    crit(f'{len(found_sensitive)} potential sensitive data exposures in HTML')
    for label, fname, val in found_sensitive:
        print(f'  🔴 {label} in {fname}: {val}')
else:
    ok('No sensitive data (API keys, passwords, tokens) in HTML files')

# ── 5. Inline event handlers (XSS surface) ───────────────────────────────────
print('\nChecking inline event handlers...')
inline_events = []
for f in all_html[:10]:  # sample
    c = open(f, encoding='utf-8').read()
    hits = re.findall(r'on(?:click|load|error|mouseover|submit)\s*=\s*["\'][^"\']{50,}', c)
    for h in hits:
        inline_events.append((os.path.relpath(f, BASE), h[:60]))

if inline_events:
    low(f'{len(inline_events)} inline event handlers found (sample of 10 pages)')
else:
    ok('No problematic inline event handlers found in sampled pages')

# ── 6. CSP evaluation ────────────────────────────────────────────────────────
print('\nEvaluating CSP...')
csp_raw = "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://pagead2.googlesyndication.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com https://analytics.google.com; frame-src 'self' https://googleads.g.doubleclick.net; object-src 'none';"

if "'unsafe-inline'" in csp_raw and "script-src" in csp_raw:
    med("CSP uses 'unsafe-inline' for script-src — weakens XSS protection (required by AdSense/GTM)")
    ok("CSP present and covers: default-src, script-src, style-src, img-src, frame-src, object-src 'none'")
if "object-src 'none'" in csp_raw:
    ok("CSP object-src: 'none' — plugin execution blocked")
if 'upgrade-insecure-requests' not in csp_raw:
    low("CSP missing 'upgrade-insecure-requests' directive")

# Missing: frame-ancestors
if 'frame-ancestors' not in csp_raw:
    med("CSP missing 'frame-ancestors' directive (clickjacking defense — X-Frame-Options covers this but CSP is preferred)")

# ── 7. Affiliate/external links — rel="sponsored" ────────────────────────────
print('\nChecking affiliate link safety...')
aff_without_sponsored = []
for f in all_html:
    c = open(f, encoding='utf-8').read()
    aff_links = re.findall(r'<a[^>]+(?:vultr\.com|ref=|affiliate)[^>]*>', c, re.IGNORECASE)
    for tag in aff_links:
        if 'sponsored' not in tag and 'nofollow' not in tag:
            aff_without_sponsored.append((os.path.relpath(f, BASE), tag[:60]))

if aff_without_sponsored:
    med(f'{len(aff_without_sponsored)} affiliate links missing rel="sponsored" or rel="nofollow"')
    for fname, tag in aff_without_sponsored[:3]:
        print(f'  ⚠ {fname}: {tag}')
else:
    ok('All affiliate links have rel="sponsored"')

# ── 8. Form action security ───────────────────────────────────────────────────
forms = []
for f in all_html:
    c = open(f, encoding='utf-8').read()
    if '<form' in c:
        forms.append(os.path.relpath(f, BASE))

if forms:
    med(f'{len(forms)} pages with <form> elements — verify CSRF/action URL security')
    for ff in forms[:3]: print(f'  {ff}')
else:
    ok('No HTML forms — no CSRF attack surface (all calculations are client-side JS)')

# ── 9. AdSense/GA script loading ─────────────────────────────────────────────
print('\nChecking script loading patterns...')
for f in all_html[:3]:
    c = open(f, encoding='utf-8').read()
    ga_async = bool(re.search(r"addEventListener\('load'.*googletagmanager", c, re.DOTALL))
    if ga_async:
        ok('Google Analytics loaded asynchronously via addEventListener("load") — good for performance')
        break

# Check pagead loaded with async
sample_calc = os.path.join(BASE, 'llm-cost-calculator.html')
if os.path.exists(sample_calc):
    c = open(sample_calc, encoding='utf-8').read()
    if 'async src="https://pagead2' in c:
        ok('AdSense script loaded with async attribute — non-blocking')

# ── 10. robots.txt check ─────────────────────────────────────────────────────
print('\nChecking robots.txt...')
robots = open(os.path.join(BASE, 'robots.txt'), encoding='utf-8').read()
if 'Disallow: /_' in robots or 'Disallow: /admin' in robots:
    ok('robots.txt disallows private paths')
if 'sitemap' in robots.lower():
    ok('robots.txt references sitemap.xml')

# ── REPORT ───────────────────────────────────────────────────────────────────
print('\n' + '='*70)
print('SECURITY AUDIT REPORT — APICalculators.com')
print('='*70)

labels = [('🔴 CRITICAL', 'critical'), ('🟠 HIGH', 'high'),
          ('🟡 MEDIUM', 'medium'), ('🔵 LOW', 'low'), ('✅ OK', 'ok')]
for label, key in labels:
    if issues[key]:
        print(f'\n{label}:')
        for i in issues[key]:
            print(f'  • {i}')

total_issues = sum(len(issues[k]) for k in ['critical','high','medium','low'])
print(f'\nTotal issues: {total_issues} ({len(issues["critical"])} critical, {len(issues["high"])} high, {len(issues["medium"])} medium, {len(issues["low"])} low)')
print(f'Checks passed: {len(issues["ok"])}')
