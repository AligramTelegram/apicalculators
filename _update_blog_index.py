#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update all 4 blog index files with all posts."""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\muham\Desktop\APICalculators'

# ── All blog posts per language ────────────────────────────────────────────────
# format: (slug, icon, tag1, tag2, title, desc, date, readtime)
POSTS = {
    'en': [
        ('llm-api-cost-guide-2026.html', '🔤', 'LLM', 'GUIDE',
         'How to Estimate Your LLM API Costs in 2026 — GPT-4o, Claude & Gemini Compared',
         'A complete breakdown of token pricing across every major provider. Input vs output token splits, context windows, and batching decisions explained with real examples.',
         'June 2, 2026', '12 min read', 'llm guide', True),
        ('reduce-llm-api-costs-2026.html', '⚡', 'LLM', 'OPTIMIZATION',
         'How to Reduce Your LLM API Costs by 60%: 7 Proven Strategies',
         'Prompt caching, model routing, Batch API, context truncation — battle-tested strategies with real dollar savings examples.',
         'June 2, 2026', '13 min read', 'llm guide', False),
        ('vector-database-cost-comparison-2026.html', '🧊', 'VECTOR DB', 'COMPARISON',
         'Pinecone vs Supabase vs Qdrant vs Weaviate: Vector DB Cost 2026',
         'Exact costs at 1M, 10M, and 100M vectors. Find the cheapest vector database for your production workload.',
         'June 2, 2026', '10 min read', 'vector guide', False),
        ('stripe-vs-paddle-fees-2026.html', '💳', 'PAYMENT', 'SAAS',
         'Stripe vs Paddle vs Lemon Squeezy: True SaaS Cost 2026',
         'The true cost including VAT handling, chargebacks, and hidden fees at $5K, $25K, and $100K MRR.',
         'June 2, 2026', '11 min read', 'payment guide', False),
        ('dalle3-vs-stable-diffusion-cost-2026.html', '🎨', 'IMAGE GEN', 'COMPARISON',
         'DALL·E 3 vs Stable Diffusion vs Flux: Cost & Quality 2026',
         'At 100K images/month the cost gap is $3,500+. Find out exactly where each model wins and when switching pays off.',
         'June 2, 2026', '9 min read', 'image guide', False),
        ('lemon-squeezy-vs-stripe-2026.html', '🍋', 'PAYMENT', 'GUIDE',
         'Lemon Squeezy vs Stripe: Full Cost Comparison for SaaS 2026',
         'Merchant of Record vs payment processor: tax handling, fees, and the real break-even point for indie devs.',
         'June 3, 2026', '9 min read', 'payment guide', False),
        ('midjourney-vs-dalle-cost-2026.html', '🖼️', 'IMAGE GEN', 'COMPARISON',
         'Midjourney vs DALL·E 3: Cost & Quality Comparison 2026',
         'Subscription vs pay-per-use. Which wins for your workflow? Real cost breakdown at different volume tiers.',
         'June 3, 2026', '8 min read', 'image guide', False),
        ('pinecone-pricing-guide-2026.html', '📌', 'VECTOR DB', 'GUIDE',
         'Pinecone Pricing Guide 2026: Serverless vs Pod-Based Costs',
         'Full breakdown of Pinecone serverless vs pod-based pricing. Exact costs at every scale with comparison to Qdrant and Weaviate.',
         'June 3, 2026', '10 min read', 'vector guide', False),
        ('cloud-vps-cost-comparison-2026.html', '☁️', 'CLOUD VPS', 'COMPARISON',
         'Vultr vs Hetzner vs DigitalOcean vs Linode: VPS Cost 2026',
         'Full price breakdown at every tier. Find the cheapest cloud VPS for your CPU/RAM/storage needs.',
         'June 4, 2026', '11 min read', 'cloud guide', False),
        ('aws-lambda-cost-calculator-2026.html', '⚡', 'SERVERLESS', 'GUIDE',
         'AWS Lambda vs Vercel Functions vs Cloudflare Workers: Cost 2026',
         'Invocation costs, memory pricing, free tiers — full breakdown at 1M, 10M, and 100M invocations.',
         'June 4, 2026', '10 min read', 'serverless guide', False),
        ('embedding-api-cost-2026.html', '🔢', 'EMBEDDINGS', 'COMPARISON',
         'OpenAI vs Cohere vs Voyage AI: Embedding API Cost 2026',
         'Cost per 1M tokens, latency, and quality trade-offs across all major embedding providers.',
         'June 4, 2026', '9 min read', 'embedding guide', False),
        ('stt-tts-api-cost-2026.html', '🎙️', 'STT / TTS', 'COMPARISON',
         'Whisper vs ElevenLabs vs Google Speech: STT & TTS API Cost 2026',
         'Cost per minute for STT, per 1000 characters for TTS. Full breakdown with real-world usage estimates.',
         'June 4, 2026', '10 min read', 'stt guide', False),
        ('api-gateway-pricing-2026.html', '🔀', 'API GATEWAY', 'GUIDE',
         'AWS API Gateway vs Cloudflare vs Kong: Cost 2026',
         'Per-million request costs, data transfer fees, and the break-even points at every traffic scale.',
         'June 4, 2026', '9 min read', 'gateway guide', False),
        ('ai-agent-cost-calculator-2026.html', '🤖', 'AI AGENT', 'GUIDE',
         'AI Agent Pipeline Cost Calculator 2026: GPT-4o, Claude & Gemini',
         'How multi-step reasoning, tool calls, and memory compound your real agent spend. Worked examples.',
         'June 4, 2026', '11 min read', 'agent guide', False),
    ],
    'de': [
        ('llm-kosten-leitfaden-2026.html', '🔤', 'LLM', 'LEITFADEN',
         'LLM API-Kosten 2026 schätzen — GPT-4o, Claude & Gemini im Vergleich',
         'Vollständige Aufschlüsselung der Token-Preise aller großen Anbieter. Input vs. Output-Tokens, Kontextfenster und Batching verständlich erklärt.',
         '2. Juni 2026', '12 Min.', 'llm guide', True),
        ('llm-kosten-senken-2026.html', '⚡', 'LLM', 'OPTIMIERUNG',
         'LLM API-Kosten um 60% senken: 7 bewährte Strategien',
         'Prompt-Caching, Modell-Routing, Batch-API, Kontext-Kürzung — praxiserprobte Strategien mit echten Einsparungsbeispielen.',
         '2. Juni 2026', '13 Min.', 'llm guide', False),
        ('vektordatenbank-kosten-vergleich-2026.html', '🧊', 'VECTOR DB', 'VERGLEICH',
         'Pinecone vs Supabase vs Qdrant vs Weaviate: Vector-DB-Kosten 2026',
         'Exakte Kosten bei 1M, 10M und 100M Vektoren. Finden Sie die günstigste Vektordatenbank für Ihre Produktion.',
         '2. Juni 2026', '10 Min.', 'vector guide', False),
        ('stripe-vs-paddle-gebuehren-2026.html', '💳', 'ZAHLUNG', 'SAAS',
         'Stripe vs Paddle vs Lemon Squeezy: Wahre SaaS-Kosten 2026',
         'Die echten Kosten inklusive MwSt-Abwicklung, Chargebacks und versteckten Gebühren bei 5K, 25K und 100K € MRR.',
         '2. Juni 2026', '11 Min.', 'payment guide', False),
        ('dalle-vs-stable-diffusion-kosten-2026.html', '🎨', 'BILDGENERIERUNG', 'VERGLEICH',
         'DALL·E 3 vs Stable Diffusion vs Flux: Kosten & Qualität 2026',
         'Bei 100K Bildern/Monat beträgt die Kostendifferenz über $3.500. Wo jedes Modell gewinnt.',
         '2. Juni 2026', '9 Min.', 'image guide', False),
        ('lemon-squeezy-vs-stripe-2026.html', '🍋', 'ZAHLUNG', 'LEITFADEN',
         'Lemon Squeezy vs Stripe: Vollständiger Kostenvergleich für SaaS 2026',
         'Merchant of Record vs Zahlungsabwickler: Steuerabwicklung, Gebühren und der Break-even-Punkt für Indie-Entwickler.',
         '3. Juni 2026', '9 Min.', 'payment guide', False),
        ('cloud-vps-kostenvergleich-2026.html', '☁️', 'CLOUD VPS', 'VERGLEICH',
         'Vultr vs Hetzner vs DigitalOcean vs Linode: VPS-Kosten 2026',
         'Vollständige Preisaufschlüsselung auf jeder Stufe. Finden Sie den günstigsten Cloud-VPS für Ihre CPU/RAM-Anforderungen.',
         '4. Juni 2026', '11 Min.', 'cloud guide', False),
        ('aws-lambda-kosten-guide-2026.html', '⚡', 'SERVERLESS', 'LEITFADEN',
         'AWS Lambda vs Vercel Functions vs Cloudflare Workers: Kosten 2026',
         'Aufrufkosten, Speicherpreise, kostenlose Kontingente — vollständige Aufschlüsselung bei 1M, 10M und 100M Aufrufen.',
         '4. Juni 2026', '10 Min.', 'serverless guide', False),
        ('embedding-api-kosten-2026.html', '🔢', 'EMBEDDINGS', 'VERGLEICH',
         'OpenAI vs Cohere vs Voyage AI: Embedding API-Kosten 2026',
         'Kosten pro 1M Token, Latenz und Qualitäts-Trade-offs aller wichtigen Embedding-Anbieter.',
         '4. Juni 2026', '9 Min.', 'embedding guide', False),
        ('stt-tts-api-kosten-2026.html', '🎙️', 'STT / TTS', 'VERGLEICH',
         'Whisper vs ElevenLabs vs Google Speech: STT & TTS API-Kosten 2026',
         'Kosten pro Minute für STT, pro 1000 Zeichen für TTS. Vollständige Aufschlüsselung mit realen Nutzungsschätzungen.',
         '4. Juni 2026', '10 Min.', 'stt guide', False),
        ('api-gateway-preise-2026.html', '🔀', 'API GATEWAY', 'LEITFADEN',
         'AWS API Gateway vs Cloudflare vs Kong: Kosten 2026',
         'Kosten pro Million Anfragen, Datentransfergebühren und Break-even-Punkte bei jeder Traffic-Größe.',
         '4. Juni 2026', '9 Min.', 'gateway guide', False),
        ('ki-agent-kosten-2026.html', '🤖', 'KI-AGENT', 'LEITFADEN',
         'KI-Agent Pipeline-Kosten 2026: GPT-4o, Claude & Gemini',
         'Wie mehrstufiges Reasoning, Tool-Aufrufe und Speicher Ihre echten Agentenkosten erhöhen. Praktische Beispiele.',
         '4. Juni 2026', '11 Min.', 'agent guide', False),
    ],
    'fr': [
        ('guide-couts-llm-2026.html', '🔤', 'LLM', 'GUIDE',
         'Estimer les coûts API LLM en 2026 — GPT-4o, Claude & Gemini comparés',
         'Décomposition complète des prix par token pour tous les grands fournisseurs. Tokens entrée/sortie, fenêtres contextuelles et batching expliqués.',
         '2 juin 2026', '12 min', 'llm guide', True),
        ('reduire-couts-llm-2026.html', '⚡', 'LLM', 'OPTIMISATION',
         'Réduire les coûts API LLM de 60% : 7 stratégies éprouvées',
         'Cache de prompts, routage de modèles, Batch API, troncature — stratégies éprouvées avec exemples d\'économies réelles.',
         '2 juin 2026', '13 min', 'llm guide', False),
        ('comparaison-couts-base-vectorielle-2026.html', '🧊', 'VECTOR DB', 'COMPARAISON',
         'Pinecone vs Supabase vs Qdrant vs Weaviate : Coûts Vector DB 2026',
         'Coûts exacts à 1M, 10M et 100M vecteurs. Trouvez la base vectorielle la moins chère pour votre charge de production.',
         '2 juin 2026', '10 min', 'vector guide', False),
        ('stripe-vs-paddle-frais-2026.html', '💳', 'PAIEMENT', 'SAAS',
         'Stripe vs Paddle vs Lemon Squeezy : Coût SaaS réel 2026',
         'Le coût réel incluant la gestion TVA, les chargebacks et les frais cachés à 5K, 25K et 100K € MRR.',
         '2 juin 2026', '11 min', 'payment guide', False),
        ('dalle-vs-stable-diffusion-cout-2026.html', '🎨', 'IMAGE GEN', 'COMPARAISON',
         'DALL·E 3 vs Stable Diffusion vs Flux : Coût & Qualité 2026',
         'À 100K images/mois, l\'écart de coût dépasse $3 500. Découvrez où chaque modèle gagne.',
         '2 juin 2026', '9 min', 'image guide', False),
        ('lemon-squeezy-vs-stripe-frais-2026.html', '🍋', 'PAIEMENT', 'GUIDE',
         'Lemon Squeezy vs Stripe : Comparaison complète pour SaaS 2026',
         'Marchand délégué vs processeur : TVA, frais et point d\'équilibre pour développeurs indépendants.',
         '3 juin 2026', '9 min', 'payment guide', False),
        ('cloud-vps-comparaison-prix-2026.html', '☁️', 'CLOUD VPS', 'COMPARAISON',
         'Vultr vs Hetzner vs DigitalOcean vs Linode : Coût VPS 2026',
         'Décomposition complète à chaque niveau. Trouvez le VPS cloud le moins cher selon CPU/RAM.',
         '4 juin 2026', '11 min', 'cloud guide', False),
        ('cout-serverless-aws-lambda-2026.html', '⚡', 'SERVERLESS', 'GUIDE',
         'AWS Lambda vs Vercel Functions vs Cloudflare Workers : Coût 2026',
         'Coûts d\'invocation, prix mémoire, niveaux gratuits — décomposition complète à 1M, 10M et 100M invocations.',
         '4 juin 2026', '10 min', 'serverless guide', False),
        ('cout-api-embedding-2026.html', '🔢', 'EMBEDDINGS', 'COMPARAISON',
         'OpenAI vs Cohere vs Voyage AI : Coût API Embedding 2026',
         'Coût par 1M tokens, latence et compromis qualité pour tous les grands fournisseurs d\'embeddings.',
         '4 juin 2026', '9 min', 'embedding guide', False),
        ('cout-api-stt-tts-2026.html', '🎙️', 'STT / TTS', 'COMPARAISON',
         'Whisper vs ElevenLabs vs Google Speech : Coût API STT & TTS 2026',
         'Coût par minute pour STT, par 1000 caractères pour TTS. Décomposition complète avec estimations réelles.',
         '4 juin 2026', '10 min', 'stt guide', False),
        ('prix-api-gateway-2026.html', '🔀', 'API GATEWAY', 'GUIDE',
         'AWS API Gateway vs Cloudflare vs Kong : Coût 2026',
         'Coûts par million de requêtes, frais de transfert et points d\'équilibre à chaque échelle de trafic.',
         '4 juin 2026', '9 min', 'gateway guide', False),
        ('cout-agent-ia-2026.html', '🤖', 'AGENT IA', 'GUIDE',
         'Calculateur de coûts Agent IA 2026 : GPT-4o, Claude & Gemini',
         'Comment le raisonnement multi-étapes, les appels d\'outils et la mémoire augmentent votre dépense réelle.',
         '4 juin 2026', '11 min', 'agent guide', False),
    ],
    'tr': [
        ('llm-maliyet-rehberi-2026.html', '🔤', 'LLM', 'REHBER',
         'LLM API Maliyetlerini 2026\'da Tahmin Etme — GPT-4o, Claude & Gemini Karşılaştırması',
         'Tüm büyük sağlayıcıların token fiyatlandırmasının tam dökümü. Girdi/çıktı token oranları, bağlam pencereleri açıklandı.',
         '2 Haziran 2026', '12 dk', 'llm guide', True),
        ('llm-maliyet-dusurme-2026.html', '⚡', 'LLM', 'OPTİMİZASYON',
         'LLM API Maliyetlerinizi %60 Düşürün: 7 Kanıtlanmış Strateji',
         'İstem önbellekleme, model yönlendirme, Batch API, bağlam kısaltma — gerçek tasarruf örnekleriyle savaşta test edilmiş stratejiler.',
         '2 Haziran 2026', '13 dk', 'llm guide', False),
        ('vektor-veritabani-maliyet-karsilastirmasi-2026.html', '🧊', 'VECTOR DB', 'KARŞILAŞTIRMA',
         'Pinecone vs Supabase vs Qdrant vs Weaviate: Vektör DB Maliyeti 2026',
         '1M, 10M ve 100M vektörde tam maliyetler. Üretim iş yükünüz için en ucuz vektör veritabanını bulun.',
         '2 Haziran 2026', '10 dk', 'vector guide', False),
        ('stripe-vs-paddle-ucretleri-2026.html', '💳', 'ÖDEME', 'SAAS',
         'Stripe vs Paddle vs Lemon Squeezy: Gerçek SaaS Maliyeti 2026',
         'KDV işleme, chargeback ve gizli ücretler dahil gerçek maliyet. 5K, 25K ve 100K$ MRR\'da kırılım noktası.',
         '2 Haziran 2026', '11 dk', 'payment guide', False),
        ('dalle-vs-stable-diffusion-maliyet-2026.html', '🎨', 'GÖRSEL ÜRETİM', 'KARŞILAŞTIRMA',
         'DALL·E 3 vs Stable Diffusion vs Flux: Maliyet & Kalite 2026',
         'Ayda 100K görüntüde maliyet farkı $3.500+. Her modelin nerede kazandığını öğrenin.',
         '2 Haziran 2026', '9 dk', 'image guide', False),
        ('lemon-squeezy-vs-stripe-karsilastirma-2026.html', '🍋', 'ÖDEME', 'REHBER',
         'Lemon Squeezy vs Stripe: SaaS için Tam Maliyet Karşılaştırması 2026',
         'Ticaret temsilcisi vs ödeme işlemcisi: vergi yönetimi, ücretler ve indie geliştiriciler için başabaş noktası.',
         '3 Haziran 2026', '9 dk', 'payment guide', False),
        ('bulut-vps-maliyet-karsilastirma-2026.html', '☁️', 'CLOUD VPS', 'KARŞILAŞTIRMA',
         'Vultr vs Hetzner vs DigitalOcean vs Linode: VPS Maliyeti 2026',
         'Her seviyede tam fiyat dökümü. CPU/RAM gereksinimleriniz için en ucuz bulut VPS\'i bulun.',
         '4 Haziran 2026', '11 dk', 'cloud guide', False),
        ('aws-lambda-maliyet-2026.html', '⚡', 'SUNUCUSUZ', 'REHBER',
         'AWS Lambda vs Vercel Functions vs Cloudflare Workers: Maliyet 2026',
         'Çağrı maliyetleri, bellek fiyatlandırması, ücretsiz katmanlar — 1M, 10M ve 100M çağrıda tam döküm.',
         '4 Haziran 2026', '10 dk', 'serverless guide', False),
        ('embedding-api-maliyet-2026.html', '🔢', 'EMBEDDİNG', 'KARŞILAŞTIRMA',
         'OpenAI vs Cohere vs Voyage AI: Embedding API Maliyeti 2026',
         '1M token başına maliyet, gecikme ve tüm büyük embedding sağlayıcılarının kalite takası.',
         '4 Haziran 2026', '9 dk', 'embedding guide', False),
        ('stt-tts-api-maliyet-2026.html', '🎙️', 'STT / TTS', 'KARŞILAŞTIRMA',
         'Whisper vs ElevenLabs vs Google Speech: STT & TTS API Maliyeti 2026',
         'STT için dakika başına, TTS için 1000 karakter başına maliyet. Gerçek kullanım tahminleriyle tam döküm.',
         '4 Haziran 2026', '10 dk', 'stt guide', False),
        ('api-gateway-fiyat-2026.html', '🔀', 'API GATEWAY', 'REHBER',
         'AWS API Gateway vs Cloudflare vs Kong: Maliyet 2026',
         'Milyon istek başına maliyetler, veri aktarım ücretleri ve her trafik ölçeğinde başabaş noktaları.',
         '4 Haziran 2026', '9 dk', 'gateway guide', False),
        ('yapay-zeka-ajan-maliyet-2026.html', '🤖', 'YZ AJAN', 'REHBER',
         'YZ Ajan Pipeline Maliyet Hesaplayıcısı 2026: GPT-4o, Claude & Gemini',
         'Çok adımlı akıl yürütme, araç çağrıları ve belleğin gerçek ajan harcamanızı nasıl artırdığı.',
         '4 Haziran 2026', '11 dk', 'agent guide', False),
    ],
}

