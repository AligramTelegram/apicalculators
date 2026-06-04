#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Section 2: Add missing Article, FAQ, Breadcrumb schemas + SoftwareApplication to homepage."""
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── Per-file metadata ──────────────────────────────────────────────────────────
# lang -> filename -> (headline, datePublished, dateModified)
META = {
    'en': {
        'midjourney-vs-dalle-cost-2026': (
            'Midjourney vs DALL·E 3 Cost Comparison 2026',
            '2026-06-02', '2026-06-04'
        ),
        'pinecone-pricing-guide-2026': (
            'Pinecone Pricing Guide 2026: Real Costs at Scale',
            '2026-06-02', '2026-06-04'
        ),
    },
    'de': {},
    'fr': {
        'midjourney-vs-dalle-cout-2026': (
            'Midjourney vs DALL·E 3 : Comparaison des coûts 2026',
            '2026-06-02', '2026-06-04'
        ),
        'pinecone-guide-tarifs-2026': (
            'Guide des tarifs Pinecone 2026 : coûts réels à grande échelle',
            '2026-06-02', '2026-06-04'
        ),
    },
    'tr': {
        'midjourney-vs-dalle-maliyet-2026': (
            'Midjourney vs DALL·E 3 Maliyet Karşılaştırması 2026',
            '2026-06-02', '2026-06-04'
        ),
        'pinecone-fiyat-rehberi-2026': (
            'Pinecone Fiyat Rehberi 2026: Gerçek Maliyetler',
            '2026-06-02', '2026-06-04'
        ),
        'stripe-vs-paddle-ucretleri-2026': (
            'Stripe vs Paddle Ücretleri 2026: SaaS için Hangisi Daha Ucuz?',
            '2026-06-02', '2026-06-04'
        ),
    },
}

