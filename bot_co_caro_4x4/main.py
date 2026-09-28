"""
Cờ caro 4x4 với bot TỰ HỌC TỪ SAI LẦM - giao diện tkinter.

Cách dùng:
  1. Chạy:  python main.py
  2. Bấm "Cho 2 bot tự đấu để học" (khuyên dùng >= 50.000 ván, mất khoảng 1 phút).
  3. Chơi với bot. Mỗi lần bot thua, nó sẽ ghi nhớ sai lầm và không mắc lại.
"""

import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from ai_core import (EMPTY, N_CELLS, O, SIZE, SYMBOL, WIN_LINE_NAMES,
                     WIN_LINES, X, LearningBot, empty_cells, other, winner_of)

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
