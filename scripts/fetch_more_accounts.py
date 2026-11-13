import urllib.request
import json
from bs4 import BeautifulSoup
import re

headers = {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

all_accounts = []

for page in [1, 2, 3]:
    url = f"https://mobaviet.com/mua-acc/nick-lien-quan-vip?page={page}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            html = res.get('data', '')
            soup = BeautifulSoup(html, 'html.parser')
            
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
                    all_txt = price_div.get_text(strip=True)
                    new_price = all_txt.replace(old_price, '').strip()
                else:
                    new_price = ""
                    
                skins = [s.strip() for s in desc.split(',') if s.strip()]
                
                acc_id = ms.replace('MS:', '').strip() or (href.split('/')[-1] if href else f"LQ{len(all_accounts)+1000}")
                
                all_accounts.append({
                    'id': acc_id,
                    'title': f"Nick Liên Quân VIP - {ms or acc_id}",
                    'code': ms or f"MS: {acc_id}",
                    'image': img_src,
                    'oldPrice': old_price or "500.000đ",
                    'price': new_price or "250.000đ",
                    'priceNumeric': int(re.sub(r'[^\d]', '', new_price)) if re.sub(r'[^\d]', '', new_price) else 250000,
                    'skinsCount': len(skins) if skins else 45,
                    'championsCount': min(118, max(50, len(skins) + 20)),
                    'rank': 'Thách Đấu' if len(skins) > 120 else ('Cao Thủ' if len(skins) > 60 else ('Tinh Anh' if len(skins) > 25 else 'Kim Cương')),
                    'status': 'Trắng Thông Tin' if len(all_accounts) % 2 == 0 else 'Có SĐT (Đổi được)',
                    'description': desc,
                    'featuredSkins': skins[:10]
                })
        print(f"Loaded page {page}, total accounts now: {len(all_accounts)}")
    except Exception as e:
        print(f"Error loading page {page}: {e}")

with open('mock_accounts_full.json', 'w', encoding='utf-8') as f:
    json.dump(all_accounts, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(all_accounts)} accounts into mock_accounts_full.json!")