# ── FAQ data per post ──────────────────────────────────────────────────────────
FAQ_DATA = {
    # EN
    'midjourney-vs-dalle-cost-2026': [
        ('Is Midjourney cheaper than DALL·E 3?',
         'Midjourney Basic ($10/mo) gives ~200 images/mo at $0.05 each. DALL·E 3 via API costs $0.04 per standard 1024×1024 image. For high volume, DALL·E 3 API wins; for casual use, Midjourney is simpler.'),
        ('What is the cheapest AI image generator in 2026?',
         'Stable Diffusion on a $6/mo Hetzner VPS is cheapest at scale (near $0/image after setup). For API-based, DALL·E 3 standard ($0.04) and Flux via Replicate (~$0.003) are lowest.'),
        ('Does Midjourney have an API?',
         'No official API as of 2026. Midjourney requires Discord interaction or unofficial third-party wrappers. For programmatic access, DALL·E 3 (OpenAI API) or Stable Diffusion (Replicate/self-host) are recommended.'),
    ],
    'pinecone-pricing-guide-2026': [
        ('How much does Pinecone cost for 1 million vectors?',
         'Approximately $10–30/month on the Starter or Standard plan depending on query volume. Storage runs ~$3, plus $16 per million read units. For 1M vectors with moderate traffic expect $15–25/mo.'),
        ('Is Pinecone free?',
         'Pinecone has a free Starter tier: 1 index, up to 100K vectors, shared infrastructure. For production workloads over 100K vectors or requiring dedicated resources, paid plans start at ~$70/mo.'),
        ('What is cheaper than Pinecone?',
         'Supabase pgvector at $25/mo (500K vectors included). Qdrant Cloud free tier up to 1GB. Self-hosted Qdrant on a $6/mo VPS. Weaviate Cloud has a free sandbox tier. All significantly cheaper than Pinecone Standard at scale.'),
    ],
    # FR
    'midjourney-vs-dalle-cout-2026': [
        ('Midjourney est-il moins cher que DALL·E 3 ?',
         'Midjourney Basic (10 $/mois) donne ~200 images/mois à 0,05 $ l\'unité. DALL·E 3 via API coûte 0,04 $ par image standard 1024×1024. Pour les gros volumes, l\'API DALL·E 3 est avantageuse ; pour un usage occasionnel, Midjourney est plus simple.'),
        ('Quel est le générateur d\'images IA le moins cher en 2026 ?',
         'Stable Diffusion sur un VPS Hetzner à 6 $/mois est le moins cher à grande échelle (quasi 0 $/image). Pour les API, DALL·E 3 standard (0,04 $) et Flux via Replicate (~0,003 $) sont les moins coûteux.'),
    ],
    'pinecone-guide-tarifs-2026': [
        ('Combien coûte Pinecone pour 1 million de vecteurs ?',
         'Environ 10 à 30 $/mois selon le volume de requêtes. Le stockage coûte ~3 $, plus 16 $ par million d\'unités de lecture. Pour 1M de vecteurs avec un trafic modéré, prévoyez 15 à 25 $/mois.'),
        ('Pinecone est-il gratuit ?',
         'Pinecone propose un niveau Starter gratuit : 1 index, jusqu\'à 100 K vecteurs, infrastructure partagée. Pour une production dépassant 100 K vecteurs, les plans payants commencent à ~70 $/mois.'),
        ('Quelle alternative est moins chère que Pinecone ?',
         'Supabase pgvector à 25 $/mois (500 K vecteurs inclus). Qdrant Cloud gratuit jusqu\'à 1 Go. Qdrant auto-hébergé sur un VPS à 6 $/mois. Toutes sont bien moins chères que Pinecone Standard à grande échelle.'),
    ],
    # TR
    'midjourney-vs-dalle-maliyet-2026': [
        ('Midjourney mi DALL·E 3 mü daha ucuz?',
         'Midjourney Basic (10 $/ay) ~200 görsel/ay verir, görsel başına 0,05 $. DALL·E 3 API ile 1024×1024 standart görsel 0,04 $. Yüksek hacimde DALL·E 3 API kazanır; sıradan kullanım için Midjourney daha pratiktir.'),
        ('2026\'da en ucuz yapay zeka görsel üretici hangisi?',
         'Hetzner\'de 6 $/aylık VPS üzerinde Stable Diffusion en ucuz seçenek (kurulum sonrası görsel başına neredeyse 0 $). API tabanlı için DALL·E 3 standart (0,04 $) ve Flux via Replicate (~0,003 $) en düşük maliyetlidir.'),
        ('Midjourney\'nin API\'si var mı?',
         '2026 itibarıyla resmi API yok. Discord üzerinden veya resmi olmayan üçüncü taraf sarmalayıcılarla kullanılıyor. Programatik erişim için DALL·E 3 (OpenAI API) veya Stable Diffusion (Replicate/kendi sunucu) önerilir.'),
    ],
    'pinecone-fiyat-rehberi-2026': [
        ('1 milyon vektör için Pinecone ne kadar tutar?',
         'Sorgu hacmine göre ayda yaklaşık 10–30 $. Depolama ~3 $, artı her milyon okuma birimi için 16 $. Orta trafikli 1M vektör için aylık 15–25 $ bekleyin.'),
        ('Pinecone ücretsiz mi?',
         'Pinecone\'un ücretsiz Starter katmanı var: 1 index, 100 bin vektöre kadar, paylaşımlı altyapı. 100K üzeri prodüksiyon için ücretli planlar ~70 $/aydan başlıyor.'),
        ('Pinecone\'dan ucuz alternatif nedir?',
         'Supabase pgvector 25 $/ay (500K vektör dahil). Qdrant Cloud 1 GB\'a kadar ücretsiz. 6 $/aylık VPS üzerinde kendi Qdrant kurulumu. Hepsi büyük ölçekte Pinecone Standard\'dan çok daha ucuz.'),
    ],
    'stripe-vs-paddle-ucretleri-2026': [
        ('Stripe Türkiye\'de kullanılabilir mi?',
         'Evet, Stripe Türkiye\'de hizmet vermektedir. Ancak TRY (Türk lirası) ödemeleri için yerel ödeme yöntemleri entegrasyonu ve kur farkı maliyetleri göz önünde bulundurulmalıdır.'),
        ('Stripe mi Paddle mi daha ucuz SaaS için?',
         'Ham ücret olarak Stripe daha ucuz (%2,9 vs %5). Ancak Stripe Tax, uluslararası kart ücretleri ve iade maliyetleri eklenince 12–18K $ aylık gelirin altında Paddle genellikle toplam olarak daha ucuzdur.'),
        ('Merchant of Record (MoR) nedir?',
         'MoR, ödemeyi işleyen ve tüm vergi yükümlülüklerini üstlenen yasal kuruluştur. Paddle ve Lemon Squeezy MoR\'dur — küresel KDV/satış vergisini onlar toplar. Stripe değildir.'),
    ],
}

# ── Breadcrumb builder ─────────────────────────────────────────────────────────
LANG_LABELS = {
    'en': ('Home', 'Blog'),
    'de': ('Startseite', 'Blog'),
    'fr': ('Accueil', 'Blog'),
    'tr': ('Ana Sayfa', 'Blog'),
}
LANG_PREFIXES = {'en': '', 'de': '/de', 'fr': '/fr', 'tr': '/tr'}

