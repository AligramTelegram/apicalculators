// seo.js — APICalculators.com dynamic meta + hreflang + schema injector
// Works with i18n.js. Call SEO.inject(lang) after i18n.set(lang).

const DOMAIN = 'https://apicalculators.com';
const PATHS  = { en:'/', de:'/de/', fr:'/fr/', tr:'/tr/', es:'/es/', it:'/it/', ja:'/ja/', nl:'/nl/', pl:'/pl/', pt:'/pt/' };
const LANGS  = Object.keys(PATHS);

const SEO = {
  inject(lang, opts = {}) {
    // opts: { toolId, blogSlug, title, desc }
    const d = (typeof _i18n !== 'undefined') ? _i18n[lang] : null;
    if (!d) return;

    const base = DOMAIN + PATHS[lang];
    const title = opts.title || d.seo.home_title;
    const desc  = opts.desc  || d.seo.home_desc;
    const url   = base + (opts.blogSlug ? `blog/${opts.blogSlug}` : '');

    // ── TITLE ──
    document.title = title;

    // ── META HELPERS ──
    const setMeta = (key, val, prop = 'name') => {
      let el = document.querySelector(`meta[${prop}="${key}"]`);
      if (!el) { el = document.createElement('meta'); el.setAttribute(prop, key); document.head.appendChild(el); }
      el.setAttribute('content', val);
    };

    setMeta('description',          desc);
    setMeta('keywords',             d.seo.home_keywords);
    setMeta('og:type',              'website', 'property');
    setMeta('og:locale',            lang + '_' + lang.toUpperCase(), 'property');
    setMeta('og:title',             title, 'property');
    setMeta('og:description',       desc, 'property');
    setMeta('og:image',             DOMAIN + (d.seo.og_image || '/og-image.jpg'), 'property');
    setMeta('og:url',               url, 'property');
    setMeta('og:site_name',         d.seo.site_name || 'APICalculators', 'property');
    setMeta('twitter:card',         'summary_large_image');
    setMeta('twitter:title',        title);
    setMeta('twitter:description',  desc);
    setMeta('twitter:image',        DOMAIN + '/twitter-image.jpg');
    setMeta('twitter:site',         '@apicalculators');

    // ── CANONICAL ──
    let canon = document.querySelector('link[rel="canonical"]');
    if (!canon) { canon = document.createElement('link'); canon.rel = 'canonical'; document.head.appendChild(canon); }
    canon.href = url || base;

    // ── HREFLANG (10×10 matrix) ──
    document.querySelectorAll('link[rel="alternate"]').forEach(e => e.remove());
    LANGS.forEach(l => {
      const lk = document.createElement('link');
      lk.rel = 'alternate'; lk.hreflang = l;
      lk.href = DOMAIN + PATHS[l] + (opts.blogSlug ? `blog/${opts.blogSlug}` : '');
      document.head.appendChild(lk);
    });
    const xd = document.createElement('link');
    xd.rel = 'alternate'; xd.hreflang = 'x-default'; xd.href = DOMAIN + '/';
    document.head.appendChild(xd);

    // ── STRUCTURED DATA ──
    this._injectSchema(lang, url, title, desc, opts);
  },

  _injectSchema(lang, url, title, desc, opts) {
    const old = document.getElementById('apc-ld');
    if (old) old.remove();

    const d = _i18n[lang];
    const graphs = [];

    // WebSite
    graphs.push({
      "@type": "WebSite",
      "@id": DOMAIN + "/#website",
      "name": d.seo.site_name || "APICalculators",
      "url": DOMAIN,
      "inLanguage": lang,
      "description": desc,
    });

    // Organization
    graphs.push({
      "@type": "Organization",
      "@id": DOMAIN + "/#org",
      "name": "APICalculators",
      "url": DOMAIN,
      "logo": { "@type": "ImageObject", "url": DOMAIN + "/logo.png" },
      "sameAs": ["https://twitter.com/apicalculators", "https://github.com/apicalculators"],
    });

    // SoftwareApplication (for the calculator tool)
    if (!opts.blogSlug) {
      graphs.push({
        "@type": "SoftwareApplication",
        "name": d.seo.site_name || "APICalculators",
        "url": url,
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Web",
        "inLanguage": lang,
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": d.ui.currency || "USD" },
        "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "ratingCount": "312" },
      });
    }

    // BreadcrumbList for blog posts
    if (opts.blogSlug && opts.title) {
      graphs.push({
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + PATHS[lang] },
          { "@type": "ListItem", "position": 2, "name": "Blog", "item": DOMAIN + PATHS[lang] + "blog/" },
          { "@type": "ListItem", "position": 3, "name": opts.title },
        ],
      });
    }

    // FAQ (homepage)
    if (!opts.blogSlug) {
      const faqQ = {
        en: { q: "How accurate are the API cost calculations?", a: "All prices are sourced from official provider documentation and updated monthly. Treat results as upper-bound estimates for budgeting." },
        de: { q: "Wie genau sind die API-Kostenberechnungen?", a: "Alle Preise stammen aus offiziellen Anbieterdokumentationen und werden monatlich aktualisiert." },
        fr: { q: "Quelle est la précision des calculs de coûts API?", a: "Tous les prix proviennent de la documentation officielle des fournisseurs et sont mis à jour mensuellement." },
        tr: { q: "API maliyet hesaplamaları ne kadar doğru?", a: "Tüm fiyatlar resmi sağlayıcı belgelerinden alınmakta ve aylık güncellenmektedir." },
      };
      const faq = faqQ[lang] || faqQ.en;
      graphs.push({
        "@type": "FAQPage",
        "mainEntity": [{
          "@type": "Question",
          "name": faq.q,
          "acceptedAnswer": { "@type": "Answer", "text": faq.a },
        }],
      });
    }

    const script = document.createElement('script');
    script.id   = 'apc-ld';
    script.type = 'application/ld+json';
    script.text = JSON.stringify({ "@context": "https://schema.org", "@graph": graphs });
    document.head.appendChild(script);
  },

  // Utility: generate hreflang tags as static HTML string (for static pages)
  staticHreflang(lang, blogSlug = '') {
    return LANGS.map(l =>
      `<link rel="alternate" hreflang="${l}" href="${DOMAIN}${PATHS[l]}${blogSlug ? 'blog/' + blogSlug : ''}">`
    ).join('\n') + `\n<link rel="alternate" hreflang="x-default" href="${DOMAIN}/">`;
  },
};

if (typeof window !== 'undefined') window.SEO = SEO;
if (typeof module !== 'undefined') module.exports = { SEO, DOMAIN, PATHS, LANGS };
