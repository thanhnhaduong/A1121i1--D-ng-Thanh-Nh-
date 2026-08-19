#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chess App - Ung dung Co vua hoan chinh bang Tkinter + python-chess + Stockfish
================================================================================
Tinh nang:
  - PvP (Local pass & play), PvBot (Stockfish voi Elo tuy chinh), Bot vs Bot
  - Evaluation bar realtime, Move classification kieu Chess.com
    (Brilliant / Great / Best / Good / Inaccuracy / Mistake / Blunder / Book)
  - Mui ten goi y nuoc di tot nhat (co the bat/tat)
  - Danh sach nuoc di theo Algebraic Notation, dong ho, accuracy % cuoi van
  - Da luong: moi tinh toan Stockfish chay o thread rieng, khong lam dong UI
"""

import os
import sys
import time
import queue
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import chess
    import chess.engine
    import chess.pgn
except ImportError:
    print("Missing 'python-chess'. Install: pip install python-chess")
    sys.exit(1)

# CONSTANTS
APP_TITLE = "PyChess Pro - Co vua + Stockfish"
BOARD_PIXELS = 960
SQUARE = BOARD_PIXELS // 8
EVAL_BAR_WIDTH = 12

COLOR_LIGHT = "#EEEED2"
COLOR_DARK = "#769656"
COLOR_SELECTED = "#F6F669"
COLOR_LASTMOVE = "#BACA44"
COLOR_LEGAL_DOT = "#000000"
COLOR_CHECK = "#FF4444"
COLOR_ARROW_BEST = "#1BAA55"
BG_DARK = "#1E1E1E"
BG_PANEL = "#2B2B2B"
FG_TEXT = "#EAEAEA"

PIECE_UNICODE = {
    "P": "\u2659", "N": "\u2658", "B": "\u2657", "R": "\u2656", "Q": "\u2655", "K": "\u2654",
    "p": "\u265F", "n": "\u265E", "b": "\u265D", "r": "\u265C", "q": "\u265B", "k": "\u265A",
}

STOCKFISH_DEFAULT_PATHS = [
    os.environ.get("STOCKFISH_PATH", ""),
    "/usr/games/stockfish", "/usr/local/bin/stockfish", "/usr/bin/stockfish",
    "stockfish", "stockfish.exe",
]

CLASS_STYLE = {
    "book":        ("Khai cuoc",     "\U0001F4DA", "#8B6DB5", "Nuoc di chuan trong sach khai cuoc."),
    "brilliant":   ("Xuat sac",      "\u2B50",     "#1AACA8", "Nuoc hy sinh, tan cong cuc ky thong minh."),
    "great":       ("Tuyet voi",     "\U0001F7E2", "#4CAF50", "Nuoc di duy nhat va quan trong."),
    "best":        ("Tot nhat",      "\u2714",     "#6FA8DC", "Nuoc di toi uu theo Stockfish."),
    "good":        ("Kha",           "\u2714",     "#8FBF7F", "Nuoc di hop ly, an toan."),
    "inaccuracy":  ("Diem yeu nhe",  "\u2753",     "#E8C547", "Nuoc di hoi kem."),
    "mistake":     ("Sai lam",       "\u26A0",     "#E8912D", "Nuoc di gay mat loi the."),
    "blunder":     ("Thao hoa",      "\u274C",     "#D9534F", "Sai lam tram trong."),
}

MATE_CP = 100000

def find_stockfish_path():
    for p in STOCKFISH_DEFAULT_PATHS:
        if not p: continue
        if os.path.isfile(p): return p
        found = shutil.which(p)
        if found: return found
    return None


class AsyncRunner:
    def __init__(self, root):
        self.root = root
        self._q = queue.Queue()
        self._alive = True
        self.root.after(30, self._poll)

    def run(self, func, callback):
        def worker():
            try:
                result = func()
                self._q.put((callback, result, None))
            except Exception as exc:
                self._q.put((callback, None, exc))
        threading.Thread(target=worker, daemon=True).start()

    def _poll(self):
        try:
            while True:
                callback, result, err = self._q.get_nowait()
                if callback: callback(result, err)
        except queue.Empty:
            pass
        if self._alive:
            self.root.after(30, self._poll)

    def stop(self):
        self._alive = False


class EngineWrapper:
    def __init__(self, path):
        self.path = path
        self._engine = None
        self._lock = threading.Lock()
        self.elo = 1500
        self._open()

    def _open(self):
        self._engine = chess.engine.SimpleEngine.popen_uci(self.path)

    def close(self):
        with self._lock:
            try:
                if self._engine:
                    self._engine.quit()
            except Exception:
                pass

    def configure_strength(self, elo):
        self.elo = elo
        with self._lock:
            try:
                if "UCI_LimitStrength" in self._engine.options:
                    self._engine.configure({"UCI_LimitStrength": True, "UCI_Elo": min(int(elo), 3190)})
            except:
                pass

    def play(self, board):
        with self._lock:
            limit = chess.engine.Limit(time=0.5)
            result = self._engine.play(board, limit)
            return result.move

    def analyse(self, board, multipv=3, time_limit=0.5):
        with self._lock:
            limit = chess.engine.Limit(time=time_limit)
            infos = self._engine.analyse(board, limit, multipv=multipv)
        if isinstance(infos, dict):
            infos = [infos]
        out = []
        for info in infos:
            score = info.get("score")
            if score is None: continue
            pov = score.pov(board.turn)
            cp = pov.score(mate_score=MATE_CP)
            pv = info.get("pv", [])
            move = pv[0] if pv else None
            if move is None: continue
            try:
                san = board.san(move)
            except:
                san = move.uci()
            out.append({"move": move, "san": san, "score_cp": cp})
        return out


def material_count(board, color):
    total = 0
    for pt in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        val = [1, 3, 3, 5, 9][pt]
        total += val * len(board.pieces(pt, color))
    return total


class MoveClassifier:
    def classify(self, board_before, move, top_before, eval_before_cp, eval_after_cp):
        best_cp = top_before[0]["score_cp"] if top_before else eval_before_cp
        is_top_choice = bool(top_before) and top_before[0]["move"] == move
        cp_loss = max(0, best_cp - eval_after_cp)

        mover_color = board_before.turn
        board_after = board_before.copy()
        board_after.push(move)

        mat_before = material_count(board_before, mover_color) - material_count(board_before, not mover_color)
        mat_after = material_count(board_after, mover_color) - material_count(board_after, not mover_color)
        sacrifice = (mat_after - mat_before) <= -2
        is_mate = board_after.is_checkmate()

        if is_mate:
            return "brilliant" if sacrifice else "best"
        if sacrifice and cp_loss <= 40:
            return "brilliant"
        if is_top_choice and (best_cp - (top_before[1]["score_cp"] if len(top_before) > 1 else best_cp - 400)) >= 200:
            return "great"
        if is_top_choice or cp_loss <= 10:
            return "best"
        if cp_loss <= 50:
            return "good"
        if cp_loss <= 120:
            return "inaccuracy"
        if cp_loss <= 250:
            return "mistake"
        return "blunder"


def compute_accuracy(cp_losses):
    if not cp_losses: return 100.0
    import math
    scores = []
    for loss in cp_losses:
        loss = max(0, loss)
        acc = 103.1668 * math.exp(-0.04354 * (loss / 100.0)) - 3.1668
        scores.append(max(0.0, min(100.0, acc)))
    return sum(scores) / len(scores) if scores else 100.0


class BoardCanvas(tk.Canvas):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, width=BOARD_PIXELS, height=BOARD_PIXELS, highlightthickness=0, bg=BG_DARK, **kwargs)
        self.app = app
        self.flipped = False
        self.selected_sq = None
        self.legal_targets = []
        self.dragging = False
        self.best_move_arrow = None
        self.last_move = None
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.redraw()

    def sq_to_xy(self, square):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        col, row = (7 - file, rank) if self.flipped else (file, 7 - rank)
        return col * SQUARE, row * SQUARE

    def xy_to_sq(self, x, y):
        col, row = int(x // SQUARE), int(y // SQUARE)
        if not (0 <= col <= 7 and 0 <= row <= 7): return None
        file, rank = (7 - col, row) if self.flipped else (col, 7 - row)
        return chess.square(file, rank)

    def flip(self):
        self.flipped = not self.flipped
        self.redraw()

    def _draw_piece_glyph(self, cx, cy, piece):
        fill = "#FFFFFF" if piece.color == chess.WHITE else "#101010"
        outline = "#202020" if piece.color == chess.WHITE else "#FFFFFF"
        font = ("Segoe UI Symbol", int(SQUARE * 0.72))
        glyph = PIECE_UNICODE[piece.symbol()]
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            self.create_text(cx + dx, cy + dy, text=glyph, font=font, fill=outline)
        return self.create_text(cx, cy, text=glyph, font=font, fill=fill)

    def redraw(self):
        self.delete("all")
        board = self.app.board
        king_check_sq = board.king(board.turn) if board.is_check() else None

        for square in chess.SQUARES:
            x, y = self.sq_to_xy(square)
            is_light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
            color = COLOR_LIGHT if is_light else COLOR_DARK
            if self.last_move and square in (self.last_move.from_square, self.last_move.to_square):
                color = COLOR_LASTMOVE
            if self.selected_sq == square:
                color = COLOR_SELECTED
            self.create_rectangle(x, y, x + SQUARE, y + SQUARE, fill=color, outline="")

            if square == king_check_sq:
                self.create_oval(x + 4, y + 4, x + SQUARE - 4, y + SQUARE - 4, outline=COLOR_CHECK, width=4)

        for i in range(8):
            file_letter = chr(ord('a') + (7 - i if self.flipped else i))
            rank_num = str(i + 1 if self.flipped else 8 - i)
            self.create_text(8 + i * SQUARE, BOARD_PIXELS - 12, text=file_letter, anchor="sw", font=("Segoe UI", 11, "bold"), fill=COLOR_DARK)
            self.create_text(BOARD_PIXELS - 10, 12 + i * SQUARE, text=rank_num, anchor="ne", font=("Segoe UI", 11, "bold"), fill=COLOR_DARK)

        for t in self.legal_targets:
            x, y = self.sq_to_xy(t)
            cx, cy = x + SQUARE / 2, y + SQUARE / 2
            r = SQUARE * 0.16
            self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=COLOR_LEGAL_DOT, outline="")

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and not (self.dragging and self.selected_sq == square):
                x, y = self.sq_to_xy(square)
                self._draw_piece_glyph(x + SQUARE / 2, y + SQUARE / 2, piece)

        if self.best_move_arrow and self.app.show_best_arrow_var.get():
            x1, y1 = self.sq_to_xy(self.best_move_arrow.from_square)
            x2, y2 = self.sq_to_xy(self.best_move_arrow.to_square)
            self.create_line(x1 + SQUARE / 2, y1 + SQUARE / 2, x2 + SQUARE / 2, y2 + SQUARE / 2,
                           fill=COLOR_ARROW_BEST, width=12, arrow=tk.LAST, arrowshape=(26, 32, 14))

    def on_press(self, event):
        if not self.app.human_can_move(): return
        sq = self.xy_to_sq(event.x, event.y)
        if sq is None: return
        piece = self.app.board.piece_at(sq)

        if self.selected_sq is not None and sq in self.legal_targets:
            self.app.attempt_human_move(self.selected_sq, sq)
            self.selected_sq = None
            self.legal_targets = []
            self.redraw()
            return

        if piece and piece.color == self.app.board.turn:
            self.selected_sq = sq
            self.legal_targets = [m.to_square for m in self.app.board.legal_moves if m.from_square == sq]
            self.dragging = True
            self.redraw()
        else:
            self.selected_sq = None
            self.legal_targets = []
            self.redraw()

    def on_drag(self, event):
        if not self.dragging or self.selected_sq is None: return
        piece = self.app.board.piece_at(self.selected_sq)
        if piece: self._draw_piece_glyph(event.x, event.y, piece)

    def on_release(self, event):
        if self.selected_sq is None:
            self.dragging = False
            return
        target = self.xy_to_sq(event.x, event.y)
        self.dragging = False
        if target is not None and target in self.legal_targets:
            self.app.attempt_human_move(self.selected_sq, target)
            self.selected_sq = None
            self.legal_targets = []
        self.redraw()


class EvalBar(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=EVAL_BAR_WIDTH, height=BOARD_PIXELS, highlightthickness=0, bg="#111111", **kwargs)
        self.cp_white = 0
        self.draw()

    def set_eval(self, cp_white):
        self.cp_white = cp_white
        self.draw()

    def draw(self):
        self.delete("all")
        import math
        frac = 1 / (1 + math.exp(-self.cp_white / 350.0))
        white_h = int(BOARD_PIXELS * frac)
        self.create_rectangle(0, 0, EVAL_BAR_WIDTH, BOARD_PIXELS, fill="#222222", outline="")
        self.create_rectangle(0, BOARD_PIXELS - white_h, EVAL_BAR_WIDTH, BOARD_PIXELS, fill="#F5F5F5", outline="")
        label = f"{self.cp_white/100:+.1f}"
        self.create_text(EVAL_BAR_WIDTH / 2, 15, text=label, fill="#111111", font=("Consolas", 10, "bold"))


MODE_PVP = "pvp"
MODE_PVBOT = "pvbot"
MODE_BOTBOT = "botbot"


class ChessApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_TITLE)
        root.configure(bg=BG_DARK)
        root.resizable(False, False)

        self.async_runner = AsyncRunner(root)
        self.board = chess.Board()
        self.classifier = MoveClassifier()

        self.mode_var = tk.StringVar(value=MODE_PVP)
        self.human_color_var = tk.StringVar(value="white")
        self.elo_white = tk.IntVar(value=1500)
        self.elo_black = tk.IntVar(value=1500)
        self.show_best_arrow_var = tk.BooleanVar(value=True)
        self.show_eval_var = tk.BooleanVar(value=True)

        self.san_history = []
        self.row_iids = []
        self.cp_loss_white = []
        self.cp_loss_black = []
        self.ply_count = 0
        self.game_over = False
        self.bot_thinking = False
        self.paused = True

        self.engine_bot_white = None
        self.engine_bot_black = None
        self.engine_analysis = None
        self.engine_path = find_stockfish_path()

        self._build_ui()
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self._init_engines()
        self.new_game()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TFrame", background=BG_PANEL)
        style.configure("TLabel", background=BG_PANEL, foreground=FG_TEXT)
        style.configure("Treeview", background="#232323", foreground=FG_TEXT, rowheight=24)

        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(padx=12, pady=12)

        left = tk.Frame(main, bg=BG_DARK)
        left.grid(row=0, column=0)

        board_row = tk.Frame(left, bg=BG_DARK)
        board_row.pack()

        self.eval_bar = EvalBar(board_row)
        self.eval_bar.pack(side="left", padx=(0, 8))

        self.board_canvas = BoardCanvas(board_row, self)
        self.board_canvas.pack(side="left")

        self.status_label = tk.Label(left, text="Sẵn sàng.", bg=BG_DARK, fg=FG_TEXT, font=("Segoe UI", 11, "bold"))
        self.status_label.pack(pady=(10, 0), anchor="w")

        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="n", padx=(16, 0))

        mode_box = ttk.Frame(right, relief="groove", borderwidth=1)
        mode_box.pack(fill="x", pady=(0, 10))
        ttk.Label(mode_box, text="CHỰ ĐỘ CHƠI", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8, pady=(8, 4))
        for val, text in [(MODE_PVP, "Người vs Người"), (MODE_PVBOT, "Người vs Bot"), (MODE_BOTBOT, "Bot vs Bot")]:
            ttk.Radiobutton(mode_box, text=text, value=val, variable=self.mode_var, command=self.on_mode_change).pack(anchor="w", padx=16, pady=2)

        btns = ttk.Frame(right)
        btns.pack(fill="x", pady=(0, 10))
        ttk.Button(btns, text="Ván mới", command=self.new_game).grid(row=0, column=0, padx=3, sticky="ew")
        ttk.Button(btns, text="Lật bàn", command=self.board_canvas.flip).grid(row=0, column=1, padx=3, sticky="ew")
        ttk.Button(btns, text="Hoàn nước", command=self.undo_move).grid(row=1, column=0, padx=3, sticky="ew")
        ttk.Button(btns, text="Lưu PGN", command=self.save_pgn).grid(row=1, column=1, padx=3, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        moves_box = ttk.Frame(right, relief="groove", borderwidth=1)
        moves_box.pack(fill="both", expand=True, pady=(0, 10))
        ttk.Label(moves_box, text="LỊCH SỬ NƯỚC ĐI", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8, pady=(8, 4))
        cols = ("no", "white", "black")
        self.tree = ttk.Treeview(moves_box, columns=cols, show="headings", height=12)
        self.tree.heading("no", text="#")
        self.tree.heading("white", text="Trắng")
        self.tree.heading("black", text="Đen")
        self.tree.column("no", width=40, anchor="center")
        self.tree.column("white", width=175, anchor="w")
        self.tree.column("black", width=175, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        acc_box = ttk.Frame(right, relief="groove", borderwidth=1)
        acc_box.pack(fill="x")
        ttk.Label(acc_box, text="ĐỘ CHÍNH XÁC", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8, pady=(8, 4))
        self.accuracy_label = ttk.Label(acc_box, text="Trắng: -- %    Đen: -- %", font=("Consolas", 11, "bold"))
        self.accuracy_label.pack(anchor="w", padx=12, pady=(0, 10))

        self.on_mode_change()

    def on_mode_change(self):
        self.new_game()

    def _init_engines(self):
        if not self.engine_path:
            self.status_label.config(text="Không tìm thấy Stockfish.")
            return
        try:
            self.engine_bot_white = EngineWrapper(self.engine_path)
            self.engine_bot_black = EngineWrapper(self.engine_path)
            self.engine_analysis = EngineWrapper(self.engine_path)
            self.status_label.config(text="✓ Đã kết nối Stockfish")
        except Exception as exc:
            messagebox.showerror("Lỗi Stockfish", f"Lỗi:\n{exc}")

    def new_game(self):
        self.board = chess.Board()
        self.san_history = []
        self.row_iids = []
        self.cp_loss_white = []
        self.cp_loss_black = []
        self.ply_count = 0
        self.game_over = False
        self.bot_thinking = False
        self.paused = True
        self.board_canvas.last_move = None
        self.board_canvas.best_move_arrow = None
        self.board_canvas.selected_sq = None
        self.board_canvas.legal_targets = []
        self.board_canvas.redraw()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.eval_bar.set_eval(0)
        self.accuracy_label.config(text="Trắng: -- %    Đen: -- %")
        self.status_label.config(text="Ván mới bắt đầu.")
        if self.engines_ready():
            self.request_suggestion_arrow()
            self.trigger_next_turn()

    def engines_ready(self):
        return self.engine_bot_white and self.engine_bot_black and self.engine_analysis

    def human_can_move(self):
        if self.game_over: return False
        mode = self.mode_var.get()
        if mode == MODE_PVP: return True
        if mode == MODE_PVBOT:
            wanted = chess.WHITE if self.human_color_var.get() == "white" else chess.BLACK
            return self.board.turn == wanted
        return False

    def attempt_human_move(self, from_sq, to_sq):
        if self.bot_thinking: return
        candidates = [m for m in self.board.legal_moves if m.from_square == from_sq and m.to_square == to_sq]
        if not candidates: return
        self.commit_move(candidates[0])

    def commit_move(self, move):
        board_before = self.board.copy()
        mover_color = self.board.turn
        san = self.board.san(move)
        self.board.push(move)
        self.ply_count += 1

        self.board_canvas.last_move = move
        self.board_canvas.selected_sq = None
        self.board_canvas.legal_targets = []
        self.board_canvas.best_move_arrow = None
        self.board_canvas.redraw()

        self.san_history.append(san)
        self._add_move_to_tree(san, mover_color)

        if self.board.is_game_over():
            self.game_over = True
            result = self.board.outcome()
            if result.winner == chess.WHITE:
                msg = "Trắng thắng!"
            elif result.winner == chess.BLACK:
                msg = "Đen thắng!"
            else:
                msg = "Hòa!"
            self.status_label.config(text=msg)
            acc_w = compute_accuracy(self.cp_loss_white)
            acc_b = compute_accuracy(self.cp_loss_black)
            self.accuracy_label.config(text=f"Trắng: {acc_w:.1f}%    Đen: {acc_b:.1f}%")
            messagebox.showinfo("Kết thúc", msg)
            return

        self.trigger_next_turn()
        self.request_suggestion_arrow()

        if self.engines_ready():
            self._request_classification(board_before, move, san, mover_color)

    def trigger_next_turn(self):
        if self.game_over or self.bot_thinking: return
        mode = self.mode_var.get()
        if mode == MODE_PVP: return
        if not self.engines_ready(): return
        if mode == MODE_PVBOT:
            bot_color = chess.BLACK if self.human_color_var.get() == "white" else chess.WHITE
            if self.board.turn == bot_color:
                self.request_bot_move(bot_color)
        elif mode == MODE_BOTBOT and not self.paused:
            self.request_bot_move(self.board.turn)

    def request_bot_move(self, color):
        if self.bot_thinking or self.game_over or not self.engines_ready(): return
        self.bot_thinking = True
        engine = self.engine_bot_white if color == chess.WHITE else self.engine_bot_black
        elo = self.elo_white.get() if color == chess.WHITE else self.elo_black.get()
        board_copy = self.board.copy()

        def work():
            engine.configure_strength(elo)
            return engine.play(board_copy)

        def cb(move, err):
            self.bot_thinking = False
            if err or move is None or self.game_over: return
            if move not in self.board.legal_moves: return
            self.commit_move(move)

        self.async_runner.run(work, cb)

    def request_suggestion_arrow(self):
        if not self.engines_ready() or self.game_over: return
        board_copy = self.board.copy()

        def work():
            res = self.engine_analysis.analyse(board_copy, multipv=1, time_limit=0.3)
            return res[0]["move"] if res else None

        def cb(move, err):
            if err or move is None: return
            if self.board.fen() != board_copy.fen(): return
            self.board_canvas.best_move_arrow = move
            self.board_canvas.redraw()

        self.async_runner.run(work, cb)

    def _request_classification(self, board_before, move, san, mover_color):
        def work():
            top_before = self.engine_analysis.analyse(board_before, multipv=3, time_limit=0.35)
            board_after = board_before.copy()
            board_after.push(move)
            top_after = self.engine_analysis.analyse(board_after, multipv=1, time_limit=0.35)
            eval_white_after = 0
            if top_after:
                cp = top_after[0]["score_cp"]
                eval_white_after = cp if board_after.turn == chess.WHITE else -cp
            return top_before, eval_white_after

        def cb(result, err):
            if err or result is None: return
            top_before, eval_white_after = result
            eval_after_mover = eval_white_after if mover_color == chess.WHITE else -eval_white_after
            best_cp = top_before[0]["score_cp"] if top_before else eval_after_mover
            cls = self.classifier.classify(board_before, move, top_before, best_cp, eval_after_mover)
            cp_loss = max(0, best_cp - eval_after_mover)

            label_vn, icon, _, _ = CLASS_STYLE[cls]
            turn_name = "Trắng" if mover_color == chess.WHITE else "Đen"
            self.status_label.config(text=f"[{turn_name}] {icon} {label_vn.upper()}")

            if mover_color == chess.WHITE:
                self.cp_loss_white.append(cp_loss)
            else:
                self.cp_loss_black.append(cp_loss)
            if self.show_eval_var.get():
                self.eval_bar.set_eval(eval_white_after)

        self.async_runner.run(work, cb)

    def _add_move_to_tree(self, san, mover_color):
        move_no = (self.ply_count + 1) // 2
        if mover_color == chess.WHITE:
            iid = self.tree.insert("", "end", values=(move_no, san, ""))
            self.row_iids.append(iid)
        else:
            if self.row_iids:
                iid = self.row_iids[-1]
                vals = list(self.tree.item(iid, "values"))
                vals[2] = san
                self.tree.item(iid, values=vals)

    def undo_move(self):
        if self.bot_thinking or not self.board.move_stack: return
        self.board.pop()
        self.ply_count -= 1
        if self.san_history: self.san_history.pop()
        if self.row_iids:
            iid = self.row_iids[-1]
            if self.board.turn == chess.BLACK:
                vals = list(self.tree.item(iid, "values"))
                vals[2] = ""
                self.tree.item(iid, values=vals)
            else:
                self.tree.delete(iid)
                self.row_iids.pop()
        self.game_over = False
        self.board_canvas.last_move = self.board.peek() if self.board.move_stack else None
        self.board_canvas.redraw()
        self.request_suggestion_arrow()

    def save_pgn(self):
        game = chess.pgn.Game()
        node = game
        for mv in self.board.move_stack:
            node = node.add_variation(mv)
        path = filedialog.asksaveasfilename(defaultextension=".pgn", filetypes=[("PGN files", "*.pgn")])
        if not path: return
        with open(path, "w") as f:
            f.write(str(game))
        messagebox.showinfo("Lưu thành công", f"Đã lưu tại:\n{path}")

    def on_close(self):
        for e in (self.engine_bot_white, self.engine_bot_black, self.engine_analysis):
            if e:
                try:
                    e.close()
                except:
                    pass
        self.async_runner.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
