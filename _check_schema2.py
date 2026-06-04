import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\muham\Desktop\APICalculators'

for lang in ['en', 'de', 'fr', 'tr']:
    blog_dir = os.path.join(BASE, 'blog') if lang == 'en' else os.path.join(BASE, lang, 'blog')
    files = sorted(f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html')
    print(f'\n=== {lang.upper()} ===')
    for fname in files:
        c = open(os.path.join(blog_dir, fname), encoding='utf-8').read()
        has_article = '"@type":"Article"' in c or '"@type": "Article"' in c
        has_faq = 'FAQPage' in c
        has_breadcrumb = 'BreadcrumbList' in c
        print(f'  {fname}: Article={has_article} FAQ={has_faq} Breadcrumb={has_breadcrumb}')
