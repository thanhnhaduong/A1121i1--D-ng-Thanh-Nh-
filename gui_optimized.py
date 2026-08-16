#!/usr/bin/env python3
"""
♟ CHESS MASTER - Optimized & Fast with Move Evaluation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import chess
from chess_engine import ChessGame, MultiEngineGame, MoveEvaluation
from openings_50 import get_opening_by_moves, get_all_openings, get_teaching_data

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
        self.opponent_skill_level = 18
        self.eval_cache = {}

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

        self.ELO_LEVELS = {
            'Easy (5)': 5,
            'Beginner (8)': 8,
            'Intermediate (12)': 12,
            'Advanced (16)': 16,
            'Master (18)': 18,
            'GrandMaster (20)': 20
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
        self.eval_label.pack(fill=tk.X, padx=10, pady=(0, 5))

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

        # Move evaluation display
        bottom = tk.Frame(main, bg='#2a2a2a')
        bottom.pack(fill=tk.X, padx=10, pady=(5, 10))

        tk.Label(bottom, text="📊 Đánh Giá Nước Đi", bg='#2a2a2a', fg='#4a9eff',
                font=("Arial", 10, "bold")).pack(fill=tk.X, padx=10, pady=(5, 0))

        # Info display
        self.eval_display = tk.Text(bottom, height=3, bg='#1a1a1a', fg='#ffffff',
                                   font=("Arial", 9), wrap=tk.WORD)
        self.eval_display.pack(fill=tk.X, padx=10, pady=5)

        # Analysis button
        self.analysis_btn = ttk.Button(bottom, text="🔍 Xem Phân Tích (Bot Tiếp Tục)",
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

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                x1, y1 = col * self.square_size, row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                color = self.COLORS['light'] if (row + col) % 2 == 0 else self.COLORS['dark']
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        if self.game and self.game.is_check():
            king_pos = self.game.board.king(self.game.board.turn)
            if king_pos:
                row, col = king_pos // 8, king_pos % 8
                x1, y1 = col * self.square_size, row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.COLORS['check'], width=3)

        if self.game:
            for square in chess.SQUARES:
                piece = self.game.board.piece_at(square)
                if piece:
                    row, col = square // 8, square % 8
                    x = col * self.square_size + self.square_size // 2
                    y = row * self.square_size + self.square_size // 2
                    piece_color = self.COLORS['white'] if piece.color else self.COLORS['black']
                    self.canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                           font=("Arial", 50, "bold"), fill=piece_color)

    def on_board_click(self, event):
        if not self.game or self.ai_thinking:
            return

        if self.game_mode == 'human_vs_ai':
            if self.game.get_current_turn() == 'white' and not self.is_human_white:
                return
            if self.game.get_current_turn() == 'black' and self.is_human_white:
                return

        col = event.x // self.square_size
        row = event.y // self.square_size
        square = row * 8 + col

        if self.selected_square is None:
            piece = self.game.board.piece_at(square)
            if piece and piece.color == self.game.board.turn:
                self.selected_square = square
                self.highlight_moves(square)
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.game.board.legal_moves:
                self.game.make_move(move.uci())
                self.selected_square = None
                self.draw_board()
                self.update_all()

                if self.game_mode == 'human_vs_ai' and not self.game.is_game_over():
                    self.root.after(1000, self.ai_move)
            else:
                self.selected_square = None
                self.draw_board()

    def highlight_moves(self, square):
        self.draw_board()

        row, col = square // 8, square % 8
        x1, y1 = col * self.square_size, row * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=3)

        for move in self.game.board.legal_moves:
            if move.from_square == square:
                to_row, to_col = move.to_square // 8, move.to_square % 8
                x = to_col * self.square_size + self.square_size // 2
                y = to_row * self.square_size + self.square_size // 2
                self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='lime')

    def ai_move(self):
        if not self.game or self.game.is_game_over():
            return

        self.ai_thinking = True
        self.status_label.config(text="🤖 AI đang suy nghĩ...")
        self.root.update_idletasks()

        best_move = self.game.get_best_move(time_ms=2000)

        if best_move:
            self.game.make_move(best_move)
            self.draw_board()
            self.update_all()

        self.ai_thinking = False

        if self.game.is_game_over():
            messagebox.showinfo("Kết Thúc", self.get_game_result())
        else:
            self.status_label.config(text="Lượt của bạn")

    def select_difficulty(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Chọn Độ Khó")
        dialog.geometry("300x350")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Độ khó AI:", font=("Arial", 11, "bold")).pack(pady=15)

        selected = tk.StringVar(value="Master (18)")

        for level in self.ELO_LEVELS.keys():
            tk.Radiobutton(dialog, text=level, variable=selected, value=level,
                          font=("Arial", 10)).pack(anchor=tk.W, padx=30, pady=3)

        def start():
            self.opponent_skill_level = self.ELO_LEVELS[selected.get()]
            self.start_game("human_vs_ai")
            dialog.destroy()

        tk.Button(dialog, text="Chơi", command=start, bg='#4a9eff', fg='white',
                 font=("Arial", 10, "bold"), padx=15, pady=8).pack(pady=15)

    def show_engine_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("AI vs AI")
        dialog.geometry("300x350")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Trắng:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        white = tk.StringVar(value="Master (18)")
        for level in self.ELO_LEVELS.keys():
            tk.Radiobutton(dialog, text=level, variable=white, value=level,
                          font=("Arial", 9)).pack(anchor=tk.W, padx=30, pady=1)

        tk.Label(dialog, text="Đen:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        black = tk.StringVar(value="Advanced (16)")
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
        win = tk.Toplevel(self.root)
        win.title(f"AI vs AI - Level {white_elo} vs {black_elo}")
        win.geometry("600x400")

        text = tk.Text(win, font=("Courier", 10), bg='#1a1a1a', fg='#ffffff')
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, f"Level {white_elo} vs {black_elo}\nChơi...\n")
        win.update()

        game = MultiEngineGame(engine1_skill=white_elo, engine2_skill=black_elo)
        moves = game.play_full_game(max_moves=200)
        result = game.get_result()

        text.delete(1.0, tk.END)
        text.insert(tk.END, f"Kết quả: {result}\n")
        text.insert(tk.END, f"Nước: {len(moves)}\n\n")
        move_str = ""
        for i, move in enumerate(moves, 1):
            move_str += f"{i}. {move}  "
            if i % 10 == 0:
                move_str += "\n"
        text.insert(tk.END, move_str)

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
                canvas.delete("all")
                for row in range(8):
                    for col in range(8):
                        x1, y1 = col * 60, row * 60
                        x2, y2 = x1 + 60, y1 + 60
                        color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                for square in chess.SQUARES:
                    piece = board.piece_at(square)
                    if piece:
                        row, col = square // 8, square % 8
                        x = col * 60 + 30
                        y = row * 60 + 30
                        piece_color = '#ffffff' if piece.color else '#000000'
                        canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                         font=("Arial", 40, "bold"), fill=piece_color)
                anim_win.update()

            def animate():
                try:
                    playback_board = chess.Board()

                    for i, move_uci in enumerate(moves):
                        try:
                            move = chess.Move.from_uci(move_uci)
                            playback_board.push(move)
                        except:
                            continue

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
            canvas.delete("all")
            for row in range(8):
                for col in range(8):
                    x1, y1 = col * 60, row * 60
                    x2, y2 = x1 + 60, y1 + 60
                    color = '#f0d9b5' if (row + col) % 2 == 0 else '#b58863'
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece:
                    row, col = square // 8, square % 8
                    x = col * 60 + 30
                    y = row * 60 + 30
                    piece_color = '#ffffff' if piece.color else '#000000'
                    canvas.create_text(x, y, text=self.PIECE_UNICODE[piece.symbol()],
                                     font=("Arial", 40, "bold"), fill=piece_color)
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
            self.game.stockfish.set_skill_level(self.opponent_skill_level)

        self.status_label.config(text="👥 Chơi" if mode == "human_vs_human" else "🤖 vs AI")
        self.is_human_white = True
        self.eval_display.config(state=tk.NORMAL)
        self.eval_display.delete(1.0, tk.END)
        self.eval_display.config(state=tk.DISABLED)

        self.draw_board()
        self.update_all()

    def update_all(self):
        if not self.game:
            return

        try:
            # Evaluation - handle None case
            eval_val = self.game.get_evaluation()
            if eval_val is None:
                eval_val = 0
            self.draw_eval_bar(eval_val)
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
            # Opening
            opening_name, _ = get_opening_by_moves(self.game.move_history)
            self.opening_label.config(text=f"Khai cuộc: {opening_name or '-'}")
        except Exception as e:
            print(f"Error getting opening: {e}")
            self.opening_label.config(text="Khai cuộc: -")

        try:
            # Move evaluation display
            self.eval_display.config(state=tk.NORMAL)
            self.eval_display.delete(1.0, tk.END)

            has_last_move = False
            if self.game.evaluation_history:
                has_last_move = True
                last = self.game.evaluation_history[-1]
                try:
                    # Try to unpack evaluation value
                    evaluation = last['evaluation']
                    if hasattr(evaluation, 'value'):
                        eval_sym, eval_range, desc = evaluation.value
                    else:
                        eval_sym = str(evaluation)
                        eval_range = "?"
                        desc = "Không có lý do"

                    msg = f"{eval_sym} Nước: {last['move']}\n"
                    msg += f"Đánh giá: {eval_range}"

                    self.eval_display.insert(tk.END, msg)
                except (ValueError, AttributeError, TypeError) as unpack_error:
                    print(f"Error unpacking evaluation: {unpack_error}")
                    self.eval_display.insert(tk.END, f"Nước: {last['move']}\nĐánh giá: N/A")

            # Enable/disable analysis button
            if has_last_move and self.game.stockfish_available:
                self.analysis_btn.config(state=tk.NORMAL)
            else:
                self.analysis_btn.config(state=tk.DISABLED)

            self.eval_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error updating eval display: {e}")
            try:
                self.eval_display.config(state=tk.DISABLED)
                self.analysis_btn.config(state=tk.DISABLED)
            except:
                pass

    def draw_eval_bar(self, eval_val):
        try:
            self.eval_canvas.delete("all")

            width = 1200
            height = 35

            # Safely handle eval_val
            if eval_val is None or not isinstance(eval_val, (int, float)):
                eval_val = 0

            pct = min(max((eval_val / 500), -1), 1)
            white_width = (width / 2) * (1 + pct)

            self.eval_canvas.create_rectangle(0, 0, white_width, height, fill='#ffffff', outline='')
            self.eval_canvas.create_rectangle(white_width, 0, width, height, fill='#000000', outline='')
            self.eval_canvas.create_line(width / 2, 0, width / 2, height, fill='#444444', width=2)

            eval_str = f"{eval_val/100:+.2f}"
            msg = "Bằng" if abs(eval_val) < 5 else ("Trắng thắng" if eval_val > 300 else "Đen thắng")

            self.eval_label.config(text=f"Đánh giá: {eval_str} | {msg}")
        except Exception as e:
            print(f"Error in draw_eval_bar: {e}")

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
            eval_val = self.game.stockfish.get_evaluation()

            if not best_move:
                messagebox.showwarning("Lỗi", "Không thể tính toán nước đi")
                return

            # Convert to readable format
            move = chess.Move.from_uci(best_move)
            move_san = self.game.board.san(move)

            # Display suggestion
            msg = f"💡 Nước Gợi Ý: {move_san} ({best_move})\n\n"

            if eval_val:
                eval_val_float = eval_val['value'] / 100 if eval_val['type'] == 'cp' else eval_val['value']
                msg += f"📊 Đánh Giá: {eval_val_float:+.2f}\n\n"

            msg += "Nước này là tốt nhất theo Stockfish.\n"
            msg += "Bạn có muốn áp dụng nước này không?"

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

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    def get_game_result(self):
        if self.game.board.is_checkmate():
            return "Chiếu hết!"
        return "Hòa" if self.game.board.is_stalemate() else "Hết"


def main():
    root = tk.Tk()
    gui = ChessGUI(root)
    gui.draw_board()
    root.mainloop()


if __name__ == "__main__":
    main()
