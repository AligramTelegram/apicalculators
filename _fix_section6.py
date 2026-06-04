#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 6: Strengthen aws-lambda and cloud-vps blog posts."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── AWS Lambda additions ──────────────────────────────────────────────────────

LAMBDA_NEW_SECTIONS = '''
<h2>Real-World Cost Examples</h2>
<p>Abstract pricing tables only go so far. Here are three realistic workloads with exact numbers.</p>

<h3>Example 1: REST API — 10M requests/month, 256 MB, 200 ms avg</h3>
<table class="ptable"><thead><tr><th>Cost component</th><th>Calculation</th><th>Monthly cost</th></tr></thead><tbody>
<tr><td>Invocations (after 1M free)</td><td class="mono">9M × $0.20/M</td><td class="mono">$1.80</td></tr>
<tr><td>Compute GB-sec (after 400K free)</td><td class="mono">10M × 0.2s × 0.25 GB × $0.0000166</td><td class="mono">$0.83</td></tr>
<tr class="best"><td><strong>Lambda total</strong></td><td></td><td class="mono"><strong>$2.63</strong></td></tr>
<tr><td>Cloudflare Workers (Paid)</td><td class="mono">$5 flat covers 10M req</td><td class="mono">$5.00</td></tr>
</tbody></table>
<p><strong>Winner: Lambda</strong> — REST APIs at this scale land well under $5/mo thanks to the free tier.</p>

<h3>Example 2: Image Processing — 1M requests/month, 1024 MB, 2000 ms avg</h3>
<table class="ptable"><thead><tr><th>Cost component</th><th>Calculation</th><th>Monthly cost</th></tr></thead><tbody>
<tr><td>Invocations (within free tier)</td><td class="mono">1M — 1M free = 0</td><td class="mono">$0.00</td></tr>
<tr><td>Compute GB-sec</td><td class="mono">1M × 2s × 1 GB × $0.0000166</td><td class="mono">$33.20</td></tr>
<tr class="best"><td><strong>Lambda total</strong></td><td></td><td class="mono"><strong>$33.20</strong></td></tr>
<tr><td>Cloudflare Workers</td><td colspan="2">Not suitable — 50 ms CPU cap on free, 30 s on paid but no GPU</td></tr>
</tbody></table>
<p><strong>Winner: Lambda</strong> — the only sensible choice for compute-heavy workloads. Workers' CPU wall clock limit disqualifies it here.</p>

<h3>Example 3: High-Frequency Edge API — 100M requests/month, 30 ms avg</h3>
<table class="ptable"><thead><tr><th>Platform</th><th>Cost breakdown</th><th>Monthly total</th></tr></thead><tbody>
<tr><td>Lambda + API Gateway</td><td class="mono">$18 Lambda + $35 API GW</td><td class="mono">$53.00</td></tr>
<tr class="best"><td><strong>Cloudflare Workers</strong></td><td class="mono">$5 base + 90M × $0.50/M</td><td class="mono"><strong>$50.00</strong></td></tr>
<tr><td>Vercel Functions</td><td class="mono">$40 + egress</td><td class="mono">~$45–60</td></tr>
</tbody></table>
<p><strong>Winner: Cloudflare Workers</strong> — at 100M short requests the Workers flat pricing wins, especially once you factor in API Gateway costs Lambda accrues.</p>

<h2>Hidden Costs Most Tutorials Skip</h2>
<p>The Lambda pricing page shows two numbers: invocations and GB-seconds. Your actual invoice will include several more line items that tutorials rarely mention.</p>
<ul>
  <li><strong>API Gateway: $3.50 per million requests</strong> — if your Lambda is HTTP-facing, API Gateway typically doubles the bill. At 10M req/mo that's an extra $35 you won't see coming until the invoice arrives.</li>
  <li><strong>CloudWatch Logs: $0.50 per GB ingested</strong> — a verbose logger writing 5 KB per invocation at 10M calls generates 50 GB of logs = $25/mo. Set log retention to 7 days and log only errors in production.</li>
  <li><strong>NAT Gateway: $0.045 per GB of data processed</strong> — Lambda inside a VPC (required for RDS access) must route outbound traffic through NAT Gateway. At 100 GB/mo that's $4.50 in NAT alone, plus $0.045/GB of data. Heavy S3 or DynamoDB access amplifies this fast.</li>
  <li><strong>Cold start duration charges</strong> — cold starts themselves aren't billed separately, but the added 50–500 ms initialization time <em>is</em> billed as GB-seconds. A 512 MB function with 300 ms cold starts at 1% cold-start rate across 10M invocations adds ~$1.27/mo in invisible compute.</li>
  <li><strong>Provisioned Concurrency: $0.0000097222 per GB-second</strong> — keeping functions warm costs ~$14/mo per always-warm 512 MB instance. Often worth it for latency-sensitive endpoints but plan for it.</li>
</ul>
<div class="callout"><p><strong>Rule of thumb:</strong> multiply your raw Lambda estimate by 1.5–2× to account for API Gateway and logging before presenting it to stakeholders.</p></div>

<h2>When to Choose Lambda vs Alternative</h2>
<p>No single serverless platform wins every workload. Use this decision table to match your use case to the right tool.</p>
<table class="ptable"><thead><tr><th>Use case</th><th>Best pick</th><th>Why</th><th>Monthly cost (10M req)</th></tr></thead><tbody>
<tr class="best"><td>Short API (&lt;50 ms)</td><td><strong>Cloudflare Workers</strong></td><td>No cold starts, edge PoPs, flat pricing</td><td class="mono">$5</td></tr>
<tr><td>AWS-integrated backend</td><td><strong>Lambda</strong></td><td>Native S3/DDB/SQS triggers, IAM</td><td class="mono">$3–6</td></tr>
<tr><td>Next.js / React SSR</td><td><strong>Vercel Functions</strong></td><td>Zero-config deploy, built-in CDN</td><td class="mono">$20+ (Pro)</td></tr>
<tr><td>Image / video processing</td><td><strong>Lambda (1–10 GB)</strong></td><td>High memory, long timeout (15 min)</td><td class="mono">$30–150</td></tr>
<tr><td>Global low-latency API</td><td><strong>Workers or GCP</strong></td><td>200+ PoPs, sub-ms routing</td><td class="mono">$5–15</td></tr>
<tr><td>Scheduled jobs / cron</td><td><strong>Lambda + EventBridge</strong></td><td>Native cron, pay-per-execution</td><td class="mono">&lt;$1</td></tr>
<tr><td>ML inference (&gt;3 GB)</td><td><strong>VPS or Lambda SnapStart</strong></td><td>Lambda max 10 GB RAM; VPS cheaper at scale</td><td class="mono">$10–80</td></tr>
</tbody></table>
<p>If your function duration consistently exceeds 500 ms and you run more than 5M invocations per month, <a href="/blog/cloud-vps-cost-comparison-2026.html">a $6 VPS may undercut Lambda on total cost</a> once you factor in API Gateway.</p>
'''

