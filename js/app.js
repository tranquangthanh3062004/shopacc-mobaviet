/**
 * TSHOP PRODUCTION APP CONTROLLER
 * Brand: TSHOP.VN - Premium Gaming Store
 * Handles State, Auth, Wallet, Recharges, Buying, Minigames, 3D Tilt UI, and Toast UI
 */

(function() {
    'use strict';

    // 1. Initial State
    const DEFAULT_STATE = {
        user: {
            isLoggedIn: true,
            id: 2953358,
            username: "tshop_vip",
            fullname: "VIP Pro Member",
            balance: 1000000, // 1.000.000đ initial test balance
            phone: "0987654321"
        },
        orders: [
            {
                orderId: "ORD-98412",
                accId: "EQQT16608",
                title: "Nick Liên Quân VIP - MS: EQQT16608",
                price: 500000,
                username: "tshop_acc16608",
                password: "Password@9921",
                twoFactor: "389 122",
                date: "12/11/2026 14:20"
            }
        ],
        transactions: [
            {
                id: "TX-10924",
                type: "ATM (VietQR)",
                amount: 1000000,
                status: "Thành công",
                date: "12/11/2026 14:15"
            }
        ]
    };

    // Load or initialize state
    function loadState() {
        try {
            const saved = localStorage.getItem('tshop_state') || localStorage.getItem('mobaviet_state');
            if (saved) return JSON.parse(saved);
        } catch (e) {
            console.error("State parse error", e);
        }
        return DEFAULT_STATE;
    }

    function saveState(state) {
        localStorage.setItem('tshop_state', JSON.stringify(state));
        localStorage.setItem('mobaviet_state', JSON.stringify(state));
    }

    window.AppState = loadState();

    // Utility: Format currency
    const formatMoney = window.formatMoney = function(num) {
        if (!num) return '0đ';
        return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.') + 'đ';
    };

    // Utility: Toast notification
    const showToast = window.showToast = function(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast-msg ${type}`;
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        toast.innerHTML = `<i class="fas ${icon}" style="font-size: 18px; color: ${type === 'success' ? '#2ecc71' : '#ff4757'};"></i> <span>${message}</span>`;
        
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3200);
    };

    // 2. Render Header Auth UI
    window.renderHeaderAuth = function() {
        const headerActions = document.getElementById('header-auth-actions');
        if (!headerActions) return;

        const user = window.AppState.user;
        if (user && user.isLoggedIn) {
            headerActions.innerHTML = `
                <div class="user-logged-box">
                    <div class="user-avatar">${user.username.charAt(0).toUpperCase()}</div>
                    <div class="user-meta">
                        <span class="user-name">${user.username}</span>
                        <span class="user-balance">${formatMoney(user.balance)}</span>
                    </div>
                    <a href="thong-tin.html" title="Tài khoản" style="color: #a0aec0; margin-left: 4px;"><i class="fas fa-cog"></i></a>
                    <button class="btn-logout" id="btn-logout" title="Đăng xuất"><i class="fas fa-sign-out-alt"></i></button>
                </div>
                <button class="btn-header btn-recharge" onclick="openRechargeModal('card')">
                    <i class="fas fa-plus-circle"></i> Nạp tiền
                </button>
            `;
            document.getElementById('btn-logout').onclick = handleLogout;
        } else {
            headerActions.innerHTML = `
                <button class="btn-header btn-login" onclick="openLoginModal()">
                    <i class="fas fa-user"></i> Đăng nhập
                </button>
                <button class="btn-header btn-register" onclick="openRegisterModal()">
                    <i class="fas fa-user-plus"></i> Đăng ký
                </button>
                <button class="btn-header btn-recharge" onclick="openRechargeModal('card')">
                    <i class="fas fa-wallet"></i> Nạp tiền
                </button>
            `;
        }
    };

    // 3. Auth Handlers
    function handleLogout() {
        window.AppState.user.isLoggedIn = false;
        saveState(window.AppState);
        window.renderHeaderAuth();
        showToast("Đã đăng xuất tài khoản!", "success");
    }

    // 3. Auth Modals
    const openLoginModal = window.openLoginModal = function() {
        const m = document.getElementById('loginModal');
        if (m) m.classList.add('show');
    };

    const openRegisterModal = window.openRegisterModal = function() {
        const m = document.getElementById('registerModal');
        if (m) m.classList.add('show');
    };

    const closeModal = window.closeModal = function(modalId) {
        const m = document.getElementById(modalId);
        if (m) m.classList.remove('show');
    };

    // 4. Modal Event Setup
    document.addEventListener('DOMContentLoaded', function() {
        window.renderHeaderAuth();
        setupFlashSaleCountdown();
        setupNoticeModal();
        initRechargeComponent();

        // Close modal on backdrop click
        document.querySelectorAll('.modal-backdrop').forEach(b => {
            b.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.classList.remove('show');
                }
            });
        });

        // Login Form Submit
        const loginForm = document.getElementById('form-login');
        if (loginForm) {
            loginForm.onsubmit = function(e) {
                e.preventDefault();
                const u = document.getElementById('login-username').value.trim();
                if (!u) {
                    showToast("Vui lòng nhập tên tài khoản", "error");
                    return;
                }
                window.AppState.user = {
                    isLoggedIn: true,
                    id: Math.floor(1000000 + Math.random() * 9000000),
                    username: u,
                    fullname: u,
                    balance: window.AppState.user?.balance || 500000,
                    phone: "09" + Math.floor(10000000 + Math.random() * 90000000)
                };
                saveState(window.AppState);
                window.renderHeaderAuth();
                closeModal('loginModal');
                showToast(`Chào mừng ${u} quay trở lại!`, "success");
            };
        }

        // Register Form Submit
        const regForm = document.getElementById('form-register');
        if (regForm) {
            regForm.onsubmit = function(e) {
                e.preventDefault();
                const u = document.getElementById('reg-username').value.trim();
                const p = document.getElementById('reg-password').value;
                const cp = document.getElementById('reg-confirm-password').value;
                if (!u || !p) {
                    showToast("Vui lòng nhập đầy đủ thông tin", "error");
                    return;
                }
                if (p !== cp) {
                    showToast("Mật khẩu xác nhận không khớp!", "error");
                    return;
                }
                window.AppState.user = {
                    isLoggedIn: true,
                    id: Math.floor(1000000 + Math.random() * 9000000),
                    username: u,
                    fullname: u,
                    balance: 500000, // Bonus 500k to test!
                    phone: "0987654321"
                };
                saveState(window.AppState);
                window.renderHeaderAuth();
                closeModal('registerModal');
                showToast(`Đăng ký thành công! Tặng ngay 500.000đ trải nghiệm.`, "success");
            };
        }
    });

    // 5. Flash Sale Countdown Timer
    function setupFlashSaleCountdown() {
        const timerBoxes = document.querySelectorAll('.flash-countdown .timer-box');
        if (!timerBoxes.length) return;

        let totalSeconds = 4 * 3600 + 45 * 60 + 20; // 4h 45m 20s
        setInterval(() => {
            if (totalSeconds > 0) totalSeconds--;
            const h = Math.floor(totalSeconds / 3600).toString().padStart(2, '0');
            const m = Math.floor((totalSeconds % 3600) / 60).toString().padStart(2, '0');
            const s = (totalSeconds % 60).toString().padStart(2, '0');

            if (timerBoxes[0]) timerBoxes[0].textContent = h;
            if (timerBoxes[1]) timerBoxes[1].textContent = m;
            if (timerBoxes[2]) timerBoxes[2].textContent = s;
        }, 1000);
    }

    // 6. Notice Modal (Popup announcement)
    function setupNoticeModal() {
        const notice = document.getElementById('noticeModal');
        if (!notice) return;
        const dismissed = sessionStorage.getItem('tshop_notice_dismissed');
        if (!dismissed) {
            setTimeout(() => {
                notice.classList.add('show');
            }, 600);
        }
    }

    window.dismissNotice = function(permanent = false) {
        if (permanent) sessionStorage.setItem('tshop_notice_dismissed', '1');
        closeModal('noticeModal');
    };

    // 7. Recharge Modal Logic (Cards & ATM/VietQR)
    const openRechargeModal = window.openRechargeModal = function(tab = 'card') {
        const m = document.getElementById('rechargeModal');
        if (!m) return;
        m.classList.add('show');
        switchRechargeTab(tab);
    };

    window.switchRechargeTab = function(tab) {
        const btnCard = document.getElementById('tab-btn-card');
        const btnAtm = document.getElementById('tab-btn-atm');
        const viewCard = document.getElementById('recharge-view-card');
        const viewAtm = document.getElementById('recharge-view-atm');

        if (tab === 'card') {
            if (btnCard) btnCard.classList.add('active');
            if (btnAtm) btnAtm.classList.remove('active');
            if (viewCard) viewCard.style.display = 'block';
            if (viewAtm) viewAtm.style.display = 'none';
        } else {
            if (btnAtm) btnAtm.classList.add('active');
            if (btnCard) btnCard.classList.remove('active');
            if (viewAtm) viewAtm.style.display = 'block';
            if (viewCard) viewCard.style.display = 'none';
            updateVietQR();
        }
    };

    function initRechargeComponent() {
        const selectTelecom = document.getElementById('recharge-telecom');
        const amountsGrid = document.getElementById('recharge-amounts-grid');
        if (!selectTelecom || !window.MOBAVIET_DATA) return;

        // Populate telecoms
        selectTelecom.innerHTML = window.MOBAVIET_DATA.telecoms.map(t => 
            `<option value="${t.id}">${t.name}</option>`
        ).join('');

        function renderAmounts(telecomId) {
            const tel = window.MOBAVIET_DATA.telecoms.find(t => t.id === telecomId) || window.MOBAVIET_DATA.telecoms[0];
            amountsGrid.innerHTML = tel.denominations.map((amt, idx) => `
                <div class="amount-pill ${idx === 3 ? 'selected' : ''}" data-val="${amt}">
                    ${formatMoney(amt)}
                </div>
            `).join('');

            amountsGrid.querySelectorAll('.amount-pill').forEach(pill => {
                pill.onclick = function() {
                    amountsGrid.querySelectorAll('.amount-pill').forEach(p => p.classList.remove('selected'));
                    this.classList.add('selected');
                };
            });
        }

        selectTelecom.onchange = (e) => renderAmounts(e.target.value);
        renderAmounts(selectTelecom.value);

        // Card form submit
        const formCard = document.getElementById('form-card-recharge');
        if (formCard) {
            formCard.onsubmit = function(e) {
                e.preventDefault();
                const pin = document.getElementById('card-pin').value.trim();
                const serial = document.getElementById('card-serial').value.trim();
                const selPill = amountsGrid.querySelector('.amount-pill.selected');
                const amount = selPill ? parseInt(selPill.getAttribute('data-val')) : 50000;

                if (!pin || pin.length < 8) {
                    showToast("Mã thẻ không hợp lệ (tối thiểu 8 ký tự)", "error");
                    return;
                }
                if (!serial || serial.length < 8) {
                    showToast("Số serial không hợp lệ", "error");
                    return;
                }

                // Simulate processing
                const submitBtn = formCard.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang nạp thẻ...';

                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Nạp thẻ ngay';

                    // Update user balance
                    window.AppState.user.balance += amount;
                    window.AppState.transactions.unshift({
                        id: "TX-" + Math.floor(10000 + Math.random() * 90000),
                        type: `Thẻ ${selectTelecom.value} (${formatMoney(amount)})`,
                        amount: amount,
                        status: "Thành công",
                        date: new Date().toLocaleString('vi-VN')
                    });
                    saveState(window.AppState);
                    window.renderHeaderAuth();
                    closeModal('rechargeModal');

                    showToast(`Nạp thẻ thành công! +${formatMoney(amount)} vào tài khoản.`, "success");
                    formCard.reset();
                }, 1000);
            };
        }

        // ATM amount change
        const atmAmountSelect = document.getElementById('atm-amount-select');
        if (atmAmountSelect) {
            atmAmountSelect.onchange = updateVietQR;
        }
    }

    function updateVietQR() {
        const atmAmountSelect = document.getElementById('atm-amount-select');
        const amount = atmAmountSelect ? parseInt(atmAmountSelect.value) : 100000;
        const user = window.AppState.user;
        const content = encodeURIComponent((window.MOBAVIET_DATA.bankInfo.syntaxPrefix + (user.username || 'GUEST')).trim());
        const qrUrl = window.MOBAVIET_DATA.bankInfo.qrTemplate
            .replace('{amount}', amount)
            .replace('{content}', content);

        const qrImg = document.getElementById('vietqr-image');
        if (qrImg) qrImg.src = qrUrl;

        const synElem = document.getElementById('atm-syntax-content');
        if (synElem) synElem.textContent = decodeURIComponent(content);
    }

    window.simulateAtmPayment = function() {
        const atmAmountSelect = document.getElementById('atm-amount-select');
        const amount = (atmAmountSelect && parseInt(atmAmountSelect.value)) ? parseInt(atmAmountSelect.value) : 100000;

        window.AppState.user.balance += amount;
        window.AppState.transactions.unshift({
            id: "TX-" + Math.floor(10000 + Math.random() * 90000),
            type: `ATM / VietQR (${formatMoney(amount)})`,
            amount: amount,
            status: "Thành công",
            date: new Date().toLocaleString('vi-VN')
        });
        saveState(window.AppState);
        window.renderHeaderAuth();
        closeModal('rechargeModal');
        showToast(`Hệ thống đã nhận thanh toán ATM! +${formatMoney(amount)}`, "success");
    };

    // 8. Account Purchase Flow
    window.purchaseAccount = function(accId) {
        const acc = window.MOBAVIET_DATA.accounts.find(a => a.id === accId);
        if (!acc) {
            showToast("Không tìm thấy thông tin tài khoản!", "error");
            return;
        }

        const user = window.AppState.user;
        if (!user || !user.isLoggedIn) {
            showToast("Vui lòng đăng nhập để mua tài khoản!", "error");
            openLoginModal();
            return;
        }

        if (user.balance < acc.priceNumeric) {
            const diff = acc.priceNumeric - user.balance;
            if (confirm(`Số dư không đủ! Bạn cần thêm ${formatMoney(diff)} để mua tài khoản này.\n\nNhấn OK để Nạp tiền ngay!`)) {
                openRechargeModal('card');
            }
            return;
        }

        if (confirm(`Xác nhận mua [${acc.code}] với giá ${formatMoney(acc.priceNumeric)}?`)) {
            // Deduct balance
            user.balance -= acc.priceNumeric;

            // Generate delivery credentials
            const fakeUser = "lq_" + acc.id.toLowerCase();
            const fakePass = "Moba@" + Math.floor(100000 + Math.random() * 900000);
            const fake2fa = Math.floor(100 + Math.random() * 900) + " " + Math.floor(100 + Math.random() * 900);

            // Add order
            const newOrder = {
                orderId: "ORD-" + Math.floor(10000 + Math.random() * 90000),
                accId: acc.id,
                title: acc.title,
                price: acc.priceNumeric,
                username: fakeUser,
                password: fakePass,
                twoFactor: fake2fa,
                date: new Date().toLocaleString('vi-VN')
            };
            window.AppState.orders.unshift(newOrder);

            // Add transaction
            window.AppState.transactions.unshift({
                id: "TX-" + Math.floor(10000 + Math.random() * 90000),
                type: `Mua acc ${acc.code}`,
                amount: -acc.priceNumeric,
                status: "Thành công",
                date: new Date().toLocaleString('vi-VN')
            });

            saveState(window.AppState);
            window.renderHeaderAuth();

            // Show Success Modal with credentials
            showPurchaseSuccessModal(newOrder);
        }
    };

    function showPurchaseSuccessModal(order) {
        const modal = document.getElementById('successModal');
        if (!modal) return;

        document.getElementById('success-acc-id').textContent = order.accId;
        document.getElementById('success-username').value = order.username;
        document.getElementById('success-password').value = order.password;
        document.getElementById('success-2fa').value = order.twoFactor;

        modal.classList.add('show');
        showToast("Mua tài khoản thành công!", "success");
    }

    // 9. Account Detail Modal
    window.openAccountDetailModal = function(accId) {
        const acc = window.MOBAVIET_DATA.accounts.find(a => a.id === accId);
        if (!acc) return;

        const modal = document.getElementById('accountDetailModal');
        if (!modal) return;

        document.getElementById('modal-detail-title').textContent = acc.title;
        document.getElementById('modal-detail-img').src = acc.image;
        document.getElementById('modal-detail-id').textContent = acc.code;
        document.getElementById('modal-detail-rank').textContent = acc.rank;
        document.getElementById('modal-detail-champs').textContent = acc.championsCount;
        document.getElementById('modal-detail-skins').textContent = acc.skinsCount;
        document.getElementById('modal-detail-status').textContent = acc.status;
        document.getElementById('modal-detail-price').textContent = acc.price;
        document.getElementById('modal-detail-oldprice').textContent = acc.oldPrice;

        const skinsContainer = document.getElementById('modal-detail-skins-list');
        if (skinsContainer) {
            skinsContainer.innerHTML = acc.featuredSkins.map(s => 
                `<span class="stat-chip" style="background: #eef2f6; font-size: 11px;"><i class="fas fa-magic" style="color: #32c5d2;"></i> ${s}</span>`
            ).join('');
        }

        const buyBtn = document.getElementById('modal-detail-buy-btn');
        if (buyBtn) {
            buyBtn.onclick = function() {
                closeModal('accountDetailModal');
                purchaseAccount(acc.id);
            };
        }

        modal.classList.add('show');
    };

    // 10. Copy Helper
    window.copyText = function(elementId) {
        const el = document.getElementById(elementId);
        if (!el) return;
        const text = el.value || el.textContent;
        navigator.clipboard.writeText(text).then(() => {
            showToast("Đã sao chép vào bộ nhớ tạm!", "success");
        });
    };

    // 11. 3D Tilt Effect on mousemove for Cards & Elements
    window.init3DTilt = function() {
        const cards = document.querySelectorAll('.account-card, .category-card, .top-charge-card, .hero-banner-slider');
        cards.forEach(card => {
            if (card.dataset.tiltInit) return;
            card.dataset.tiltInit = 'true';
            
            card.addEventListener('mousemove', function(e) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -8;
                const rotateY = ((x - centerX) / centerX) * 8;
                card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-8px) scale3d(1.02, 1.02, 1.02)`;
            });

            card.addEventListener('mouseleave', function() {
                card.style.transform = '';
            });
        });
    };

    // Auto-init 3D Tilt on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(window.init3DTilt, 200);
    });

})();
