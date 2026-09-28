"""
# Cờ caro 4x4 – Bot tự học từ sai lầm (Python + tkinter)

Luật: bàn 4x4, ai có **4 quân liên tiếp** (hàng, cột hoặc chéo) trước thì thắng.

## Chạy
```bash
python co_caro_4x4.py
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

Tất cả nằm trong 1 file này: phần BỘ NÃO (LearningBot) ở trên, phần GIAO DIỆN tkinter (App) ở dưới.

---------------------------------------------------------------
Bộ não của bot cờ caro 4x4 (thắng khi có 4 quân liên tiếp: hàng, cột, đường chéo).

Bot KHÔNG được lập trình sẵn cách thắng. Nó bắt đầu với bộ nhớ rỗng
(mọi thế cờ đều được đánh giá 50/50) và tự học bằng cách:
  1. Tự đấu với chính nó (hai bot đấu với nhau) hàng chục nghìn ván.
  2. Sau mỗi ván, đi NGƯỢC từ cuối ván về đầu ván và cập nhật giá trị
     từng thế cờ (Temporal-Difference learning):
        - Nước dẫn tới thắng  -> giá trị tăng dần về 1.0
        - Nước dẫn tới thua   -> giá trị giảm dần về 0.0  (HỌC TỪ SAI LẦM)
        - Hòa                 -> giá trị về 0.5
  3. Lần sau gặp lại thế cờ đó (hoặc thế cờ đối xứng/xoay của nó),
     bot sẽ tránh nước đi đã từng làm nó thua.
"""


import gzip
import os
import pickle
import queue
import random
import threading
import tkinter as tk
from tkinter import messagebox, ttk

SIZE = 4
N_CELLS = SIZE * SIZE
EMPTY, X, O = 0, 1, 2
SYMBOL = {EMPTY: "", X: "X", O: "O"}

# 10 đường thắng: 4 hàng, 4 cột, 2 đường chéo
WIN_LINES = (
    [tuple(r * SIZE + c for c in range(SIZE)) for r in range(SIZE)]
    + [tuple(r * SIZE + c for r in range(SIZE)) for c in range(SIZE)]
    + [tuple(i * SIZE + i for i in range(SIZE)),
       tuple(i * SIZE + (SIZE - 1 - i) for i in range(SIZE))]
)
WIN_LINE_NAMES = (
    [f"Hàng {r + 1}" for r in range(SIZE)]
    + [f"Cột {c + 1}" for c in range(SIZE)]
    + ["Chéo chính", "Chéo phụ"]
)


def _build_symmetries():
    """8 phép biến đổi của hình vuông (xoay 0/90/180/270 + lật gương).
    Nhờ vậy bot học 1 thế cờ là hiểu luôn 7 thế cờ đối xứng với nó."""
    def rot(r, c):
        return c, SIZE - 1 - r

    def flip(r, c):
        return r, SIZE - 1 - c

    perms = []
    for do_flip in (False, True):
        for k in range(4):
            perm = []
            for idx in range(N_CELLS):
                r, c = divmod(idx, SIZE)
                if do_flip:
                    r, c = flip(r, c)
                for _ in range(k):
                    r, c = rot(r, c)
                perm.append(r * SIZE + c)
            # perm[i] = ô mới của ô i -> ta cần ô cũ cho mỗi ô mới
            inv = [0] * N_CELLS
            for old, new in enumerate(perm):
                inv[new] = old
            perms.append(tuple(inv))
    return tuple(set(perms))


SYMMETRIES = _build_symmetries()


def canonical(board):
    """Khóa chuẩn hóa của thế cờ (nhỏ nhất trong 8 phiên bản đối xứng)."""
    return min(bytes(board[i] for i in p) for p in SYMMETRIES)


def winner_of(board):
    """Trả về (người thắng, chỉ số đường thắng) hoặc (None, None)."""
    for li, line in enumerate(WIN_LINES):
        v = board[line[0]]
        if v != EMPTY and all(board[i] == v for i in line):
            return v, li
    return None, None


def empty_cells(board):
    return [i for i, v in enumerate(board) if v == EMPTY]


def other(player):
    return O if player == X else X