# ── Blog index HTML template ───────────────────────────────────────────────────
LANG_STRINGS = {
    'en': {
        'title': 'Blog — Infra Cost Guides for Developers | APICalculators',
        'desc': 'Practical breakdowns on LLM pricing, vector DB costs, image generation, and payment processor fees — with direct links to the calculators.',
        'canon': 'https://apicalculators.com/blog/',
        'hero_tag': 'Updated June 2026',
        'hero_title': 'Infra cost guides for developers',
        'hero_sub': 'Practical breakdowns on LLM pricing, vector DB costs, image generation, and payment processor fees — with direct links to the calculators.',
        'all': 'All posts', 'read': 'Read →',
        'calc_link': '/', 'calc_label': 'Calculators',
        'nav_blog': '/blog/', 'nav_about': '/about.html',
        'lang_prefix': '/blog/',
        'alt_links': [
            ('en', 'https://apicalculators.com/blog/'),
            ('de', 'https://apicalculators.com/de/blog/'),
            ('fr', 'https://apicalculators.com/fr/blog/'),
            ('tr', 'https://apicalculators.com/tr/blog/'),
        ],
        'filter_labels': ['All posts', 'LLM / Tokens', 'Vector DB', 'Image Gen', 'Payment', 'Guides'],
        'filter_tags': ['all', 'llm', 'vector', 'image', 'payment', 'guide'],
        'about': '/about.html', 'about_label': 'About',
    },
    'de': {
        'title': 'Blog — KI- & API-Kostenratgeber | APICalculators',
        'desc': 'Ausführliche Ratgeber zu LLM-Preisen, Vektordatenbank-Kosten, KI-Bildgenerierungs-Budgets und SaaS-Zahlungsgebühren.',
        'canon': 'https://apicalculators.com/de/blog/',
        'hero_tag': 'Aktualisiert Juni 2026',
        'hero_title': 'Infra-Kostenratgeber für Entwickler',
        'hero_sub': 'Praxisnahe Analysen zu LLM-Preisen, Vektordatenbank-Kosten, Bildgenerierung und Zahlungsgebühren — mit direkten Links zu den Rechnern.',
        'all': 'Alle Beiträge', 'read': 'Lesen →',
        'calc_link': '/de/', 'calc_label': 'Rechner',
        'nav_blog': '/de/blog/', 'nav_about': '/de/about.html',
        'lang_prefix': '/de/blog/',
        'alt_links': [
            ('en', 'https://apicalculators.com/blog/'),
            ('de', 'https://apicalculators.com/de/blog/'),
            ('fr', 'https://apicalculators.com/fr/blog/'),
            ('tr', 'https://apicalculators.com/tr/blog/'),
        ],
        'filter_labels': ['Alle', 'LLM / Token', 'Vector DB', 'Bildgen', 'Zahlung', 'Leitfäden'],
        'filter_tags': ['all', 'llm', 'vector', 'image', 'payment', 'guide'],
        'about': '/de/about.html', 'about_label': 'Über uns',
    },
    'fr': {
        'title': 'Blog — Guides de coûts infra pour développeurs | APICalculators',
        'desc': 'Analyses pratiques sur les prix LLM, les coûts des bases vectorielles, la génération d\'images et les frais de paiement.',
        'canon': 'https://apicalculators.com/fr/blog/',
        'hero_tag': 'Mis à jour juin 2026',
        'hero_title': 'Guides de coûts infra pour développeurs',
        'hero_sub': "Analyses pratiques sur les prix LLM, les coûts des bases vectorielles, la génération d'images et les frais de paiement — avec liens directs vers les calculateurs.",
        'all': 'Tous les articles', 'read': 'Lire →',
        'calc_link': '/fr/', 'calc_label': 'Calculateurs',
        'nav_blog': '/fr/blog/', 'nav_about': '/fr/about.html',
        'lang_prefix': '/fr/blog/',
        'alt_links': [
            ('en', 'https://apicalculators.com/blog/'),
            ('de', 'https://apicalculators.com/de/blog/'),
            ('fr', 'https://apicalculators.com/fr/blog/'),
            ('tr', 'https://apicalculators.com/tr/blog/'),
        ],
        'filter_labels': ['Tous', 'LLM / Tokens', 'Vector DB', 'Image Gen', 'Paiement', 'Guides'],
        'filter_tags': ['all', 'llm', 'vector', 'image', 'payment', 'guide'],
        'about': '/fr/about.html', 'about_label': 'À propos',
    },
    'tr': {
        'title': 'Blog — Geliştiriciler için Altyapı Maliyet Rehberleri | APICalculators',
        'desc': 'LLM fiyatlandırması, vektör DB maliyetleri, görsel üretim ve ödeme işlemcisi ücretlerine dair pratik analizler.',
        'canon': 'https://apicalculators.com/tr/blog/',
        'hero_tag': 'Haziran 2026\'da güncellendi',
        'hero_title': 'Geliştiriciler için altyapı maliyet rehberleri',
        'hero_sub': 'LLM fiyatlandırması, vektör DB maliyetleri, görsel üretim ve ödeme işlemcisi ücretlerine dair pratik analizler — hesaplayıcılara doğrudan bağlantılarla.',
        'all': 'Tüm yazılar', 'read': 'Oku →',
        'calc_link': '/tr/', 'calc_label': 'Hesaplayıcılar',
        'nav_blog': '/tr/blog/', 'nav_about': '/tr/about.html',
        'lang_prefix': '/tr/blog/',
        'alt_links': [
            ('en', 'https://apicalculators.com/blog/'),
            ('de', 'https://apicalculators.com/de/blog/'),
            ('fr', 'https://apicalculators.com/fr/blog/'),
            ('tr', 'https://apicalculators.com/tr/blog/'),
        ],
        'filter_labels': ['Tümü', 'LLM / Token', 'Vector DB', 'Görsel Üretim', 'Ödeme', 'Rehberler'],
        'filter_tags': ['all', 'llm', 'vector', 'image', 'payment', 'guide'],
        'about': '/tr/about.html', 'about_label': 'Hakkımızda',
    },
}

