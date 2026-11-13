import json
from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

sections = []

for ci in soup.select('.content-items'):
    heading_elem = ci.select_one('.items-title')
    heading = heading_elem.get_text(strip=True) if heading_elem else "Danh Mục"
    
    items = []
    # Find all items in this section
    for card in ci.select('.col-6, .col-lg-3, .col-sm-6'):
        title_el = card.select_one('.game-list-title, .title')
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        img_el = card.select_one('img')
        img_src = (img_el.get('data-src') or img_el.get('src')) if img_el else ""
        if img_src.startswith('//'):
            img_src = 'https:' + img_src
            
        desc_el = card.select_one('.game-list-description, .game-list-total')
        desc = desc_el.get_text(strip=True) if desc_el else ""
        
        link_el = card.select_one('a')
        href = link_el.get('href') if link_el else ""
        
        # Check if already added
        if not any(x['title'] == title for x in items):
            items.append({
                'title': title,
                'image': img_src,
                'count': desc,
                'link': href
            })
            
    if items:
        sections.append({
            'heading': heading,
            'items': items
        })

print(f"Extracted {len(sections)} sections:")
for s in sections:
    print(f"== {s['heading']} ({len(s['items'])} items) ==")
    for it in s['items']:
        print(f"  * {it['title']} - {it['count']} -> {it['image']}")

with open('mock_sections.json', 'w', encoding='utf-8') as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)
