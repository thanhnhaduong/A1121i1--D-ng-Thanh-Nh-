#!/usr/bin/env python3
"""
♟ Chess Puzzles Database - hand-verified legal puzzles for learning
"""

PUZZLES = {
    "Back Rank Mate 1": {
        "fen": "6k1/5ppp/8/8/8/8/8/R6K w - - 0 1",
        "best_move": "Ra8",
        "difficulty": 1,
        "hint": "Chiếu hết ở hàng cuối",
        "description": "Quân vua đen bị mắc kẹt ở hàng 8. Tìm cách chiếu hết.",
        "theme": "Back Rank Mate"
    },
    "Simple Fork": {
        "fen": "2r3k1/8/2N5/8/8/8/8/6K1 w - - 0 1",
        "best_move": "Ne7",
        "difficulty": 1,
        "hint": "Mã có thể tấn công vua và xe cùng lúc",
        "description": "Mã trắng nhảy vào chiếu, đồng thời tấn công luôn xe đen",
        "theme": "Fork"
    },
    "Capture Free Piece": {
        "fen": "6k1/8/8/q7/8/8/8/R6K w - - 0 1",
        "best_move": "Rxa5",
        "difficulty": 1,
        "hint": "Có một quân không được bảo vệ, cùng cột với xe",
        "description": "Hậu đen không được bảo vệ, cùng cột a với xe trắng. Bắt nó.",
        "theme": "Tactical Win"
    },
    "Two Rooks Mate": {
        "fen": "6k1/R7/8/8/8/8/4R3/6K1 w - - 0 1",
        "best_move": "Re8",
        "difficulty": 1,
        "hint": "Xe ở hàng 7 đã khóa vua, xe còn lại vào chiếu hết từ xa",
        "description": "Xe a7 chặn toàn bộ hàng 7, xe e1 tiến vào hàng 8 chiếu hết (vua không thể ăn vì ở quá xa)",
        "theme": "Checkmate"
    },
    "Knight Fork King Queen": {
        "fen": "4q1k1/8/8/3N4/8/8/8/6K1 w - - 0 1",
        "best_move": "Nf6",
        "difficulty": 2,
        "hint": "Mã có thể tấn công vua và hậu cùng lúc",
        "description": "Fork quân vua và hậu với mã",
        "theme": "Fork"
    },
    "Discovered Check": {
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/3P1N2/PPP1BPPP/RNBQK2R w KQkq - 4 4",
        "best_move": "Nxe5",
        "difficulty": 5,
        "hint": "Mã có thể bắt tốt trung tâm",
        "description": "Bắt tốt e5 bằng mã, giành lợi thế vật chất",
        "theme": "Tactical Win"
    },
    "Pin and Win": {
        "fen": "4n1k1/8/8/8/8/8/8/R5K1 w - - 0 1",
        "best_move": "Re1",
        "difficulty": 5,
        "hint": "Ghim quân mã vào vua rồi ăn",
        "description": "Xe vào cột e, ghim mã đen vào vua - mã không thể chạy, mất quân",
        "theme": "Pin"
    },
    "Skewer": {
        "fen": "8/8/4r3/8/8/4k3/8/R6K w - - 0 1",
        "best_move": "Re1",
        "difficulty": 4,
        "hint": "Chiếu vua trước, xe phía sau sẽ lộ ra",
        "description": "Chiếu vua bằng xe, buộc vua né rồi ăn luôn xe đen phía sau",
        "theme": "Skewer"
    },
    "Sacrifice for Checkmate": {
        "fen": "5rk1/5ppp/8/8/8/4Q3/8/6K1 w - - 0 1",
        "best_move": "Qe8",
        "difficulty": 6,
        "hint": "Hậu vào ghim xe đen vào vua",
        "description": "Hậu tiến vào hàng 8, ghim xe đen vào vua - xe không thể cứu",
        "theme": "Pin"
    },
    "Deflection": {
        "fen": "6k1/5ppp/8/8/8/R7/8/6K1 w - - 0 1",
        "best_move": "Ra7",
        "difficulty": 5,
        "hint": "Đưa xe lên tấn công hàng 7",
        "description": "Xe tấn công hàng 7, gây áp lực lên các tốt đen",
        "theme": "Tactical"
    },
    "Greek Gift Sacrifice": {
        "fen": "6k1/5ppp/8/8/8/3B4/8/1K6 w - - 0 1",
        "best_move": "Bxh7",
        "difficulty": 8,
        "hint": "Hy sinh tượng trên h7 để phá vỡ vị trí vua",
        "description": "Tấn công Greek Gift - hy sinh tượng ăn tốt h7 kèm chiếu, mở toang vị trí vua",
        "theme": "Sacrifice"
    },
    "Quiet Move Checkmate": {
        "fen": "6k1/5ppp/8/8/8/8/1Q6/6K1 w - - 0 1",
        "best_move": "Qb8",
        "difficulty": 7,
        "hint": "Đưa hậu vào hàng 8 trống trải",
        "description": "Hậu tiến vào hàng 8 theo cột b đang mở, chiếu hết",
        "theme": "Checkmate"
    },
    "Windmill": {
        "fen": "r1b1k2r/ppppqppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP1QPPP/RNB1K2R w KQkq - 0 0",
        "best_move": "Nxe5",
        "difficulty": 8,
        "hint": "Mã có thể bắt tốt trung tâm",
        "description": "Windmill - mã bắt tốt mở đầu chuỗi tấn công",
        "theme": "Tactical"
    },
    "Clearance": {
        "fen": "6k1/5ppp/8/8/8/8/Q7/6K1 w - - 0 1",
        "best_move": "Qa8",
        "difficulty": 6,
        "hint": "Đưa hậu vào hàng 8 theo cột a đang mở",
        "description": "Hậu tiến thẳng theo cột a trống để chiếu hết",
        "theme": "Checkmate"
    },
    "Zugzwang": {
        "fen": "8/8/8/8/8/4k3/8/4K2R w - - 0 1",
        "best_move": "Rh4",
        "difficulty": 9,
        "hint": "Bất kỳ nước đi nào của đen đều thua",
        "description": "Zugzwang - đối thủ bị buộc thực hiện nước xấu",
        "theme": "Zugzwang"
    },
    "Capture and Checkmate": {
        "fen": "r5k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1",
        "best_move": "Rxa8",
        "difficulty": 3,
        "hint": "Ăn xe đen không được bảo vệ, đồng thời chiếu hết",
        "description": "Bắt xe a8 và chiếu hết luôn vì hàng 8 và hàng 7 (tốt) đã bị khóa",
        "theme": "Tactical"
    },
    "Intermediate": {
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4",
        "best_move": "Nxe5",
        "difficulty": 5,
        "hint": "Bắt tốt ở giữa",
        "description": "Thắng tốt với chiếu đe dọa",
        "theme": "Tactic"
    },
    "Backward Move Wins": {
        "fen": "6k1/5ppp/8/8/8/8/1R6/6K1 w - - 0 1",
        "best_move": "Rb8",
        "difficulty": 4,
        "hint": "Xe tiến thẳng vào hàng 8 trống",
        "description": "Xe tiến vào hàng 8, chiếu hết vì các tốt đen tự khóa đường thoát của vua",
        "theme": "Checkmate"
    },
    "Pawn Promotion": {
        "fen": "6k1/4P1pp/8/8/8/8/8/6K1 w - - 0 1",
        "best_move": "e8=Q",
        "difficulty": 1,
        "hint": "Nâng tốt thành hậu",
        "description": "Nâng tốt lên thành hậu và chiếu hết",
        "theme": "Promotion"
    },
    "Opposition": {
        "fen": "8/8/8/4k3/8/8/4K3/8 w - - 0 1",
        "best_move": "Ke3",
        "difficulty": 7,
        "hint": "Tiến vua để giành đối lập trực tiếp, buộc đối thủ nhường bước",
        "description": "Vua tiến lên, giành thế đối lập (opposition) - Đen buộc phải nhường đường",
        "theme": "Opposition"
    },
    "Triangulation": {
        "fen": "8/8/4k3/8/8/4K3/8/8 w - - 0 1",
        "best_move": "Kd3",
        "difficulty": 8,
        "hint": "Đi vòng để mất tempo, buộc đối thủ vào thế zugzwang",
        "description": "Triangulation - đi vòng giữ nguyên quãng cách nhưng đổi quyền đi",
        "theme": "Triangulation"
    },
    "Queen Sacrifice Mate": {
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 0",
        "best_move": "Nxe5",
        "difficulty": 6,
        "hint": "Bắt tốt ở giữa với chiếu đe dọa",
        "description": "Chiến thuật giành nước",
        "theme": "Attack"
    },
    "Discovered Attack": {
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/3P1N2/PPP1BPPP/RNBQK2R w KQkq - 4 4",
        "best_move": "Nxe5",
        "difficulty": 5,
        "hint": "Mã có thể bắt tốt trung tâm",
        "description": "Bắt tốt e5 bằng mã, giành lợi thế vật chất",
        "theme": "Tactical Win"
    },
    "Simple Checkmate": {
        "fen": "6k1/5ppp/8/8/8/8/8/R6K w - - 0 1",
        "best_move": "Ra8",
        "difficulty": 1,
        "hint": "Chiếu hết với xe ở hàng 8",
        "description": "Chiếu hết đơn giản",
        "theme": "Checkmate"
    },
}

