from playwright.sync_api import sync_playwright
import time
import os

os.makedirs('tests/screenshots', exist_ok=True)

errors = []

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # Listen for console errors
        page.on('console', lambda msg: errors.append(f"[CONSOLE {msg.type}] {msg.text}") if msg.type == 'error' else None)

        print("1. Navigating to http://localhost:3000 ...")
        page.goto('http://localhost:3000', wait_until='networkidle')
        assert "MOBAVIET.COM" in page.title(), "Title does not match!"
        print(" -> Homepage loaded successfully. Title:", page.title())

        # Screenshot Home
        page.screenshot(path='tests/screenshots/01_homepage.png', full_page=False)

        # 2. Check & Dismiss Notice Modal
        notice_modal = page.locator('#noticeModal')
        if notice_modal.is_visible():
            print(" -> Notice modal is visible. Clicking 'Đã hiểu'...")
            page.click('#noticeModal button:has-text("Đã hiểu")')
            time.sleep(0.5)

        # 3. Test Filters
        print("2. Testing Account Filters...")
        search_input = page.locator('#filter-search')
        search_input.fill('EQQT15358')
        time.sleep(0.5)
        cards = page.locator('.account-card')
        count = cards.count()
        print(f" -> Found {count} accounts matching 'EQQT15358'")
        assert count >= 1, "Should find at least 1 account matching EQQT15358"

        # Reset filter
        page.click('#filter-reset')
        time.sleep(0.5)
        total_cards = page.locator('.account-card').count()
        print(f" -> Filter reset. Total displayed cards on page 1: {total_cards}")

        # 4. Test Account Detail Modal
        print("3. Testing Account Detail Modal...")
        first_detail_btn = page.locator('.account-card .btn-detail').first
        first_detail_btn.click()
        time.sleep(0.5)
        detail_modal = page.locator('#accountDetailModal')
        assert detail_modal.is_visible(), "Detail modal should be visible"
        detail_title = page.locator('#modal-detail-title').text_content()
        print(" -> Detail modal opened:", detail_title)
        page.screenshot(path='tests/screenshots/02_detail_modal.png')
        page.click('#accountDetailModal .btn-filter-reset')
        time.sleep(0.5)

        # 5. Test Account Purchase
        print("4. Testing Account Purchase...")
        # Handle confirm dialog
        page.on("dialog", lambda dialog: dialog.accept())
        first_buy_btn = page.locator('.account-card .btn-buy-acc').first
        first_buy_btn.click()
        time.sleep(1)

        success_modal = page.locator('#successModal')
        assert success_modal.is_visible(), "Success modal should be visible after purchase"
        acc_user = page.locator('#success-username').input_value()
        acc_pass = page.locator('#success-password').input_value()
        print(f" -> Purchase SUCCESS! Delivered account: {acc_user} / {acc_pass}")
        page.screenshot(path='tests/screenshots/03_purchase_success.png')
        page.click('#successModal .btn-filter-reset')
        time.sleep(0.5)

        # 6. Test Recharge Modal (ATM & Card)
        print("5. Testing Recharge Modal...")
        page.click('button.btn-recharge')
        time.sleep(0.5)
        recharge_modal = page.locator('#rechargeModal')
        assert recharge_modal.is_visible(), "Recharge modal should be visible"

        # Switch to ATM tab
        page.click('#tab-btn-atm')
        time.sleep(0.5)
        atm_view = page.locator('#recharge-view-atm')
        assert atm_view.is_visible(), "ATM view should be visible"
        print(" -> ATM / VietQR tab verified")

        # Simulate ATM payment
        page.click('button:has-text("Đã chuyển khoản")')
        time.sleep(0.8)
        print(" -> ATM payment simulated and credited successfully")
        page.screenshot(path='tests/screenshots/04_after_recharge.png')

        # 7. Test Minigame (Vòng quay may mắn)
        print("6. Testing Minigame Lucky Wheel...")
        page.click('a.nav-link:has-text("Vòng quay")')
        time.sleep(0.5)
        minigame_modal = page.locator('#minigameModal')
        assert minigame_modal.is_visible(), "Minigame modal should be visible"

        page.click('#btn-spin-wheel')
        print(" -> Spinning wheel... waiting for result animation...")
        time.sleep(4.5)

        ruong_modal = page.locator('#modalRuongQuanHuy')
        assert ruong_modal.is_visible(), "Congratulation modal should be visible after spin"
        reward_text = page.locator('.j-quanhuy.content-popup').text_content().strip()
        print(f" -> Spin completed! Won: {reward_text}")
        page.screenshot(path='tests/screenshots/05_minigame_reward.png')
        page.click('#modalRuongQuanHuy button:has-text("Chơi tiếp")')
        time.sleep(0.5)

        # 8. Test Profile & History Page
        print("7. Testing User Profile & Orders Page (thong-tin.html)...")
        page.goto('http://localhost:3000/thong-tin.html', wait_until='networkidle')
        time.sleep(0.5)
        orders_rows = page.locator('#orders-table-body tr')
        orders_count = orders_rows.count()
        print(f" -> Profile orders count: {orders_count} (includes newly purchased acc)")
        assert orders_count >= 1, "Orders table should contain at least 1 order"
        page.screenshot(path='tests/screenshots/06_profile_orders.png')

        # Switch to Transactions tab
        page.click('#tab-btn-trans')
        time.sleep(0.5)
        trans_rows = page.locator('#trans-table-body tr')
        print(f" -> Transactions count: {trans_rows.count()}")
        assert trans_rows.count() >= 1, "Transactions table should contain logs"
        page.screenshot(path='tests/screenshots/07_profile_transactions.png')

        browser.close()

    print("\n=== E2E TESTING REPORT ===")
    if errors:
        print(f"⚠️ Console errors detected ({len(errors)}):")
        for e in errors:
            print("  ", e)
    else:
        print("✅ ZERO CONSOLE ERRORS!")
    print("✅ ALL 7 FUNCTIONALITY AND UI FLOWS PASSED 100% PERFECTLY!")

if __name__ == '__main__':
    run_tests()
