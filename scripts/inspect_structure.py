from bs4 import BeautifulSoup

with open('mobaviet_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Body direct children:")
for child in soup.body.find_all(recursive=False):
    print(child.name, child.get('class'), child.get('id'))

print("\nAll main sections or containers:")
for elem in soup.find_all(['header', 'nav', 'main', 'footer', 'section', 'article']):
    print(elem.name, elem.get('class'), elem.get('id'))

print("\nDivs with class containing 'content' or 'body' or 'wrapper' or 'container':")
for div in soup.find_all('div'):
    classes = div.get('class', [])
    cls_str = " ".join(classes)
    if any(k in cls_str for k in ['content', 'layout', 'home', 'shop', 'service', 'category', 'banner', 'heading', 'title']):
        print(div.name, classes[:3], div.get('id'))
