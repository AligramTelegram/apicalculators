// i18n.js — APICalculators.com central language controller
// 10 languages × 10 tools × 7 blog articles
// Usage: i18n.t('ui.calculate_btn') | i18n.formatCurrency(123.45) | i18n.set('de')

const _i18n = {
  en: {
    seo: {
      site_name: "APICalculators.com",
      home_title: "API & LLM Cost Calculator Hub | Developer Infrastructure Tools",
      home_desc: "Free real-time calculators for LLM tokens, cloud infrastructure, vector databases, image generation APIs, and payment fees. Used by 10,000+ developers.",
      home_keywords: "API cost calculator, LLM cost calculator, cloud cost estimator, vector database pricing, AI infrastructure tools",
    },
    ui: {
      nav_brand: "APICalculators",
      calculate_btn: "Calculate",
      monthly_label: "Monthly Estimate",
      annual_label: "Annual Estimate",
      currency: "USD", currency_symbol: "$", number_locale: "en-US",
      tab_tools: "Tools", tab_blog: "Blog",
      footer_copy: "© 2026 APICalculators.com — Free developer cost tools.",
      affiliate_cta_do: "Get $200 Free Cloud Credits →",
      affiliate_cta_vultr: "Get $100 Free at Vultr →",
      affiliate_cta_supabase: "Start Free on Supabase →",
      related_tools: "Related Calculators",
      related_blogs: "Related Articles",
      lang_soon: "SOON",
    },
    tools: {
      "llm-cost":    { name: "LLM Token Cost Calculator",           desc: "Estimate GPT-4o, Claude, Gemini monthly token spend" },
      "image-cost":  { name: "AI Image Generation Cost Calculator", desc: "DALL-E 3, Midjourney, Stable Diffusion pricing" },
      "cloud-vps":   { name: "Cloud VPS & DB Cost Comparison",      desc: "Vultr vs DigitalOcean vs Hetzner server costs" },
      "vector-db":   { name: "Vector Database Pricing Estimator",   desc: "Pinecone, Qdrant, Milvus, Weaviate budgeting" },
      "stt-tts":     { name: "STT & TTS API Cost Calculator",       desc: "Whisper, ElevenLabs, Google Speech pricing" },
      "serverless":  { name: "Serverless Compute Cost Calculator",   desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "API Gateway Traffic Cost Calculator",  desc: "AWS API GW, Kong, Cloudflare pricing" },
      "payment-fee": { name: "SaaS Payment Fee Calculator",         desc: "Stripe vs Paddle vs LemonSqueezy net revenue" },
      "embedding":   { name: "Embedding API Cost Calculator",       desc: "OpenAI, Cohere, Voyage AI embedding costs" },
      "agent-chain": { name: "AI Agent Multi-Model Cost Estimator",  desc: "Multi-step agent pipeline total cost" },
    },
    blog: {
      hub_title: "Developer Cost Optimization Blog",
      hub_desc: "Guides and cost breakdowns for AI infrastructure, cloud, and SaaS tools.",
      articles: [
        { slug: "llm-api-cost-guide-2026",        title: "How to Estimate LLM API Costs in 2026",              keyword: "LLM API cost 2026",            tool: "llm-cost"    },
        { slug: "vector-database-pricing-2026",   title: "Vector Database Pricing Comparison 2026",            keyword: "vector database pricing 2026", tool: "vector-db"   },
        { slug: "stripe-vs-paddle-fees",          title: "Stripe vs Paddle: Complete Fee Breakdown",           keyword: "Stripe vs Paddle 2026",        tool: "payment-fee" },
        { slug: "aws-lambda-cost-optimization",   title: "AWS Lambda Cost Optimization: Developer Guide",      keyword: "AWS Lambda cost calculator",   tool: "serverless"  },
        { slug: "ai-image-generation-cost",       title: "AI Image Generation API Cost Guide 2026",           keyword: "AI image generation API cost", tool: "image-cost"  },
        { slug: "embedding-api-cost-comparison",  title: "Embedding API Cost Comparison: OpenAI vs Cohere",   keyword: "embedding API cost comparison",tool: "embedding"   },
        { slug: "ai-agent-infrastructure-budget", title: "AI Agent Infrastructure: Full Budget Breakdown 2026",keyword: "AI agent cost 2026",           tool: "agent-chain" },
      ],
    },
  },

  de: {
    seo: {
      site_name: "APICalculators.de",
      home_title: "LLM Kostenrechner & KI-Infrastruktur Preistools | APICalculators",
      home_desc: "Kostenlose Echtzeit-Rechner für LLM-Token, Cloud-Infrastruktur, Vektordatenbanken und KI-Bildgenerierung. Von 10.000+ Entwicklern genutzt.",
      home_keywords: "LLM Kostenrechner, API Preisrechner, Cloud Kostenvergleich, Vektordatenbank Preise, KI Infrastruktur",
    },
    ui: {
      currency: "EUR", currency_symbol: "€", number_locale: "de-DE",
      calculate_btn: "Berechnen", monthly_label: "Monatliche Schätzung",
      affiliate_cta_do: "200 USD Cloud-Guthaben erhalten →",
      affiliate_cta_vultr: "100 USD bei Vultr erhalten →",
      affiliate_cta_supabase: "Kostenlos auf Supabase starten →",
      related_tools: "Verwandte Rechner", related_blogs: "Verwandte Artikel",
      lang_soon: "BALD",
    },
    tools: {
      "llm-cost":    { name: "LLM Token Kostenrechner",              desc: "GPT-4o, Claude, Gemini monatliche Kosten schätzen" },
      "image-cost":  { name: "KI-Bildgenerierung Kostenrechner",    desc: "DALL-E 3, Midjourney, Stable Diffusion Preise" },
      "cloud-vps":   { name: "Cloud VPS & DB Kostenvergleich",      desc: "Vultr vs DigitalOcean vs Hetzner Serverkosten" },
      "vector-db":   { name: "Vektordatenbank Preisrechner",         desc: "Pinecone, Qdrant, Milvus, Weaviate Budgetierung" },
      "stt-tts":     { name: "STT & TTS API Kostenrechner",         desc: "Whisper, ElevenLabs, Google Speech Preise" },
      "serverless":  { name: "Serverless Compute Kostenrechner",    desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "API Gateway Traffic Kostenrechner",   desc: "AWS API GW, Kong, Cloudflare Preise" },
      "payment-fee": { name: "SaaS Zahlungsgebühren Rechner",       desc: "Stripe vs Paddle vs LemonSqueezy Nettoeinnahmen" },
      "embedding":   { name: "Embedding API Kostenrechner",         desc: "OpenAI, Cohere, Voyage AI Embedding Kosten" },
      "agent-chain": { name: "KI-Agent Multi-Modell Kostenrechner", desc: "Mehrstufige Agent-Pipeline Gesamtkosten" },
    },
    blog: {
      hub_title: "Blog für Entwickler-Kostenoptimierung",
      hub_desc: "Leitfäden und Kostenaufschlüsselungen für KI-Infrastruktur, Cloud und SaaS-Tools.",
      articles: [
        { slug: "llm-api-kosten-2026",           title: "LLM API Kosten 2026 schätzen",                    keyword: "LLM API Kosten 2026",           tool: "llm-cost"    },
        { slug: "vektordatenbank-preisvergleich", title: "Vektordatenbank Preisvergleich 2026",             keyword: "Vektordatenbank Preise 2026",   tool: "vector-db"   },
        { slug: "stripe-vs-paddle-gebuehren",    title: "Stripe vs Paddle: Vollständiger Gebührenvergleich",keyword: "Stripe vs Paddle 2026",         tool: "payment-fee" },
        { slug: "aws-lambda-optimierung",        title: "AWS Lambda Kostenoptimierung: Entwickler-Guide",  keyword: "AWS Lambda Kostenrechner",      tool: "serverless"  },
        { slug: "ki-bildgenerierung-kosten",     title: "KI-Bildgenerierungs API Kostenguide 2026",       keyword: "KI Bildgenerierung API Kosten",  tool: "image-cost"  },
        { slug: "embedding-api-vergleich",       title: "Embedding API Kosten: OpenAI vs Cohere",         keyword: "Embedding API Kosten Vergleich", tool: "embedding"   },
        { slug: "ki-agent-infrastruktur-budget", title: "KI-Agent Infrastruktur: Budget-Analyse 2026",    keyword: "KI Agent Kosten 2026",          tool: "agent-chain" },
      ],
    },
  },

  fr: {
    seo: {
      site_name: "APICalculators.fr",
      home_title: "Calculatrice Coûts LLM & Outils Infrastructure IA | APICalculators",
      home_desc: "Calculatrices gratuites en temps réel pour tokens LLM, cloud, bases vectorielles et APIs d'images IA. Utilisé par 10 000+ développeurs.",
      home_keywords: "calculatrice coûts LLM, calculateur API prix, comparaison cloud, tarification base vectorielle, outils infrastructure IA",
    },
    ui: {
      currency: "EUR", currency_symbol: "€", number_locale: "fr-FR",
      calculate_btn: "Calculer", monthly_label: "Estimation mensuelle",
      affiliate_cta_do: "Obtenez 200 USD de crédits cloud →",
      affiliate_cta_vultr: "Obtenez 100 USD chez Vultr →",
      affiliate_cta_supabase: "Démarrez gratuitement sur Supabase →",
      related_tools: "Calculatrices associées", related_blogs: "Articles associés",
      lang_soon: "BIENTÔT",
    },
    tools: {
      "llm-cost":    { name: "Calculatrice Coûts Tokens LLM",            desc: "Estimez vos dépenses GPT-4o, Claude, Gemini" },
      "image-cost":  { name: "Calculatrice Coûts Génération Images IA",  desc: "Tarifs DALL-E 3, Midjourney, Stable Diffusion" },
      "cloud-vps":   { name: "Comparaison Coûts Cloud VPS & DB",         desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Estimateur Prix Base Vectorielle",          desc: "Budgétisation Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "Calculatrice API STT & TTS",               desc: "Tarifs Whisper, ElevenLabs, Google Speech" },
      "serverless":  { name: "Calculatrice Coûts Serverless",            desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "Calculatrice Coûts API Gateway",           desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "Calculatrice Frais Paiement SaaS",         desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Calculatrice API Embedding",               desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "Estimateur Coûts Agent IA Multi-Modèle",   desc: "Coût total pipeline multi-étapes" },
    },
    blog: {
      hub_title: "Blog Optimisation des Coûts Développeurs",
      hub_desc: "Guides et analyses de coûts pour l'infrastructure IA, cloud et outils SaaS.",
      articles: [
        { slug: "guide-couts-api-llm-2026",            title: "Comment Estimer les Coûts API LLM en 2026",         keyword: "coûts API LLM 2026",           tool: "llm-cost"    },
        { slug: "comparaison-bases-vectorielles-2026", title: "Comparaison Tarifs Bases Vectorielles 2026",        keyword: "tarifs base vectorielle 2026",  tool: "vector-db"   },
        { slug: "stripe-vs-paddle-frais",              title: "Stripe vs Paddle: Analyse Complète des Frais",      keyword: "Stripe vs Paddle 2026",         tool: "payment-fee" },
        { slug: "optimisation-aws-lambda",             title: "Optimisation Coûts AWS Lambda: Guide Développeur",  keyword: "calculateur coût AWS Lambda",   tool: "serverless"  },
        { slug: "cout-generation-images-ia",           title: "Guide Coûts API Génération Images IA 2026",        keyword: "coût API génération images IA", tool: "image-cost"  },
        { slug: "comparaison-api-embedding",           title: "Comparaison API Embedding: OpenAI vs Cohere",      keyword: "comparaison coût API embedding",tool: "embedding"   },
        { slug: "budget-infrastructure-agent-ia",      title: "Infrastructure Agent IA: Analyse Budget Complète", keyword: "coût agent IA 2026",            tool: "agent-chain" },
      ],
    },
  },

  tr: {
    seo: {
      site_name: "APICalculators.tr",
      home_title: "LLM Maliyet Hesaplayıcı & YZ Altyapısı Araçları | APICalculators",
      home_desc: "LLM token, bulut altyapısı, vektör veritabanı ve YZ görsel API'leri için ücretsiz gerçek zamanlı hesaplayıcılar. 10.000+ yazılımcı tarafından kullanılıyor.",
      home_keywords: "LLM maliyet hesaplayıcı, API fiyat tahmini, bulut maliyet karşılaştırma, vektör veritabanı fiyatlandırma, YZ altyapı araçları",
    },
    ui: {
      currency: "TRY", currency_symbol: "₺", number_locale: "tr-TR",
      calculate_btn: "Hesapla", monthly_label: "Aylık Tahmin",
      affiliate_cta_do: "$200 Ücretsiz Bulut Kredisi Al →",
      affiliate_cta_vultr: "Vultr'da $100 Ücretsiz Al →",
      affiliate_cta_supabase: "Supabase'de Ücretsiz Başla →",
      related_tools: "İlgili Hesaplayıcılar", related_blogs: "İlgili Makaleler",
      lang_soon: "YAKINDA",
    },
    tools: {
      "llm-cost":    { name: "LLM Token Maliyet Hesaplayıcı",           desc: "GPT-4o, Claude, Gemini aylık harcama tahmini" },
      "image-cost":  { name: "YZ Görsel Üretim Maliyet Hesaplayıcı",   desc: "DALL-E 3, Midjourney, Stable Diffusion fiyatları" },
      "cloud-vps":   { name: "Bulut VPS & DB Maliyet Karşılaştırması", desc: "Vultr, DigitalOcean, Hetzner sunucu maliyetleri" },
      "vector-db":   { name: "Vektör Veritabanı Fiyat Hesaplayıcı",    desc: "Pinecone, Qdrant, Milvus, Weaviate bütçeleme" },
      "stt-tts":     { name: "STT & TTS API Maliyet Hesaplayıcı",     desc: "Whisper, ElevenLabs, Google Speech fiyatları" },
      "serverless":  { name: "Serverless Hesaplama Maliyet Hesaplayıcı",desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "API Gateway Trafik Maliyet Hesaplayıcı", desc: "AWS API GW, Kong, Cloudflare fiyatlandırması" },
      "payment-fee": { name: "SaaS Ödeme Ücreti Hesaplayıcı",          desc: "Stripe vs Paddle vs LemonSqueezy net gelir" },
      "embedding":   { name: "Embedding API Maliyet Hesaplayıcı",       desc: "OpenAI, Cohere, Voyage AI embedding maliyetleri" },
      "agent-chain": { name: "YZ Ajan Çoklu Model Maliyet Tahmincisi", desc: "Çok adımlı ajan pipeline toplam maliyeti" },
    },
    blog: {
      hub_title: "Geliştirici Maliyet Optimizasyonu Blogu",
      hub_desc: "YZ altyapısı, bulut ve SaaS araçları için rehberler ve maliyet analizleri.",
      articles: [
        { slug: "llm-api-maliyet-rehberi-2026",        title: "2026'da LLM API Maliyetleri Nasıl Tahmin Edilir",   keyword: "LLM API maliyet 2026",              tool: "llm-cost"    },
        { slug: "vektor-veritabani-fiyat-2026",        title: "Vektör Veritabanı Fiyat Karşılaştırması 2026",      keyword: "vektör veritabanı fiyatlandırma",   tool: "vector-db"   },
        { slug: "stripe-vs-paddle-ucretler",           title: "Stripe vs Paddle: Eksiksiz Ücret Analizi",         keyword: "Stripe vs Paddle 2026",             tool: "payment-fee" },
        { slug: "aws-lambda-maliyet-optimizasyon",     title: "AWS Lambda Maliyet Optimizasyonu: Geliştirici Rehberi",keyword: "AWS Lambda maliyet hesaplayıcı", tool: "serverless"  },
        { slug: "yapay-zeka-gorsel-uretim-maliyeti",   title: "YZ Görsel Üretim API Maliyet Rehberi 2026",       keyword: "YZ görsel üretim API maliyeti",     tool: "image-cost"  },
        { slug: "embedding-api-maliyet-karsilastirma", title: "Embedding API Maliyeti: OpenAI vs Cohere",        keyword: "embedding API maliyet karşılaştırma",tool: "embedding"  },
        { slug: "yapay-zeka-ajan-altyapi-butce",       title: "YZ Ajan Altyapısı: Eksiksiz Bütçe Analizi 2026", keyword: "YZ ajan maliyeti 2026",             tool: "agent-chain" },
      ],
    },
  },

  es: {
    seo: {
      site_name: "APICalculators.es",
      home_title: "Calculadora de Costos LLM & Herramientas de Infraestructura IA | APICalculators",
      home_desc: "Calculadoras gratuitas en tiempo real para tokens LLM, nube, bases de datos vectoriales y APIs de imágenes IA. Usado por 10.000+ desarrolladores.",
      home_keywords: "calculadora costos LLM, estimador precios API, comparación nube, precios base datos vectorial, herramientas infraestructura IA",
    },
    ui: {
      currency: "USD", currency_symbol: "$", number_locale: "es-ES",
      calculate_btn: "Calcular", monthly_label: "Estimación mensual",
      affiliate_cta_do: "Obtén $200 en créditos cloud →",
      affiliate_cta_supabase: "Empieza gratis en Supabase →",
      related_tools: "Calculadoras relacionadas", related_blogs: "Artículos relacionados",
      lang_soon: "PRÓXIMO",
    },
    tools: {
      "llm-cost":    { name: "Calculadora de Costos de Tokens LLM",        desc: "Estima gastos mensuales GPT-4o, Claude, Gemini" },
      "image-cost":  { name: "Calculadora Costos Generación Imágenes IA",  desc: "Precios DALL-E 3, Midjourney, Stable Diffusion" },
      "cloud-vps":   { name: "Comparación Costos Cloud VPS & DB",          desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Estimador de Precios Base de Datos Vectorial",desc: "Presupuesto Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "Calculadora API STT & TTS",                  desc: "Precios Whisper, ElevenLabs, Google Speech" },
      "serverless":  { name: "Calculadora Costos Serverless",              desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "Calculadora Costos API Gateway",             desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "Calculadora Comisiones Pago SaaS",           desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Calculadora API de Embeddings",              desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "Estimador Costos Agente IA Multi-Modelo",    desc: "Costo total pipeline multi-paso" },
    },
    blog: {
      hub_title: "Blog de Optimización de Costos para Desarrolladores",
      hub_desc: "Guías y análisis de costos para infraestructura IA, cloud y herramientas SaaS.",
      articles: [
        { slug: "guia-costos-api-llm-2026",           title: "Cómo Estimar Costos de API LLM en 2026",            keyword: "costos API LLM 2026",              tool: "llm-cost"    },
        { slug: "comparacion-bases-vectoriales-2026", title: "Comparación de Precios Bases Vectoriales 2026",     keyword: "precios base datos vectorial 2026",tool: "vector-db"   },
        { slug: "stripe-vs-paddle-comisiones",        title: "Stripe vs Paddle: Análisis Completo de Comisiones", keyword: "Stripe vs Paddle 2026",            tool: "payment-fee" },
        { slug: "optimizacion-aws-lambda",            title: "Optimización Costos AWS Lambda: Guía Desarrollador", keyword: "calculadora costo AWS Lambda",    tool: "serverless"  },
        { slug: "costo-generacion-imagenes-ia",       title: "Guía Costos API Generación Imágenes IA 2026",      keyword: "costo API generación imágenes IA", tool: "image-cost"  },
        { slug: "comparacion-api-embeddings",         title: "Costos API Embedding: OpenAI vs Cohere",           keyword: "comparación costos API embedding", tool: "embedding"   },
        { slug: "presupuesto-infraestructura-agente", title: "Infraestructura Agente IA: Análisis Presupuesto",   keyword: "costo agente IA 2026",            tool: "agent-chain" },
      ],
    },
  },

  it: {
    seo: {
      site_name: "APICalculators.it",
      home_title: "Calcolatore Costi LLM & Strumenti Infrastruttura IA | APICalculators",
      home_desc: "Calcolatori gratuiti in tempo reale per token LLM, cloud, database vettoriali e API di generazione immagini IA. Usato da 10.000+ sviluppatori.",
      home_keywords: "calcolatore costi LLM, stimatore prezzi API, confronto cloud, prezzi database vettoriale, strumenti infrastruttura IA",
    },
    ui: {
      currency: "EUR", currency_symbol: "€", number_locale: "it-IT",
      calculate_btn: "Calcola", monthly_label: "Stima mensile",
      affiliate_cta_do: "Ottieni $200 di crediti cloud →",
      affiliate_cta_supabase: "Inizia gratis su Supabase →",
      related_tools: "Calcolatori correlati", related_blogs: "Articoli correlati",
      lang_soon: "PRESTO",
    },
    tools: {
      "llm-cost":    { name: "Calcolatore Costi Token LLM",              desc: "Stima spese mensili GPT-4o, Claude, Gemini" },
      "image-cost":  { name: "Calcolatore Costi Generazione Immagini IA",desc: "Prezzi DALL-E 3, Midjourney, Stable Diffusion" },
      "cloud-vps":   { name: "Confronto Costi Cloud VPS & DB",           desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Stimatore Prezzi Database Vettoriale",     desc: "Budget Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "Calcolatore API STT & TTS",                desc: "Prezzi Whisper, ElevenLabs, Google Speech" },
      "serverless":  { name: "Calcolatore Costi Serverless",             desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "Calcolatore Costi API Gateway",            desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "Calcolatore Commissioni Pagamento SaaS",   desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Calcolatore API Embedding",                desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "Stimatore Costi Agente IA Multi-Modello",  desc: "Costo totale pipeline multi-step" },
    },
    blog: {
      hub_title: "Blog Ottimizzazione Costi per Sviluppatori",
      hub_desc: "Guide e analisi dei costi per infrastruttura IA, cloud e strumenti SaaS.",
      articles: [
        { slug: "guida-costi-api-llm-2026",        title: "Come Stimare i Costi API LLM nel 2026",              keyword: "costi API LLM 2026",            tool: "llm-cost"    },
        { slug: "confronto-database-vettoriali",   title: "Confronto Prezzi Database Vettoriali 2026",          keyword: "prezzi database vettoriale 2026",tool: "vector-db"   },
        { slug: "stripe-vs-paddle-commissioni",    title: "Stripe vs Paddle: Analisi Completa Commissioni",     keyword: "Stripe vs Paddle 2026",         tool: "payment-fee" },
        { slug: "ottimizzazione-costi-aws-lambda", title: "Ottimizzazione Costi AWS Lambda: Guida Sviluppatore",keyword: "calcolatore costo AWS Lambda",  tool: "serverless"  },
        { slug: "costo-generazione-immagini-ia",   title: "Guida Costi API Generazione Immagini IA 2026",      keyword: "costo API generazione immagini", tool: "image-cost"  },
        { slug: "confronto-api-embedding",         title: "Costi API Embedding: OpenAI vs Cohere",             keyword: "confronto costi API embedding", tool: "embedding"   },
        { slug: "budget-infrastruttura-agente-ia", title: "Infrastruttura Agente IA: Analisi Budget Completa", keyword: "costo agente IA 2026",          tool: "agent-chain" },
      ],
    },
  },

  ja: {
    seo: {
      site_name: "APICalculators.jp",
      home_title: "LLMコスト計算機 & AI インフラ料金ツール | APICalculators",
      home_desc: "LLMトークン、クラウドインフラ、ベクターDB、AI画像生成APIの無料リアルタイム計算機。1万人以上の開発者が利用中。",
      home_keywords: "LLMコスト計算機, API料金見積もり, クラウドコスト比較, ベクターデータベース料金, AIインフラツール",
    },
    ui: {
      currency: "JPY", currency_symbol: "¥", number_locale: "ja-JP",
      calculate_btn: "計算する", monthly_label: "月額見積もり",
      affiliate_cta_do: "$200無料クラウドクレジットを取得 →",
      affiliate_cta_supabase: "Supabaseで無料スタート →",
      related_tools: "関連計算機", related_blogs: "関連記事",
      lang_soon: "近日公開",
    },
    tools: {
      "llm-cost":    { name: "LLMトークンコスト計算機",         desc: "GPT-4o、Claude、Geminiの月額コスト見積もり" },
      "image-cost":  { name: "AI画像生成コスト計算機",          desc: "DALL-E 3、Midjourney、Stable Diffusionの料金" },
      "cloud-vps":   { name: "クラウドVPS & DBコスト比較",      desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "ベクターDB料金見積もり",          desc: "Pinecone、Qdrant、Milvusの予算計画" },
      "stt-tts":     { name: "STT & TTS APIコスト計算機",      desc: "Whisper、ElevenLabs、Google Speechの料金" },
      "serverless":  { name: "サーバーレス計算コスト計算機",    desc: "AWS Lambda、Vercel Functions、CF Workers" },
      "api-gateway": { name: "APIゲートウェイコスト計算機",     desc: "AWS API GW、Kong、Cloudflare" },
      "payment-fee": { name: "SaaS決済手数料計算機",            desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Embedding APIコスト計算機",       desc: "OpenAI、Cohere、Voyage AI" },
      "agent-chain": { name: "AIエージェントマルチモデルコスト", desc: "マルチステップパイプラインの総コスト" },
    },
    blog: {
      hub_title: "開発者コスト最適化ブログ",
      hub_desc: "AIインフラ、クラウド、SaaSツールのガイドとコスト分析。",
      articles: [
        { slug: "llm-api-cost-guide-2026-ja",    title: "2026年LLM APIコストの見積もり方法",          keyword: "LLM APIコスト 2026",           tool: "llm-cost"    },
        { slug: "vector-db-pricing-2026-ja",     title: "ベクターDBコスト比較 2026",                  keyword: "ベクターデータベース料金 2026", tool: "vector-db"   },
        { slug: "stripe-vs-paddle-ja",           title: "Stripe vs Paddle: 最新手数料完全比較",       keyword: "Stripe vs Paddle 最新手数料",  tool: "payment-fee" },
        { slug: "aws-lambda-cost-ja",            title: "AWS Lambdaコスト最適化ガイド",               keyword: "AWS Lambda コスト計算",        tool: "serverless"  },
        { slug: "ai-image-api-cost-ja",          title: "AI画像生成APIコストガイド 2026",             keyword: "AI画像生成 APIコスト",         tool: "image-cost"  },
        { slug: "embedding-api-comparison-ja",   title: "Embedding APIコスト: OpenAI vs Cohere",     keyword: "Embedding APIコスト比較",      tool: "embedding"   },
        { slug: "ai-agent-budget-ja",            title: "AIエージェントインフラ: 予算完全分析 2026",  keyword: "AIエージェント コスト 2026",   tool: "agent-chain" },
      ],
    },
  },

  nl: {
    seo: {
      site_name: "APICalculators.nl",
      home_title: "LLM Kostencalculator & AI Infrastructuurtools | APICalculators",
      home_desc: "Gratis realtime calculators voor LLM-tokens, cloud, vectordatabases en AI-beeldgeneratie-API's. Door 10.000+ ontwikkelaars gebruikt.",
      home_keywords: "LLM kostencalculator, API prijsschatting, cloud vergelijking, vectordatabase prijzen, AI infrastructuurtools",
    },
    ui: {
      currency: "EUR", currency_symbol: "€", number_locale: "nl-NL",
      calculate_btn: "Berekenen", monthly_label: "Maandelijkse schatting",
      affiliate_cta_do: "Ontvang $200 gratis cloudtegoed →",
      affiliate_cta_supabase: "Gratis starten op Supabase →",
      related_tools: "Gerelateerde calculators", related_blogs: "Gerelateerde artikelen",
      lang_soon: "BINNENKORT",
    },
    tools: {
      "llm-cost":    { name: "LLM Token Kostencalculator",         desc: "Schat maandelijkse GPT-4o, Claude, Gemini kosten" },
      "image-cost":  { name: "AI Beeldgeneratie Kostencalculator", desc: "DALL-E 3, Midjourney, Stable Diffusion prijzen" },
      "cloud-vps":   { name: "Cloud VPS & DB Kostenvergelijking",  desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Vectordatabase Prijsschatting",      desc: "Budgettering Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "STT & TTS API Kostencalculator",    desc: "Whisper, ElevenLabs, Google Speech prijzen" },
      "serverless":  { name: "Serverless Compute Calculator",      desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "API Gateway Kostencalculator",       desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "SaaS Betaalkosten Calculator",       desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Embedding API Kostencalculator",     desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "AI Agent Multi-Model Kostenschatter",desc: "Totale kosten multi-stap pipeline" },
    },
    blog: {
      hub_title: "Blog voor Ontwikkelaars Kostenoptimalisatie",
      hub_desc: "Handleidingen en kostenanalyses voor AI-infrastructuur, cloud en SaaS-tools.",
      articles: [
        { slug: "llm-api-kosten-gids-2026",         title: "LLM API Kosten Schatten in 2026",               keyword: "LLM API kosten 2026",             tool: "llm-cost"    },
        { slug: "vectordatabase-vergelijking-2026", title: "Vectordatabase Prijsvergelijking 2026",          keyword: "vectordatabase prijzen 2026",     tool: "vector-db"   },
        { slug: "stripe-vs-paddle-kosten",          title: "Stripe vs Paddle: Volledige Kostenvergelijking", keyword: "Stripe vs Paddle 2026",           tool: "payment-fee" },
        { slug: "aws-lambda-optimalisatie",         title: "AWS Lambda Kostenoptimalisatie: Handleiding",    keyword: "AWS Lambda kostenberekening",     tool: "serverless"  },
        { slug: "ai-afbeelding-api-kosten",         title: "AI Beeldgeneratie API Kostengids 2026",         keyword: "AI afbeelding generatie API kosten",tool: "image-cost"},
        { slug: "embedding-api-vergelijking",       title: "Embedding API Kosten: OpenAI vs Cohere",        keyword: "embedding API kosten vergelijking",tool: "embedding"   },
        { slug: "ai-agent-infrastructuur-budget",   title: "AI Agent Infrastructuur: Budget Analyse 2026",  keyword: "AI agent kosten 2026",            tool: "agent-chain" },
      ],
    },
  },

  pl: {
    seo: {
      site_name: "APICalculators.pl",
      home_title: "Kalkulator Kosztów LLM & Narzędzia Infrastruktury AI | APICalculators",
      home_desc: "Bezpłatne kalkulatory czasu rzeczywistego dla tokenów LLM, chmury, baz wektorowych i API generowania obrazów AI. Używane przez 10 000+ deweloperów.",
      home_keywords: "kalkulator kosztów LLM, estymator cen API, porównanie chmury, ceny baz wektorowych, narzędzia infrastruktury AI",
    },
    ui: {
      currency: "PLN", currency_symbol: "zł", number_locale: "pl-PL",
      calculate_btn: "Oblicz", monthly_label: "Miesięczna szacunkowa",
      affiliate_cta_do: "Uzyskaj $200 darmowych kredytów →",
      affiliate_cta_supabase: "Zacznij za darmo na Supabase →",
      related_tools: "Powiązane kalkulatory", related_blogs: "Powiązane artykuły",
      lang_soon: "WKRÓTCE",
    },
    tools: {
      "llm-cost":    { name: "Kalkulator Kosztów Tokenów LLM",         desc: "Szacuj miesięczne wydatki GPT-4o, Claude, Gemini" },
      "image-cost":  { name: "Kalkulator Kosztów Generowania Obrazów AI",desc: "Ceny DALL-E 3, Midjourney, Stable Diffusion" },
      "cloud-vps":   { name: "Porównanie Kosztów Cloud VPS & DB",      desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Estymator Cen Baz Wektorowych",          desc: "Budżetowanie Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "Kalkulator API STT & TTS",               desc: "Ceny Whisper, ElevenLabs, Google Speech" },
      "serverless":  { name: "Kalkulator Kosztów Serverless",          desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "Kalkulator Kosztów API Gateway",         desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "Kalkulator Opłat Płatności SaaS",        desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Kalkulator API Embedding",               desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "Estymator Kosztów Agenta AI Multi-Model",desc: "Całkowity koszt pipeline'u multi-etapowego" },
    },
    blog: {
      hub_title: "Blog Optymalizacji Kosztów dla Deweloperów",
      hub_desc: "Przewodniki i analizy kosztów infrastruktury AI, chmury i narzędzi SaaS.",
      articles: [
        { slug: "przewodnik-koszty-llm-2026",        title: "Jak Szacować Koszty API LLM w 2026",             keyword: "koszty API LLM 2026",             tool: "llm-cost"    },
        { slug: "porownanie-baz-wektorowych-2026",   title: "Porównanie Cen Baz Wektorowych 2026",            keyword: "ceny baz wektorowych 2026",       tool: "vector-db"   },
        { slug: "stripe-vs-paddle-oplaty",           title: "Stripe vs Paddle: Pełna Analiza Opłat",         keyword: "Stripe vs Paddle 2026",           tool: "payment-fee" },
        { slug: "optymalizacja-kosztow-aws-lambda",  title: "Optymalizacja Kosztów AWS Lambda: Poradnik",    keyword: "kalkulator kosztów AWS Lambda",   tool: "serverless"  },
        { slug: "koszt-generowania-obrazow-ai",      title: "Przewodnik Kosztów API Generowania Obrazów AI", keyword: "koszt API generowania obrazów AI", tool: "image-cost"  },
        { slug: "porownanie-api-embedding",          title: "Koszty API Embedding: OpenAI vs Cohere",       keyword: "porównanie kosztów API embedding", tool: "embedding"   },
        { slug: "budzet-infrastruktura-agent-ai",    title: "Infrastruktura Agenta AI: Pełna Analiza Budżetu",keyword: "koszty agenta AI 2026",          tool: "agent-chain" },
      ],
    },
  },

  pt: {
    seo: {
      site_name: "APICalculators.pt",
      home_title: "Calculadora de Custos LLM & Ferramentas de Infraestrutura IA | APICalculators",
      home_desc: "Calculadoras gratuitas em tempo real para tokens LLM, nuvem, bancos de dados vetoriais e APIs de geração de imagens IA. Usado por 10.000+ desenvolvedores.",
      home_keywords: "calculadora custos LLM, estimador preços API, comparação nuvem, preços banco dados vetorial, ferramentas infraestrutura IA",
    },
    ui: {
      currency: "BRL", currency_symbol: "R$", number_locale: "pt-BR",
      calculate_btn: "Calcular", monthly_label: "Estimativa mensal",
      affiliate_cta_do: "Obtenha $200 em créditos cloud →",
      affiliate_cta_supabase: "Comece grátis no Supabase →",
      related_tools: "Calculadoras relacionadas", related_blogs: "Artigos relacionados",
      lang_soon: "EM BREVE",
    },
    tools: {
      "llm-cost":    { name: "Calculadora de Custos de Tokens LLM",        desc: "Estime gastos mensais GPT-4o, Claude, Gemini" },
      "image-cost":  { name: "Calculadora Custos Geração Imagens IA",      desc: "Preços DALL-E 3, Midjourney, Stable Diffusion" },
      "cloud-vps":   { name: "Comparação Custos Cloud VPS & DB",           desc: "Vultr vs DigitalOcean vs Hetzner" },
      "vector-db":   { name: "Estimador de Preços de Banco Vetorial",      desc: "Orçamento Pinecone, Qdrant, Milvus" },
      "stt-tts":     { name: "Calculadora API STT & TTS",                  desc: "Preços Whisper, ElevenLabs, Google Speech" },
      "serverless":  { name: "Calculadora Custos Serverless",              desc: "AWS Lambda, Vercel Functions, CF Workers" },
      "api-gateway": { name: "Calculadora Custos API Gateway",             desc: "AWS API GW, Kong, Cloudflare" },
      "payment-fee": { name: "Calculadora Taxas Pagamento SaaS",           desc: "Stripe vs Paddle vs LemonSqueezy" },
      "embedding":   { name: "Calculadora API de Embeddings",              desc: "OpenAI, Cohere, Voyage AI" },
      "agent-chain": { name: "Estimador Custos Agente IA Multi-Modelo",    desc: "Custo total pipeline multi-etapa" },
    },
    blog: {
      hub_title: "Blog de Otimização de Custos para Desenvolvedores",
      hub_desc: "Guias e análises de custos para infraestrutura IA, cloud e ferramentas SaaS.",
      articles: [
        { slug: "guia-custos-api-llm-2026",           title: "Como Estimar Custos de API LLM em 2026",           keyword: "custos API LLM 2026",              tool: "llm-cost"    },
        { slug: "comparacao-bancos-vetoriais-2026",   title: "Comparação de Preços Bancos Vetoriais 2026",        keyword: "preços banco dados vetorial 2026", tool: "vector-db"   },
        { slug: "stripe-vs-paddle-taxas",             title: "Stripe vs Paddle: Análise Completa de Taxas",      keyword: "Stripe vs Paddle 2026",           tool: "payment-fee" },
        { slug: "otimizacao-custos-aws-lambda",       title: "Otimização Custos AWS Lambda: Guia Desenvolvedor", keyword: "calculadora custo AWS Lambda",    tool: "serverless"  },
        { slug: "custo-geracao-imagens-ia",           title: "Guia Custos API Geração Imagens IA 2026",         keyword: "custo API geração imagens IA",    tool: "image-cost"  },
        { slug: "comparacao-api-embeddings",          title: "Custos API Embedding: OpenAI vs Cohere",          keyword: "comparação custos API embedding", tool: "embedding"   },
        { slug: "orcamento-infraestrutura-agente-ia", title: "Infraestrutura Agente IA: Análise Orçamento 2026", keyword: "custo agente IA 2026",            tool: "agent-chain" },
      ],
    },
  },
};

// ─── LANGUAGE CONTROLLER ───────────────────────────────────────────────────
const i18n = {
  current: 'en',
  supported: ['en','de','fr','tr','es','it','ja','nl','pl','pt'],
  paths: { en:'/', de:'/de/', fr:'/fr/', tr:'/tr/', es:'/es/', it:'/it/', ja:'/ja/', nl:'/nl/', pl:'/pl/', pt:'/pt/' },
  flags: { en:'🇬🇧', de:'🇩🇪', fr:'🇫🇷', tr:'🇹🇷', es:'🇪🇸', it:'🇮🇹', ja:'🇯🇵', nl:'🇳🇱', pl:'🇵🇱', pt:'🇵🇹' },
  names: { en:'English', de:'Deutsch', fr:'Français', tr:'Türkçe', es:'Español', it:'Italiano', ja:'日本語', nl:'Nederlands', pl:'Polski', pt:'Português' },
  live: ['en','de','fr','tr'], // mark as SOON if not in this list

  detect() {
    const seg = window.location.pathname.split('/')[1];
    const saved = localStorage.getItem('apc_lang');
    const browser = (navigator.language || '').slice(0, 2);
    if (this.supported.includes(seg)) return seg;
    if (this.supported.includes(saved)) return saved;
    if (this.supported.includes(browser)) return browser;
    return 'en';
  },

  set(lang) {
    if (!this.supported.includes(lang)) return;
    this.current = lang;
    localStorage.setItem('apc_lang', lang);
    document.documentElement.lang = lang;
    this._applyDOM();
  },

  t(path) {
    return path.split('.').reduce((o, k) => o?.[k], _i18n[this.current]) ?? '';
  },

  _applyDOM() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const v = this.t(el.dataset.i18n);
      if (v) el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const v = this.t(el.dataset.i18nPlaceholder);
      if (v) el.placeholder = v;
    });
  },

  formatCurrency(amount) {
    const { currency, number_locale } = _i18n[this.current].ui;
    return new Intl.NumberFormat(number_locale, {
      style: 'currency', currency, maximumFractionDigits: 2,
    }).format(amount);
  },

  // Render 10-language dropdown HTML (call once on page load)
  renderLangDropdown(containerId, currentLang) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const lang = currentLang || this.current;
    const isLive = l => this.live.includes(l);
    el.innerHTML = this.supported.map(l => {
      const soon = !isLive(l);
      const soonLabel = _i18n[lang]?.ui?.lang_soon || 'SOON';
      return `<a ${soon ? 'class="soon"' : (l === lang ? 'class="on"' : '')}
                 ${!soon ? `href="${this.paths[l]}"` : ''}
                 ${!soon ? `hreflang="${l}"` : ''}>
        <span class="flag">${this.flags[l]}</span>
        ${this.names[l]}
        <span class="code">${soon ? soonLabel : l.toUpperCase()}</span>
      </a>`;
    }).join('');
  },

  // Render footer tool×language link matrix
  renderFooterMatrix(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const lang = this.current;
    const toolIds = Object.keys(_i18n.en.tools);
    el.innerHTML = toolIds.map(id => `
      <div>
        <div class="fm-tool">${_i18n[lang]?.tools?.[id]?.name || _i18n.en.tools[id].name}</div>
        ${this.supported.map(l => `
          <a href="${this.paths[l]}#${id}" hreflang="${l}"
             class="fm-link">${l.toUpperCase()}</a>
        `).join('')}
      </div>`).join('');
  },

  // Render related tools grid for a given tool
  renderRelatedTools(containerId, currentToolId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const lang = this.current;
    const toolIds = Object.keys(_i18n.en.tools).filter(id => id !== currentToolId).slice(0, 6);
    el.innerHTML = toolIds.map(id => `
      <a href="${this.paths[lang]}#${id}" class="related-tool-chip">
        ${_i18n[lang]?.tools?.[id]?.name || _i18n.en.tools[id].name}
      </a>`).join('');
  },
};

// Auto-init on load
if (typeof window !== 'undefined') {
  window.i18n = i18n;
  document.addEventListener('DOMContentLoaded', () => {
    i18n.set(i18n.detect());
  });
}
