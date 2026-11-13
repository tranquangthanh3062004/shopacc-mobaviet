from bs4 import BeautifulSoup
import re

with open('ajax_accounts.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else "No title")

# Check if there is an account card or list
for a in soup.find_all('a', href=re.compile(r'/acc/')):
    print("Found acc link:", a.get('href'), a.get_text(strip=True)[:100])

# Look for text with 'MS' or 'Mã số' or 'Tướng' or 'Trang phục'
cards = []
for div in soup.find_all(['div', 'article']):
    txt = div.get_text(separator=' ', strip=True)
    if 'Tướng' in txt and 'Trang phục' in txt and ('đ' in txt or 'VNĐ' in txt or 'k' in txt):
        if len(txt) < 400:
            cards.append(div)

print(f"Found {len(cards)} card candidates")
if cards:
    print(cards[0].prettify()[:1000])
