import urllib.request
import os

assets = {
    'logo.png': 'https://static3.mingame88.com/bp-cdn/upload/images/MwQ64eVbnQ_1735568235(1).png',
    'banner.png': 'https://static3.mingame88.com/bp-cdn/upload/images/33.png',
    'tuimu.png': 'https://static3.mingame88.com/bp-cdn/upload/fastcdn/acc-category-mobavietcom/153254/images/TUimu(1).png',
    'tuimu-vethan.png': 'https://static3.mingame88.com/bp-cdn/upload/fastcdn/acc-category-mobavietcom/153257/images/tuimuvethan.png',
    'sansale.gif': 'https://static3.mingame88.com/bp-cdn/upload/images/SANSALE.gif',
    'nick-vip.png': 'https://static3.mingame88.com/bp-cdn/upload/fastcdn/acc-category-mobavietcom/153116/images/NickLQVIP-1200x700.png',
    'thu-van-may.png': 'https://static3.mingame88.com/bp-cdn/upload/images/ThuVanMay_1200x700.png',
    'ban-qh.gif': 'https://static3.mingame88.com/bp-cdn/upload/fastcdn/service-config-Y0VOdmtLOFR3TTJseHQ0Q09QR1hMQT09/images/BANQH.gif',
    'ring.svg': 'https://mobaviet.com/assets/frontend/theme_1/image/nam/ring.svg',
    'profile-close.svg': 'https://mobaviet.com/assets/frontend/theme_1/image/nam/profile_close.svg',
    'close.svg': 'https://mobaviet.com/assets/frontend/theme_1/image/son/close.svg',
    'success.png': 'https://mobaviet.com/assets/frontend/theme_5/image/son/success.png'
}

os.makedirs('assets', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for fname, url in assets.items():
    dest = os.path.join('assets', fname)
    if not os.path.exists(dest):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp, open(dest, 'wb') as out:
                out.write(resp.read())
            print(f"Downloaded {fname} ({os.path.getsize(dest)} bytes)")
        except Exception as e:
            print(f"Failed {fname}: {e}")
