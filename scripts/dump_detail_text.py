from bs4 import BeautifulSoup

with open('acc_detail_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

main_content = soup.select_one('.content, .main-lay-out, main, .c-layout-page')
if main_content:
    print(main_content.get_text(separator='\n', strip=True)[:2500])
