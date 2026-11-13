import re

with open('listing_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Look for ajax calls or endpoints
endpoints = re.findall(r'url\s*:\s*[\'"]([^\'"]+)[\'"]', html)
print("AJAX URLs in listing page:")
for u in set(endpoints):
    print(" -", u)

# Check load data or account list container ID
containers = re.findall(r'id=[\'"]([^\'"]*acc[^\'"]*|[^\'"]*list[^\'"]*|[^\'"]*data[^\'"]*)[\'"]', html, re.I)
print("\nContainers:", set(containers))

# Check inline scripts
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nInline scripts count: {len(scripts)}")
for i, s in enumerate(scripts):
    if 'ajax' in s or 'load' in s or 'fetch' in s:
        print(f"--- Script {i} ---")
        print(s[:500])
