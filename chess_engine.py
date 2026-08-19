#!/usr/bin/env python3
"""
♟ Chess Engine - Core logic with Stockfish
"""

import os
import chess
import chess.pgn
from stockfish import Stockfish
from enum import Enum
from datetime import datetime

# Tối ưu cho phần cứng yếu/tầm trung (vd: Intel i3 đời 8):
# để lại 1 nhân cho hệ điều hành/giao diện, giới hạn tối đa 4 luồng
ENGINE_THREADS = max(1, min(4, (os.cpu_count() or 2) - 1))
ENGINE_HASH_MB = 64

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
        has_second_move = len(top_moves_before) > 1
        is_top_choice = bool(top_moves_before) and top_moves_before[0]["move"] == move.uci()

        # Adjust perspective for Black (negate values so positive = good for moving player)
        perspective = 1 if board_before.turn else -1
        best_cp_adjusted = best_cp * perspective
        eval_before_adjusted = eval_before_cp * perspective
        eval_after_adjusted = eval_after_cp * perspective

        cp_loss = max(0, best_cp_adjusted - eval_after_adjusted)
        cp_gain = max(0, eval_after_adjusted - best_cp_adjusted)

        # Khoảng cách best/2nd-best chỉ tính khi có dữ liệu nước nhì thực sự.
        # Không có dữ liệu -> gap = 0, tránh kích hoạt "great"/"brilliant" sai lệch
        # (trước đây dùng giá trị giả định best_cp-400, nhưng sau khi nhân perspective
        # nó luôn đúng cho Trắng và luôn sai cho Đen một cách hệ thống).
        if has_second_move:
            second_cp = top_moves_before[1]["score_cp"]
            gap = best_cp_adjusted - (second_cp * perspective)
        else:
            gap = 0

        mover_color = board_before.turn
        board_after = board_before.copy(stack=False)
        board_after.push(move)

        mat_before = material_count(board_before, mover_color) - material_count(board_before, not mover_color)
        mat_after = material_count(board_after, mover_color) - material_count(board_after, not mover_color)
        sacrifice = (mat_after - mat_before) <= -2
        material_gain = (mat_after - mat_before) >= 2

        is_mate = board_after.is_checkmate()

        # Phân loại logic - Brilliant và Blunder chỉ khi mất/nhận quá nhiều
        if is_mate:
            return "best"

        # Brilliant: chỉ khi nhận quá nhiều lợi thế hoặc hy sinh thông minh
        if cp_gain >= 300:
            return "brilliant"
        if material_gain and cp_loss <= 100:
            return "brilliant"
        if sacrifice and is_top_choice and cp_loss <= 50 and gap >= 300:
            return "brilliant"

        if is_top_choice and gap >= 200 and abs(eval_before_adjusted) <= 100:
            return "great"

        if is_top_choice or cp_loss <= 15:
            return "best"
        if cp_loss <= 75:
            return "good"
        if cp_loss <= 175:
            return "inaccuracy"
        if cp_loss <= 350:
            return "mistake"
        # Blunder: chỉ khi mất quá nhiều (>3.5 pawn)
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

        # Skill Level dùng riêng cho nước đi CỦA AI đối thủ (độ khó người dùng chọn).
        # Việc ĐÁNH GIÁ nước đi (evaluation/classification) luôn dùng full-strength
        # (20) bất kể độ khó AI, để không bỏ sót đòn phản công/chiến thuật sâu
        # sau các nước hy sinh - nếu không, engine bị làm yếu đi (Skill Level)
        # sẽ vừa chơi kém vừa ĐÁNH GIÁ kém, gây phân loại sai (vd: thí hậu tồi
        # bị chấm "brilliant" vì engine yếu không thấy được đòn bắt lại).
        self.opponent_skill_level = 18
        FULL_STRENGTH_SKILL = 20

        for path in stockfish_paths:
            try:
                self.stockfish = Stockfish(
                    path=path,
                    parameters={"Threads": ENGINE_THREADS, "Hash": ENGINE_HASH_MB}
                )
                self.stockfish.set_skill_level(FULL_STRENGTH_SKILL)
                self.stockfish_available = True
                print(f"✅ Stockfish loaded from: {path} (Threads={ENGINE_THREADS}, Hash={ENGINE_HASH_MB}MB)")
                break
            except Exception as e:
                continue

        if not self.stockfish_available:
            print(f"⚠️ Stockfish not found. Tried paths: {stockfish_paths}")
        else:
            self._detect_eval_convention()

    def _detect_eval_convention(self):
        """Thư viện stockfish có thể trả điểm LUÔN theo góc Trắng, hoặc theo góc
        BÊN ĐANG ĐI (turn-relative) tùy phiên bản cài đặt. Kiểm tra thực nghiệm
        bằng 1 thế cờ Trắng thắng rõ ràng (thừa hậu), thử cả 2 trường hợp
        "tới lượt Trắng" và "tới lượt Đen" để xác định đúng quy ước, thay vì
        đoán mò (nguồn gốc gây sai lệch đánh giá Trắng/Đen trước đây)."""
        self.eval_turn_relative = False
        try:
            fen_white_to_move = "4k3/8/8/8/8/8/8/Q3K3 w - - 0 1"
            fen_black_to_move = "4k3/8/8/8/8/8/8/Q3K3 b - - 0 1"

            self.stockfish.set_fen_position(fen_white_to_move)
            eval_w = self.stockfish.get_evaluation()
            self.stockfish.set_fen_position(fen_black_to_move)
            eval_b = self.stockfish.get_evaluation()

            val_w = eval_w['value'] if eval_w and eval_w.get('type') == 'cp' else 0
            val_b = eval_b['value'] if eval_b and eval_b.get('type') == 'cp' else 0

            # Trắng luôn thắng thế ở cả 2 FEN trên. Nếu quy ước "luôn theo góc
            # Trắng" thì cả 2 giá trị đều dương. Nếu "theo bên đang đi" thì giá
            # trị khi Đen đi sẽ âm (bất lợi cho Đen).
            self.eval_turn_relative = (val_w > 0) and (val_b < 0)
            print(f"ℹ️ Quy ước điểm Stockfish: {'theo bên đang đi' if self.eval_turn_relative else 'luôn theo góc Trắng'}")

            # Khôi phục vị trí ván đấu hiện tại
            self.stockfish.set_fen_position(self.board.fen())
        except Exception as e:
            self.eval_turn_relative = False

    def _to_white_perspective(self, raw_value, side_to_move_is_white):
        """Chuẩn hóa điểm số thô từ Stockfish về góc nhìn CỐ ĐỊNH của Trắng
        (dương = có lợi cho Trắng), bất kể thư viện dùng quy ước nào."""
        if self.eval_turn_relative and not side_to_move_is_white:
            return -raw_value
        return raw_value

    def make_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move not in self.board.legal_moves:
                return False

            fen_before = self.board.fen()
            board_before = self.board.copy(stack=False)

            # Lấy nước tốt nhất trước khi đi (1-2 lượt tìm kiếm thay vì đánh giá mọi nước)
            top_moves_before = self.get_top_moves(3)
            eval_before = top_moves_before[0]['score_cp'] if top_moves_before else self.get_evaluation()

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
            self.stockfish.set_skill_level(20)  # luôn đánh giá ở sức mạnh tối đa
            self.stockfish.set_fen_position(self.board.fen())
            eval_value = self.stockfish.get_evaluation()
            side_white = self.board.turn

            if eval_value['type'] == 'cp':
                return self._to_white_perspective(eval_value['value'], side_white)
            elif eval_value['type'] == 'mate':
                mate_in = eval_value['value']
                raw = 10000 if mate_in > 0 else -10000
                return self._to_white_perspective(raw, side_white)

            return None
        except:
            return None

    def get_best_move(self, time_ms=1000):
        """Nước đi của AI ĐỐI THỦ - dùng đúng độ khó người dùng chọn (có thể yếu hơn)."""
        if not self.stockfish_available:
            return None

        try:
            self.stockfish.set_skill_level(self.opponent_skill_level)
            self.stockfish.set_fen_position(self.board.fen())
            best_move = self.stockfish.get_best_move_time(time_ms)
            return best_move
        except:
            return None

    def get_top_moves(self, count=3):
        """Lấy nước đi tốt nhất để CHẤM ĐIỂM - luôn full-strength, không theo độ
        khó AI đối thủ, để không bỏ sót đòn phản công sau các nước hy sinh."""
        if not self.stockfish_available:
            return []

        try:
            self.stockfish.set_skill_level(20)
            self.stockfish.set_fen_position(self.board.fen())
            best_move_uci = self.stockfish.get_best_move_time(600)

            if not best_move_uci:
                return []

            # Đánh giá vị trí SAU nước tốt nhất (chỉ 1 lượt tìm kiếm)
            temp_board = self.board.copy()
            temp_board.push(chess.Move.from_uci(best_move_uci))
            self.stockfish.set_fen_position(temp_board.fen())
            eval_val = self.stockfish.get_evaluation()
            side_white = temp_board.turn

            best_score_cp = 0
            if eval_val:
                if eval_val['type'] == 'cp':
                    best_score_cp = self._to_white_perspective(eval_val['value'], side_white)
                elif eval_val['type'] == 'mate':
                    raw = 10000 if eval_val['value'] > 0 else -10000
                    best_score_cp = self._to_white_perspective(raw, side_white)

            return [{'move': best_move_uci, 'score_cp': best_score_cp}]
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
            self.stockfish.set_skill_level(20)
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

        # 2 engine cùng tồn tại song song -> chia đôi số luồng để tránh quá tải CPU
        battle_threads = max(1, ENGINE_THREADS // 2)
        engine_params = {"Threads": battle_threads, "Hash": ENGINE_HASH_MB // 2}

        # Initialize with found path or default
        if stockfish_path:
            self.stockfish1 = Stockfish(path=stockfish_path, parameters=engine_params)
            self.stockfish2 = Stockfish(path=stockfish_path, parameters=engine_params)
        else:
            self.stockfish1 = Stockfish(parameters=engine_params)
            self.stockfish2 = Stockfish(parameters=engine_params)

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
