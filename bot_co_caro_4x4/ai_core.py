"""
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
import random

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
        with gzip.open(path, "wb") as f:
            pickle.dump(self.__dict__, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        if not os.path.exists(path):
            return False
        with gzip.open(path, "rb") as f:
            data = pickle.load(f)
        data.pop("mistakes_learned", None)
        self.__dict__.update(data)
        return True
