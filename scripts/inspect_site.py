import re
from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else "No title")

# CSS links
css_links = []
for link in soup.find_all('link', rel='stylesheet'):
    href = link.get('href')
    if href:
        css_links.append(href)
print(f"\nCSS Files ({len(css_links)}):")
for c in css_links:
    print(" -", c)

# JS scripts
js_scripts = []
for s in soup.find_all('script', src=True):
    src = s.get('src')
    if src:
        js_scripts.append(src)
print(f"\nJS Scripts ({len(js_scripts)}):")
for j in js_scripts:
    print(" -", j)

# Check main sections/navigation
nav = soup.find('nav') or soup.find('header')
print("\nHeader/Nav text preview:")
if nav:
    print(nav.get_text(separator=' | ', strip=True)[:300])

# Sections or main elements
print("\nMajor elements/IDs/classes:")
for div in soup.find_all(['section', 'div'], id=True)[:15]:
    print(f" - #{div.get('id')} class='{div.get('class')}'")

# Look for categories / games / account lists
categories = soup.find_all(['div', 'a'], class_=lambda x: x and ('category' in x or 'box' in x or 'card' in x or 'item' in x))
print(f"\nFound {len(categories)} potential category/card items")