class LearningBot:
    """Bot học tăng cường (Reinforcement Learning) bằng bảng giá trị.

    self.V[khóa thế cờ] = xác suất thắng ước lượng của NGƯỜI VỪA ĐI
    để tạo ra thế cờ đó.
    """

    DEFAULT = 0.5

    def __init__(self, alpha=0.25):
        self.alpha = alpha
        self.V = {}
        self.games_trained = 0
        self.stats = {X: 0, O: 0, "draw": 0}
        self.bad_moves = set()             # các nước đi bot đã nhận ra là SAI
        self.win_lines_found = set()       # các đường thắng đã từng thắng
        self.win_patterns = set()          # các thế thắng khác nhau đã gặp

    # ------------------------------------------------------------ đánh giá
    def value_after(self, board, move, player):
        nb = list(board)
        nb[move] = player
        w, _ = winner_of(nb)
        if w == player:
            return 1.0
        return self.V.get(canonical(nb), self.DEFAULT)

    def move_values(self, board, player):
        return {m: self.value_after(board, m, player) for m in empty_cells(board)}

    @staticmethod
    def _allows_opponent_win(board, move, player):
        nb = list(board)
        nb[move] = player
        opp = other(player)
        for r in empty_cells(nb):
            nb[r] = opp
            w, _ = winner_of(nb)
            nb[r] = EMPTY
            if w == opp:
                return True
        return False

    def choose_move(self, board, player, epsilon=0.0, careful=False):
        """careful=True: ngoài bộ nhớ đã học, bot còn "nhìn trước 1 nước"
        để không đi nước khiến đối thủ thắng ngay (dùng khi đấu với người)."""
        moves = empty_cells(board)
        if not moves:
            return None
        if epsilon > 0 and random.random() < epsilon:
            return random.choice(moves)          # thử nước lạ để khám phá
        vals = self.move_values(board, player)
        candidates = list(vals)
        if careful:
            safe = [m for m in candidates
                    if vals[m] == 1.0 or not self._allows_opponent_win(board, m, player)]
            candidates = safe or candidates
        best = max(vals[m] for m in candidates)
        best_moves = [m for m in candidates if abs(vals[m] - best) < 1e-9]
        return random.choice(best_moves)

    # ------------------------------------------------------------ học tập
    def learn_from_game(self, history, winner, win_line=None):
        """history: danh sách các thế cờ (tuple) sau mỗi nước đi, theo thứ tự.
        Đi ngược từ cuối ván: giá trị thế cờ của mình = 1 - giá trị thế cờ
        mà đối thủ tạo ra ngay sau đó."""
        keys = [canonical(b) for b in history]
        n = len(keys)
        if n == 0:
            return
        # Nước cuối cùng: kết quả thật của ván đấu
        self.V[keys[-1]] = 1.0 if winner else 0.5
        self.bad_moves.discard(keys[-1])
        for i in range(n - 2, -1, -1):
            k = keys[i]
            old = self.V.get(k, self.DEFAULT)
            target = 1.0 - self.V.get(keys[i + 1], self.DEFAULT)
            new = old + self.alpha * (target - old)
            if new < 0.3:
                self.bad_moves.add(k)            # bot "nhớ": nước này dẫn tới thua
            else:
                self.bad_moves.discard(k)
            self.V[k] = new

        self.games_trained += 1
        if winner:
            self.stats[winner] += 1
            if win_line is not None:
                self.win_lines_found.add(win_line)
            self.win_patterns.add(keys[-1])
        else:
            self.stats["draw"] += 1

    def learn_from_human_game(self, history, winner, win_line=None, repeat=5):
        """Học từ ván đấu với người. Nếu bot thua, học lại nhiều lần để
        ghi nhớ thật kỹ sai lầm đó (lần sau không đi lại nước sai)."""
        times = repeat if winner else 1
        for _ in range(times):
            self.learn_from_game(history, winner, win_line)
        self.games_trained -= times - 1
        if winner:
            self.stats[winner] -= times - 1
        else:
            self.stats["draw"] -= times - 1

    # ------------------------------------------------------------ tự đấu
    def play_self_game(self, epsilon=0.1):
        """Hai bot (cùng bộ não) đấu với nhau 1 ván rồi học từ ván đó."""
        board = [EMPTY] * N_CELLS
        player = X
        history = []
        while True:
            m = self.choose_move(board, player, epsilon)
            board[m] = player
            history.append(tuple(board))
            w, line = winner_of(board)
            if w or not empty_cells(board):
                self.learn_from_game(history, w, line)
                return w
            player = other(player)

    def train(self, n_games, eps_start=0.3, eps_end=0.02, callback=None,
              stop_flag=None, report_every=500):
        for g in range(n_games):
            if stop_flag is not None and stop_flag():
                break
            frac = g / max(1, n_games - 1)
            eps = eps_start + (eps_end - eps_start) * frac
            self.play_self_game(eps)
            if callback and (g + 1) % report_every == 0:
                callback(g + 1, n_games)
        if callback:
            callback(n_games, n_games)

    # ------------------------------------------------------------ lưu / tải
    @property
    def mistakes_learned(self):
        return len(self.bad_moves)

    def save(self, path):
        """Ghi ra file tạm rồi mới đổi tên thành file thật. Nhờ vậy nếu chương
        trình bị tắt ngang lúc đang lưu thì file bộ nhớ cũ vẫn còn nguyên."""
        tmp = path + ".tmp"
        with gzip.open(tmp, "wb", compresslevel=1) as f:   # nén nhẹ -> lưu rất nhanh
            pickle.dump(self.__dict__, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)

    def load(self, path):
        """Trả về "ok", "missing" (chưa có file) hoặc "corrupt" (file bị hỏng:
        đổi tên thành *.hong để giữ lại, bot bắt đầu với bộ nhớ trống)."""
        if not os.path.exists(path):
            return "missing"
        try:
            with gzip.open(path, "rb") as f:
                data = pickle.load(f)
            if not isinstance(data, dict) or not isinstance(data.get("V"), dict):
                raise ValueError("sai định dạng")
        except Exception:   # file ghi dở / hỏng có thể gây ra rất nhiều loại lỗi
            try:
                os.replace(path, path + ".hong")
            except OSError:
                pass
            return "corrupt"
        data.pop("mistakes_learned", None)
        self.__dict__.update(data)
        return "ok"


