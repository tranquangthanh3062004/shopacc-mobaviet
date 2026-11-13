from bs4 import BeautifulSoup
import re

with open('listing_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Look for divs with class containing 'item' or 'card':")
cards = []
for div in soup.find_all('div'):
    cls = " ".join(div.get('class', []))
    if any(k in cls for k in ['item', 'card', 'box-account', 'col-']):
        if div.find('a', href=re.compile(r'/acc/|/mua-acc/|/tai-khoan/')):
            cards.append(div)

print(f"Found {len(cards)} card elements")
if cards:
    print(cards[0].prettify()[:1000])

# Check all links containing acc
acc_links = soup.find_all('a', href=re.compile(r'/acc/|/mua-acc/\d+|/tai-khoan/\d+'))
print(f"Account detail links: {len(acc_links)}")
for a in acc_links[:5]:
    print(a.get('href'), a.get_text(strip=True))
