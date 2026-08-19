#!/usr/bin/env python3
"""
♟ Chess Engine - Core logic with Stockfish
"""

import chess
import chess.pgn
from stockfish import Stockfish
from enum import Enum
from datetime import datetime

CLASS_STYLE = {
    "book":        ("Khai cuoc",     "📚", "Nước di chuan trong sach khai cuoc."),
    "brilliant":   ("Xuat sac",      "⭐", "Nước hy sinh, tan cong cuc ky thong minh."),
    "great":       ("Tuyet voi",     "🟢", "Nước di duy nhat va quan trong."),
    "best":        ("Tot nhat",      "✓", "Nước di toi uu theo Stockfish."),
    "good":        ("Kha",           "✓", "Nước di hop ly, an toan."),
    "inaccuracy":  ("Diem yeu nhe",  "❓", "Nước di hoi kem."),
    "mistake":     ("Sai lam",       "⚠️", "Nước di gay mat loi the."),
    "blunder":     ("Thao hoa",      "❌", "Sai lam tram trong."),
}

class MoveEvaluation(Enum):
    BLUNDER = ("💥 Blunder", "< -3.00", "Nước đi tàn tệ, mất lợi thế lớn")
    MISTAKE = ("❌ Mistake", "-1.00 to -3.00", "Sai lầm đáng kể, mất lợi thế")
    INACCURACY = ("⚠️ Inaccuracy", "-0.25 to -1.00", "Không chính xác, mất chút lợi thế")
    GOOD = ("👍 Good", "-0.25 to +0.25", "Nước đi tốt, bình thường")
    EXCELLENT = ("✓ Excellent", "+1.00 to +3.00", "Nước đi xuất sắc, tăng lợi thế")
    BRILLIANT = ("✨ Brilliant", "> +3.00", "Nước đi tuyệt vời, chuyển bất lợi thành lợi")

def material_count(board, color):
    """Tính tổng giá trị quân cờ"""
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
    total = 0
    for pt, val in piece_values.items():
        total += val * len(board.pieces(pt, color))
    return total

