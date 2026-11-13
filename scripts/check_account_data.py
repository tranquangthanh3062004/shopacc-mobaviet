from bs4 import BeautifulSoup

with open('listing_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

account_data = soup.find(id='account_data')
if account_data:
    print("Found #account_data!")
    print(account_data.prettify()[:2500])
else:
    print("#account_data not found directly")
