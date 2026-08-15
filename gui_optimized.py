#!/usr/bin/env python3
"""
♟ CHESS MASTER - Optimized & Fast with Move Evaluation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import chess
from chess_engine import ChessGame, MultiEngineGame, MoveEvaluation
from openings_50 import get_opening_by_moves, get_all_openings

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

        self.eval_display = tk.Text(bottom, height=4, bg='#1a1a1a', fg='#ffffff',
                                   font=("Arial", 9), wrap=tk.WORD)
        self.eval_display.pack(fill=tk.X, padx=10, pady=5)

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

        ttk.Button(parent, text="Xem 50+ Khai Cuộc", command=self.show_openings,
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

            if self.game.evaluation_history:
                last = self.game.evaluation_history[-1]
                eval_sym, eval_range, desc = last['evaluation'].value

                msg = f"{eval_sym} Nước: {last['move']}\n"
                msg += f"Đánh giá: {eval_range}\n"
                msg += f"Lý do: {desc}"

                self.eval_display.insert(tk.END, msg)

            self.eval_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error updating eval display: {e}")
            self.eval_display.config(state=tk.DISABLED)

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
