# Cờ caro 4x4 – Bot tự học từ sai lầm (Python + tkinter)

Luật: bàn 4x4, ai có **4 quân liên tiếp** (hàng, cột hoặc chéo) trước thì thắng.

## Chạy
```bash
python main.py
```
(Chỉ dùng thư viện chuẩn của Python. Trên Linux có thể cần `sudo apt install python3-tk`.)

## Cách dùng
1. Bấm **"Cho 2 bot tự đấu để học"** (nên chọn ≥ 50.000 ván, khoảng 1 phút).
2. Bấm **"Xem 2 bot đấu 1 ván"** để xem 2 bot đã học đấu với nhau.
3. Chọn X hoặc O rồi chơi với bot. Bật "Hiện suy nghĩ của bot" để thấy % thắng bot ước lượng cho từng ô.

Bộ nhớ được tự động lưu vào `bot_memory.pkl.gz`, lần sau mở lại bot vẫn nhớ.

## Bot học như thế nào?
- Ban đầu bot **không biết gì**: mọi thế cờ đều được đánh giá 50%.
- Hai bot (dùng chung một bộ não) tự đấu với nhau. Đôi khi chúng đi nước ngẫu nhiên để khám phá cách mới.
- Hết ván, bot đi **ngược từ cuối ván về đầu ván** và cập nhật giá trị từng thế cờ
  (Temporal-Difference learning):
  - nước dẫn tới **thắng** → giá trị tăng dần về 100%
  - nước dẫn tới **thua** → giá trị giảm dần về 0% → bot **ghi nhớ sai lầm** và lần sau tránh
- Nhờ 8 phép đối xứng (xoay/lật bàn cờ), học 1 thế cờ = hiểu luôn 7 thế cờ tương đương.
- Khi bạn thắng bot, bot học lại ván đó 5 lần để nhớ thật kỹ sai lầm.
- Tùy chọn "Bot cảnh giác" cho bot nhìn trước 1 nước để không để bạn thắng ngay lập tức (tắt đi để thấy bot chỉ dùng bộ nhớ đã học).

File: `ai_core.py` (bộ não, không phụ thuộc giao diện) và `main.py` (giao diện tkinter).
