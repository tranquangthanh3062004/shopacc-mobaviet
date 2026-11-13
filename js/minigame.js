/**
 * MOBAVIET MINIGAME CONTROLLER
 * Interactive Lucky Wheel & Mystery Chest (Rương Quân Huy)
 */

(function() {
    'use strict';

    let isSpinning = false;
    const SPIN_COST = 20000;

    const showToast = (...args) => window.showToast ? window.showToast(...args) : console.log(...args);
    const openLoginModal = (...args) => window.openLoginModal && window.openLoginModal(...args);
    const closeModal = (...args) => window.closeModal && window.closeModal(...args);
    const openRechargeModal = (...args) => window.openRechargeModal && window.openRechargeModal(...args);
    const saveState = (s) => localStorage.setItem('mobaviet_state', JSON.stringify(s));

    window.openMinigameModal = function() {
        const m = document.getElementById('minigameModal');
        if (m) {
            m.classList.add('show');
            drawWheel();
        }
    };

    function drawWheel() {
        const canvas = document.getElementById('wheelCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const prizes = window.MOBAVIET_DATA.luckyWheelPrizes;
        const numPrizes = prizes.length;
        const arc = (2 * Math.PI) / numPrizes;
        const radius = canvas.width / 2;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        prizes.forEach((prize, i) => {
            const angle = i * arc;
            ctx.beginPath();
            ctx.fillStyle = prize.color;
            ctx.moveTo(radius, radius);
            ctx.arc(radius, radius, radius - 6, angle, angle + arc);
            ctx.lineTo(radius, radius);
            ctx.fill();
            ctx.stroke();

            // Text
            ctx.save();
            ctx.translate(radius, radius);
            ctx.rotate(angle + arc / 2);
            ctx.textAlign = "right";
            ctx.fillStyle = "#fff";
            ctx.font = "bold 13px 'Montserrat', sans-serif";
            ctx.shadowColor = "rgba(0,0,0,0.4)";
            ctx.shadowBlur = 4;
            ctx.fillText(prize.name, radius - 20, 5);
            ctx.restore();
        });

        // Center circle
        ctx.beginPath();
        ctx.arc(radius, radius, 25, 0, 2 * Math.PI);
        ctx.fillStyle = "#1e222d";
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = "#32c5d2";
        ctx.stroke();

        ctx.fillStyle = "#fff";
        ctx.font = "bold 11px 'Montserrat', sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("QUAY", radius, radius);
    }

    window.spinWheel = function() {
        if (isSpinning) return;

        const user = window.AppState.user;
        if (!user || !user.isLoggedIn) {
            showToast("Vui lòng đăng nhập để tham gia quay thưởng!", "error");
            openLoginModal();
            return;
        }

        if (user.balance < SPIN_COST) {
            if (confirm(`Số dư không đủ! Mỗi lượt quay cần 20.000đ. Nhấn OK để Nạp tiền ngay!`)) {
                closeModal('minigameModal');
                openRechargeModal('card');
            }
            return;
        }

        // Deduct cost
        user.balance -= SPIN_COST;
        saveState(window.AppState);
        if (window.renderHeaderAuth) window.renderHeaderAuth();

        isSpinning = true;
        const spinBtn = document.getElementById('btn-spin-wheel');
        if (spinBtn) spinBtn.disabled = true;

        const prizes = window.MOBAVIET_DATA.luckyWheelPrizes;
        const targetIndex = Math.floor(Math.random() * prizes.length);
        const winningPrize = prizes[targetIndex];

        const canvas = document.getElementById('wheelCanvas');
        const degreesPerSlice = 360 / prizes.length;
        const stopAngle = 360 - (targetIndex * degreesPerSlice + degreesPerSlice / 2);
        const totalRotation = 360 * 5 + stopAngle;

        let currentRotation = 0;
        const startTime = performance.now();
        const duration = 4000;

        function animate(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            currentRotation = ease * totalRotation;

            if (canvas) {
                canvas.style.transform = `rotate(${currentRotation}deg)`;
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                isSpinning = false;
                if (spinBtn) spinBtn.disabled = false;
                handleSpinResult(winningPrize);
            }
        }

        requestAnimationFrame(animate);
    };

    function handleSpinResult(prize) {
        const modalRuong = document.getElementById('modalRuongQuanHuy');
        const contentPopup = document.querySelector('.j-quanhuy.content-popup');

        if (prize.type === 'money') {
            window.AppState.user.balance += prize.val;
            saveState(window.AppState);
            if (window.renderHeaderAuth) window.renderHeaderAuth();
        }

        window.AppState.transactions.unshift({
            id: "SPIN-" + Math.floor(10000 + Math.random() * 90000),
            type: `Vòng quay: ${prize.name}`,
            amount: prize.type === 'money' ? prize.val - SPIN_COST : -SPIN_COST,
            status: "Thành công",
            date: new Date().toLocaleString('vi-VN')
        });
        saveState(window.AppState);

        if (contentPopup) {
            contentPopup.innerHTML = `
                <div style="font-size: 18px; font-weight: 800; color: #ff4757; margin-bottom: 8px;">
                    ${prize.name}
                </div>
                <p style="color: #64748b; font-size: 13px;">Phần thưởng đã được cộng vào tài khoản của bạn!</p>
            `;
        }

        closeModal('minigameModal');
        if (modalRuong) modalRuong.classList.add('show');
        showToast(`Chúc mừng bạn nhận được: ${prize.name}!`, "success");
    }

})();
