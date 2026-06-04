import os
base = r'C:\Users\muham\Desktop\APICalculators'
for lang in ['en', 'de', 'fr', 'tr']:
    blog_dir = os.path.join(base, 'blog') if lang == 'en' else os.path.join(base, lang, 'blog')
    if os.path.exists(blog_dir):
        files = sorted(f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html')
        print(lang + ':')
        for f in files:
            print('  ' + f)
