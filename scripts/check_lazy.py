from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

for ci in soup.select('.content-items'):
    for item in ci.select('.item, .col-item, [class*="game-list"]'):
        img = item.select_one('img')
        if img:
            print("Attrs:", {k: v for k, v in img.attrs.items() if k in ['src', 'data-src', 'data-original', 'class', 'lazy-src']})