# Insertion point: before the FAQ h2 block
LAMBDA_INSERT_BEFORE = '<h2>FAQ</h2>'

# ── Cloud VPS additions ───────────────────────────────────────────────────────

VPS_NEW_SECTIONS = '''
<h2>Total Cost of Ownership: Egress Is the Hidden Multiplier</h2>
<p>Raw compute prices are only half the story. Network egress — data transferred <em>out</em> to the internet — is where providers make back margin lost on cheap VMs. Run these numbers before you sign a contract.</p>
<table class="ptable"><thead><tr><th>Provider</th><th>Included egress</th><th>Overage rate</th><th>Cost at 10 TB/mo extra</th></tr></thead><tbody>
<tr class="best"><td><strong>Hetzner</strong></td><td class="mono">20 TB/mo</td><td class="mono">€0.01/GB</td><td class="mono"><strong>€0</strong> (within free)</td></tr>
<tr><td>DigitalOcean</td><td class="mono">1 TB/mo</td><td class="mono">$0.01/GB</td><td class="mono">$90</td></tr>
<tr><td>Vultr</td><td class="mono">3 TB/mo</td><td class="mono">$0.01/GB</td><td class="mono">$70</td></tr>
<tr><td>Linode (Akamai)</td><td class="mono">1–5 TB/mo</td><td class="mono">$0.01/GB</td><td class="mono">$50–90</td></tr>
</tbody></table>
<p>A media-serving app at 10 TB/mo egress pays <strong>€0 on Hetzner</strong> but up to <strong>$90/mo on DigitalOcean</strong> — on top of compute. At that scale Hetzner's effective all-in cost for a 4 GB instance is ~€8.50/mo vs $72/mo on DO. That's an 8× gap.</p>
<div class="callout"><p><strong>Watch out:</strong> inbound traffic (uploads, API calls to your server) is free on all major providers. The egress meter only ticks when data leaves your VPS toward users or the public internet.</p></div>

<h2>Which Provider for Which Use Case</h2>
<p>There is no universal "best VPS" — the right answer depends on your audience geography, managed-service needs, and traffic profile.</p>
<table class="ptable"><thead><tr><th>Use case</th><th>Best pick</th><th>Runner-up</th><th>Reason</th></tr></thead><tbody>
<tr class="best"><td>EU-audience SaaS / GDPR</td><td><strong>Hetzner</strong></td><td>Scaleway</td><td>Cheapest EU compute, GDPR by default, 20 TB free egress</td></tr>
<tr><td>US-audience startup</td><td><strong>Vultr (NY/LA)</strong></td><td>DigitalOcean</td><td>Competitive US pricing, 32 locations, $300 credit</td></tr>
<tr><td>Global CDN / multi-region</td><td><strong>Vultr</strong></td><td>Linode</td><td>32 PoPs including SEA, LatAm, Africa</td></tr>
<tr><td>Managed Postgres / Redis</td><td><strong>DigitalOcean</strong></td><td>Render</td><td>Native managed DBs, App Platform, mature ecosystem</td></tr>
<tr><td>GPU / ML workloads</td><td><strong>Vultr GPU</strong></td><td>Lambda Labs</td><td>Hourly A100/H100 available; cheaper than AWS on-demand</td></tr>
<tr><td>Dev / staging server</td><td><strong>Hetzner CX22</strong></td><td>Vultr $6</td><td>€4.50/mo with 20 GB NVMe — unmatched dev value</td></tr>
<tr><td>High-availability cluster</td><td><strong>Hetzner + Floating IP</strong></td><td>DO + Load Balancer</td><td>Hetzner HA clusters cost 3–5× less than DO equivalent</td></tr>
</tbody></table>

<h2>Setup Time &amp; Support Comparison</h2>
<p>Price isn't everything. Developer experience, provisioning speed, and support quality affect real total cost — especially if your team is small.</p>
<table class="ptable"><thead><tr><th>Provider</th><th>Provisioning</th><th>Control panel</th><th>Support</th><th>Docs quality</th></tr></thead><tbody>
<tr><td><strong>Hetzner</strong></td><td class="mono">&lt;45 sec</td><td>Cloud Console (excellent)</td><td>Ticket only (fast, 2–4 hr)</td><td>Good (German-precise)</td></tr>
<tr class="best"><td><strong>DigitalOcean</strong></td><td class="mono">&lt;60 sec</td><td>Best-in-class UX</td><td>Email + chat (Pro: phone)</td><td>Best-in-class tutorials</td></tr>
<tr><td><strong>Vultr</strong></td><td class="mono">&lt;60 sec</td><td>Modern, clean</td><td>Ticket + 24/7 chat</td><td>Good</td></tr>
<tr><td><strong>Linode (Akamai)</strong></td><td class="mono">&lt;90 sec</td><td>Dated but functional</td><td>24/7 phone on all plans</td><td>Extensive</td></tr>
</tbody></table>
<p>If your team is new to self-managed VPS, DigitalOcean's documentation library and community tutorials provide a faster ramp-up despite the higher price. Once comfortable, migrating a working stack to Hetzner takes an afternoon and saves $15–40/mo.</p>
<p>Need a serverless alternative instead? Read: <a href="/blog/aws-lambda-cost-calculator-2026.html">when Lambda costs more than a VPS</a> — or use the <a href="/#cloud">VPS cost calculator</a> to model your exact spec.</p>
'''