class MoveClassifier:
    """Phân loại nước đi dựa trên cp_loss (best_cp - eval_after)"""

    def classify(self, board_before, move, top_moves_before, eval_before_cp, eval_after_cp, ply_index=0):
        best_cp = top_moves_before[0]["score_cp"] if top_moves_before else eval_before_cp
        second_cp = top_moves_before[1]["score_cp"] if len(top_moves_before) > 1 else best_cp - 400
        is_top_choice = bool(top_moves_before) and top_moves_before[0]["move"] == move

        cp_loss = max(0, best_cp - eval_after_cp)

        mover_color = board_before.turn
        board_after = board_before.copy(stack=False)
        board_after.push(move)

        mat_before = material_count(board_before, mover_color) - material_count(board_before, not mover_color)
        mat_after = material_count(board_after, mover_color) - material_count(board_after, not mover_color)
        sacrifice = (mat_after - mat_before) <= -2

        is_mate = board_after.is_checkmate()

        # Phân loại logic
        if is_mate:
            return "brilliant" if sacrifice else "best"

        if sacrifice and cp_loss <= 40 and eval_after_cp >= -50:
            return "brilliant"
        if sacrifice and is_top_choice and cp_loss <= 20 and (best_cp - second_cp) >= 150:
            return "brilliant"

        if is_top_choice and (best_cp - second_cp) >= 200 and eval_before_cp <= 100:
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

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        self.evaluation_history = []
        self.stockfish_available = False
        self.stockfish = None
        self.opening_name = None
        self.game_pgn = chess.pgn.Game()
        self.node = self.game_pgn

        # Try multiple paths to find Stockfish
        stockfish_paths = [
            r"C:\Users\admin\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe",
            r"C:\Program Files\Stockfish\stockfish.exe",
            r"C:\Program Files (x86)\Stockfish\stockfish.exe",
            "stockfish"
        ]

        for path in stockfish_paths:
            try:
                self.stockfish = Stockfish(path=path)
                self.stockfish.set_skill_level(18)
                self.stockfish_available = True
                print(f"✅ Stockfish loaded from: {path}")
                break
            except Exception as e:
                continue

        if not self.stockfish_available:
            print(f"⚠️ Stockfish not found. Tried paths: {stockfish_paths}")

    def make_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move not in self.board.legal_moves:
                return False

            fen_before = self.board.fen()
            board_before = self.board.copy(stack=False)
            eval_before = self.get_evaluation()

            # Get top moves before making the move
            top_moves_before = self.get_top_moves(5)

            self.board.push(move)
            self.move_history.append(move_uci)
            self.node = self.node.add_variation(move)

            eval_after = self.get_evaluation()

            # Use MoveClassifier for evaluation
            classifier = MoveClassifier()
            move_class = classifier.classify(
                board_before,
                move,
                top_moves_before,
                eval_before if eval_before is not None else 0,
                eval_after if eval_after is not None else 0,
                len(self.move_history) - 1
            )

            self.evaluation_history.append({
                'move': move_uci,
                'evaluation': move_class,
                'eval_before': eval_before,
                'eval_after': eval_after,
                'fen_before': fen_before,
                'classification': move_class
            })

            return True
        except:
            return False

    def _evaluate_move(self, eval_before, eval_after):
        if eval_before is None or eval_after is None:
            return MoveEvaluation.GOOD

        if isinstance(eval_before, int) and isinstance(eval_after, int):
            change = eval_after - eval_before

            # Flip perspective for Black's moves
            # len(move_history) is EVEN after Black moves (1, 3, 5... = white; 2, 4, 6... = black)
            if len(self.move_history) % 2 == 0:  # Black just moved
                change = -change

            change_pawn = change / 100

            # Thresholds in centipawns (sensitive range: -50 to 50)
            # BRILLIANT: >= +100 cp (exceptional improvement)
            # EXCELLENT: >= +50 cp (good improvement)
            # GOOD: >= +10 cp (slight improvement)
            # NEUTRAL: -10 to +10 cp (nearly even)
            # INACCURACY: -10 to -50 cp (slight deterioration)
            # MISTAKE: -50 to -100 cp (notable deterioration)
            # BLUNDER: < -100 cp (serious mistake)

            if change >= 100:
                return MoveEvaluation.BRILLIANT
            elif change >= 50:
                return MoveEvaluation.EXCELLENT
            elif change >= 10:
                return MoveEvaluation.GOOD
            elif change >= -10:
                return MoveEvaluation.GOOD
            elif change >= -50:
                return MoveEvaluation.INACCURACY
            elif change >= -100:
                return MoveEvaluation.MISTAKE
            else:
                return MoveEvaluation.BLUNDER

        return MoveEvaluation.GOOD

    def get_evaluation(self):
        if not self.stockfish_available:
            return None

        try:
            self.stockfish.set_fen_position(self.board.fen())
            eval_value = self.stockfish.get_evaluation()

            if eval_value['type'] == 'cp':
                return eval_value['value']
            elif eval_value['type'] == 'mate':
                mate_in = eval_value['value']
                return 10000 if mate_in > 0 else -10000

            return None
        except:
            return None

    def get_best_move(self, time_ms=1000):
        if not self.stockfish_available:
            return None

        try:
            self.stockfish.set_fen_position(self.board.fen())
            best_move = self.stockfish.get_best_move_time(time_ms)
            return best_move
        except:
            return None

    def get_top_moves(self, count=5):
        if not self.stockfish_available:
            return []

        try:
            self.stockfish.set_fen_position(self.board.fen())
            top_moves = []
            for move in list(self.board.legal_moves)[:count]:
                self.stockfish.set_fen_position(self.board.fen())
                move_uci = move.uci()
                # Make temporary move to evaluate
                temp_board = self.board.copy()
                temp_board.push(move)
                self.stockfish.set_fen_position(temp_board.fen())
                eval_after = self.stockfish.get_evaluation()

                score_cp = 0
                if eval_after:
                    if eval_after['type'] == 'cp':
                        score_cp = eval_after['value']
                    elif eval_after['type'] == 'mate':
                        score_cp = 10000 if eval_after['value'] > 0 else -10000

                top_moves.append({
                    'move': move_uci,
                    'score_cp': score_cp
                })

            # Sort by score descending
            top_moves.sort(key=lambda x: x['score_cp'], reverse=True)
            return top_moves[:count]
        except:
            return []

    def is_game_over(self):
        return self.board.is_game_over()

    def is_check(self):
        return self.board.is_check()

    def get_current_turn(self):
        return 'white' if self.board.turn else 'black'

    def undo_move(self):
        if self.move_history:
            self.board.pop()
            self.move_history.pop()
            self.evaluation_history.pop()
            return True
        return False

    def get_pgn_string(self):
        return str(self.game_pgn)

    def analyze_position(self, depth=15):
        if not self.stockfish_available:
            return None

        try:
            self.stockfish.set_fen_position(self.board.fen())
            self.stockfish.set_depth(depth)
            info = self.stockfish.get_best_move()
            return info
        except:
            return None

class MultiEngineGame:
    def __init__(self, engine1_skill=18, engine2_skill=15):
        self.board = chess.Board()

        # Try multiple paths to find Stockfish
        stockfish_paths = [
            r"C:\Users\admin\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe",
            r"C:\Program Files\Stockfish\stockfish.exe",
            r"C:\Program Files (x86)\Stockfish\stockfish.exe",
            "stockfish"
        ]

        stockfish_path = None
        for path in stockfish_paths:
            try:
                test = Stockfish(path=path)
                stockfish_path = path
                break
            except:
                continue

        # Initialize with found path or default
        if stockfish_path:
            self.stockfish1 = Stockfish(path=stockfish_path)
            self.stockfish2 = Stockfish(path=stockfish_path)
        else:
            self.stockfish1 = Stockfish()
            self.stockfish2 = Stockfish()

        self.stockfish1.set_skill_level(engine1_skill)
        self.stockfish2.set_skill_level(engine2_skill)

        self.moves = []

    def play_full_game(self, max_moves=200):
        for _ in range(max_moves):
            if self.board.is_game_over():
                break

            if self.board.turn:
                self.stockfish1.set_fen_position(self.board.fen())
                best_move = self.stockfish1.get_best_move_time(1000)
            else:
                self.stockfish2.set_fen_position(self.board.fen())
                best_move = self.stockfish2.get_best_move_time(1000)

            if best_move:
                move = chess.Move.from_uci(best_move)
                self.board.push(move)
                self.moves.append(best_move)

        return self.moves

    def get_result(self):
        if self.board.is_checkmate():
            return "Checkmate - " + ("Engine 1 wins" if not self.board.turn else "Engine 2 wins")
        elif self.board.is_stalemate():
            return "Draw - Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw - Insufficient material"
        else:
            return "Game incomplete"