def make_card(post, s, is_featured=False):
    slug, icon, tag1, tag2, title, desc, date, readtime, tags, _ = post
    prefix = s['lang_prefix']
    cls = 'post-card featured' if is_featured else 'post-card'
    return f'''    <a href="{prefix}{slug}" class="{cls}" data-tags="{tags}">
      <div class="card-tags"><span class="tag t-{tags.split()[0]}">{icon} {tag1}</span><span class="tag">{tag2}</span></div>
      <h2 class="card-title">{title}</h2>
      <p class="card-desc">{desc}</p>
      <div class="card-meta"><span>{date} · {readtime}</span><span class="read-link">{s['read']}</span></div>
    </a>'''

def make_index(lang, s, posts):
    hreflangs = '\n'.join(f'<link rel="alternate" hreflang="{hl}" href="{url}">' for hl, url in s['alt_links'])
    filters = ''.join(
        f'<button class="filter-btn{" on" if t=="all" else ""}" data-filter="{t}">{l}</button>'
        for l, t in zip(s['filter_labels'], s['filter_tags'])
    )
    cards = '\n'.join(make_card(p, s, p[9]) for p in posts)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{s['title']}</title>
<meta name="description" content="{s['desc']}">
<link rel="canonical" href="{s['canon']}">
<meta name="robots" content="index, follow">
{hreflangs}
<meta property="og:title" content="{s['title']}">
<meta property="og:description" content="{s['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{s['canon']}">
<style>
:root{{--bg:#0a0c10;--bg2:#0c0f15;--surface:#12161d;--surface2:#161b24;--border:#1d2530;--border2:#27313e;--text:#e8edf1;--muted:#8b97a4;--lime:#b8ff2e;--cyan:#4dd6ff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;line-height:1.65}}
a{{color:inherit;text-decoration:none}}.wrap{{max-width:1100px;margin:0 auto;padding:0 22px}}
header.nav{{position:sticky;top:0;z-index:50;backdrop-filter:blur(14px);background:rgba(10,12,16,.72);border-bottom:1px solid var(--border)}}
.nav-in{{display:flex;align-items:center;justify-content:space-between;height:60px}}
.logo{{font-family:'Arial Black',system-ui,sans-serif;font-weight:900;font-size:18px}}.logo b{{color:var(--lime)}}
.nav-r{{display:flex;gap:22px}}.nav-r a{{color:var(--muted);font-size:14px;font-weight:500}}.nav-r a.on{{color:var(--lime)}}
.blog-hero{{padding:60px 0 40px;border-bottom:1px solid var(--border)}}
.hero-tag{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;color:var(--lime);text-transform:uppercase;margin-bottom:16px}}
.blog-hero h1{{font-size:clamp(28px,5vw,48px);font-weight:800;line-height:1.15;margin-bottom:14px;max-width:700px}}
.blog-hero p{{color:var(--muted);font-size:16px;max-width:620px}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;padding:28px 0 0}}
.filter-btn{{padding:7px 16px;border-radius:20px;border:1px solid var(--border2);background:transparent;color:var(--muted);font-size:13px;font-weight:600;cursor:pointer;transition:all .15s}}
.filter-btn.on,.filter-btn:hover{{background:var(--surface2);color:var(--text);border-color:var(--border2)}}
.filter-btn.on{{color:var(--lime)}}
.posts-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;padding:40px 0 80px}}
.post-card{{display:flex;flex-direction:column;gap:12px;padding:24px;border-radius:14px;border:1px solid var(--border);background:var(--surface);transition:border-color .18s,background .18s}}
.post-card:hover{{border-color:var(--border2);background:var(--surface2)}}
.post-card.featured{{border-color:rgba(184,255,46,.3);grid-column:span 2}}
@media(max-width:680px){{.post-card.featured{{grid-column:span 1}}}}
.card-tags{{display:flex;gap:8px;flex-wrap:wrap}}
.tag{{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:.06em;border:1px solid var(--border2);color:var(--muted);text-transform:uppercase}}
.t-llm{{border-color:rgba(184,255,46,.3);color:var(--lime)}}
.t-vector{{border-color:rgba(77,214,255,.3);color:var(--cyan)}}
.t-image{{border-color:rgba(255,180,50,.3);color:#ffb432}}
.t-payment{{border-color:rgba(120,200,120,.3);color:#78c878}}
.t-cloud{{border-color:rgba(100,180,255,.3);color:#64b4ff}}
.t-serverless{{border-color:rgba(255,150,50,.3);color:#ff9632}}
.t-embedding{{border-color:rgba(200,100,255,.3);color:#c864ff}}
.t-agent{{border-color:rgba(255,100,150,.3);color:#ff6496}}
.t-stt{{border-color:rgba(100,220,200,.3);color:#64dcc8}}
.t-gateway{{border-color:rgba(220,180,100,.3);color:#dcb464}}
.card-title{{font-size:17px;font-weight:700;line-height:1.35;color:var(--text)}}
.card-desc{{font-size:14px;color:var(--muted);line-height:1.6;flex:1}}
.card-meta{{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--muted);margin-top:auto;padding-top:8px;border-top:1px solid var(--border)}}
.read-link{{color:var(--lime);font-weight:700}}
footer{{border-top:1px solid var(--border);padding:32px 0;text-align:center;color:var(--muted);font-size:13px}}
footer a{{color:var(--muted)}}.post-card.hidden{{display:none}}
</style>
</head>
<body>
<header class="nav"><div class="nav-in wrap">
  <a href="{s['calc_link']}" class="logo">&#127381; API <b>Calculators</b></a>
  <nav class="nav-r">
    <a href="{s['calc_link']}">{s['calc_label']}</a>
    <a href="{s['nav_blog']}" class="on">Blog</a>
    <a href="{s['about']}">{s['about_label']}</a>
  </nav>
</div></header>
<div class="wrap">
  <div class="blog-hero">
    <span class="hero-tag">{s['hero_tag']}</span>
    <h1>{s['hero_title']}</h1>
    <p>{s['hero_sub']}</p>
    <div class="filters">{filters}</div>
  </div>
  <div class="posts-grid" id="postsGrid">
{cards}
  </div>
</div>
<footer><div class="wrap"><p>&copy; 2026 <a href="{s['calc_link']}">APICalculators.com</a></p></div></footer>
<script>
document.querySelectorAll('.filter-btn').forEach(btn=>{{
  btn.addEventListener('click',()=>{{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('on'));
    btn.classList.add('on');
    const f=btn.dataset.filter;
    document.querySelectorAll('.post-card').forEach(c=>{{
      c.classList.toggle('hidden', f!=='all' && !c.dataset.tags.includes(f));
    }});
  }});
}});
</script>
</body>
</html>'''

# ── Write files ────────────────────────────────────────────────────────────────
PATHS = {
    'en': os.path.join(BASE, 'blog', 'index.html'),
    'de': os.path.join(BASE, 'de', 'blog', 'index.html'),
    'fr': os.path.join(BASE, 'fr', 'blog', 'index.html'),
    'tr': os.path.join(BASE, 'tr', 'blog', 'index.html'),
}

for lang, path in PATHS.items():
    s = LANG_STRINGS[lang]
    posts = POSTS[lang]
    html = make_index(lang, s, posts)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{lang}: {len(posts)} posts written → {path}')

print('All blog indexes updated.')
