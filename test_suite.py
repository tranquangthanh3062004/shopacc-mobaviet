import urllib.request
import json
import sys

BASE_URL = 'http://localhost:3000'

endpoints = [
    ('/', 200, 'text/html'),
    ('/index.html', 200, 'text/html'),
    ('/thong-tin.html', 200, 'text/html'),
    ('/css/style.css', 200, 'text/css'),
    ('/js/data.js', 200, 'application/javascript'),
    ('/js/app.js', 200, 'application/javascript'),
    ('/js/filter.js', 200, 'application/javascript'),
    ('/js/minigame.js', 200, 'application/javascript'),
    ('/assets/logo.png', 200, 'image/png'),
    ('/assets/banner.png', 200, 'image/png'),
    ('/assets/tuimu.png', 200, 'image/png'),
    ('/assets/nick-vip.png', 200, 'image/png')
]

print("=== STARTING MOBAVIET TEST SUITE ===")
all_passed = True

for path, expected_status, expected_mime in endpoints:
    url = BASE_URL + path
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            status = res.status
            content_type = res.headers.get('Content-Type', '')
            length = len(res.read())
            
            status_ok = (status == expected_status)
            mime_ok = expected_mime in content_type
            
            if status_ok and mime_ok and length > 0:
                print(f" [PASS] {path:<25} Status: {status} | Size: {length:>7} bytes | Content-Type: {content_type}")
            else:
                print(f" [FAIL] {path:<25} Status: {status} (exp {expected_status}) | MIME: {content_type}")
                all_passed = False
    except Exception as e:
        print(f" [ERROR] {path:<25} -> {e}")
        all_passed = False

if all_passed:
    print("\n✅ ALL ENDPOINTS AND ASSETS VERIFIED SUCCESSFULLY!")
else:
    print("\n❌ SOME TESTS FAILED.")
    sys.exit(1)
