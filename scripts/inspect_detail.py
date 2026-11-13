from bs4 import BeautifulSoup

with open('acc_detail_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else "")

# Key details
price = soup.select_one('[class*="price"]')
print("Price element:", price.get_text(strip=True) if price else "Not found")

# Images / Gallery
gallery = []
for img in soup.select('.item_buy_list_img img, .gallery img, .slider-for img, .swiper-slide img, [class*="detail"] img'):
    s = img.get('data-src') or img.get('src')
    if s:
        gallery.append(s)
print(f"Gallery images ({len(gallery)}):", gallery[:8])

# Attribute table or list (Tướng, Trang phục, Rank, v.v.)
for row in soup.select('.row, tr, [class*="attribute"], [class*="info"]'):
    txt = row.get_text(separator=' : ', strip=True)
    if any(k in txt for k in ['Tướng', 'Trang phục', 'Rank', 'Đăng ký', 'Mã số', 'Giá tiền']):
        if len(txt) < 150:
            print("Attribute:", txt)

# Buy button or form
buy_btn = soup.select_one('[class*="btn-buy"], [class*="buy"], form[action*="buy"]')
print("Buy button/form:", buy_btn.prettify()[:300] if buy_btn else "Not found")
