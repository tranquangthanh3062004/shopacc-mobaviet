from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

modal = soup.find(id='rechargeModal')
if modal:
    print(modal.prettify()[:3000])
