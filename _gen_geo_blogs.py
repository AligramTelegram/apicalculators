#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 7: Generate 6 geo-specific blog posts (DE×2, FR×2, TR×2)."""
import sys, os, json, html
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

def blog_post(lang, locale, region, title, h1, desc, intro, body_html, faq_items, related_links, path):
    """Generate complete blog post HTML."""

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            }
            for q, a in faq_items
        ]
    }

    related_html = '\n          '.join(
        f'<a href="{url}">{title}</a>'
        for url, title in related_links
    )

    breadcrumb_title = h1[:60]
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://apicalculators.com/{'' if lang == 'en' else lang + '/'}"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://apicalculators.com/{'' if lang == 'en' else lang + '/'}blog/"},
            {"@type": "ListItem", "position": 3, "name": breadcrumb_title}
        ]
    }

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "description": desc,
        "datePublished": "2026-06-04",
        "dateModified": "2026-06-04",
        "author": {"@type": "Organization", "name": "APICalculators"},
        "publisher": {
            "@type": "Organization",
            "name": "APICalculators",
            "logo": {"@type": "ImageObject", "url": "https://apicalculators.com/logo.png"}
        }
    }

    home_url = '/' if lang == 'en' else f'/{lang}/'
    blog_url = f'{home_url}blog/' if lang == 'en' else f'/{lang}/blog/'

    html_content = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://apicalculators.com{path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:locale" content="{locale}" />
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://apicalculators.com{path}">
<meta property="og:image" content="https://apicalculators.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" hreflang="{lang}" href="https://apicalculators.com{path}">
<link rel="alternate" hreflang="x-default" href="https://apicalculators.com{path}">
<meta name="geo.region" content="{region}" />
<script type="application/ld+json">{json.dumps(article_schema)}</script>
<script type="application/ld+json">{json.dumps(faq_schema)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_schema)}</script>
<style>
:root{{--bg:#0a0c10;--bg2:#0c0f15;--surface:#12161d;--surface2:#161b24;--border:#1d2530;--border2:#27313e;--text:#e8edf1;--muted:#8b97a4;--muted2:#8a96a5;--lime:#b8ff2e;--cyan:#4dd6ff;--amber:#ffb24d}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;line-height:1.75}}
a{{color:var(--lime);text-decoration:none}}a:hover{{text-decoration:underline}}.wrap{{max-width:820px;margin:0 auto;padding:0 22px}}
header.nav{{position:sticky;top:0;z-index:50;backdrop-filter:blur(14px);background:rgba(10,12,16,.72);border-bottom:1px solid var(--border)}}
.nav-in{{display:flex;align-items:center;justify-content:space-between;height:60px;max-width:1100px;margin:0 auto;padding:0 22px}}
.logo{{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:18px}}.logo b{{color:var(--lime)}}
.nav-r{{display:flex;gap:22px}}.nav-r a{{color:var(--muted);font-size:14px;font-weight:500}}
.breadcrumb{{display:flex;gap:8px;font-family:'Cascadia Code','Consolas',monospace;font-size:12px;color:var(--muted2);margin-bottom:24px;flex-wrap:wrap}}
.breadcrumb a{{color:var(--muted2)}}.breadcrumb span{{color:var(--border2)}}
.atag{{font-family:'Cascadia Code','Consolas',monospace;font-size:10px;border:1px solid var(--border2);border-radius:5px;padding:3px 8px;color:var(--muted2)}}.atag.hi{{border-color:rgba(184,255,46,.35);color:var(--lime)}}
h1{{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:clamp(24px,4vw,36px);letter-spacing:-.03em;line-height:1.1;margin-bottom:16px}}
.art-meta{{font-family:'Cascadia Code','Consolas',monospace;font-size:12px;color:var(--muted2);margin-bottom:28px}}
.intro{{font-size:18px;color:#cdd6dd;margin-bottom:32px;padding-bottom:28px;border-bottom:1px solid var(--border)}}
h2{{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:22px;margin:36px 0 13px}}
h3{{font-family:'Arial Black',system-ui,sans-serif;font-weight:700;font-size:16px;margin:22px 0 9px;color:#d4dce3}}
p{{color:#cdd6dd;margin-bottom:14px}}ul,ol{{color:#cdd6dd;padding-left:22px;margin-bottom:14px}}li{{margin-bottom:7px}}strong{{color:var(--text)}}
.ptable{{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.5px}}
.ptable th{{text-align:left;font-family:'Cascadia Code','Consolas',monospace;font-size:11px;text-transform:uppercase;color:var(--muted2);padding:8px 12px;border-bottom:2px solid var(--border);white-space:nowrap}}
.ptable td{{padding:9px 12px;border-bottom:1px solid var(--border);color:#cdd6dd}}.ptable .best td{{background:rgba(184,255,46,.04)}}.ptable .best td:first-child{{border-left:2px solid var(--lime)}}
.mono{{font-family:'Cascadia Code','Consolas',monospace}}
.callout{{border-radius:12px;padding:15px 18px;margin:18px 0;border-left:3px solid var(--lime);background:rgba(184,255,46,.07)}}.callout p{{margin:0}}
.ilink-box{{background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:18px;margin:28px 0}}
.ilink-box .il-title{{font-family:'Cascadia Code','Consolas',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted2);margin-bottom:12px;font-weight:700}}
.ilink-box .il-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}}
.ilink-box a{{display:flex;align-items:center;gap:8px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:9px 12px;color:var(--muted);font-size:13px;font-weight:500;transition:all .15s}}
.ilink-box a:hover{{border-color:var(--lime);color:var(--text);text-decoration:none}}
.ilink-box a::before{{content:"→";color:var(--lime);font-weight:700}}
footer{{border-top:1px solid var(--border);padding:28px 0;font-family:'Cascadia Code','Consolas',monospace;font-size:12px;color:var(--muted2)}}
.foot-in{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;max-width:1100px;margin:0 auto;padding:0 22px}}footer a{{color:var(--muted2)}}
.affiliate-cta{{margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(184,255,46,.06);border:1px solid rgba(184,255,46,.25);border-radius:8px}}
.aff-headline{{margin:0 0 .6rem;font-size:.85rem;color:#b8ff2e;font-weight:600;letter-spacing:.02em}}
.aff-links{{display:flex;flex-wrap:wrap;gap:.5rem}}
.aff-btn{{display:inline-block;padding:.35rem .75rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:6px;color:#e8eaed;text-decoration:none;font-size:.82rem;transition:background .15s,border-color .15s}}
.aff-btn:hover{{background:rgba(184,255,46,.15);border-color:rgba(184,255,46,.5);color:#b8ff2e}}
@media(max-width:600px){{.ilink-box .il-grid{{grid-template-columns:1fr}}}}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
</head>
<body>
<header class="nav"><div class="nav-in"><a href="{home_url}" class="logo">API<b>Calculators</b></a><nav class="nav-r"><a href="{home_url}#calc">Calculators</a><a href="{blog_url}">Blog</a></nav></div></header>
<main class="wrap" style="padding:48px 0 80px">
  <nav class="breadcrumb"><a href="{home_url}">Home</a><span>/</span><a href="{blog_url}">Blog</a><span>/</span><span>{h1[:50]}</span></nav>
  <h1>{h1}</h1>
  <div class="art-meta">2026-06-04 · 10 min read · APICalculators</div>
  <p class="intro">{intro}</p>

  {body_html}

  <h2>FAQ</h2>
'''

    for q, a in faq_items:
        html_content += f'''  <h3>{q}</h3>
  <p>{a}</p>
'''

    html_content += f'''
<div class="ilink-box">
  <div class="il-title">Related Tools & Guides</div>
  <div class="il-grid">
          {related_html}
          <a href="{blog_url}">Blog Index</a>
  </div>
</div>
<div style="display:flex;gap:16px;align-items:flex-start;background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:20px;margin-top:32px">
<div style="width:48px;height:48px;border-radius:10px;background:var(--lime);display:grid;place-items:center;font-size:22px;flex-shrink:0">🧮</div>
<div><div style="font-family:'Arial Black',system-ui;font-weight:900;font-size:15px;margin-bottom:4px">APICalculators</div>
<p style="color:var(--muted);font-size:13px;margin:0">APICalculators Team · Free developer cost tools. Prices from official documentation, updated monthly.</p></div></div>
</main>
<footer><div class="foot-in"><span>© 2026 APICalculators.com</span><span><a href="{home_url}">Home</a> · <a href="{blog_url}">Blog</a> · <a href="{home_url}privacy.html">Privacy</a></span></div></footer>
</body>
</html>'''

    return html_content

# ── DE Blog Posts ─────────────────────────────────────────────────────────────

de_llm_body = '''<h2>LLM-API-Kosten: Die Grundlagen</h2>
<p>Jede LLM-API berechnet nach zwei Dimensionen: <strong>Input-Tokens</strong> (Ihr Prompt) und <strong>Output-Tokens</strong> (die Antwort des Modells). GPT-4o kostet €2,32 pro Million Input-Tokens und €9,28 pro Million Output-Tokens (Umrechnung EUR, Juni 2026).</p>

<h2>2026 LLM-Preise im Überblick</h2>
<table class="ptable"><thead><tr><th>Modell</th><th>Input / 1M Tokens</th><th>Output / 1M Tokens</th></tr></thead><tbody>
<tr class="best"><td><strong>GPT-4o</strong></td><td class="mono">€2,32</td><td class="mono">€9,28</td></tr>
<tr><td>Claude 3.5 Sonnet</td><td class="mono">€2,77</td><td class="mono">€13,89</td></tr>
<tr><td>Gemini 1.5 Pro</td><td class="mono">€1,15</td><td class="mono">€4,62</td></tr>
<tr><td>Gemini 1.5 Flash</td><td class="mono">€0,07</td><td class="mono">€0,28</td></tr>
</tbody></table>

<h2>Kostenersparnis: Batch API & Cached Tokens</h2>
<p>OpenAI und Anthropic bieten Kostensparen-Optionen:</p>
<ul>
<li><strong>Batch API:</strong> 50% Rabatt auf Input-Tokens, aber 24-Stunden Latenz — ideal für Offline-Verarbeitung.</li>
<li><strong>Prompt Caching (Claude):</strong> Wiederverwendete Prompts kosten nur 10% des normalen Preises.</li>
<li><strong>Gemini Cached Tokens:</strong> Ähnlich Claude — perfekt für RAG-Pipelines mit häufigen Kontext-Blöcken.</li>
</ul>

<h2>Echte Beispiele: 10K Requests / Monat</h2>
<table class="ptable"><thead><tr><th>Szenario</th><th>Modell</th><th>Monatliche Kosten</th></tr></thead><tbody>
<tr class="best"><td>Chat-Bot (1000 Tokens avg)</td><td>Gemini Flash</td><td class="mono">€0,70</td></tr>
<tr><td>Dokumentation suchen (5000 Tokens)</td><td>GPT-4o mini</td><td class="mono">€15,00</td></tr>
<tr><td>Code-Analyse (10K Tokens)</td><td>Claude 3.5 Sonnet</td><td class="mono">€277,00</td></tr>
</tbody></table>

<div class="callout"><p><strong>💡 Tipp:</strong> Nutze <a href="/{home_url}#llm">unseren LLM-Kostenrechner</a>, um Deine genauen Token-Mengen einzugeben und sofort zu sehen, welches Modell am günstigsten ist.</p></div>

<div class="affiliate-cta">
  <p class="aff-headline">Bereit zu starten? Kostenlose Credits:</p>
  <div class="aff-links">
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">💳 €300 Vultr-Guthaben</a>
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇩🇪 Hetzner EU-Server</a>
  </div>
</div>
'''

de_llm_faq = [
    ("Kostet Claude 3.5 Sonnet mehr als GPT-4o?", "Ja — Claude 3.5 Sonnet kostet €2,77/M Input-Tokens vs. GPT-4o €2,32/M. Claude ist bei langen Outputs teurer (€13,89 vs €9,28). Wähle GPT-4o für Kosteneffizienz."),
    ("Wie spare ich mit Batch API?", "Die Batch API von OpenAI bietet 50% Rabatt, benötigt aber eine 24-Stunden Wartezeit. Ideal für nächtliche Verarbeitung, E-Mail-Analysen, Batch-Übersetzungen."),
    ("Welches Modell ist für deutsche Nutzer optimal?", "Für Deutsch: Gemini 1.5 Flash ist preiswert; Claude 3.5 Haiku ist schneller. GPT-4o ist am genauesten, kostet aber mehr."),
]

de_llm_related = [
    ("/de/#llm", "LLM-Kostenrechner öffnen"),
    ("/de/blog/", "Blog-Übersicht"),
    ("/de/blog/vektordatenbank-kosten-vergleich-2026.html", "Vector DB Kosten"),
]

# ── Hetzner vs DigitalOcean (DE) ──────────────────────────────────────────────

de_vps_body = '''<h2>Preisvergleich: Hetzner vs DigitalOcean (Juni 2026)</h2>
<table class="ptable"><thead><tr><th>Spezifikation</th><th>Hetzner</th><th>DigitalOcean</th><th>Ersparnis</th></tr></thead><tbody>
<tr class="best"><td>1 vCPU / 2 GB RAM</td><td class="mono">€3,99</td><td class="mono">$12</td><td><strong>~€8</strong></td></tr>
<tr><td>2 vCPU / 4 GB RAM</td><td class="mono">€4,50</td><td class="mono">$24</td><td><strong>~€20</strong></td></tr>
<tr><td>4 vCPU / 8 GB RAM</td><td class="mono">€8,50</td><td class="mono">$48</td><td><strong>~€40</strong></td></tr>
</tbody></table>

<h2>Warum ist Hetzner so günstig?</h2>
<ul>
<li><strong>Deutsche Infrastruktur:</strong> Rechenzentren in Deutschland und Finnland — weniger Gemeinkosten als US-Betrieb.</li>
<li><strong>Europäisches Geschäftsmodell:</strong> Hetzner verdient durch Volumen, nicht durch Premium-Pricing.</li>
<li><strong>Egress-Richtlinie:</strong> 20 TB/Monat kostenlos — DigitalOcean berechnet $0,01/GB nach 1 TB.</li>
</ul>

<h2>Sicherheit, Datenschutz & GDPR</h2>
<p>Hetzner ist <strong>GDPR-konform by default</strong>. Alle Server stehen in der EU. DigitalOcean hat Rechenzentren weltweit, was Datenschutz-Compliance kompliziert macht. Für deutsche SaaS: Hetzner ist die offensichtliche Wahl.</p>

<div class="callout"><p><strong>⚖️ Hinweis:</strong> Hetzner hat weniger globale Standorte (2 vs. DO 13). Falls Du Latenz zu US-Kunden brauchst, ist DigitalOcean möglicherweise besser — aber 5× teurer.</p></div>

<h2>Wann DigitalOcean?</h2>
<ul>
<li>Global verteilte Teams (Latenz zu mehreren Regionen)</li>
<li>Managed Databases brauchst (Postgres, MySQL als Service)</li>
<li>App Platform (Heroku-ähnliche Erfahrung) möchtest</li>
<li>Managed Kubernetes (DOKS) brauchst</li>
</ul>

<p>Für reine VM-Leistung, EU-Datenschutz und Kosteneffizienz: <strong>wähle Hetzner</strong>.</p>

<div class="affiliate-cta">
  <p class="aff-headline">Jetzt starten:</p>
  <div class="aff-links">
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇩🇪 Hetzner — günstige EU-Server</a>
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">🌍 Vultr — globale Standorte</a>
  </div>
</div>
'''

de_vps_faq = [
    ("Ist Hetzner sicher?", "Ja — ISO 27001 zertifiziert, GDPR-konform, Einrichtungen in Deutschland. Sicherheit ist mit DigitalOcean vergleichbar."),
    ("Wie gut ist der Support?", "Ticket-basiert, deutsche Sprachunterstützung. DigitalOcean hat 24/7 Chat-Support, aber weniger Deutsch-Speaker."),
    ("Kann ich von DigitalOcean zu Hetzner migrieren?", "Ja — rsync oder Snapshot-Export funktioniert. Migration dauert ~2–4 Stunden für typische VPS."),
]

de_vps_related = [
    ("/de/#cloud", "Cloud-VPS-Rechner öffnen"),
    ("/de/blog/", "Blog-Übersicht"),
    ("/de/blog/aws-lambda-kosten-guide-2026.html", "Serverless statt VPS?"),
]

# ── FR Blog Posts ─────────────────────────────────────────────────────────────

fr_llm_body = '''<h2>Prix des API LLM en euros (2026)</h2>
<p>Les tarifs officiels sont en dollars USD. Pour la France, convertissez au taux EUR (~€0,92 par $). GPT-4o coûte $2,50/M tokens input = <strong>€2,30/M</strong>.</p>

<h2>Tableau des prix 2026</h2>
<table class="ptable"><thead><tr><th>Modèle</th><th>Input / 1M tokens</th><th>Output / 1M tokens</th></tr></thead><tbody>
<tr class="best"><td><strong>GPT-4o</strong></td><td class="mono">€2,30</td><td class="mono">€9,20</td></tr>
<tr><td>Claude 3.5 Sonnet</td><td class="mono">€2,76</td><td class="mono">€13,80</td></tr>
<tr><td>Gemini 1.5 Pro</td><td class="mono">€1,15</td><td class="mono">€4,60</td></tr>
<tr><td>Mistral Large 2</td><td class="mono">€0,81</td><td class="mono">€2,43</td></tr>
</tbody></table>

<h2>Modèles français : Mistral vs OpenAI</h2>
<p><strong>Mistral Large 2</strong> est une excellente alternative française. Comparable à GPT-4o en qualité, mais 60% moins cher. Parfait pour les startups françaises sous CNIL/RGPD strict.</p>

<h2>Exemple: Chatbot français / 100K requests/mois</h2>
<table class="ptable"><thead><tr><th>Modèle</th><th>Coût / mois</th></tr></thead><tbody>
<tr class="best"><td>Mistral Large 2</td><td class="mono">€81</td></tr>
<tr><td>GPT-4o mini</td><td class="mono">€18</td></tr>
<tr><td>Claude 3.5 Haiku</td><td class="mono">€92</td></tr>
</tbody></table>

<div class="callout"><p><strong>🇫🇷 Conseil RGPD:</strong> Mistral héberge les modèles en France. Aucun transfert de données vers les USA — idéal pour les données sensibles.</p></div>

<div class="affiliate-cta">
  <p class="aff-headline">Infrastructure pour ta startup IA :</p>
  <div class="aff-links">
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇩🇪 Serveurs Hetzner EU</a>
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">💳 €300 Vultr</a>
  </div>
</div>
'''

fr_llm_faq = [
    ("Mistral est-il moins bon que GPT-4o?", "Non — Mistral Large 2 est comparable en qualité générale. GPT-4o excelle en raisonnement complexe. Pour 80% des cas d'usage, Mistral suffit."),
    ("Comment convertir les prix USD en euros?", "Multiplie par le taux EUR (~0,92). $100 = ~€92. Les tarifs changent rarement, les taux EUR fluctuent."),
    ("Quel modèle choisir pour une startup française?", "Mistral Large 2 pour RGPD strict. Claude pour nuance/qualité. GPT-4o pour raisonnement."),
]

fr_llm_related = [
    ("/fr#llm", "Ouvrir calculateur LLM"),
    ("/fr/blog/", "Index blog FR"),
    ("/fr/blog/comparaison-couts-base-vectorielle-2026.html", "Coûts Vector DB"),
]

# ── Comparatif VPS France (FR) ────────────────────────────────────────────────

fr_vps_body = '''<h2>VPS en France : Hetzner vs OVHcloud vs DigitalOcean</h2>
<table class="ptable"><thead><tr><th>Fournisseur</th><th>2 vCPU / 4 GB</th><th>Localisation</th><th>Prix/an</th></tr></thead><tbody>
<tr class="best"><td><strong>Hetzner (Strasbourg)</strong></td><td class="mono">€4,50/mo</td><td>France/Allemagne</td><td class="mono">€54</td></tr>
<tr><td>OVHcloud (Roubaix)</td><td class="mono">€8,99/mo</td><td>France</td><td class="mono">€108</td></tr>
<tr><td>Scaleway (Paris)</td><td class="mono">€6,99/mo</td><td>France</td><td class="mono">€84</td></tr>
<tr><td>DigitalOcean (Paris)</td><td class="mono">€20/mo</td><td>Monde</td><td class="mono">€240</td></tr>
</tbody></table>

<h2>Pourquoi choisir Hetzner pour la France?</h2>
<ul>
<li><strong>Latence optimale :</strong> Strasbourg = 20 ms à Paris/Lyon. Comparable à OVHcloud.</li>
<li><strong>GDPR certifié :</strong> Données restent en EU. Pas de transfert vers les USA.</li>
<li><strong>Prix :</strong> 50% moins cher qu'OVHcloud, infrastructure identique.</li>
<li><strong>Egress gratuit :</strong> 20 TB/mois compris. OVHcloud facture $0,01/GB après 100 Go.</li>
</ul>

<h2>Quand choisir OVHcloud?</h2>
<p>OVHcloud a un avantage : support français natif 24/7, et certains clients préfèrent une "entreprise française". Mais techniquement et économiquement, Hetzner gagne.</p>

<h2>Infrastructure: RGPD et localisation des données</h2>
<p>Pour une SaaS française, toutes ces options (Hetzner, OVHcloud, Scaleway) sont RGPD-compliant. La différence : coût et latence. Hetzner gagne sur les deux.</p>

<div class="affiliate-cta">
  <p class="aff-headline">Lance ta plateforme en France :</p>
  <div class="aff-links">
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇩🇪 Hetzner Strasbourg</a>
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">💳 €300 Vultr</a>
  </div>
</div>
'''

fr_vps_faq = [
    ("Hetzner est allemand — GDPR ok?", "Oui, 100%. Les données restent en Allemagne/Finlande, dans l'EU. Aucun transfert USA."),
    ("OVHcloud vs Hetzner pour RGPD strict?", "Les deux sont conformes. Hetzner est plus connu pour GDPR. Support français fait la différence si tu préfères téléphoner en français."),
    ("Scaleway (Iliad) — pourquoi pas?", "Scaleway est bon, mais plus cher que Hetzner (€6,99 vs €4,50). Moins d'options de stockage à bas prix."),
]

fr_vps_related = [
    ("/fr#cloud", "Ouvrir calculateur VPS"),
    ("/fr/blog/", "Index blog FR"),
    ("/fr/blog/guide-cout-aws-lambda-2026.html", "Serverless vs VPS"),
]

# ── TR Blog Posts ─────────────────────────────────────────────────────────────

tr_llm_body = '''<h2>GPT API Türkiye: Token Fiyatlandırması 2026</h2>
<p>OpenAI API fiyatlandırması USD cinsinden. Türkiye'den kullanırsan dolar kuruna dikkat et (~38 ₺/$). GPT-4o $2,50/M tokens = <strong>~95 ₺/M token</strong>.</p>

<h2>2026 LLM Fiyatları (TRY cinsinden)</h2>
<table class="ptable"><thead><tr><th>Model</th><th>Input / 1M token</th><th>Output / 1M token</th></tr></thead><tbody>
<tr class="best"><td><strong>GPT-4o</strong></td><td class="mono">~95 ₺</td><td class="mono">~380 ₺</td></tr>
<tr><td>Claude 3.5 Sonnet</td><td class="mono">~114 ₺</td><td class="mono">~570 ₺</td></tr>
<tr><td>Gemini 1.5 Flash</td><td class="mono">~3 ₺</td><td class="mono">~11 ₺</td></tr>
<tr><td>Llama 3.1 (Meta)</td><td class="mono">Free</td><td class="mono">Free</td></tr>
</tbody></table>

<h2>Meta Llama 3.1: Ücretsiz Alternatif</h2>
<p>Meta Llama 3.1 tamamen ücretsiz ve açık kaynak. Kendi sunucunda çalıştırabilirsin. Kalite GPT-4o kadar iyi değil ama %80'i yapabiliyor — ve sıfır dolar.</p>

<h2>Gerçek Örnek: Türkçe Chatbot / 50K request/ay</h2>
<table class="ptable"><thead><tr><th>Seçenek</th><th>Aylık maliyet (TRY)</th></tr></thead><tbody>
<tr class="best"><td>Llama 3.1 (kendi sunucuda)</td><td class="mono">~500 ₺ (sunucu)</td></tr>
<tr><td>GPT-4o mini (OpenAI)</td><td class="mono">~285 ₺</td></tr>
<tr><td>Claude 3.5 Haiku</td><td class="mono">~304 ₺</td></tr>
</tbody></table>

<div class="callout"><p><strong>💡 İpucu:</strong> Türkçe NLP için Llama 3.1 harika. Kurulum vakit alır ama uzun vadede çok ucuz.</p></div>

<div class="affiliate-cta">
  <p class="aff-headline">Sunucu bulut altyapısı:</p>
  <div class="aff-links">
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">💳 $300 Vultr kredisi</a>
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇪🇺 Hetzner EU</a>
  </div>
</div>
'''

tr_llm_faq = [
    ("Llama 3.1 kendi sunucuda çalıştırmak zor mu?", "Orta zorluk. Docker ve Python gerekli. Ama bir kere kurdum mı, tamamen özel — no API bills."),
    ("Türkiye'de dolar kuruna dikkat etmeli miyim?", "Evet! Kur döneminde %20 fark oluşabilir. Dolarla fiyatlandırılmış API'ler riskli, coğrafi arbitraj var."),
    ("Hangisini seçmeliyim, Llama mı GPT mı?", "Hacı ürün MVP hızlı lazım: GPT-4o. Türkçe sohbet botu: Llama 3.1. Doğruluk kritik: Claude."),
]

tr_llm_related = [
    ("/tr#llm", "LLM Hesaplayıcısını Aç"),
    ("/tr/blog/", "Blog Endeksi TR"),
    ("/tr/blog/vektor-veritabani-maliyet-karsilastirmasi-2026.html", "Vector DB Maliyeti"),
]

# ── Stripe Türkiye (TR) ───────────────────────────────────────────────────────

tr_stripe_body = '''<h2>Stripe Türkiye: Ücretler ve Sınırlamalar (2026)</h2>
<p>Stripe resmen Türkiye'ye para göndermez (ülke kısıtlaması). Ancak Stripe'ı dolaylı olarak kullanabilirsin: USD veya EUR cüzdanında para tut.</p>

<h2>Alternatifler: Türkiye'de Ödeme Alımı</h2>
<table class="ptable"><thead><tr><th>Ödeme Sağlayıcı</th><th>Türkiye Desteği</th><th>Komisyon</th><th>Para Çekme</th></tr></thead><tbody>
<tr class="best"><td><strong>Iyzico (Türk)</strong></td><td>✅ Full</td><td class="mono">%2,49 + 0,99 ₺</td><td>3–5 gün TRY</td></tr>
<tr><td>2Checkout</td><td>✅ Full</td><td class="mono">%3,5–5%</td><td>Weekly USD</td></tr>
<tr><td>Paystack</td><td>❌ No</td><td>—</td><td>—</td></tr>
<tr><td>Stripe (USD cüzdan)</td><td>⚠️ Indirect</td><td class="mono">%2,9 + $0,30</td><td>Manual TRY</td></tr>
</tbody></table>

<h2>Niye Stripe Türkiye Desteklemez?</h2>
<p>Geopolitik ve denetim riski. Stripe ABD şirketi, OFAC yaptırımlarına tabi. Ödeme altyapısını Türkiye'ye kurması kompleks. Iyzico yerel, daha basit.</p>

<h2>Önerilen Kurulum</h2>
<ul>
<li><strong>Düşük hacim (&lt;₺50K/ay):</strong> Iyzico. Basit kurulum, hızlı para çekme.</li>
<li><strong>Yüksek hacim / USD gerekli:</strong> Stripe + USD transfer servisi (Wise vb.).</li>
<li><strong>Uluslararası müşteri:</strong> 2Checkout + Iyzico dual setup.</li>
</ul>

<div class="affiliate-cta">
  <p class="aff-headline">Sunucu ve altyapı:</p>
  <div class="aff-links">
    <a href="https://www.vultr.com/?ref=9904710-9J" rel="sponsored" target="_blank" class="aff-btn">💳 $300 Vultr</a>
    <a href="[HETZNER_AFFILIATE_LINK]" rel="sponsored" target="_blank" class="aff-btn">🇪🇺 EU Sunucu</a>
  </div>
</div>
'''

tr_stripe_faq = [
    ("Stripe'ı Türkiye'den kullanabilir miyim?", "Dolaylı olarak evet. USD/EUR cüzdan aç, ödeme al. Ama para çekme zor — Wise gibi dönüştürücü gerek."),
    ("Iyzico ne kadar emniyetli?", "Türkiye'nin en büyük ödeme ağı. Binlerce tüccar kullanıyor. Stripe kadar iyi değil ama iyi."),
    ("Hangisini seçmeliyim başında?", "SaaS başladıysan: 2Checkout. E-ticaret: Iyzico. Enterprise: tüm üçünü kurmaya bak."),
]

tr_stripe_related = [
    ("/tr#payment", "Ödeme Hesaplayıcısını Aç"),
    ("/tr/blog/", "Blog Endeksi TR"),
    ("/tr/blog/aws-lambda-maliyet-rehberi-2026.html", "Serverless Maliyeti"),
]

# ── Write files ───────────────────────────────────────────────────────────────

posts = [
    ('de', 'de_DE', 'DE', 'LLM-API-Kosten berechnen: GPT-4o, Claude & Gemini 2026',
     'LLM-API-Kosten berechnen: GPT-4o, Claude & Gemini im Vergleich',
     'Berechne die Kosten deiner LLM-API-Nutzung in 2026. Vergleich von GPT-4o, Claude 3.5 Sonnet und Gemini mit realen Beispielen und Kostenoptimierungstipps.',
     'Die meisten Entwickler unterschätzen ihre LLM-Kosten, bis die Rechnung kommt. Dieser Leitfaden zeigt dir, wie du GPT-4o, Claude und Gemini kostet, versteckte Kostenoptimierungen nutzt und dein Budget genau prognostizierst — mit kostenlosen Rechnern.',
     de_llm_body, de_llm_faq, de_llm_related, '/de/blog/llm-api-kosten-2026.html'),

    ('de', 'de_DE', 'DE', 'Hetzner vs DigitalOcean 2026: Vollständiger Kostenvergleich',
     'Hetzner vs DigitalOcean 2026: VPS-Kostenvergleich für Deutschland',
     'Vergleiche Hetzner und DigitalOcean: Spezifikationen, GDPR, Egress-Kosten. Welcher VPS ist am günstigsten für EU-Workloads?',
     'Die VPS-Wahl entscheidet über die Cloud-Kosten deines Startups. Hetzner ist 5× günstiger als DigitalOcean für EU-Workloads — aber wann ist DO besser? Dieser Leitfaden vergleicht beide mit echten Zahlen.',
     de_vps_body, de_vps_faq, de_vps_related, '/de/blog/hetzner-digitalocean-vergleich-2026.html'),

    ('fr', 'fr_FR', 'FR', 'Quel est le vrai coût de l\'API GPT-4o en 2026?',
     'Calculer le coût API LLM 2026: GPT-4o, Claude & Gemini en euros',
     'Tarifs LLM en euros: GPT-4o €2,30/M tokens. Guide complet pour calculer tes coûts API 2026 avec exemples réels et optimisations.',
     'Chaque startup IA doit comprendre ses coûts API — sinon c\'est la surprise à la facture. Ce guide détaille les tarifs LLM 2026 en euros, te montre comment les calculer et t\'aide à choisir le bon modèle.',
     fr_llm_body, fr_llm_faq, fr_llm_related, '/fr/blog/cout-api-llm-2026.html'),

    ('fr', 'fr_FR', 'FR', 'Comparatif VPS Cloud France 2026: Hetzner vs OVHcloud vs Scaleway',
     'Comparateur Prix VPS Cloud France 2026: Hetzner vs OVHcloud vs Scaleway',
     'VPS pour la France: Hetzner €4,50/mo vs OVHcloud €8,99. GDPR, latence, prix — quel serveur choisir?',
     'Lancer une SaaS en France signifie choisir son serveur. Hetzner, OVHcloud, Scaleway — qui gagne sur le prix, la latence et la conformité RGPD? Ce guide compare les trois.',
     fr_vps_body, fr_vps_faq, fr_vps_related, '/fr/blog/comparatif-vps-cloud-france-2026.html'),

    ('tr', 'tr_TR', 'TR', 'GPT API Türkçe Token Maliyet Hesaplama 2026',
     'GPT-4o API Türkiye Maliyet: Token Fiyatlandırması 2026',
     'GPT-4o Türkiye fiyatı ~95 ₺/M token. LLM maliyet hesapla, Llama 3.1 alternatifini öğren, Türkiye\'de API seç.',
     'OpenAI API Türkiye\'de pahalı görünüyor, ama alternatifler var. Llama 3.1 ücretsiz, Gemini çok uygun — bu rehber Türkçe chatbot ve AI uygulaması için en ucuz seçeneği gösterir.',
     tr_llm_body, tr_llm_faq, tr_llm_related, '/tr/blog/gpt-api-turkce-maliyet-2026.html'),

    ('tr', 'tr_TR', 'TR', 'Stripe Türkiye Komisyon 2026: SaaS için Ödeme Sistemi Seçimi',
     'Stripe Türkiye Komisyon ve Alternatifler: Iyzico vs 2Checkout vs Stripe',
     'Stripe Türkiye desteklemez. Alternatif: Iyzico %2,49, 2Checkout %3,5. Hangisini seç? Rehber.',
     'Stripe resmen Türkiye\'ye para göndermez — ancak alternatifler var. Iyzico, 2Checkout, Paystack karşılaştırması, komisyonlar, para çekme hızı. Hangi ödeme sistemini seç?',
     tr_stripe_body, tr_stripe_faq, tr_stripe_related, '/tr/blog/stripe-turkiye-komisyon-2026.html'),
]

for lang, locale, region, title, h1, desc, intro, body, faq, related, path in posts:
    output_html = blog_post(lang, locale, region, title, h1, desc, intro, body, faq, related, path)
    filepath = os.path.join(BASE, path.lstrip('/'))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output_html)
    print(f'✓ {path}')

print('\nSection 7 done. 6 geo blog posts created.')
