/**
 * MOBAVIET FILTER & LISTING CONTROLLER
 * Handles Real-time search, filters, sorting, and pagination
 */

(function() {
    'use strict';

    let currentPage = 1;
    const ITEMS_PER_PAGE = 8;
    let filteredList = [];

    window.initAccountFilter = function() {
        if (!window.MOBAVIET_DATA || !window.MOBAVIET_DATA.accounts) return;
        filteredList = [...window.MOBAVIET_DATA.accounts];
        
        setupFilterListeners();
        applyFilter();
    };

    function setupFilterListeners() {
        const searchInput = document.getElementById('filter-search');
        const priceSelect = document.getElementById('filter-price');
        const rankSelect = document.getElementById('filter-rank');
        const statusSelect = document.getElementById('filter-status');
        const sortSelect = document.getElementById('filter-sort');
        const resetBtn = document.getElementById('filter-reset');

        if (searchInput) searchInput.addEventListener('input', debounce(applyFilter, 250));
        if (priceSelect) priceSelect.addEventListener('change', applyFilter);
        if (rankSelect) rankSelect.addEventListener('change', applyFilter);
        if (statusSelect) statusSelect.addEventListener('change', applyFilter);
        if (sortSelect) sortSelect.addEventListener('change', applyFilter);

        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                if (searchInput) searchInput.value = '';
                if (priceSelect) priceSelect.value = 'all';
                if (rankSelect) rankSelect.value = 'all';
                if (statusSelect) statusSelect.value = 'all';
                if (sortSelect) sortSelect.value = 'newest';
                applyFilter();
            });
        }
    }

    function applyFilter() {
        const search = document.getElementById('filter-search')?.value.toLowerCase().trim() || '';
        const price = document.getElementById('filter-price')?.value || 'all';
        const rank = document.getElementById('filter-rank')?.value || 'all';
        const status = document.getElementById('filter-status')?.value || 'all';
        const sort = document.getElementById('filter-sort')?.value || 'newest';

        filteredList = window.MOBAVIET_DATA.accounts.filter(acc => {
            // Search filter
            if (search) {
                const matchId = acc.code.toLowerCase().includes(search) || acc.id.toLowerCase().includes(search);
                const matchDesc = acc.description.toLowerCase().includes(search);
                if (!matchId && !matchDesc) return false;
            }

            // Price filter
            if (price !== 'all') {
                const p = acc.priceNumeric;
                if (price === 'under100' && p >= 100000) return false;
                if (price === '100to300' && (p < 100000 || p > 300000)) return false;
                if (price === '300to1m' && (p < 300000 || p > 1000000)) return false;
                if (price === 'over1m' && p <= 1000000) return false;
            }

            // Rank filter
            if (rank !== 'all' && acc.rank !== rank) {
                return false;
            }

            // Status filter
            if (status !== 'all' && acc.status !== status) {
                return false;
            }

            return true;
        });

        // Sorting
        if (sort === 'price_asc') {
            filteredList.sort((a, b) => a.priceNumeric - b.priceNumeric);
        } else if (sort === 'price_desc') {
            filteredList.sort((a, b) => b.priceNumeric - a.priceNumeric);
        } else if (sort === 'skins_desc') {
            filteredList.sort((a, b) => b.skinsCount - a.skinsCount);
        }

        currentPage = 1;
        renderAccounts();
    }

    function renderAccounts() {
        const container = document.getElementById('accounts-container');
        const countBadge = document.getElementById('filter-result-count');
        const paginationWrap = document.getElementById('accounts-pagination');

        if (!container) return;

        if (countBadge) {
            countBadge.textContent = `(${filteredList.length} tài khoản)`;
        }

        if (filteredList.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: #fff; border-radius: 12px; border: 1px dashed #cbd5e1;">
                    <i class="fas fa-search" style="font-size: 36px; color: #94a3b8; margin-bottom: 12px;"></i>
                    <h3 style="font-size: 16px; font-weight: 700; color: #334155;">Không tìm thấy tài khoản phù hợp</h3>
                    <p style="font-size: 13px; color: #64748b; margin-top: 6px;">Vui lòng thử lại với các tiêu chí lọc khác.</p>
                </div>
            `;
            if (paginationWrap) paginationWrap.innerHTML = '';
            return;
        }

        // Pagination slice
        const totalPages = Math.ceil(filteredList.length / ITEMS_PER_PAGE);
        const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
        const pageItems = filteredList.slice(startIndex, startIndex + ITEMS_PER_PAGE);

        container.innerHTML = pageItems.map(acc => `
            <div class="account-card">
                <div class="account-thumb">
                    <img src="${acc.image}" alt="${acc.code}" loading="lazy" onerror="this.src='assets/nick-vip.png'">
                    <span class="account-id-tag">${acc.code}</span>
                    <span class="account-rank-badge">${acc.rank}</span>
                </div>
                <div class="account-body">
                    <div class="account-stats">
                        <span class="stat-chip"><i class="fas fa-shield-alt"></i> ${acc.championsCount} Tướng</span>
                        <span class="stat-chip"><i class="fas fa-vest"></i> ${acc.skinsCount} Trang phục</span>
                    </div>
                    <div class="account-skins-preview" title="${acc.description}">
                        ${acc.featuredSkins.slice(0, 4).join(', ') || 'Full ngọc chuẩn rank, tướng hot meta'}
                    </div>
                    <div class="account-price-box">
                        <span class="price-current">${acc.price}</span>
                        <span class="price-old">${acc.oldPrice}</span>
                    </div>
                    <div class="account-actions">
                        <button class="btn-detail" onclick="openAccountDetailModal('${acc.id}')">
                            <i class="fas fa-eye"></i> Chi tiết
                        </button>
                        <button class="btn-buy-acc" onclick="purchaseAccount('${acc.id}')">
                            <i class="fas fa-shopping-cart"></i> Mua ngay
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        // Render Pagination
        if (paginationWrap) {
            if (totalPages <= 1) {
                paginationWrap.innerHTML = '';
            } else {
                let html = '';
                for (let i = 1; i <= totalPages; i++) {
                    html += `
                        <button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="window.goToAccountPage(${i})">
                            ${i}
                        </button>
                    `;
                }
                paginationWrap.innerHTML = html;
            }
        }
    }

    window.goToAccountPage = function(page) {
        currentPage = page;
        renderAccounts();
        document.getElementById('accounts-section')?.scrollIntoView({ behavior: 'smooth' });
    };

    function debounce(fn, delay) {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

})();
