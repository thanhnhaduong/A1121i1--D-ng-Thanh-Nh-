# 📖 Hướng Dẫn Chạy Cờ Vua trên Thonny

**Cho người dùng Windows với Thonny IDE**

## 🎯 Bước 1: Kiểm Tra File

Bạn cần có những file này trong một thư mục:
```
📁 chess-folder/
├── main.py                 ← Chạy file này
├── gui_optimized.py        ← Giao diện
├── chess_engine.py         ← Logic cờ vua
├── openings_50.py          ← 50+ khai cuộc
├── requirements.txt        ← Danh sách thư viện
└── README.md               ← Hướng dẫn đầy đủ
```

## 🎯 Bước 2: Cài Đặt Thư Viện (Python Libraries)

**Cách dễ nhất - Dùng Thonny:**

1. Mở **Thonny**
2. Mở file `main.py` (File → Open)
3. Nhấn menu **Tools** → **Manage packages** (hoặc 3 chấm nếu không thấy)
4. Cài 4 thư viện (gõ vào search box):
   - ✅ `python-chess` → Install
   - ✅ `stockfish` → Install
   - ⭐ `Pillow` → Install (tùy chọn)
   - ⭐ `requests` → Install (tùy chọn)

**Nếu không thấy "Manage packages":**
1. Nhấn `Tools` → `Open system shell`
2. Gõ lệnh:
```bash
python -m pip install python-chess stockfish Pillow requests
```

## 🎯 Bước 3: Cài Đặt Stockfish

Stockfish là engine chơi cờ và đánh giá nước đi.

### Tùy Chọn 1: Cài Đặt Chính Thức (Khuyên)
1. Vào https://stockfishchess.org/download/
2. Tải **Stockfish 16 or later**
3. Giải nén vào: `C:\Program Files\Stockfish\`
4. App sẽ tự tìm thấy ✅

### Tùy Chọn 2: Nếu Stockfish Đã Có ở Nơi Khác
Bạn nói rằng Stockfish ở:
```
C:\Users\admin\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe
```

Điều này đã được cấu hình sẵn trong file `chess_engine.py`! ✅

## 🎯 Bước 4: Chạy Ứng Dụng

**Cách 1: Thonny (Dễ Nhất)**
1. Mở `main.py` trong Thonny
2. Nhấn nút ▶️ (Run) hoặc phím `F5`
3. Chờ cửa sổ cờ vua xuất hiện

**Cách 2: PowerShell**
1. Mở PowerShell
2. Đi vào thư mục chứa file:
```bash
cd C:\path\to\chess\folder
```
3. Chạy:
```bash
python main.py
```

## 🎮 Khi Ứng Dụng Chạy

### Lần Đầu Tiên
- Chọn chế độ chơi (2 người, vs Bot, v.v.)
- Nếu bot từng lâu mới di chuyển = Bình thường, Stockfish đang phân tích

### Các Nút Điều Khiển
- **👥 2 Người**: 2 người chơi (1 máy tính)
- **🤖 vs Bot**: Bạn vs Bot AI
- **🤖 Bot vs Bot**: 2 Bot đấu nhau
- **🎛️ Chọn Độ Khó**: Easy (5) → GrandMaster (20)
- **📖 Khai Cuộc**: Xem 50+ hướng dẫn mở cuộc
- **↩️ Undo**: Lùi 1 nước
- **🔄 Reset**: Chơi lại

### Bảng Đánh Giá Nước Đi
Mỗi nước được đánh giá:
```
✨ Brilliant   = Nước tuyệt vời (+3.00)
✓ Excellent   = Nước xuất sắc (+1.00 to +3.00)
👍 Good       = Nước tốt (-0.25 to +0.25)
⚠️ Inaccuracy = Hơi yếu (-0.25 to -1.00)
❌ Mistake    = Sai lầm (-1.00 to -3.00)
💥 Blunder    = Kinh khủng (< -3.00)
```

## ⚠️ Khắc Phục Sự Cố

### Lỗi: "ModuleNotFoundError: No module named 'chess'"
**Giải pháp:** Cài đặt `python-chess`
1. Thonny → Tools → Manage packages
2. Tìm `python-chess` → Install

### Lỗi: "AttributeError: 'NoneType' object has no attribute 'set_skill_level'"
**Nghĩa:** Stockfish không tìm thấy
**Giải pháp:**
1. Cài Stockfish từ https://stockfishchess.org/download/
2. Đặt vào `C:\Program Files\Stockfish\`
3. Hoặc sửa đường dẫn trong file `chess_engine.py` dòng 32-37

### Lỗi: "FileNotFoundError: No such file or directory"
**Giải pháp:**
1. Kiểm tra tất cả 5 file ở trên đã có chưa
2. Đảm bảo cùng thư mục

### Ứng Dụng Chạy Chậm
**Nguyên nhân:** Stockfish đang phân tích
**Giải pháp:**
- Kiên nhẫn đợi (lần đầu chậm nhất)
- Hoặc giảm độ khó bot xuống "Intermediate (12)"

### Không Có Quân Cờ trên Bàn
**Giải pháp:** Chọn chế độ chơi "2 Người" trước
- Nhấn "👥 2 Người"
- Nhấn "Reset"

## 💡 Mẹo Sử Dụng

1. **Lần Đầu:** Chơi "2 Người" để quen giao diện
2. **Học:** Xem đánh giá nước đi để hiểu tại sao bot chơi như vậy
3. **Khai Cuộc:** Xem "📖 Khai Cuộc" để học chiến lược
4. **Khó Dần:** Tăng độ khó bot khi thắng nhiều

## ✅ Checklist Trước Chạy

- [ ] Có 5 file Python trong 1 thư mục
- [ ] Cài đặt `python-chess`, `stockfish` qua Thonny
- [ ] Cài Stockfish từ https://stockfishchess.org/download/
- [ ] Mở `main.py` trong Thonny
- [ ] Nhấn ▶️ (Run) hoặc F5
- [ ] Chọn chế độ chơi

## 🎉 Sẵn Sàng!

Nếu bạn đã làm theo các bước trên, ứng dụng sẽ chạy ngay!

```
    ♔ ♕ ♖ ♗ ♘ ♙
    ♚ ♛ ♜ ♝ ♞ ♟
    Chúc bạn chơi vui!
```

---
**Câu Hỏi?** Xem README.md để hướng dẫn chi tiết
