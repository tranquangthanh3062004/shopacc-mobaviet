from bs4 import BeautifulSoup

with open('listing_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else "")

# Filters
print("\n--- FILTERS ---")
for f_form in soup.select('form, .form-filter, .filter-category, [class*="filter"]'):
    for select in f_form.select('select, input'):
        name = select.get('name')
        placeholder = select.get('placeholder', '')
        options = [o.get_text(strip=True) for o in select.select('option')[:5]]
        print(f"Filter Field: {name} (placeholder='{placeholder}'): {options}")

# Account Cards
print("\n--- ACCOUNT CARDS SAMPLE ---")
items = soup.select('.item-acc, .account-item, [class*="item_acc"], [class*="item-list"], .col-item')
print(f"Total account items found: {len(items)}")
for it in items[:3]:
    print("------------------------------------------")
    img = it.select_one('img')
    print("Image:", (img.get('data-src') or img.get('src')) if img else "None")
    print("Card Text:", it.get_text(separator=' | ', strip=True)[:300])

# Modals on listing page
print("\n--- MODALS ---")
for m in soup.select('.modal'):
    print(f"Modal ID: #{m.get('id')} class='{m.get('class')}'")
