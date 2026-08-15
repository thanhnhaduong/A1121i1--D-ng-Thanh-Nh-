# ♟ CHESS MASTER - Cờ Vua Stockfish

**Ứng dụng cờ vua chuyên nghiệp với đánh giá nước đi từ Stockfish (kiểu Chess.com)**

## 🌟 Tính Năng

✅ **Đánh giá nước đi từ Stockfish** - Hiển thị tất cả nước đi với lý do chi tiết
- 💥 Blunder (mất lợi thế lớn)
- ❌ Mistake (sai lầm)
- ⚠️ Inaccuracy (không chính xác)
- 👍 Good (tốt)
- ✓ Excellent (xuất sắc)
- ✨ Brilliant (tuyệt vời)

✅ **Nhiều chế độ chơi**
- 👥 2 người chơi
- 🤖 1 người vs Bot (tùy chỉnh ELO)
- 🤖🤖 Bot vs Bot
- ⚙️ Engine vs Engine (Stockfish đấu với chính nó)

✅ **50+ Hướng Dẫn Khai Cuộc**
- Hiển thị tên khai cuộc tự động
- Chi tiết lịch sử, chiến lược
- Di chuyển đề xuất

✅ **Thanh Đánh Giá Kiểu Chess.com**
- Hiển thị lợi thế trắng/đen
- Cập nhật tự động sau mỗi nước đi

✅ **Tối Ưu Hóa Hiệu Năng**
- Tải nhanh
- Phù hợp với máy tính yếu

## 📦 Cài Đặt

### Bước 1: Cài Đặt Python (nếu chưa có)
Nếu bạn đã cài **Thonny**, bạn có thể bỏ qua bước này.

Tải từ: https://www.python.org/downloads/

### Bước 2: Cài Đặt Dependencies

**Cách 1: Dùng Thonny (Khuyến Khích)**
1. Mở file `main.py` bằng Thonny
2. Nhấn `Tools → Manage packages`
3. Cài đặt từng package:
   - `python-chess`
   - `stockfish`
   - `Pillow` (tùy chọn)
   - `requests` (tùy chọn)

**Cách 2: Dùng PowerShell/CMD**
```bash
cd /path/to/chess/folder
python -m pip install -r requirements.txt
```

### Bước 3: Cài Đặt Stockfish

Stockfish là engine đánh giá nước đi.

1. Tải Stockfish: https://stockfishchess.org/download/
2. Giải nén vào `C:\Program Files\Stockfish\` hoặc bất kỳ nơi nào
3. App sẽ tự tìm nó

**Nếu Stockfish ở vị trí tùy chỉnh:**
- Sửa file `chess_engine.py` tại dòng 32-37
- Thêm đường dẫn của bạn vào danh sách `stockfish_paths`

Ví dụ:
```python
stockfish_paths = [
    r"C:\Users\admin\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe",
    r"C:\Program Files\Stockfish\stockfish.exe",
    "stockfish"
]
```

## 🎮 Cách Chơi

### Chạy Ứng Dụng

**Cách 1: Thonny**
- Mở file `main.py`
- Nhấn `F5` hoặc nút "Run"

**Cách 2: PowerShell/CMD**
```bash
python main.py
```

### Giao Diện

1. **Bàn Cờ** (trái): Click để di chuyển quân
2. **Thanh Đánh Giá** (trên): Hiển thị lợi thế trắng/đen
3. **Đánh Giá Nước Đi** (dưới): Lý do cho nước đi cuối cùng
4. **Bảng Điều Khiển** (phải):
   - Chọn chế độ chơi
   - Chọn độ khó của bot
   - Xem hướng dẫn khai cuộc
   - Undo, Reset nước đi

## 📋 Các File

| File | Chức Năng |
|------|----------|
| `main.py` | **Điểm vào chính** - Chạy file này |
| `gui_optimized.py` | Giao diện người dùng tối ưu |
| `chess_engine.py` | Logic cờ vua + Stockfish |
| `openings_50.py` | 50+ Khai cuộc + hướng dẫn |
| `requirements.txt` | Danh sách dependencies |

## ⚙️ Tùy Chỉnh

### Thay Đổi Độ Khó Bot
Trong `gui_optimized.py`, tìm `ELO_LEVELS` (khoảng dòng 41-48):
```python
self.ELO_LEVELS = {
    'Easy (5)': 5,
    'Beginner (8)': 8,
    'Intermediate (12)': 12,
    'Advanced (16)': 16,
    'Master (18)': 18,
    'GrandMaster (20)': 20
}
```

### Thay Đổi Màu Bàn Cờ
Tìm `COLORS` (dòng 28-34):
```python
self.COLORS = {
    'light': '#f0d9b5',  # Màu ô sáng
    'dark': '#b58863',   # Màu ô tối
}
```

## 🐛 Khắc Phục Sự Cố

### Lỗi: "ModuleNotFoundError: No module named 'chess'"
→ Cài đặt dependencies (xem bước 2)

### Lỗi: "⚠️ Stockfish not found"
→ Cài đặt Stockfish hoặc cập nhật đường dẫn (xem bước 3)

### Ứng Dụng Chạy Chậm
→ Giảm độ khó bot hoặc đợi Stockfish phân tích

## 📊 Thống Kê Nước Đi

Mỗi nước được đánh giá dựa trên **centipawn** (1 tốt = 100 centipawn):
- **Brilliant (✨)**: +3.00 tốt
- **Excellent (✓)**: +1.00 đến +3.00 tốt
- **Good (👍)**: -0.25 đến +0.25
- **Inaccuracy (⚠️)**: -0.25 đến -1.00
- **Mistake (❌)**: -1.00 đến -3.00
- **Blunder (💥)**: -3.00 tốt

## 🎓 Học Từ Ứng Dụng

1. Xem đánh giá nước đi của bạn
2. Hiểu tại sao nước đó tốt hay xấu
3. Học hướng dẫn khai cuộc mà bot dùng
4. Lặp lại cho đến khi thắng!

## 🚀 Cải Tiến Tương Lai

- [ ] Lưu game (PGN format)
- [ ] Lịch sử di chuyển chi tiết
- [ ] Phân tích đầy đủ ván đấu
- [ ] Chế độ luyện tập (puzzles)

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra Stockfish đã cài chưa
2. Kiểm tra Python >= 3.7
3. Cài lại dependencies: `pip install --upgrade -r requirements.txt`

---

**Chúc bạn chơi cờ vui vẻ! ♞♟**

Phiên bản: 1.0 (Tối Ưu)
