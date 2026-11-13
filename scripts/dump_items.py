from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("--- ITEMS TITLES ---")
for it in soup.select('.items-title'):
    print(it.get_text(strip=True))

print("\n--- GAME LIST TITLES ---")
for gt in soup.select('.game-list-title'):
    print(gt.get_text(strip=True))

print("\n--- ITEMS CONTAINERS ---")
for ci in soup.select('.content-items'):
    heading = ci.select_one('.items-title')
    print("CATEGORY SECTION:", heading.get_text(strip=True) if heading else "No heading")
    for item in ci.select('.item, .col-item, [class*="game-list"]'):
        title = item.select_one('.game-list-title, .title, h3, h4, .name')
        if title:
            # find count or extra text
            txt = item.get_text(separator=' | ', strip=True)
            img = item.select_one('img')
            img_src = img.get('src') or img.get('data-src') if img else None
            print(f"   -> {title.get_text(strip=True)} | Image: {img_src}")
            # print description or stats
            desc = item.select_one('.game-list-description, .description, .game-list-total')
            if desc:
                print(f"      Stats: {desc.get_text(strip=True)}")
