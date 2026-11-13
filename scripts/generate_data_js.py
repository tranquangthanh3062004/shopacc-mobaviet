import json

with open('mock_accounts_full.json', 'r', encoding='utf-8') as f:
    accounts = json.load(f)

with open('mock_sections.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

top_nappers = [
    {"rank": 1, "username": "****8top", "amount": 5500000, "reward": "5.000 Quân Huy + Nick VIP 500k"},
    {"rank": 2, "username": "****nthien221", "amount": 3500000, "reward": "3.000 Quân Huy + Nick VIP 300k"},
    {"rank": 3, "username": "****pe373", "amount": 2200000, "reward": "2.000 Quân Huy"},
    {"rank": 4, "username": "****depzai", "amount": 450000, "reward": "500 Quân Huy"},
    {"rank": 5, "username": "****mi3", "amount": 310000, "reward": "300 Quân Huy"}
]

telecoms = [
    {
        "id": "VIETTEL", "name": "Viettel (Tự động 30s)", "discount": "0%",
        "denominations": [10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
    },
    {
        "id": "VINAPHONE", "name": "Vinaphone (Tự động 30s)", "discount": "0%",
        "denominations": [10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000]
    },
    {
        "id": "MOBIFONE", "name": "Mobifone (Tự động 30s)", "discount": "0%",
        "denominations": [10000, 20000, 30000, 50000, 100000, 200000, 300000, 500000]
    },
    {
        "id": "GARENA", "name": "Thẻ Garena (+10% giá trị)", "discount": "+10%",
        "denominations": [20000, 50000, 100000, 200000, 500000]
    },
    {
        "id": "ZING", "name": "Thẻ Zing (+5% giá trị)", "discount": "+5%",
        "denominations": [20000, 50000, 100000, 200000, 500000]
    }
]

bank_info = {
    "bankName": "MB BANK (Ngân hàng Quân Đội)",
    "accountNumber": "0362443838",
    "accountHolder": "NGUYEN VAN THOAI (MOBAVIET)",
    "qrTemplate": "https://api.vietqr.io/image/970422-0362443838-compact2.png?amount={amount}&addInfo={content}&accountName=NGUYEN%20VAN%20THOAI",
    "syntaxPrefix": "MOBAVIET NAP "
}

lucky_wheel_prizes = [
    {"id": 1, "name": "999 Quân Huy", "type": "qh", "val": 999, "chance": 5, "color": "#f1c40f"},
    {"id": 2, "name": "Nick Full Tướng", "type": "acc", "val": "FULL_CHAMPS", "chance": 10, "color": "#e74c3c"},
    {"id": 3, "name": "100.000 VNĐ", "type": "money", "val": 100000, "chance": 15, "color": "#9b59b6"},
    {"id": 4, "name": "50.000 VNĐ", "type": "money", "val": 50000, "chance": 25, "color": "#3498db"},
    {"id": 5, "name": "20.000 VNĐ", "type": "money", "val": 20000, "chance": 30, "color": "#2ecc71"},
    {"id": 6, "name": "Chúc Bạn May Mắn", "type": "empty", "val": 0, "chance": 15, "color": "#34495e"}
]

js_content = f"""// Mobaviet Data Layer
window.MOBAVIET_DATA = {{
    categories: {json.dumps(sections, ensure_ascii=False, indent=2)},
    accounts: {json.dumps(accounts, ensure_ascii=False, indent=2)},
    topNappers: {json.dumps(top_nappers, ensure_ascii=False, indent=2)},
    telecoms: {json.dumps(telecoms, ensure_ascii=False, indent=2)},
    bankInfo: {json.dumps(bank_info, ensure_ascii=False, indent=2)},
    luckyWheelPrizes: {json.dumps(lucky_wheel_prizes, ensure_ascii=False, indent=2)}
}};
"""

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated js/data.js ({len(accounts)} accounts, {len(sections)} sections)")