VPS_INSERT_BEFORE = '<h2>FAQ</h2>'

# ── Apply changes ─────────────────────────────────────────────────────────────

import os

def strengthen(path, new_html, marker):
    c = open(path, encoding='utf-8').read()
    if 'Real-World Cost Examples' in c or 'Total Cost of Ownership: Egress Is the Hidden Multiplier' in c:
        print(f'SKIP (already patched): {path}')
        return
    if marker not in c:
        print(f'ERROR: marker not found in {path}')
        return
    c = c.replace(marker, new_html + '\n' + marker, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'OK: {path}')

strengthen(
    os.path.join(BASE, 'blog', 'aws-lambda-cost-calculator-2026.html'),
    LAMBDA_NEW_SECTIONS,
    LAMBDA_INSERT_BEFORE
)

strengthen(
    os.path.join(BASE, 'blog', 'cloud-vps-cost-comparison-2026.html'),
    VPS_NEW_SECTIONS,
    VPS_INSERT_BEFORE
)

# Also update read time in meta
for fname, old_time, new_time in [
    ('blog/aws-lambda-cost-calculator-2026.html', '8 min read', '12 min read'),
    ('blog/cloud-vps-cost-comparison-2026.html',  '8 min read', '12 min read'),
]:
    path = os.path.join(BASE, fname)
    c = open(path, encoding='utf-8').read()
    c = c.replace(old_time, new_time, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'  read-time updated: {fname}')

print('Section 6 done.')
