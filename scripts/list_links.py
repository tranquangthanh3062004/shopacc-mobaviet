from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

links = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    links.add(href)

print(f"Total links: {len(links)}")
for l in sorted(links):
    if not l.startswith('javascript') and not l.startswith('#'):
        print(l)