# ======================================================================
# GIAO DIỆN TKINTER
# ======================================================================
MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "bot_memory.pkl.gz")
CELL = 110
PAD = 10
COLORS = {X: "#e74c3c", O: "#2980b9"}


class App:
    def __init__(self, root):
        self.root = root
        root.title("Cờ caro 4x4 - Bot tự học từ sai lầm")
        root.resizable(False, False)

        self.bot = LearningBot()
        self.training = False
        self.stop_training = False
        self.demo_running = False
        self.msg_queue = queue.Queue()

        self.board = [EMPTY] * N_CELLS
        self.history = []
        self.turn = X
        self.game_over = False
        self.win_line = None

        self.human_var = tk.IntVar(value=X)
        self.show_hint_var = tk.BooleanVar(value=True)
        self.careful_var = tk.BooleanVar(value=True)
        self.n_games_var = tk.IntVar(value=50000)

        self._build_ui()

        status = self.bot.load(MEMORY_FILE)
        if status == "ok":
            self.log(f"Đã tải bộ nhớ: bot đã học {self.bot.games_trained:,} ván.")
        else:
            if status == "corrupt":
                self.log("⚠ File bộ nhớ bị hỏng (thường do chương trình bị tắt đúng lúc đang lưu).")
                self.log(f"  Đã đổi tên nó thành {os.path.basename(MEMORY_FILE)}.hong, "
                         "bot sẽ học lại từ đầu.")
            self.log("Bot chưa biết gì cả (bộ nhớ trống).")
            self.log("-> Hãy bấm 'Cho 2 bot tự đấu để học' trước khi chơi!")
        self.update_stats()
        self.new_game()
        self.root.after(100, self.poll_queue)

    # ================================================================ UI
    def _build_ui(self):
        size = CELL * SIZE + PAD * 2
        left = tk.Frame(self.root, padx=10, pady=10)
        left.grid(row=0, column=0, sticky="n")
        right = tk.Frame(self.root, padx=10, pady=10)
        right.grid(row=0, column=1, sticky="n")

        self.status = tk.Label(left, text="", font=("Arial", 15, "bold"))
        self.status.pack(pady=(0, 6))
        self.canvas = tk.Canvas(left, width=size, height=size, bg="#fdf6e3",
                                highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # ---- Khung huấn luyện
        tf = tk.LabelFrame(right, text=" 1. Huấn luyện (2 bot đấu với nhau) ",
                           padx=8, pady=6, font=("Arial", 10, "bold"))
        tf.pack(fill="x")
        row = tk.Frame(tf)
        row.pack(fill="x")
        tk.Label(row, text="Số ván tự đấu:").pack(side="left")
        tk.Spinbox(row, from_=1000, to=1000000, increment=10000, width=10,
                   textvariable=self.n_games_var).pack(side="left", padx=4)
        self.btn_train = tk.Button(tf, text="🤖 Cho 2 bot tự đấu để học",
                                   bg="#27ae60", fg="white",
                                   command=self.start_training)
        self.btn_train.pack(fill="x", pady=(6, 2))
        self.btn_stop = tk.Button(tf, text="⏹ Dừng huấn luyện",
                                  state="disabled", command=self.request_stop)
        self.btn_stop.pack(fill="x", pady=2)
        self.progress = ttk.Progressbar(tf, length=280, mode="determinate")
        self.progress.pack(fill="x", pady=4)
        self.btn_demo = tk.Button(tf, text="👀 Xem 2 bot đấu 1 ván",
                                  command=self.demo_game)
        self.btn_demo.pack(fill="x", pady=2)

        # ---- Khung chơi
        pf = tk.LabelFrame(right, text=" 2. Chơi với bot ", padx=8, pady=6,
                           font=("Arial", 10, "bold"))
        pf.pack(fill="x", pady=8)
        tk.Radiobutton(pf, text="Bạn cầm X (đi trước)", value=X,
                       variable=self.human_var, command=self.new_game).pack(anchor="w")
        tk.Radiobutton(pf, text="Bạn cầm O (bot đi trước)", value=O,
                       variable=self.human_var, command=self.new_game).pack(anchor="w")
        tk.Checkbutton(pf, text="Hiện suy nghĩ của bot (% thắng mỗi ô)",
                       variable=self.show_hint_var, command=self.draw).pack(anchor="w")
        tk.Checkbutton(pf, text="Bot cảnh giác (nhìn trước 1 nước)",
                       variable=self.careful_var).pack(anchor="w")
        self.btn_new = tk.Button(pf, text="🔄 Ván mới", command=self.new_game)
        self.btn_new.pack(fill="x", pady=(6, 0))

        # ---- Bộ nhớ
        mf = tk.LabelFrame(right, text=" 3. Bộ nhớ của bot ", padx=8, pady=6,
                           font=("Arial", 10, "bold"))
        mf.pack(fill="x")
        self.stats_label = tk.Label(mf, justify="left", anchor="w",
                                    font=("Consolas", 9))
        self.stats_label.pack(fill="x")
        brow = tk.Frame(mf)
        brow.pack(fill="x", pady=(4, 0))
        tk.Button(brow, text="💾 Lưu", command=self.save_memory).pack(side="left", expand=True, fill="x")
        tk.Button(brow, text="🗑 Xóa bộ nhớ", command=self.reset_memory).pack(side="left", expand=True, fill="x")

        # ---- Nhật ký
        lf = tk.LabelFrame(self.root, text=" Nhật ký học tập ", padx=6, pady=4)
        lf.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=(0, 10))
        self.log_box = tk.Text(lf, height=7, width=100, state="disabled",
                               font=("Consolas", 9))
        self.log_box.pack(fill="both")

    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_stats(self):
        b = self.bot
        found = sorted(b.win_lines_found)
        names = ", ".join(WIN_LINE_NAMES[i] for i in found) or "(chưa có)"
        self.stats_label.config(text=(
            f"Số ván đã học      : {b.games_trained:,}\n"
            f"Thế cờ đã ghi nhớ  : {len(b.V):,}\n"
            f"X thắng / O thắng / hòa: {b.stats[X]:,} / {b.stats[O]:,} / {b.stats['draw']:,}\n"
            f"Nước sai đã ghi nhớ: {b.mistakes_learned:,}\n"
            f"Kiểu thế thắng khác nhau: {len(b.win_patterns):,}\n"
            f"Đường thắng đã biết: {len(found)}/{len(WIN_LINES)}\n  {names}"
        ))
        self.stats_label.config(wraplength=300)

    # ================================================================ vẽ
    def draw(self):
        c = self.canvas
        c.delete("all")
        for i in range(SIZE + 1):
            p = PAD + i * CELL
            c.create_line(PAD, p, PAD + SIZE * CELL, p, width=2, fill="#586e75")
            c.create_line(p, PAD, p, PAD + SIZE * CELL, width=2, fill="#586e75")

        hints = {}
        if (self.show_hint_var.get() and not self.game_over and not self.training
                and not self.demo_running and self.turn == self.human_var.get()):
            # Bot cho biết nó nghĩ gì: nếu BẠN đi ô này, cơ hội thắng của bạn là bao nhiêu
            hints = self.bot.move_values(self.board, self.turn)

        for idx in range(N_CELLS):
            r, col = divmod(idx, SIZE)
            x0, y0 = PAD + col * CELL, PAD + r * CELL
            cx, cy = x0 + CELL / 2, y0 + CELL / 2
            v = self.board[idx]
            if v == X:
                m = 25
                c.create_line(x0 + m, y0 + m, x0 + CELL - m, y0 + CELL - m, width=8, fill=COLORS[X], capstyle="round")
                c.create_line(x0 + CELL - m, y0 + m, x0 + m, y0 + CELL - m, width=8, fill=COLORS[X], capstyle="round")
            elif v == O:
                m = 25
                c.create_oval(x0 + m, y0 + m, x0 + CELL - m, y0 + CELL - m, width=8, outline=COLORS[O])
            elif idx in hints:
                val = hints[idx]
                g = int(255 * val)
                color = f"#{255 - g:02x}{min(255, 80 + g):02x}80"
                c.create_text(cx, cy, text=f"{val * 100:.0f}%", fill=color,
                              font=("Arial", 13, "bold"))

        if self.win_line is not None:
            line = WIN_LINES[self.win_line]
            (r1, c1), (r2, c2) = divmod(line[0], SIZE), divmod(line[-1], SIZE)
            c.create_line(PAD + c1 * CELL + CELL / 2, PAD + r1 * CELL + CELL / 2,
                          PAD + c2 * CELL + CELL / 2, PAD + r2 * CELL + CELL / 2,
                          width=6, fill="#f1c40f", capstyle="round")

    # ================================================================ chơi
    def new_game(self):
        if self.training or self.demo_running:
            return
        self.board = [EMPTY] * N_CELLS
        self.history = []
        self.turn = X
        self.game_over = False
        self.win_line = None
        self.set_status()
        self.draw()
        if self.turn != self.human_var.get():
            self.root.after(400, self.bot_move)

    def set_status(self, text=None):
        if text is None:
            who = "Lượt của bạn" if self.turn == self.human_var.get() else "Bot đang nghĩ..."
            text = f"{who} ({SYMBOL[self.turn]})"
        self.status.config(text=text)

    def on_click(self, event):
        if self.training or self.demo_running or self.game_over:
            return
        if self.turn != self.human_var.get():
            return
        col = (event.x - PAD) // CELL
        row = (event.y - PAD) // CELL
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            return
        idx = row * SIZE + col
        if self.board[idx] != EMPTY:
            return
        self.play(idx)
        if not self.game_over:
            self.root.after(350, self.bot_move)

    def bot_move(self):
        if self.game_over or self.training or self.demo_running:
            return
        m = self.bot.choose_move(self.board, self.turn,
                                 careful=self.careful_var.get())
        self.play(m)

    def play(self, idx):
        self.board[idx] = self.turn
        self.history.append(tuple(self.board))
        w, line = winner_of(self.board)
        if w or not empty_cells(self.board):
            self.finish_human_game(w, line)
        else:
            self.turn = other(self.turn)
            self.set_status()
        self.draw()

    def finish_human_game(self, w, line):
        self.game_over = True
        self.win_line = line
        human = self.human_var.get()
        if w == human:
            self.set_status("🎉 Bạn thắng!")
            self.log("❌ Bot THUA -> đang ghi nhớ sai lầm, lần sau sẽ không đi như vậy nữa.")
        elif w:
            self.set_status("🤖 Bot thắng!")
            self.log(f"✅ Bot thắng bằng đường: {WIN_LINE_NAMES[line]}.")
        else:
            self.set_status("🤝 Hòa!")
            self.log("🤝 Hòa. Bot cũng học từ ván này.")
        # Bot học từ ván vừa đấu với người
        self.bot.learn_from_human_game(self.history, w, line)
        self.update_stats()
        self.save_memory(silent=True)

    # ================================================================ demo
    def demo_game(self):
        if self.training or self.demo_running:
            return
        self.demo_running = True
        self.board = [EMPTY] * N_CELLS
        self.history = []
        self.turn = X
        self.game_over = False
        self.win_line = None
        self.status.config(text="Bot X ⚔ Bot O")
        self.draw()
        self.root.after(500, self.demo_step)

    def demo_step(self):
        m = self.bot.choose_move(self.board, self.turn, careful=self.careful_var.get())
        self.board[m] = self.turn
        self.history.append(tuple(self.board))
        w, line = winner_of(self.board)
        if w or not empty_cells(self.board):
            self.win_line = line
            self.game_over = True
            self.demo_running = False
            res = f"Bot {SYMBOL[w]} thắng!" if w else "Hòa! (2 bot giỏi ngang nhau)"
            self.status.config(text=res)
            self.log(f"[Xem đấu] {res}")
            self.bot.learn_from_game(self.history, w, line)
            self.update_stats()
            self.draw()
            return
        self.turn = other(self.turn)
        self.draw()
        self.root.after(500, self.demo_step)

    # ================================================================ huấn luyện
    def start_training(self):
        if self.training or self.demo_running:
            return
        try:
            n = int(self.n_games_var.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Lỗi", "Số ván không hợp lệ")
            return
        if n <= 0:
            return
        self.training = True
        self.stop_training = False
        self.btn_train.config(state="disabled")
        self.btn_demo.config(state="disabled")
        self.btn_new.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.progress.config(maximum=n, value=0)
        self.status.config(text="Đang huấn luyện...")
        self.log(f"Bắt đầu cho 2 bot tự đấu {n:,} ván...")
        start = self.bot.games_trained
        before = (dict(self.bot.stats), self.bot.mistakes_learned)

        def cb(done, total):
            self.msg_queue.put(("progress", done, total))

        def worker():
            self.bot.train(n, callback=cb, stop_flag=lambda: self.stop_training)
            self.msg_queue.put(("done", start, before))

        threading.Thread(target=worker, daemon=True).start()

    def request_stop(self):
        self.stop_training = True

    def poll_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg[0] == "progress":
                    _, done, total = msg
                    self.progress.config(value=done)
                    self.status.config(text=f"Đang huấn luyện... {done:,}/{total:,}")
                    self.update_stats()
                elif msg[0] == "done":
                    self.on_training_done(*msg[1:])
        except queue.Empty:
            pass
        self.root.after(150, self.poll_queue)

    def on_training_done(self, start, before):
        b = self.bot
        played = b.games_trained - start
        old_stats, _ = before
        dx = b.stats[X] - old_stats[X]
        do = b.stats[O] - old_stats[O]
        dd = b.stats["draw"] - old_stats["draw"]
        self.training = False
        self.btn_train.config(state="normal")
        self.btn_demo.config(state="normal")
        self.btn_new.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.log(f"Xong {played:,} ván: X thắng {dx:,}, O thắng {do:,}, hòa {dd:,}. "
                 f"Tổng số nước sai đã ghi nhớ: {b.mistakes_learned:,}.")
        self.log("(Khi 2 bot càng giỏi thì tỉ lệ HÒA càng cao - vì cả hai đều đã biết chặn nhau.)")
        self.update_stats()
        self.save_memory(silent=True)
        self.new_game()

    # ================================================================ bộ nhớ
    def save_memory(self, silent=False):
        if self.training:
            return
        old_text = self.status.cget("text")
        self.status.config(text="💾 Đang lưu bộ nhớ...")
        self.root.update_idletasks()
        try:
            self.bot.save(MEMORY_FILE)
        except OSError as e:
            self.log(f"⚠ Không lưu được bộ nhớ: {e}")
        else:
            if not silent:
                self.log(f"Đã lưu bộ nhớ vào {os.path.basename(MEMORY_FILE)}")
        finally:
            self.status.config(text=old_text)

    def reset_memory(self):
        if self.training or self.demo_running:
            return
        if messagebox.askyesno("Xóa bộ nhớ", "Bot sẽ quên hết mọi thứ đã học. Chắc chắn?"):
            self.bot = LearningBot()
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
            self.log("Đã xóa bộ nhớ. Bot trở lại như mới.")
            self.update_stats()
            self.new_game()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
