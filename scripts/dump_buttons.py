from bs4 import BeautifulSoup

with open('acc_detail_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

for btn in soup.select('button, .btn, a.btn, input[type="submit"]'):
    print(btn.name, btn.get('class'), btn.get('id'), btn.get_text(strip=True)[:50])

print("\n--- Forms ---")
for f in soup.select('form'):
    print(f.get('action'), f.get('method'), f.get('id'), f.get('class'))
