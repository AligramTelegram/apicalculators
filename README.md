# APICalculators

Free, client-side infrastructure cost calculators for developers — LLM/AI API pricing, vector databases, cloud VPS, serverless, payments, and auth providers.

## Stack

Plain HTML/CSS/JS. No build step, no framework. One shared `styles.css` design system ("Overclocked Ledger") and `theme.js` for light/dark toggling.

## Structure

- `index.html` — calculator + compare directory
- `*-cost.html`, `payment-processor-fees.html`, `auth-provider-cost.html` — 12 core calculators
- `compare/` — head-to-head provider comparison pages
- `about.html`, `contact.html`, `privacy.html`, `terms.html`, `404.html` — static pages
- `robots.txt`, `sitemap.xml`, `manifest.json`, `vercel.json` — SEO/hosting config

## Pricing data

All rates are sourced from provider pricing pages and reviewed monthly. When adding or updating a calculator, verify the rate against the provider's current published pricing before committing.

## Local development

Any static file server works, e.g.:

```
python -m http.server 8000
```
