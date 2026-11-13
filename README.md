# MOBAVIET.COM - Production Web Clone

[![Deploy to GitHub Pages](https://github.com/tranquangthanh3062004/shopacc-mobaviet/actions/workflows/deploy.yml/badge.svg)](https://github.com/tranquangthanh3062004/shopacc-mobaviet/actions/workflows/deploy.yml)

> Hệ thống phân phối tài khoản game Liên Quân Mobile chính thức - Reverse Engineered & Cloned với đầy đủ tính năng tương tác thực tế và Typography chuẩn Production (Montserrat & Be Vietnam Pro).

## 🚀 Live Demo
- **GitHub Pages**: [https://tranquangthanh3062004.github.io/shopacc-mobaviet/](https://tranquangthanh3062004.github.io/shopacc-mobaviet/)
- **Local Dev Server**: `http://localhost:3000`

---

## 🌟 Tính Năng Nổi Bật

1. **Bộ Lọc & Tìm Kiếm Tài Khoản**:
   - Tìm kiếm thời gian thực theo Mã Số tài khoản, tên Tướng hoặc Trang Phục.
   - Lọc theo khoảng giá (Dưới 100k, 100k-300k, 300k-1M, Trên 1M).
   - Lọc theo bậc Rank (Kim Cương, Tinh Anh, Cao Thủ, Thách Đấu).
   - Lọc theo trạng thái thông tin (Trắng Thông Tin, Có SĐT).
   - Sắp xếp và phân trang tự động.

2. **Quy Trình Mua Nick Tự Động**:
   - Kiểm tra số dư ví người dùng theo thời gian thực.
   - Mua nick thành công lập tức cấp tài khoản đăng nhập (Garena, Password, Mã 2FA) kèm nút sao chép 1-click.
   - Tự động lưu vào lịch sử đơn hàng.

3. **Cổng Nạp Tiền Đa Phương Thức**:
   - **Thẻ cào tự động 30s**: Viettel, Vinaphone, Mobifone, Garena, Zing.
   - **ATM / VietQR Code**: Tạo mã QR VietQR động theo chuẩn Napas với đúng số tiền và cú pháp chuyển khoản.

4. **Minigame Vòng Quay Quân Huy & Rương May Mắn**:
   - Vòng quay may mắn Canvas tương tác với animation giảm tốc.
   - Thưởng Quân Huy và tài khoản VIP, tích hợp popup nhận thưởng `#modalRuongQuanHuy`.

5. **Trang Cá Nhân & Lịch Sử Giao Dịch (`thong-tin.html`)**:
   - Quản lý tài khoản, xem lại các nick đã mua và mật khẩu.
   - Theo dõi biến động số dư chi tiết.

---

## 🛠️ Khởi Chạy Local

Chạy máy chủ Node.js không cần cài đặt thêm thư viện:
```bash
npm start
```
Mở trình duyệt tại: `http://localhost:3000`

---

## 📦 Công Nghệ Sử Dụng
- **HTML5 & CSS3**: Montserrat (Headers) + Be Vietnam Pro (Body & Tiếng Việt diacritics).
- **Modern JavaScript**: ES6+, localStorage State Management, Canvas API.
- **Node.js**: Native HTTP server.
- **FontAwesome 6**: Hệ thống icon đồng bộ.
