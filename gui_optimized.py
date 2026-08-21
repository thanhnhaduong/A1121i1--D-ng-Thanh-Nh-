#!/usr/bin/env python3
"""
♟ CHESS MASTER - Optimized & Fast with Move Evaluation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import chess
from chess_engine import ChessGame, MultiEngineGame, MoveEvaluation, MoveClassifier
from openings_50 import get_opening_by_moves, get_all_openings, get_teaching_data
from puzzles import get_all_puzzles, count_puzzles

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("♟ CHESS MASTER - Cờ Vua Stockfish (Tối ưu)")
        self.root.geometry("1300x800")

        self.game = None
        self.game_mode = None
        self.is_human_white = True
        self.ai_thinking = False
        self.selected_square = None
        self.opponent_elo = 1600
        self.eval_cache = {}
        self.board_flipped = False  # Xoay bàn cờ
        self.eval_mode = "classification"  # classification, centipawn, advanced

        self.square_size = 60

        self.COLORS = {
            'light': '#f0d9b5',
            'dark': '#b58863',
            'check': '#ff4444',
            'white': '#ffffff',
            'black': '#000000'
        }

        self.PIECE_UNICODE = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }

        # ELO thật (UCI_Elo) thay vì Skill Level nội bộ (0-20, không map ra ELO
        # thực). Dưới ~1320 elo, Stockfish tự nó không thể yếu hơn được nữa,
        # engine sẽ giả lập thêm bằng cách random hóa 1 phần nước đi
        # (xem ChessGame.get_best_move trong chess_engine.py).
        self.ELO_LEVELS = {
            'Tân Thủ (~400 Elo)': 400,
            'Người Mới (~800 Elo)': 800,
            'Nghiệp Dư (1300 Elo)': 1300,
            'Trung Cấp (1600 Elo)': 1600,
            'Khá (1900 Elo)': 1900,
            'Giỏi (2200 Elo)': 2200,
            'Kiện Tướng (2500 Elo)': 2500,
            'Đại Kiện Tướng (2850 Elo)': 2850,
            'Siêu Đại KT (3190 Elo)': 3190,
        }

        self.setup_ui()

    def setup_ui(self):
        main = tk.Frame(self.root, bg='#1a1a1a')
        main.pack(fill=tk.BOTH, expand=True)

        # Evaluation bar
        self.eval_canvas = tk.Canvas(main, width=1200, height=35, bg='#333333', highlightthickness=0)
        self.eval_canvas.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.eval_label = tk.Label(main, text="Đánh giá: 0.00 | Bằng nhau",
                                   bg='#1a1a1a', fg='#ffffff', font=("Arial", 9))
        self.eval_label.pack(fill=tk.X, padx=10, pady=(0, 2))

        # Move analysis display
        self.analysis_frame = tk.Frame(main, bg='#1a1a1a')
        self.analysis_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.analysis_label = tk.Label(self.analysis_frame, text="", bg='#1a1a1a',
                                      fg='#aaaaaa', font=("Arial", 8), wraplength=1200, justify=tk.LEFT)
        self.analysis_label.pack(fill=tk.X)

        # Main area
        middle = tk.Frame(main, bg='#1a1a1a')
        middle.pack(fill=tk.BOTH, expand=True, padx=10)

        # Board
        left = tk.Frame(middle, bg='#1a1a1a')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(left, width=480, height=480, bg=self.COLORS['light'],
                               highlightthickness=1, highlightbackground='#444')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_board_click)

        # Right panel
        right = tk.Frame(middle, bg='#2a2a2a', width=380)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right.pack_propagate(False)

        self.create_right_panel(right)

        # Analysis button only
        self.analysis_btn = ttk.Button(main, text="🔍 Xem Phân Tích (Bot Tiếp Tục)",
                                       command=self.show_analysis, state=tk.DISABLED)
        self.analysis_btn.pack(fill=tk.X, padx=10, pady=5)

    def create_right_panel(self, parent):
        # Game mode
        tk.Label(parent, text="🎮 Chế Độ", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Button(parent, text="👥 2 Người", command=lambda: self.start_game("human_vs_human"),
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="🤖 vs AI", command=self.select_difficulty,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="🤖🤖 AI vs AI", command=self.show_engine_dialog,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        # Puzzle Mode
        tk.Label(parent, text="🧩 Câu Đố", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(15, 5))

        ttk.Button(parent, text=f"🧩 Giải Câu Đố ({count_puzzles()}+)", command=self.show_puzzles,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        # Evaluation Mode
        tk.Label(parent, text="📊 Chế Độ Đánh Giá", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(15, 5))

        eval_mode_var = tk.StringVar(value="classification")

        ttk.Radiobutton(parent, text="🎯 Phân Loại (Brilliant/Best/etc)",
                       variable=eval_mode_var, value="classification",
                       command=lambda: self.set_eval_mode("classification")).pack(anchor=tk.W, padx=15, pady=2)

        ttk.Radiobutton(parent, text="📈 Centipawn (+3.45 pawn)",
                       variable=eval_mode_var, value="centipawn",
                       command=lambda: self.set_eval_mode("centipawn")).pack(anchor=tk.W, padx=15, pady=2)

        ttk.Radiobutton(parent, text="🧠 Advanced (Kết hợp cả 2)",
                       variable=eval_mode_var, value="advanced",
                       command=lambda: self.set_eval_mode("advanced")).pack(anchor=tk.W, padx=15, pady=2)

        # Opening
        tk.Label(parent, text="📚 Khai Cuộc", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(15, 5))

        ttk.Button(parent, text="Xem 70+ Khai Cuộc", command=self.show_openings,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="📖 Học Khai Cuộc", command=self.show_teaching,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        self.opening_label = tk.Label(parent, text="Khai cuộc: -", bg='#2a2a2a',
                                     fg='#ffaa00', font=("Arial", 9), wraplength=360)
        self.opening_label.pack(fill=tk.X, padx=10, pady=2)

        # Status
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

        self.status_label = tk.Label(parent, text="Sẵn sàng chơi", bg='#2a2a2a',
                                    fg='#4a9eff', font=("Arial", 10, "bold"), wraplength=360)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Controls
        ttk.Button(parent, text="↶ Hoàn tác", command=self.undo_move,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="🔄 Làm mới", command=self.reset_game,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="💡 Gợi Ý Nước Đi", command=self.suggest_move,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

        ttk.Button(parent, text="🔄 Xoay Bàn Cờ", command=self.flip_board,
                  width=30).pack(fill=tk.X, padx=10, pady=2)

    def get_display_coords(self, row, col):
        """Chuyển đổi tọa độ dựa trên trạng thái xoay bàn"""
        if self.board_flipped:
            row = 7 - row
            col = 7 - col
        return row, col

    def draw_board(self, skip_square=None):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                disp_row, disp_col = self.get_display_coords(row, col)
                x1, y1 = disp_col * self.square_size, disp_row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                color = self.COLORS['light'] if (row + col) % 2 == 0 else self.COLORS['dark']
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        if self.game and self.game.is_check():
            king_pos = self.game.board.king(self.game.board.turn)
            if king_pos:
                row, col = king_pos // 8, king_pos % 8
                disp_row, disp_col = self.get_display_coords(row, col)
                x1, y1 = disp_col * self.square_size, disp_row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.COLORS['check'], width=3)

        if self.game:
            for square in chess.SQUARES:
                if square == skip_square:
                    continue
                piece = self.game.board.piece_at(square)
                if piece:
                    row, col = square // 8, square % 8
                    disp_row, disp_col = self.get_display_coords(row, col)
                    x = disp_col * self.square_size + self.square_size // 2
                    y = disp_row * self.square_size + self.square_size // 2
                    piece_color = self.COLORS['white'] if piece.color else self.COLORS['black']
                    self.canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                           font=("Arial", 50, "bold"), fill=piece_color)

    def animate_move(self, from_square, to_square, on_complete=None, duration_ms=150, steps=8):
        """Trượt quân cờ mượt từ from_square sang to_square (dựa trên trạng thái
        bàn cờ TRƯỚC khi nước đi được thực hiện), rồi gọi on_complete để cập
        nhật logic game (make_move, vẽ lại bàn cờ cuối cùng...). Nhập thành,
        bắt tốt qua đường chỉ animate quân chính, quân/tốt phụ (xe nhập thành,
        tốt bị bắt qua đường) sẽ hiện đúng vị trí cuối khi vẽ lại bàn cờ."""
        if not self.game:
            if on_complete:
                on_complete()
            return

        piece = self.game.board.piece_at(from_square)
        if not piece:
            if on_complete:
                on_complete()
            return

        from_row, from_col = from_square // 8, from_square % 8
        to_row, to_col = to_square // 8, to_square % 8
        disp_from_row, disp_from_col = self.get_display_coords(from_row, from_col)
        disp_to_row, disp_to_col = self.get_display_coords(to_row, to_col)

        start_x = disp_from_col * self.square_size + self.square_size // 2
        start_y = disp_from_row * self.square_size + self.square_size // 2
        end_x = disp_to_col * self.square_size + self.square_size // 2
        end_y = disp_to_row * self.square_size + self.square_size // 2

        # Vẽ bàn cờ (thế trước khi đi) nhưng ẩn quân đang di chuyển ở ô xuất phát
        self.draw_board(skip_square=from_square)

        piece_color = self.COLORS['white'] if piece.color else self.COLORS['black']
        moving_piece = self.canvas.create_text(start_x, start_y, text=self.PIECE_UNICODE[piece.symbol()],
                                               font=("Arial", 50, "bold"), fill=piece_color)

        step_delay = max(10, duration_ms // steps)

        def step(i):
            if not self.canvas.winfo_exists():
                return
            if i > steps:
                self.canvas.delete(moving_piece)
                if on_complete:
                    on_complete()
                return
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            self.canvas.coords(moving_piece, x, y)
            self.root.after(step_delay, lambda: step(i + 1))

        step(1)

    def on_board_click(self, event):
        if not self.game or self.ai_thinking:
            return

        if self.game.is_game_over():
            messagebox.showinfo("Trò Chơi Kết Thúc", self.get_game_result())
            return

        if self.game_mode == 'human_vs_ai':
            if self.game.get_current_turn() == 'white' and not self.is_human_white:
                return
            if self.game.get_current_turn() == 'black' and self.is_human_white:
                return

        col = event.x // self.square_size
        row = event.y // self.square_size

        # Xử lý bàn cờ xoay
        if self.board_flipped:
            row = 7 - row
            col = 7 - col

        square = row * 8 + col

        if self.selected_square is None:
            piece = self.game.board.piece_at(square)
            if piece and piece.color == self.game.board.turn:
                self.selected_square = square
                self.highlight_moves(square)
        else:
            promotion_piece = None
            if self._is_promotion_move(self.game.board, self.selected_square, square):
                promotion_piece = self._ask_promotion_piece()
            move = chess.Move(self.selected_square, square, promotion=promotion_piece)
            if move in self.game.board.legal_moves:
                from_sq, to_sq = self.selected_square, square
                self.selected_square = None

                def after_anim(move_uci=move.uci()):
                    self.game.make_move(move_uci)
                    self.draw_board()
                    self.update_all()

                    if self.game.is_game_over():
                        self.root.after(500, lambda: messagebox.showinfo("Trò Chơi Kết Thúc", self.get_game_result()))
                    elif self.game_mode == 'human_vs_ai' and not self.game.is_game_over():
                        self.root.after(1000, self.ai_move)

                self.animate_move(from_sq, to_sq, on_complete=after_anim)
            else:
                self.selected_square = None
                self.draw_board()

    def _draw_generic_board(self, canvas, board, sq_size, piece_font_size, skip_square=None):
        """Vẽ bàn cờ dùng chung cho các cửa sổ phụ (AI vs AI, Học Khai Cuộc,
        Phân Tích Thế Cờ) - không phụ thuộc self.canvas/self.game như draw_board()."""
        canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1, y1 = col * sq_size, row * sq_size
                x2, y2 = x1 + sq_size, y1 + sq_size
                color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        for square in chess.SQUARES:
            if square == skip_square:
                continue
            piece = board.piece_at(square)
            if piece:
                row, col = square // 8, square % 8
                x = col * sq_size + sq_size // 2
                y = row * sq_size + sq_size // 2
                piece_color = '#ffffff' if piece.color else '#000000'
                canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                  font=("Arial", piece_font_size, "bold"), fill=piece_color)

    def _animate_slide_blocking(self, canvas, window, board_before, move, sq_size, piece_font_size,
                                steps=6, total_ms=120):
        """Trượt quân cờ mượt cho các cửa sổ phụ chạy trong THREAD NỀN (AI vs AI,
        Học Khai Cuộc, Phân Tích Thế Cờ) - dùng time.sleep() + window.update()
        thay vì root.after() vì hàm này được gọi từ thread nền, không phải main
        thread (root.after() lập lịch cho main thread, không phù hợp ở đây)."""
        import time

        piece = board_before.piece_at(move.from_square)
        if not piece or not window.winfo_exists():
            return

        from_row, from_col = move.from_square // 8, move.from_square % 8
        to_row, to_col = move.to_square // 8, move.to_square % 8
        start_x = from_col * sq_size + sq_size // 2
        start_y = from_row * sq_size + sq_size // 2
        end_x = to_col * sq_size + sq_size // 2
        end_y = to_row * sq_size + sq_size // 2

        self._draw_generic_board(canvas, board_before, sq_size, piece_font_size, skip_square=move.from_square)

        piece_color = '#ffffff' if piece.color else '#000000'
        moving_piece = canvas.create_text(start_x, start_y, text=self.PIECE_UNICODE[piece.symbol()],
                                          font=("Arial", piece_font_size, "bold"), fill=piece_color)

        step_delay = max(0.01, (total_ms / 1000) / steps)
        for i in range(1, steps + 1):
            if not window.winfo_exists():
                return
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            canvas.coords(moving_piece, x, y)
            window.update()
            time.sleep(step_delay)

        canvas.delete(moving_piece)

    def highlight_best_move(self, move):
        """Bôi vàng nước đi tốt nhất"""
        self.draw_board()

        from_row, from_col = move.from_square // 8, move.from_square % 8
        to_row, to_col = move.to_square // 8, move.to_square % 8

        disp_from_row, disp_from_col = self.get_display_coords(from_row, from_col)
        disp_to_row, disp_to_col = self.get_display_coords(to_row, to_col)

        # Highlight from square (nguồn)
        x1, y1 = disp_from_col * self.square_size, disp_from_row * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='#FFFF00', width=4)

        # Highlight to square (đích)
        x1, y1 = disp_to_col * self.square_size, disp_to_row * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='#FFFF00', width=4)

        # Draw arrow from-to
        from_center_x = disp_from_col * self.square_size + self.square_size // 2
        from_center_y = disp_from_row * self.square_size + self.square_size // 2
        to_center_x = disp_to_col * self.square_size + self.square_size // 2
        to_center_y = disp_to_row * self.square_size + self.square_size // 2

        self.canvas.create_line(from_center_x, from_center_y, to_center_x, to_center_y,
                               fill='#FFFF00', width=3, arrow=tk.LAST)

    def _is_promotion_move(self, board, from_square, to_square):
        """Kiểm tra xem đây có phải nước tốt phong cấp hợp lệ không (bất kỳ
        quân phong cấp nào), để quyết định có cần hỏi người chơi hay không."""
        piece = board.piece_at(from_square)
        if not piece or piece.piece_type != chess.PAWN:
            return False
        to_rank = chess.square_rank(to_square)
        if not ((piece.color == chess.WHITE and to_rank == 7) or
                (piece.color == chess.BLACK and to_rank == 0)):
            return False
        return any(chess.Move(from_square, to_square, promotion=p) in board.legal_moves
                   for p in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT))

    def _ask_promotion_piece(self):
        """Hiện dialog chọn quân phong cấp (Hậu/Xe/Tượng/Mã), trả về loại quân."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Phong Cấp")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        result = {'piece': chess.QUEEN}

        tk.Label(dialog, text="Chọn quân phong cấp:", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        btn_frame = tk.Frame(dialog)
        btn_frame.pack()

        pieces = [
            ('♕', chess.QUEEN, 'Hậu'),
            ('♖', chess.ROOK, 'Xe'),
            ('♗', chess.BISHOP, 'Tượng'),
            ('♘', chess.KNIGHT, 'Mã'),
        ]

        def choose(piece_type):
            result['piece'] = piece_type
            dialog.destroy()

        for symbol, piece_type, name in pieces:
            tk.Button(btn_frame, text=f"{symbol}\n{name}", command=lambda p=piece_type: choose(p),
                     font=("Arial", 14), width=4, height=2).pack(side=tk.LEFT, padx=4, pady=5)

        dialog.protocol("WM_DELETE_WINDOW", lambda: choose(chess.QUEEN))
        self.root.wait_window(dialog)
        return result['piece']

    def highlight_moves(self, square):
        self.draw_board()

        row, col = square // 8, square % 8
        disp_row, disp_col = self.get_display_coords(row, col)
        x1, y1 = disp_col * self.square_size, disp_row * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=3)

        for move in self.game.board.legal_moves:
            if move.from_square == square:
                to_row, to_col = move.to_square // 8, move.to_square % 8
                disp_to_row, disp_to_col = self.get_display_coords(to_row, to_col)
                x = disp_to_col * self.square_size + self.square_size // 2
                y = disp_to_row * self.square_size + self.square_size // 2
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='lime')

    def ai_move(self):
        if not self.game or self.game.is_game_over():
            return

        self.ai_thinking = True
        self.status_label.config(text="🤖 AI đang suy nghĩ...")
        self.root.update_idletasks()

        best_move = self.game.get_best_move(time_ms=2000)

        if best_move:
            move = chess.Move.from_uci(best_move)

            def after_anim():
                self.game.make_move(best_move)
                self.draw_board()
                self.update_all()
                self.ai_thinking = False

                if self.game.is_game_over():
                    messagebox.showinfo("Kết Thúc", self.get_game_result())
                else:
                    self.status_label.config(text="Lượt của bạn")

            self.animate_move(move.from_square, move.to_square, on_complete=after_anim)
        else:
            self.ai_thinking = False
            if self.game.is_game_over():
                messagebox.showinfo("Kết Thúc", self.get_game_result())
            else:
                self.status_label.config(text="Lượt của bạn")

    def select_difficulty(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Chọn Độ Khó")
        dialog.geometry("320x480")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Độ khó AI (ELO):", font=("Arial", 11, "bold")).pack(pady=15)

        selected = tk.StringVar(value="Trung Cấp (1600 Elo)")

        for level in self.ELO_LEVELS.keys():
            tk.Radiobutton(dialog, text=level, variable=selected, value=level,
                          font=("Arial", 10)).pack(anchor=tk.W, padx=30, pady=3)

        def start():
            self.opponent_elo = self.ELO_LEVELS[selected.get()]
            self.start_game("human_vs_ai")
            dialog.destroy()

        tk.Button(dialog, text="Chơi", command=start, bg='#4a9eff', fg='white',
                 font=("Arial", 10, "bold"), padx=15, pady=8).pack(pady=15)

    def show_engine_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("AI vs AI")
        dialog.geometry("320x700")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Trắng:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        white = tk.StringVar(value="Khá (1900 Elo)")
        for level in self.ELO_LEVELS.keys():
            tk.Radiobutton(dialog, text=level, variable=white, value=level,
                          font=("Arial", 9)).pack(anchor=tk.W, padx=30, pady=1)

        tk.Label(dialog, text="Đen:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        black = tk.StringVar(value="Trung Cấp (1600 Elo)")
        for level in self.ELO_LEVELS.keys():
            tk.Radiobutton(dialog, text=level, variable=black, value=level,
                          font=("Arial", 9)).pack(anchor=tk.W, padx=30, pady=1)

        def start():
            white_elo = self.ELO_LEVELS[white.get()]
            black_elo = self.ELO_LEVELS[black.get()]
            self.run_battle(white_elo, black_elo)
            dialog.destroy()

        tk.Button(dialog, text="Chơi", command=start, bg='#4a9eff', fg='white',
                 font=("Arial", 10, "bold"), padx=15, pady=8).pack(pady=15)

    def run_battle(self, white_elo, black_elo):
        """AI vs AI video-style battle with close-up view"""
        win = tk.Toplevel(self.root)
        win.title(f"🎬 AI vs AI Video - {white_elo} vs {black_elo}")
        win.geometry("850x750")
        win.configure(bg='#1a1a1a')

        # Title
        title = tk.Label(win, text=f"♔ {white_elo} vs {black_elo} ♚",
                        bg='#1a1a1a', fg='#4a9eff', font=("Arial", 14, "bold"), pady=10)
        title.pack(fill=tk.X)

        # Status
        status_label = tk.Label(win, text="⏳ Đang tính toán...", bg='#1a1a1a',
                               fg='#ffaa00', font=("Arial", 11, "bold"))
        status_label.pack(fill=tk.X, padx=10, pady=5)

        # Board canvas
        board_canvas = tk.Canvas(win, width=480, height=480, bg='#f0d9b5',
                                highlightthickness=2, highlightbackground='#444')
        board_canvas.pack(pady=10)

        # Info frame
        info_frame = tk.Frame(win, bg='#2a2a2a', height=120)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        info_frame.pack_propagate(False)

        # Move info
        move_info = tk.Label(info_frame, text="Nước: ...", bg='#2a2a2a',
                            fg='#ffaa00', font=("Arial", 11, "bold"), padx=10, pady=5)
        move_info.pack(fill=tk.X)

        # Evaluation
        eval_info = tk.Label(info_frame, text="Đánh giá: ...", bg='#2a2a2a',
                            fg='#ffffff', font=("Arial", 10), padx=10)
        eval_info.pack(fill=tk.X)

        # Move list
        moves_info = tk.Label(info_frame, text="", bg='#2a2a2a',
                             fg='#ffffff', font=("Arial", 9), padx=10, pady=5, wraplength=800, justify=tk.LEFT)
        moves_info.pack(fill=tk.BOTH, expand=True)

        # Control frame
        control_frame = tk.Frame(win, bg='#2a2a2a')
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        speed_var = tk.StringVar(value="Normal")
        ttk.Label(control_frame, text="Tốc độ:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(control_frame, textvariable=speed_var,
                    values=["Chậm (4s)", "Normal (2s)", "Nhanh (1s)", "Flash (0.5s)"],
                    state='readonly', width=15).pack(side=tk.LEFT, padx=5)

        pause_btn = [ttk.Button(control_frame, text="⏸ Tạm Dừng")]
        pause_btn[0].pack(side=tk.LEFT, padx=5)

        # Chạy trận đấu: TÍNH nước đi rồi HIỆN NGAY từng nước một (không tính
        # trước toàn bộ ván rồi mới phát lại) - vừa tính vừa chạy.
        def play_battle():
            import time
            import random
            try:
                status_label.config(text="🔄 Đang khởi tạo engine...")
                win.update()

                game = MultiEngineGame(engine1_elo=white_elo, engine2_elo=black_elo)

                status_label.config(text="▶️ Đang thi đấu trực tiếp...")

                moves = []

                for i in range(200):
                    if not win.winfo_exists():
                        return
                    if game.board.is_game_over():
                        break

                    # Get speed mỗi vòng để người dùng đổi tốc độ giữa chừng vẫn có tác dụng
                    speed_text = speed_var.get()
                    if "Chậm" in speed_text:
                        delay = 4
                    elif "Nhanh" in speed_text:
                        delay = 1
                    elif "Flash" in speed_text:
                        delay = 0.5
                    else:
                        delay = 2

                    # Tính nước đi CHO LƯỢT HIỆN TẠI
                    if game.board.turn:
                        engine, random_chance = game.stockfish1, game.engine1_random_chance
                    else:
                        engine, random_chance = game.stockfish2, game.engine2_random_chance

                    engine.set_fen_position(game.board.fen())
                    best_move_uci = engine.get_best_move_time(1000)
                    if not best_move_uci:
                        break

                    if random_chance > 0 and random.random() < random_chance:
                        legal_moves = list(game.board.legal_moves)
                        if legal_moves:
                            best_move_uci = random.choice(legal_moves).uci()

                    move = chess.Move.from_uci(best_move_uci)

                    # Trượt quân trước khi cập nhật thế cờ thật
                    self._animate_slide_blocking(board_canvas, win, game.board, move, sq_size=60, piece_font_size=40)

                    game.board.push(move)
                    game.moves.append(best_move_uci)
                    moves.append(best_move_uci)

                    # HIỂN THỊ NGAY nước vừa tính xong
                    side = "♔ Trắng" if i % 2 == 0 else "♚ Đen"
                    move_num = (i // 2) + 1
                    move_info.config(text=f"Nước {i+1} ({side}): {best_move_uci}")

                    try:
                        eval_val = engine.get_evaluation()
                        if eval_val and eval_val.get('type') == 'cp':
                            eval_info.config(text=f"📊 Đánh giá: {eval_val['value']/100:+.2f}")
                    except:
                        pass

                    if i % 2 == 1:
                        move_text = f"{move_num}. {moves[i-1]} {best_move_uci}"
                    else:
                        move_text = ""

                    if move_text:
                        current = moves_info.cget("text")
                        new_text = current + move_text + "  "
                        if len(new_text.split()) > 50:
                            new_text = " ".join(new_text.split()[-40:])
                        moves_info.config(text=new_text)

                    draw_board_video(game.board)

                    time.sleep(delay)

                # Final state
                result = game.get_result()
                status_label.config(text=f"✅ Kết Thúc: {result}")
                move_info.config(text=f"🏁 Trò chơi kết thúc sau {len(moves)} nước")

            except Exception as e:
                status_label.config(text=f"❌ Lỗi: {str(e)}")

        def draw_board_video(board):
            """Vẽ bàn cờ cho video"""
            self._draw_generic_board(board_canvas, board, 60, 40)
            win.update()

        import threading
        thread = threading.Thread(target=play_battle, daemon=True)
        thread.start()

    def show_openings(self):
        win = tk.Toplevel(self.root)
        win.title("50+ Khai Cuộc")
        win.geometry("700x500")

        openings = get_all_openings()

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll = ttk.Scrollbar(frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, font=("Arial", 10), yscrollcommand=scroll.set,
                            bg='#2a2a2a', fg='#ffffff', height=20)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=listbox.yview)

        for name in openings.keys():
            listbox.insert(tk.END, name)

        def show_detail():
            if not listbox.curselection():
                return
            name = listbox.get(listbox.curselection()[0])
            opening = openings[name]

            detail = tk.Toplevel(win)
            detail.title(name)
            detail.geometry("650x450")

            text = tk.Text(detail, font=("Arial", 10), wrap=tk.WORD, bg='#2a2a2a', fg='#ffffff')
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            text.insert(tk.END, f"📖 {name}\n\n")
            text.insert(tk.END, f"📝 Mô tả:\n{opening['description']}\n\n")
            text.insert(tk.END, f"📅 Lịch sử:\n{opening['history']}\n\n")
            text.insert(tk.END, f"💡 Ý tưởng:\n{opening['idea']}\n\n")
            text.insert(tk.END, f"🎲 Nước: {' → '.join(opening['moves'])}\n")
            text.config(state=tk.DISABLED)

        ttk.Button(win, text="Xem Chi Tiết", command=show_detail).pack(pady=10)

    def show_teaching(self):
        """Hiển thị chế độ dạy khai cuộc"""
        openings = get_all_openings()

        win = tk.Toplevel(self.root)
        win.title("📖 Học Khai Cuộc")
        win.geometry("700x550")

        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll = ttk.Scrollbar(frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, font=("Arial", 10), yscrollcommand=scroll.set,
                            bg='#2a2a2a', fg='#ffffff', height=20)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=listbox.yview)

        for name in openings.keys():
            listbox.insert(tk.END, name)

        def show_lesson():
            if not listbox.curselection():
                messagebox.showwarning("Chọn Khai Cuộc", "Vui lòng chọn một khai cuộc")
                return

            name = listbox.get(listbox.curselection()[0])
            teaching_data = get_teaching_data(name)

            lesson = tk.Toplevel(win)
            lesson.title(f"Học: {name}")
            lesson.geometry("700x600")

            # Title
            title = tk.Label(lesson, text=f"📖 {name}", bg='#2a2a2a', fg='#4a9eff',
                            font=("Arial", 14, "bold"), padx=10, pady=10)
            title.pack(fill=tk.X)

            # Teaching steps
            if teaching_data:
                steps_text = tk.Text(lesson, font=("Arial", 11), wrap=tk.WORD,
                                    bg='#1a1a1a', fg='#ffffff', height=15)
                steps_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                steps_text.insert(tk.END, "🎯 Các Bước Học:\n\n")
                for i, (move, explanation) in enumerate(teaching_data.get("steps", []), 1):
                    steps_text.insert(tk.END, f"Bước {i}: {move}\n")
                    steps_text.insert(tk.END, f"{explanation}\n\n")

                steps_text.insert(tk.END, f"\n📝 Tóm Tắt:\n{teaching_data.get('summary', '')}\n")
                steps_text.config(state=tk.DISABLED)
            else:
                info = tk.Label(lesson, text=f"Khai cuộc '{name}' chưa có dữ liệu dạy.\nHãy xem chi tiết trong '70+ Khai Cuộc'",
                               bg='#2a2a2a', fg='#ffaa00', font=("Arial", 12), padx=20, pady=20)
                info.pack()

        def show_animation():
            """Xem hoạt ảnh khai cuộc"""
            if not listbox.curselection():
                messagebox.showwarning("Chọn Khai Cuộc", "Vui lòng chọn một khai cuộc")
                return

            name = listbox.get(listbox.curselection()[0])
            openings_data = get_all_openings()

            if name not in openings_data:
                messagebox.showerror("Lỗi", "Khai cuộc không tìm thấy")
                return

            opening = openings_data[name]
            moves = opening.get('moves', [])

            if not moves:
                messagebox.showwarning("Không Có Nước", "Khai cuộc này không có nước để hiển thị")
                return

            # Create animation window
            anim_win = tk.Toplevel(win)
            anim_win.title(f"🎬 Hoạt Ảnh - {name}")
            anim_win.geometry("700x650")

            # Status
            status_label = tk.Label(anim_win, text="▶️ Đang phát...", bg='#2a2a2a',
                                   fg='#4a9eff', font=("Arial", 11, "bold"), padx=10, pady=10)
            status_label.pack(fill=tk.X)

            # Canvas for board
            canvas = tk.Canvas(anim_win, width=480, height=480, bg='#f0d9b5',
                              highlightthickness=1, highlightbackground='#444')
            canvas.pack(pady=5)

            # Info
            info_label = tk.Label(anim_win, text="Nước: ...", bg='#2a2a2a',
                                 fg='#ffaa00', font=("Arial", 10, "bold"), padx=10, pady=5)
            info_label.pack(fill=tk.X)

            def draw_board(board):
                self._draw_generic_board(canvas, board, 60, 40)
                anim_win.update()

            def animate():
                try:
                    playback_board = chess.Board()

                    for i, move_uci in enumerate(moves):
                        try:
                            move = chess.Move.from_uci(move_uci)
                        except:
                            continue

                        # Trượt quân trước khi cập nhật thế cờ thật
                        self._animate_slide_blocking(canvas, anim_win, playback_board, move,
                                                     sq_size=60, piece_font_size=40)
                        playback_board.push(move)

                        side = "Trắng ♔" if i % 2 == 0 else "Đen ♚"
                        info_label.config(text=f"Nước {i+1} ({side}): {move_uci}")
                        draw_board(playback_board)

                        import time
                        time.sleep(2)

                    status_label.config(text=f"✅ Xong! ({len(moves)} nước)")
                    info_label.config(text=f"Khai cuộc hoàn thành: {opening.get('description', '')}")

                except Exception as e:
                    status_label.config(text=f"❌ Lỗi: {str(e)}")

            import threading
            thread = threading.Thread(target=animate, daemon=True)
            thread.start()

        # Buttons
        btn_frame = tk.Frame(win, bg='#2a2a2a')
        btn_frame.pack(pady=10, fill=tk.X, padx=10)

        ttk.Button(btn_frame, text="🎓 Bắt Đầu Học", command=show_lesson).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="▶️ Xem Hoạt Ảnh", command=show_animation).pack(side=tk.LEFT, padx=5)

    def show_analysis(self):
        """Chạy tiếp tục trò chơi bằng 2 bot Stockfish từ vị trí hiện tại - Với animation"""
        if not self.game or not self.game.stockfish_available:
            messagebox.showwarning("Lỗi", "Stockfish không khả dụng")
            return

        # Tạo cửa sổ phân tích
        analysis_win = tk.Toplevel(self.root)
        analysis_win.title("🎬 Phân Tích Video - Bot Tiếp Tục")
        analysis_win.geometry("700x650")

        # Control frame
        control_frame = tk.Frame(analysis_win, bg='#2a2a2a', height=50)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        status_label = tk.Label(control_frame, text="⏳ Đang tính toán...", bg='#2a2a2a',
                               fg='#4a9eff', font=("Arial", 11, "bold"))
        status_label.pack(side=tk.LEFT, padx=10)

        # Canvas for board
        canvas = tk.Canvas(analysis_win, width=480, height=480, bg='#f0d9b5',
                          highlightthickness=1, highlightbackground='#444')
        canvas.pack(pady=5)

        # Info label
        info_label = tk.Label(analysis_win, text="Nước: ...", bg='#2a2a2a',
                             fg='#ffaa00', font=("Arial", 10, "bold"), padx=10, pady=5)
        info_label.pack(fill=tk.X)

        def draw_board(board):
            """Vẽ bàn cờ"""
            self._draw_generic_board(canvas, board, 60, 40)
            analysis_win.update()

        # Animation in thread
        def run_analysis():
            try:
                # Create continuation game
                analysis_game = ChessGame()
                analysis_game.board = self.game.board.copy()

                moves = []
                for i in range(6):
                    if analysis_game.board.is_game_over():
                        break

                    analysis_game.stockfish.set_fen_position(analysis_game.board.fen())
                    best_move = analysis_game.stockfish.get_best_move_time(2000)
                    if not best_move:
                        break

                    moves.append(best_move)
                    move = chess.Move.from_uci(best_move)
                    analysis_game.board.push(move)

                # Playback animation
                status_label.config(text="▶️ Đang phát...")
                playback_board = self.game.board.copy()

                for i, move_uci in enumerate(moves):
                    move = chess.Move.from_uci(move_uci)

                    # Trượt quân trước khi cập nhật thế cờ thật
                    self._animate_slide_blocking(canvas, analysis_win, playback_board, move,
                                                 sq_size=60, piece_font_size=40)
                    playback_board.push(move)

                    # Update display
                    side = "Trắng ♔" if i % 2 == 0 else "Đen ♚"
                    info_label.config(text=f"Nước {i+1} ({side}): {move_uci}")

                    # Draw board
                    draw_board(playback_board)

                    # Wait 2 seconds between moves
                    import time
                    time.sleep(2)

                # Final eval
                final_eval = analysis_game.stockfish.get_evaluation()
                eval_str = ""
                if final_eval:
                    eval_val = final_eval['value'] / 100
                    eval_str = f"  |  📊 {eval_val:+.2f}"
                    if eval_val > 3:
                        eval_str += " (Trắng Thắng)"
                    elif eval_val < -3:
                        eval_str += " (Đen Thắng)"
                    else:
                        eval_str += " (Bằng Nhau)"

                info_label.config(text=f"✅ Xong! ({len(moves)} nước){eval_str}")
                status_label.config(text="✅ Hoàn Thành")

            except Exception as e:
                status_label.config(text=f"❌ Lỗi: {str(e)}")
                info_label.config(text=str(e))

        # Run in thread
        import threading
        thread = threading.Thread(target=run_analysis, daemon=True)
        thread.start()

    def start_game(self, mode):
        self.game_mode = mode
        self.game = ChessGame()

        if self.game.stockfish:
            # Chỉ lưu ELO cho nước đi CỦA AI đối thủ; việc đánh giá/chấm điểm
            # nước đi vẫn luôn dùng full-strength (xem get_evaluation/get_top_moves)
            self.game.opponent_elo = self.opponent_elo

        self.status_label.config(text="👥 Chơi" if mode == "human_vs_human" else "🤖 vs AI")
        self.is_human_white = True

        self.draw_board()
        self.update_all()

    def update_all(self):
        if not self.game:
            return

        try:
            # Thanh đánh giá trên cùng hiển thị eval TUYỆT ĐỐI của thế cờ hiện
            # tại (góc Trắng, giống chess.com/lichess) - lấy từ eval_after của
            # nước cuối (đã tính sẵn khi make_move, không cần hỏi lại engine).
            # Trước đây bị hard-code truyền 0 nên thanh luôn ở giữa, không bao
            # giờ lệch về phe nào dù thế cờ chênh lệch thế nào.
            current_eval = 0
            if self.game.evaluation_history:
                last_eval_after = self.game.evaluation_history[-1].get('eval_after')
                if last_eval_after is not None:
                    current_eval = last_eval_after
            self.draw_eval_bar(current_eval)
        except Exception as e:
            print(f"Error in draw_eval_bar: {e}")
            self.draw_eval_bar(0)

        try:
            # Status
            turn = "Trắng ♔" if self.game.get_current_turn() == 'white' else "Đen ♚"
            self.status_label.config(text=f"Lượt: {turn}")
        except Exception as e:
            print(f"Error updating status: {e}")

        try:
            # Opening detection
            opening_name, _ = get_opening_by_moves(self.game.move_history)
            self.opening_label.config(text=f"📚 Khai cuộc: {opening_name or '-'}")
        except Exception as e:
            print(f"Error getting opening: {e}")
            self.opening_label.config(text="📚 Khai cuộc: -")

        try:
            # Enable/disable analysis button
            has_last_move = bool(self.game.evaluation_history)
            if has_last_move and self.game.stockfish_available:
                self.analysis_btn.config(state=tk.NORMAL)
            else:
                self.analysis_btn.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error enabling analysis button: {e}")
            try:
                self.analysis_btn.config(state=tk.DISABLED)
            except:
                pass

    def draw_eval_bar(self, eval_val):
        try:
            self.eval_canvas.delete("all")

            width = 1200
            height = 35
            center = width / 2

            # Safely handle eval_val
            if eval_val is None or not isinstance(eval_val, (int, float)):
                eval_val = 0

            # Clamp evaluation to reasonable range
            eval_clamped = min(max(eval_val, -500), 500)

            # Calculate bar width based on evaluation
            pct = eval_clamped / 500.0
            white_width = center + (center * pct)
            white_width = max(0, min(white_width, width))

            # Draw white segment
            if white_width > 0:
                self.eval_canvas.create_rectangle(0, 0, white_width, height, fill='#ffffff', outline='')

            # Draw black segment
            if white_width < width:
                self.eval_canvas.create_rectangle(white_width, 0, width, height, fill='#000000', outline='')

            # Draw center line
            self.eval_canvas.create_line(center, 0, center, height, fill='#666666', width=1)

            if self.game and self.game.evaluation_history:
                last_move = self.game.evaluation_history[-1]
                classification = last_move.get('classification', 'best')
                eval_before = last_move.get('eval_before')
                eval_after = last_move.get('eval_after')
                move = last_move.get('move', '-')

                # Classification map
                class_map = {
                    'brilliant': ('✨ BRILLIANT!', '#FFD700'),
                    'great': ('🟢 GREAT!', '#00DD00'),
                    'best': ('✓ BEST', '#00AA00'),
                    'good': ('👍 Good', '#44FF44'),
                    'inaccuracy': ('⚠️ Inaccuracy', '#FFAA00'),
                    'mistake': ('❌ Mistake', '#FF6600'),
                    'blunder': ('💥 BLUNDER!', '#FF0000')
                }

                class_emoji, class_color = class_map.get(classification, ('?', '#CCCCCC'))

                # Draw indicator
                indicator_x = 20
                self.eval_canvas.create_rectangle(indicator_x - 5, 5, indicator_x + 15, height - 5,
                                                 fill=class_color, outline='')

                # Calculate cp_change for centipawn mode.
                # eval_before/eval_after are always White-perspective absolute
                # values (dương = tốt cho Trắng), nên phải đảo dấu theo đúng
                # màu quân vừa đi mới ra "positive = tốt cho người vừa đi":
                # Trắng đi tốt -> eval TĂNG (eval_after - eval_before dương)
                # Đen đi tốt -> eval GIẢM (eval_before - eval_after dương)
                # (dùng flat eval_before - eval_after trước đây chỉ đúng cho
                # Đen, làm ngược dấu cho mọi nước đi của Trắng)
                cp_change = 0
                if eval_before is not None and eval_after is not None:
                    mover_white = last_move.get('mover_white', True)
                    raw_change = eval_after - eval_before
                    cp_change = raw_change if mover_white else -raw_change

                cp_pawn = cp_change / 100.0

                # Display based on mode
                if self.eval_mode == "classification":
                    self.eval_label.config(text=f"Nước: {move} | {class_emoji}")
                    if eval_before is not None and eval_after is not None:
                        analysis_text = f"Trước: {eval_before/100:+.2f} | Sau: {eval_after/100:+.2f} | Phân loại: {classification}"
                        self.analysis_label.config(text=analysis_text)
                    else:
                        self.analysis_label.config(text=f"Phân loại: {classification}")

                elif self.eval_mode == "centipawn":
                    pawn_text = f"{cp_pawn:+.2f} pawn"
                    if cp_pawn >= 3:
                        msg = "🟢 Rất tốt"
                    elif cp_pawn >= 1:
                        msg = "✓ Tốt"
                    elif cp_pawn >= 0:
                        msg = "👍 OK"
                    elif cp_pawn >= -1:
                        msg = "⚠️ Hơi kém"
                    elif cp_pawn >= -3:
                        msg = "❌ Kém"
                    else:
                        msg = "💥 Rất kém"

                    self.eval_label.config(text=f"Nước: {move} | {pawn_text} | {msg}")
                    if eval_before is not None and eval_after is not None:
                        analysis_text = f"Trước: {eval_before/100:+.2f} | Sau: {eval_after/100:+.2f} | Thay đổi: {cp_pawn:+.2f} pawn"
                        self.analysis_label.config(text=analysis_text)
                    else:
                        self.analysis_label.config(text=pawn_text)

                elif self.eval_mode == "advanced":
                    pawn_text = f"{cp_pawn:+.2f}"
                    accuracy = min(100, max(0, int(100 - abs(cp_pawn) * 10)))
                    self.eval_label.config(text=f"Nước: {move} | {class_emoji} | {pawn_text} pawn | Độ chính xác: {accuracy}%")
                    if eval_before is not None and eval_after is not None:
                        analysis_text = f"Trước: {eval_before/100:+.2f} | Sau: {eval_after/100:+.2f} | {classification} | {cp_pawn:+.2f} pawn"
                        self.analysis_label.config(text=analysis_text)
                    else:
                        self.analysis_label.config(text=f"{class_emoji} | {pawn_text} pawn")
            else:
                self.eval_label.config(text="Đánh giá: Chưa có nước")
                self.analysis_label.config(text="")

        except Exception as e:
            print(f"Error in draw_eval_bar: {e}")
            self.eval_label.config(text="Đánh giá: N/A")
            self.analysis_label.config(text="")

    def undo_move(self):
        if self.game and self.game.move_history:
            self.game.undo_move()
            self.draw_board()
            self.update_all()

    def reset_game(self):
        if self.game_mode:
            self.start_game(self.game_mode)

    def suggest_move(self):
        """Gợi ý nước đi tốt nhất từ Stockfish"""
        if not self.game:
            messagebox.showwarning("Lỗi", "Chưa bắt đầu trò chơi")
            return

        if not self.game.stockfish_available:
            messagebox.showwarning("Lỗi", "Stockfish không khả dụng")
            return

        if self.game.board.is_game_over():
            messagebox.showinfo("Trò Chơi Kết Thúc", self.get_game_result())
            return

        try:
            # Get best move
            self.game.stockfish.set_fen_position(self.game.board.fen())
            best_move = self.game.stockfish.get_best_move_time(3000)
            eval_val_normalized = self.game.get_evaluation()  # đã chuẩn hóa theo góc Trắng

            if not best_move:
                messagebox.showwarning("Lỗi", "Không thể tính toán nước đi")
                return

            # Convert to readable format
            move = chess.Move.from_uci(best_move)
            move_san = self.game.board.san(move)

            # Display suggestion with highlight
            msg = f"💡 Nước Gợi Ý: {move_san} ({best_move})\n\n"

            if eval_val_normalized is not None:
                msg += f"📊 Đánh Giá: {eval_val_normalized/100:+.2f}\n\n"

            msg += "Nước này là tốt nhất theo Stockfish.\n"
            msg += "Bạn có muốn áp dụng nước này không?"

            # Highlight best move on board
            self.highlight_best_move(move)

            if messagebox.askyesno("Gợi Ý Nước Đi", msg):
                # Apply the suggested move
                if self.game.make_move(best_move):
                    self.selected_square = None
                    self.draw_board()
                    self.update_all()

                    # If human vs AI and it's AI's turn, let AI move
                    if self.game_mode == 'human_vs_ai' and not self.game.is_game_over():
                        self.root.after(1000, self.ai_move)
                else:
                    messagebox.showerror("Lỗi", "Không thể thực hiện nước đi")
            else:
                self.draw_board()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    def show_puzzles(self):
        """Hiển thị chế độ giải câu đố"""
        puzzles = get_all_puzzles()
        puzzle_list = list(puzzles.keys())

        win = tk.Toplevel(self.root)
        win.title(f"🧩 Giải Câu Đố ({len(puzzles)}+)")
        win.geometry("900x650")

        # Current puzzle state
        current_puzzle_idx = [0]
        solved_count = [0]

        # Top frame - puzzle selector
        top = tk.Frame(win, bg='#2a2a2a')
        top.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top, text="Chọn Câu Đố:", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        puzzle_var = tk.StringVar(value=puzzle_list[0] if puzzle_list else "")
        puzzle_combo = ttk.Combobox(top, textvariable=puzzle_var, values=puzzle_list,
                                   state='readonly', width=40)
        puzzle_combo.pack(side=tk.LEFT, padx=5)

        status_label = tk.Label(top, text=f"Giải: 0/{len(puzzles)}", bg='#2a2a2a',
                               fg='#ffaa00', font=("Arial", 10, "bold"))
        status_label.pack(side=tk.RIGHT, padx=5)

        # Middle - board and info
        middle = tk.Frame(win, bg='#1a1a1a')
        middle.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left - board
        left = tk.Frame(middle, bg='#1a1a1a')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        puzzle_canvas = tk.Canvas(left, width=480, height=480, bg='#f0d9b5',
                                 highlightthickness=1, highlightbackground='#444')
        puzzle_canvas.pack()
        puzzle_canvas.bind("<Button-1>", lambda e: on_puzzle_click(e))

        # Right - info
        right = tk.Frame(middle, bg='#2a2a2a', width=350)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right.pack_propagate(False)

        tk.Label(right, text="📋 Thông Tin", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(10, 5))

        info_text = tk.Text(right, height=8, bg='#1a1a1a', fg='#ffffff',
                           font=("Arial", 9), wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        difficulty_label = tk.Label(right, text="Độ Khó: ?", bg='#2a2a2a', fg='#ffaa00',
                                   font=("Arial", 9))
        difficulty_label.pack(fill=tk.X, padx=10, pady=2)

        theme_label = tk.Label(right, text="Chủ Đề: ?", bg='#2a2a2a', fg='#ffaa00',
                              font=("Arial", 9))
        theme_label.pack(fill=tk.X, padx=10, pady=2)

        tk.Label(right, text="💡 Gợi Ý", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(10, 5))

        hint_text = tk.Text(right, height=3, bg='#1a1a1a', fg='#ffaa00',
                           font=("Arial", 9), wrap=tk.WORD)
        hint_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Variables for puzzle state
        puzzle_game = [None]
        selected_sq = [None]

        def load_puzzle(puzzle_name):
            """Tải câu đố"""
            if puzzle_name not in puzzles:
                return

            puzzle_data = puzzles[puzzle_name]
            puzzle_board = chess.Board(puzzle_data['fen'])
            puzzle_game[0] = puzzle_board
            selected_sq[0] = None

            # Update UI
            info_text.config(state=tk.NORMAL)
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, f"📖 {puzzle_name}\n\n")
            info_text.insert(tk.END, f"Mô tả:\n{puzzle_data['description']}\n")
            info_text.config(state=tk.DISABLED)

            difficulty_label.config(text=f"Độ Khó: {'⭐' * puzzle_data['difficulty']}")
            theme_label.config(text=f"Chủ Đề: {puzzle_data['theme']}")

            hint_text.config(state=tk.NORMAL)
            hint_text.delete(1.0, tk.END)
            hint_text.insert(tk.END, puzzle_data['hint'])
            hint_text.config(state=tk.DISABLED)

            draw_puzzle_board()

        def draw_puzzle_board(skip_square=None):
            """Vẽ bàn cờ câu đố"""
            if not puzzle_game[0]:
                return

            puzzle_canvas.delete("all")
            board = puzzle_game[0]
            sq_size = 60

            # Draw squares
            for row in range(8):
                for col in range(8):
                    x1, y1 = col * sq_size, row * sq_size
                    x2, y2 = x1 + sq_size, y1 + sq_size
                    color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                    puzzle_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

            # Draw pieces
            for square in chess.SQUARES:
                if square == skip_square:
                    continue
                piece = board.piece_at(square)
                if piece:
                    row, col = square // 8, square % 8
                    x = col * sq_size + sq_size // 2
                    y = row * sq_size + sq_size // 2
                    piece_color = '#ffffff' if piece.color else '#000000'
                    puzzle_canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                             font=("Arial", 40, "bold"), fill=piece_color)

        def animate_puzzle_move(from_square, to_square, on_complete, duration_ms=150, steps=8):
            """Trượt quân cờ mượt trong chế độ câu đố, tương tự animate_move() ở
            bàn cờ chính nhưng dùng canvas/tọa độ cố định riêng của cửa sổ này."""
            board = puzzle_game[0]
            piece = board.piece_at(from_square) if board else None
            if not piece:
                on_complete()
                return

            sq_size = 60
            from_row, from_col = from_square // 8, from_square % 8
            to_row, to_col = to_square // 8, to_square % 8
            start_x = from_col * sq_size + sq_size // 2
            start_y = from_row * sq_size + sq_size // 2
            end_x = to_col * sq_size + sq_size // 2
            end_y = to_row * sq_size + sq_size // 2

            draw_puzzle_board(skip_square=from_square)

            piece_color = '#ffffff' if piece.color else '#000000'
            moving_piece = puzzle_canvas.create_text(start_x, start_y, text=self.PIECE_UNICODE[piece.symbol()],
                                                     font=("Arial", 40, "bold"), fill=piece_color)

            step_delay = max(10, duration_ms // steps)

            def step(i):
                if not puzzle_canvas.winfo_exists():
                    return
                if i > steps:
                    puzzle_canvas.delete(moving_piece)
                    on_complete()
                    return
                t = i / steps
                x = start_x + (end_x - start_x) * t
                y = start_y + (end_y - start_y) * t
                puzzle_canvas.coords(moving_piece, x, y)
                win.after(step_delay, lambda: step(i + 1))

            step(1)

        def on_puzzle_click(event):
            """Xử lý click khi giải câu đố"""
            if not puzzle_game[0]:
                return

            sq_size = 60
            col = event.x // sq_size
            row = event.y // sq_size
            square = row * 8 + col

            board = puzzle_game[0]

            if selected_sq[0] is None:
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    selected_sq[0] = square
                    draw_puzzle_board()

                    # Highlight legal moves
                    for move in board.legal_moves:
                        if move.from_square == square:
                            to_row, to_col = move.to_square // 8, move.to_square % 8
                            x = to_col * sq_size + sq_size // 2
                            y = to_row * sq_size + sq_size // 2
                            puzzle_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='lime')
            else:
                promotion_piece = None
                if self._is_promotion_move(board, selected_sq[0], square):
                    promotion_piece = self._ask_promotion_piece()
                move = chess.Move(selected_sq[0], square, promotion=promotion_piece)
                if move in board.legal_moves:
                    puzzle_name = puzzle_var.get()
                    best_move_str = puzzles[puzzle_name]['best_move']

                    # Convert move to SAN for comparison (phải tính TRƯỚC khi push)
                    try:
                        move_san = board.san(move)
                    except:
                        move_san = move.uci()

                    is_correct = (move_san == best_move_str or
                                 move_san.lower() == best_move_str.lower() or
                                 move.uci().startswith(best_move_str.lower()))

                    from_sq, to_sq = selected_sq[0], square
                    selected_sq[0] = None

                    def after_puzzle_anim():
                        board.push(move)

                        if is_correct:
                            solved_count[0] += 1
                            status_label.config(text=f"Giải: {solved_count[0]}/{len(puzzles)}")
                            messagebox.showinfo("✅ Đúng!", f"Nước gợi ý: {best_move_str}\nBạn đã giải đúng!")
                        else:
                            messagebox.showwarning("❌ Sai", f"Nước gợi ý: {best_move_str}\nHãy thử lại!")
                            board.pop()

                        draw_puzzle_board()

                    animate_puzzle_move(from_sq, to_sq, after_puzzle_anim)
                else:
                    selected_sq[0] = None
                    draw_puzzle_board()

        def on_puzzle_selected(event=None):
            """Khi chọn câu đố"""
            load_puzzle(puzzle_var.get())

        puzzle_combo.bind("<<ComboboxSelected>>", on_puzzle_selected)

        # Load first puzzle
        if puzzle_list:
            load_puzzle(puzzle_list[0])

        # Bottom buttons
        bottom = tk.Frame(win, bg='#2a2a2a')
        bottom.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(bottom, text="⬅️ Câu Trước", command=lambda: navigate_puzzle(-1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text="➡️ Câu Sau", command=lambda: navigate_puzzle(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text="🔄 Làm Lại", command=lambda: load_puzzle(puzzle_var.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom, text="💡 Xem Đáp Án", command=lambda: show_answer()).pack(side=tk.LEFT, padx=5)

        def navigate_puzzle(direction):
            """Di chuyển giữa các câu đố"""
            current = puzzle_combo.current()
            new_idx = current + direction
            if 0 <= new_idx < len(puzzle_list):
                puzzle_combo.current(new_idx)
                on_puzzle_selected()

        def show_answer():
            """Hiển thị đáp án"""
            puzzle_name = puzzle_var.get()
            if puzzle_name in puzzles:
                best = puzzles[puzzle_name]['best_move']
                messagebox.showinfo("💡 Đáp Án", f"Nước tốt nhất: {best}")

    def set_eval_mode(self, mode):
        """Thay đổi chế độ đánh giá"""
        self.eval_mode = mode
        self.update_all()

    def flip_board(self):
        """Xoay bàn cờ"""
        self.board_flipped = not self.board_flipped
        self.draw_board()

    def get_game_result(self):
        if self.game.board.is_checkmate():
            winner = "Trắng ♔" if not self.game.board.turn else "Đen ♚"
            result = f"Chiếu hết! {winner} thắng!"
        elif self.game.board.is_stalemate():
            result = "Hòa - Bế tắc!"
        elif self.game.board.is_insufficient_material():
            result = "Hòa - Quân cờ không đủ!"
        elif self.game.board.is_seventyfive_moves():
            result = "Hòa - 75 nước không ăn quân!"
        elif self.game.board.is_fivefold_repetition():
            result = "Hòa - Lặp lại 5 lần!"
        else:
            result = "Trò chơi kết thúc"

        return result + self.get_accuracy_summary()

    def get_accuracy_summary(self):
        """Tóm tắt % chính xác + ELO ước tính mỗi bên, để nối vào thông báo
        kết thúc ván. Đây chỉ là ước lượng tham khảo (xem ChessGame.get_accuracy_stats)."""
        if not self.game or not self.game.stockfish_available:
            return ""

        stats = self.game.get_accuracy_stats()
        if not stats:
            return ""

        lines = ["\n\n📊 Thống Kê Ván Đấu (ước tính):"]
        labels = {'white': 'Trắng ♔', 'black': 'Đen ♚'}
        for color in ('white', 'black'):
            s = stats.get(color)
            if s:
                lines.append(
                    f"{labels[color]}: {s['accuracy']}% chính xác "
                    f"(ACPL {s['acpl']}) — ELO ước tính ~{s['estimated_elo']}"
                )
        if len(lines) == 1:
            return ""
        return "\n".join(lines)


def main():
    root = tk.Tk()
    gui = ChessGUI(root)
    gui.draw_board()
    root.mainloop()


if __name__ == "__main__":
    main()