def breadcrumb_schema(lang, fname, headline):
    home_label, blog_label = LANG_LABELS[lang]
    prefix = LANG_PREFIXES[lang]
    domain = 'https://apicalculators.com'
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_label, "item": f"{domain}{prefix}/"},
            {"@type": "ListItem", "position": 2, "name": blog_label, "item": f"{domain}{prefix}/blog/"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": f"{domain}{prefix}/blog/{fname}.html"},
        ]
    }, ensure_ascii=False, indent=2)

def article_schema(headline, datePublished, dateModified):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "datePublished": datePublished,
        "dateModified": dateModified,
        "author": {"@type": "Organization", "name": "APICalculators"},
        "publisher": {
            "@type": "Organization",
            "name": "APICalculators",
            "url": "https://apicalculators.com"
        }
    }, ensure_ascii=False, indent=2)

def faq_schema(faqs):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            }
            for q, a in faqs
        ]
    }, ensure_ascii=False, indent=2)

def inject_schema(c, schema_json):
    tag = f'\n<script type="application/ld+json">\n{schema_json}\n</script>'
    # Insert before </head>
    return c.replace('</head>', tag + '\n</head>', 1)

# ── Process files ──────────────────────────────────────────────────────────────
changed = []

# ── 1. Blog posts missing Article/FAQ ─────────────────────────────────────────
for lang, posts in META.items():
    blog_dir = os.path.join(BASE, 'blog') if lang == 'en' else os.path.join(BASE, lang, 'blog')
    for slug, (headline, datePublished, dateModified) in posts.items():
        fname = slug + '.html'
        path = os.path.join(blog_dir, fname)
        if not os.path.exists(path):
            print(f'MISSING FILE: {path}')
            continue
        c = open(path, encoding='utf-8').read()
        orig = c

        has_article = '"@type":"Article"' in c or '"@type": "Article"' in c
        has_faq = 'FAQPage' in c
        has_breadcrumb = 'BreadcrumbList' in c

        if not has_article:
            c = inject_schema(c, article_schema(headline, datePublished, dateModified))
        if not has_faq and slug in FAQ_DATA:
            c = inject_schema(c, faq_schema(FAQ_DATA[slug]))
        if not has_breadcrumb:
            c = inject_schema(c, breadcrumb_schema(lang, slug, headline))

        if c != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            changed.append(f'/{lang}/blog/{fname}' if lang != 'en' else f'/blog/{fname}')
            print(f'  Fixed {lang}/{fname}: article={not has_article} faq={not has_faq} breadcrumb={not has_breadcrumb}')

# ── 2. Add missing Breadcrumb to posts that have Article/FAQ but no Breadcrumb ─
for lang in ['en', 'de', 'fr', 'tr']:
    blog_dir = os.path.join(BASE, 'blog') if lang == 'en' else os.path.join(BASE, lang, 'blog')
    files = sorted(f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html')
    for fname in files:
        path = os.path.join(blog_dir, fname)
        c = open(path, encoding='utf-8').read()
        if 'BreadcrumbList' in c:
            continue
        orig = c

        # Extract headline from existing Article schema or <title>
        m = re.search(r'"headline"\s*:\s*"([^"]+)"', c)
        if not m:
            m = re.search(r'<title>([^<|]+)', c)
        headline = m.group(1).strip() if m else fname.replace('-', ' ').replace('.html', '')

        slug = fname.replace('.html', '')
        c = inject_schema(c, breadcrumb_schema(lang, slug, headline))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        rel_path = f'/blog/{fname}' if lang == 'en' else f'/{lang}/blog/{fname}'
        if rel_path not in changed:
            changed.append(rel_path)
        print(f'  Breadcrumb added: {lang}/{fname}')

# ── 3. SoftwareApplication schema on homepage ──────────────────────────────────
home_path = os.path.join(BASE, 'index.html')
c = open(home_path, encoding='utf-8').read()
if 'SoftwareApplication' not in c:
    sa = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "APICalculators – AI Infrastructure Cost Tools",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "url": "https://apicalculators.com"
    }, ensure_ascii=False, indent=2)
    c = inject_schema(c, sa)
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(c)
    changed.append('/index.html')
    print('  SoftwareApplication added to homepage')
else:
    print('  Homepage already has SoftwareApplication')

print(f'\nTotal changed: {len(changed)} files')
for p in sorted(changed):
    print(f'  {p}')
