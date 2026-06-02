# 🧮 APICalculators.com

> Developer infrastructure cost optimization hub — LLM tokens, vector databases, AI image generation, and SaaS payment fees. Static, fast, privacy-first.

**Stack:** HTML5 + Vanilla JS + hand-written CSS · **Host:** Vercel (free tier / edge) · **Cost to run:** $0

---

## 📁 Dosya yapısı

```
APICalculators/
├── index.html      # Ana sayfa — 4 hesaplayıcı + SEO + schema + analytics
├── about.html      # Hakkımızda (E-E-A-T / AdSense için)
├── privacy.html    # Gizlilik politikası (AdSense zorunlu)
├── terms.html      # Kullanım şartları (AdSense zorunlu)
├── 404.html        # Özel hata sayfası
├── robots.txt      # Crawler kuralları + AI botlar + sitemap
├── sitemap.xml     # hreflang alternatifleriyle site haritası
├── vercel.json     # Güvenlik header'ları + cache + redirect
└── README.md
```

## 🚀 Lokal çalıştırma

Tek dosyalık statik site — derleme gerekmez. Çift tıkla `index.html` aç ya da:

```bash
# Python ile basit sunucu
python -m http.server 5500
# → http://localhost:5500

# veya VS Code "Live Server" eklentisi
```

## ⚙️ Tasarım kararı: neden Tailwind CDN yok?

Master plan Tailwind diyordu ama **performans bütçesi** (render-blocking yok, <17KB, LCP <1.5s) Tailwind Play CDN (~100KB+, render-blocking) ile çelişiyordu. Bu yüzden el yazımı CSS kullandım: hem bütçeye uyuyor hem de generic "AI Tailwind" görünümünden kaçınıp özgün bir tasarım veriyor. Compiled Tailwind'e geçmek istersen `<style>` bloğunu çıkarıp PostCSS build'i ekleyebilirsin.

---

## ✅ TÜRKÇE TASKLIST — Production'a Çıkış

### 🔴 FAZ 0 — Yayın öncesi zorunlu (placeholder'ları değiştir)
- [ ] `index.html` → `GA_YOUR_ID` yerine gerçek **GA4 Measurement ID**
- [ ] AdSense `ca-pub-YOUR_CODE` ve slot ID'leri ekle (onay sonrası)
- [ ] Affiliate linklerde `YOUR_CODE` (DigitalOcean refcode) güncelle
- [ ] Newsletter formunu Substack/ConvertKit/Beehiiv'e bağla
- [ ] `og-image.jpg` ve `twitter-image.jpg` (1200×630) tasarla & ekle
- [ ] `hello@apicalculators.com` mail adresini kur/değiştir
- [ ] Tüm fiyatları resmi sayfalardan **doğrula** (LLM/Vector/Image/Payment)

### 🟠 FAZ 1 — Deploy (Hafta 1)
- [ ] `git init` + GitHub repo (public)
- [ ] Vercel'e bağla → `vercel --prod`
- [ ] `apicalculators.com` domain + DNS (ALIAS @ → cname.vercel.com)
- [ ] SSL otomatik (Let's Encrypt) — doğrula
- [ ] **Google Search Console** kaydı + sitemap gönder
- [ ] **Bing Webmaster Tools** kaydı
- [ ] PageSpeed Insights testi (mobil 95+ hedef)

### 🟡 FAZ 2 — SEO derinleştirme (Hafta 2-4)  ⭐ EN ÖNCELİKLİ
- [ ] `/blog/` bölümü aç — ilk yazı: "How to Estimate Your LLM API Costs in 2026"
- [ ] Her hesaplayıcı için ayrı SEO landing içeriği (300+ kelime, H2'ler)
- [ ] İç linkleme: blog → hesaplayıcı, hesaplayıcı → blog
- [ ] Schema'ları test et → [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Core Web Vitals izle (CrUX / Search Console)
- [ ] Product Hunt + Hacker News + Dev.to lansmanı (backlink)
- [ ] Long-tail keyword sayfaları: "GPT-4o cost estimator", "Stripe vs Paddle fees"

### 🟢 FAZ 3 — Lokalizasyon (Ay 3)
- [ ] `de.` `fr.` `tr.` subdomain'leri (Vercel) — çeviri + hreflang
- [ ] TR: "API fiyat hesaplayıcı", "LLM maliyet hesaplama" keyword'leri
- [ ] Bölgesel para birimi (USD/EUR/TRY) IP-geolocation ile

### 🔵 FAZ 4 — Para kazanma (Ay 2-6)
- [ ] AdSense başvurusu (3-6 blog yazısı + 10K ziyaret sonrası)
- [ ] DigitalOcean + Supabase + Vercel affiliate onayları
- [ ] Affiliate tıklama dönüşüm takibi (GA4 events hazır)
- [ ] Premium tier planı (CSV export, alerts, API)

---

## 📊 SEO kontrol listesi (bu repoda HAZIR ✅)

| Öğe | Durum |
|---|---|
| Title + meta description (keyword-optimize) | ✅ |
| Open Graph + Twitter Card | ✅ |
| Canonical URL | ✅ |
| hreflang (en/de/fr/tr/x-default) | ✅ |
| Schema: Organization, SoftwareApplication, Breadcrumb, FAQ | ✅ |
| robots.txt (+ AI botlar + sitemap) | ✅ |
| sitemap.xml (hreflang'li) | ✅ |
| Güvenlik header'ları (HSTS, X-Frame, nosniff) | ✅ |
| Semantik HTML (header/main/section/footer, h1→h2) | ✅ |
| Mobil responsive + 48px dokunma hedefi | ✅ |
| Hızlı yükleme (render-blocking yok, inline CSS) | ✅ |
| Privacy + Terms + About (E-E-A-T) | ✅ |
| 404 sayfası | ✅ |

> ⚠️ **Fiyat sorumluluk reddi:** Hesaplayıcılardaki rakamlar 2026 kamuya açık fiyatlara dayalı *tahminlerdir*. Production bütçesi yapmadan önce sağlayıcının resmi fiyat sayfasından doğrulayın.

---

**Versiyon:** 1.0 · **Son güncelleme:** 2 Haziran 2026 · **Durum:** Production-ready
