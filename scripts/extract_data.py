import re
from bs4 import BeautifulSoup
import json

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

data = {}

# 1. Header & navigation
nav_items = []
for a in soup.select('header a, nav a, .menu a, .nav a'):
    text = a.get_text(strip=True)
    href = a.get('href')
    if text and href:
        nav_items.append({'text': text, 'href': href})
data['nav_items'] = nav_items[:30]

# 2. Banners / Sliders
banners = []
for img in soup.select('.banner img, .slider img, .swiper-slide img, .carousel img'):
    src = img.get('src') or img.get('data-src')
    alt = img.get('alt', '')
    if src:
        banners.append({'src': src, 'alt': alt})
data['banners'] = banners[:10]

# 3. Top nap
top_nappers = []
for item in soup.select('.top-charge-item, .item-top, .ranking-item, [class*="top-nap"], [class*="top_charge"]'):
    top_nappers.append(item.get_text(separator=' ', strip=True))
data['top_nappers'] = top_nappers[:10]

# 4. Service / Category cards
categories = []
for box in soup.select('.item_category, .box-category, .service-item, .item-game, .content-item, .card-item, .category-item'):
    title = box.select_one('.title, h2, h3, h4, .name')
    title_text = title.get_text(strip=True) if title else ""
    img = box.select_one('img')
    img_src = (img.get('src') or img.get('data-src')) if img else ""
    count_text = box.select_one('.count, .quantity, .total, .amount, .description')
    categories.append({
        'title': title_text,
        'img': img_src,
        'info': count_text.get_text(strip=True) if count_text else box.get_text(separator=' | ', strip=True)[:100]
    })
data['categories'] = categories[:30]

# 5. Look for account listings / products
accounts = []
for acc in soup.select('.item-acc, .account-item, .card-acc, [class*="acc-item"]'):
    accounts.append(acc.get_text(separator=' | ', strip=True)[:150])
data['accounts'] = accounts[:10]

# 6. Footer info
footer = soup.select_one('footer, .footer')
data['footer'] = footer.get_text(separator='\n', strip=True)[:1000] if footer else ""

# 7. Check all unique images
images = []
for img in soup.select('img'):
    src = img.get('src') or img.get('data-src')
    if src and src not in images and not src.startswith('data:'):
        images.append(src)
data['image_count'] = len(images)
data['sample_images'] = images[:25]

with open('site_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved site_analysis.json. Summary:")
print("Nav items:", len(data['nav_items']))
print("Banners:", len(data['banners']))
print("Categories:", len(data['categories']))
print("Top nappers:", len(data['top_nappers']))
print("Sample images:", len(data['sample_images']))
