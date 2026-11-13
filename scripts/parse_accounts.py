import json
from bs4 import BeautifulSoup
import re

with open('ajax_res.json', 'r', encoding='utf-8', errors='ignore') as f:
    res = json.load(f)

html = res.get('data', '')
soup = BeautifulSoup(html, 'html.parser')

accounts = []
for item in soup.select('.item_buy_list_in'):
    a = item.select_one('a[href*="/acc/"]')
    href = a.get('href') if a else ""
    ms_span = item.select_one('span')
    ms = ms_span.get_text(strip=True) if ms_span else ""
    img = item.select_one('img')
    img_src = img.get('data-src') or img.get('src') if img else ""
    
    desc_div = item.select_one('.item_buy_list_description .text-limit')
    desc = desc_div.get_text(strip=True) if desc_div else ""
    
    price_div = item.select_one('.item_buy_list_price')
    old_price_span = price_div.select_one('span') if price_div else None
    old_price = old_price_span.get_text(strip=True) if old_price_span else ""
    
    if price_div:
        # extract new price text
        all_txt = price_div.get_text(strip=True)
        new_price = all_txt.replace(old_price, '').strip()
    else:
        new_price = ""
        
    # count skins in desc
    skins = [s.strip() for s in desc.split(',') if s.strip()]
    
    accounts.append({
        'id': ms.replace('MS:', '').strip() or href.split('/')[-1],
        'title': f"Nick Liên Quân VIP - {ms}",
        'code': ms,
        'image': img_src,
        'oldPrice': old_price,
        'price': new_price,
        'priceNumeric': int(re.sub(r'[^\d]', '', new_price)) if re.sub(r'[^\d]', '', new_price) else 200000,
        'skinsCount': len(skins) if skins else 45,
        'championsCount': min(118, max(50, len(skins) + 20)),
        'rank': 'Cao Thủ' if 'Siêu việt' in desc or 'Thần Phượng' in desc else ('Tinh Anh' if len(skins) > 30 else 'Kim Cương'),
        'description': desc,
        'featuredSkins': skins[:8]
    })

print(f"Extracted {len(accounts)} accounts from page 1!")
for acc in accounts[:5]:
    print(acc['id'], acc['price'], acc['oldPrice'], acc['rank'], "Skins count:", acc['skinsCount'])

with open('mock_accounts.json', 'w', encoding='utf-8') as f:
    json.dump(accounts, f, ensure_ascii=False, indent=2)