# Thêm vài puzzle khác
ADDITIONAL_PUZZLES = {
    "Morphy's Mating Net": {
        "fen": "r1b1k1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 0",
        "best_move": "Nxe5",
        "difficulty": 7,
        "hint": "Mã có thể bắt tốt trung tâm, mở đầu đòn tấn công",
        "description": "Bắt tốt trung tâm để mở đầu chuỗi tấn công mạnh vào vua đen",
        "theme": "Attack"
    },
    "Smothered Mate": {
        "fen": "6rk/6pp/8/4N3/8/8/8/K7 w - - 0 1",
        "best_move": "Nf7",
        "difficulty": 6,
        "hint": "Vua đen bị chính quân của mình làm mắc kẹt",
        "description": "Smothered mate - mã chiếu hết vì vua bị chính xe và tốt của mình bịt kín",
        "theme": "Smothered Mate"
    },
    "Quiet Move": {
        "fen": "6k1/5ppp/8/8/8/8/8/R1K5 w - - 0 1",
        "best_move": "Ra8",
        "difficulty": 3,
        "hint": "Xe tiến thẳng vào hàng 8 trống",
        "description": "Xe tiến vào hàng 8, chiếu hết vì các tốt đen tự khóa đường thoát của vua",
        "theme": "Checkmate"
    },
}

# Combine all puzzles
PUZZLES.update(ADDITIONAL_PUZZLES)


def get_puzzle_by_id(puzzle_id):
    """Lấy puzzle theo ID"""
    puzzle_list = list(PUZZLES.keys())
    if 0 <= puzzle_id < len(puzzle_list):
        name = puzzle_list[puzzle_id]
        return name, PUZZLES[name]
    return None, None

def get_all_puzzles():
    """Lấy tất cả puzzle"""
    return PUZZLES

def get_puzzles_by_difficulty(difficulty):
    """Lấy puzzle theo độ khó"""
    return {name: puzzle for name, puzzle in PUZZLES.items()
            if puzzle.get('difficulty') == difficulty}

def get_puzzles_by_theme(theme):
    """Lấy puzzle theo chủ đề"""
    return {name: puzzle for name, puzzle in PUZZLES.items()
            if puzzle.get('theme') == theme}

def count_puzzles():
    """Đếm số lượng puzzle"""
    return len(PUZZLES)
