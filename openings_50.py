#!/usr/bin/env python3
"""
♟ 50+ Chess Openings Database - Optimized
"""

OPENINGS = {
    # 1.e4 Openings (20+)
    "Italian Game": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
        "description": "Khai cuộc cổ điển, tấn công f7 yếu",
        "history": "Thế kỷ 15, yêu thích của các kỳ thủ tấn công",
        "idea": "Phát triển nhanh, kiểm soát trung tâm"
    },
    "Spanish Opening (Ruy Lopez)": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
        "description": "Khai cuộc sâu sắc nhất, có lợi cho Trắng",
        "history": "Pedro Damiano 1512, yêu thích của Kasparov",
        "idea": "Ghim quân mã, tạo áp lực c6"
    },
    "Sicilian Defense": {
        "moves": ["e2e4", "c7c5"],
        "description": "Phòng thủ sắc sảo, bất đối xứng",
        "history": "Pietro Carrera 1594, ưu tiên của Fischer",
        "idea": "Tấn công d4, tránh đánh đổi đôi quân"
    },
    "French Defense": {
        "moves": ["e2e4", "e7e6"],
        "description": "Phòng thủ bền chặt, chơi dài",
        "history": "Phát triển thế kỷ 19",
        "idea": "Phòng thủ bền, chuẩn bị d5"
    },
    "Caro-Kann Defense": {
        "moves": ["e2e4", "c7c6"],
        "description": "Phòng thủ vững chắc, linh hoạt",
        "history": "Marcus Kann 1890s",
        "idea": "Bảo vệ e5, tránh lỗ hổng"
    },
    "Scandinavian Defense": {
        "moves": ["e2e4", "d7d5"],
        "description": "Phòng thủ tấn công, chiếm trung tâm ngay",
        "history": "Kỳ thủ Bắc Âu",
        "idea": "Tấn công e4, tạo bất lợi"
    },
    "Pirc Defense": {
        "moves": ["e2e4", "d7d6"],
        "description": "Phòng thủ hiện đại, kiểm soát từ xa",
        "history": "Vasja Pirc 1930s",
        "idea": "Cho phép đối thủ chiếm rồi tấn công"
    },
    "Alekhine's Defense": {
        "moves": ["e2e4", "g8f6"],
        "description": "Phòng thủ tấn công, kích thích",
        "history": "Alexander Alekhine",
        "idea": "Kích thích e4 tiến, rồi tấn công"
    },
    "Philidor Defense": {
        "moves": ["e2e4", "e7e5", "g1f3", "d7d6"],
        "description": "Phòng thủ bền, chắc chắn",
        "history": "François-André Danican Philidor",
        "idea": "Phòng thủ bền chặt"
    },
    "Petroff Defense": {
        "moves": ["e2e4", "e7e5", "g1f3", "g8f6"],
        "description": "Phòng thủ đối xứng, tránh cấp độ sắc",
        "history": "Alexander Petroff",
        "idea": "Sự cân bằng, đơn giản"
    },
    "Two Knights Defense": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6"],
        "description": "Phòng thủ sắc sảo, chiến đấu",
        "history": "Khai cuộc cổ điển",
        "idea": "Tấn công e4, tạo sự phức tạp"
    },
    "Scotch Game": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "d2d4"],
        "description": "Khai cuộc tấn công mở",
        "history": "Alonzo Fernandez del Rio",
        "idea": "Kiểm soát trung tâm, tấn công nhanh"
    },
    "Giuoco Piano": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"],
        "description": "Khai cuộc cân bằng",
        "history": "Thế kỷ 16",
        "idea": "Phát triển nhanh, cân bằng"
    },
    "Evans Gambit": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "b2b4"],
        "description": "Quân đánh bạt cổ điển",
        "history": "Captain William Davies Evans",
        "idea": "Đánh bạt để mở đường"
    },
    "Fried Liver Attack": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6", "g1f3"],
        "description": "Tấn công sắc sảo",
        "history": "Khai cuộc cổ điển",
        "idea": "Tấn công nhanh, hy sinh quân"
    },
    "Horwitz Defense": {
        "moves": ["e2e4", "b7b5"],
        "description": "Phòng thủ tấn công, lạ",
        "history": "Hiếm gặp",
        "idea": "Tấn công nhanh e4"
    },
    "Orangutan Opening": {
        "moves": ["b2b4"],
        "description": "Khai cuộc biên hiếm gặp",
        "history": "Kỳ thủ sáng tạo",
        "idea": "Kiểm soát đường chéo"
    },
    "Bird's Opening": {
        "moves": ["f2f4"],
        "description": "Khai cuộc hiếm gặp",
        "history": "Henry Bird",
        "idea": "Kiểm soát e5"
    },
    "Sokolsky Opening": {
        "moves": ["b2b4"],
        "description": "Khai cuộc biên",
        "history": "Alexei Sokolsky",
        "idea": "Kiểm soát đường chéo a1-h8"
    },
    "Van't Kruijs Opening": {
        "moves": ["e2e3"],
        "description": "Khai cuộc chắc chắn, phòng thủ",
        "history": "Chơi chắc chắn",
        "idea": "Phòng thủ chắc, tương lai linh hoạt"
    },

    # 1.d4 Openings (20+)
    "Queen's Gambit": {
        "moves": ["d2d4", "d7d5", "c2c4"],
        "description": "Khai cuộc chiến lược, tốt cho Trắng",
        "history": "Thế kỷ 17, yêu thích Kasparov",
        "idea": "Kiểm soát d5, lợi thế lâu dài"
    },
    "Slav Defense": {
        "moves": ["d2d4", "d7d5", "c2c4", "c7c6"],
        "description": "Phòng thủ vững chắc",
        "history": "Kỳ thủ Slav",
        "idea": "Bảo vệ d5, linh hoạt"
    },
    "Semi-Slav Defense": {
        "moves": ["d2d4", "d7d5", "c2c4", "e7e6", "b1c3", "c7c6"],
        "description": "Phòng thủ linh hoạt",
        "history": "Phát triển thế kỷ 20",
        "idea": "Kết hợp Slav + Black Indian"
    },
    "Queen's Indian Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6", "g1f3", "b7b6"],
        "description": "Phòng thủ quanh lân",
        "history": "Kỳ thủ Ấn Độ",
        "idea": "Fianchetto, lợi thế lâu dài"
    },
    "Nimzo-Indian Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"],
        "description": "Phòng thủ sắc sảo",
        "history": "Nimzowitsch",
        "idea": "Ghim c3, tạo bất lợi"
    },
    "King's Indian Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "g7g6"],
        "description": "Phòng thủ hiện đại",
        "history": "Fischer, Kasparov",
        "idea": "Fianchetto, kiểm soát từ xa"
    },
    "Grunfeld Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "d7d5"],
        "description": "Phòng thủ sắc sảo hiện đại",
        "history": "Ernst Grunfeld",
        "idea": "Tấn công sau khi đối thủ chiếm"
    },
    "Benko Gambit": {
        "moves": ["d2d4", "g8f6", "c2c4", "c7c5", "d4d5", "b7b5"],
        "description": "Quân đánh bạt chiến lược",
        "history": "Pal Benko",
        "idea": "Đánh bạt trên biên, mở đường chéo"
    },
    "Benoni Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "c7c5"],
        "description": "Phòng thủ chiến lược",
        "history": "Kỳ thủ Benoni",
        "idea": "Tấn công trung tâm sau"
    },
    "Catalan Opening": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6", "g1f3", "d7d5", "g2g3"],
        "description": "Khai cuộc hiện đại, linh hoạt",
        "history": "Savielly Tartakower",
        "idea": "Fianchetto, lợi thế lâu dài"
    },
    "Reti Opening": {
        "moves": ["g1f3", "d7d5", "c2c4"],
        "description": "Khai cuộc hypermodern",
        "history": "Richard Réti",
        "idea": "Kiểm soát từ xa bằng quân nhẹ"
    },
    "English Opening": {
        "moves": ["c2c4"],
        "description": "Khai cuộc linh hoạt",
        "history": "Staunton",
        "idea": "Kiểm soát d5 từ xa"
    },
    "London System": {
        "moves": ["d2d4", "d7d5", "c2c4", "c7c6", "c1f4"],
        "description": "Hệ thống dân chủ",
        "history": "Kỳ thủ kiên định",
        "idea": "Xây dựng structure vững chắc"
    },
    "Colle System": {
        "moves": ["d2d4", "d7d5", "c2c4", "c7c6", "b1c3", "g8f6", "c1f4"],
        "description": "Hệ thống cân bằng",
        "history": "Edgar Colle",
        "idea": "Xây dựng position vững, lợi thế nhỏ"
    },
    "Indian Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6"],
        "description": "Phòng thủ hiện đại",
        "history": "Kỳ thủ Ấn Độ",
        "idea": "Kiểm soát trung tâm từ xa"
    },
    "Larsen Opening": {
        "moves": ["b2b3"],
        "description": "Khai cuộc hypermodern",
        "history": "Bent Larsen",
        "idea": "Kiểm soát đường chéo"
    },
    "Polish Opening": {
        "moves": ["b2b4"],
        "description": "Khai cuộc biên",
        "history": "Sokolsky",
        "idea": "Kiểm soát đường chéo"
    },
    "Florian Defense": {
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "d7d6"],
        "description": "Phòng thủ chắc chắn",
        "history": "Montenegro",
        "idea": "Phòng thủ bền, tránh sắc"
    },
    "Robatsch Defense": {
        "moves": ["e2e4", "d7d6", "d2d4", "g8f6", "b1c3", "g7g6"],
        "description": "Phòng thủ hiện đại, fianchetto",
        "history": "Kỳ thủ sáng tạo",
        "idea": "Fianchetto, kiểm soát từ xa"
    },
    "Modern Defense": {
        "moves": ["e2e4", "d7d6"],
        "description": "Phòng thủ hiện đại, linh hoạt",
        "history": "Phát triển thế kỷ 20",
        "idea": "Phòng thủ linh hoạt từ xa"
    },

    # Rare/Special Openings (10+)
    "Ware Opening": {
        "moves": ["a2a3"],
        "description": "Khai cuộc hiếm gặp",
        "history": "Preston Ware",
        "idea": "Kiểm soát b4"
    },
    "Mieses Opening": {
        "moves": ["d2d3"],
        "description": "Khai cuộc phòng thủ",
        "history": "Jacques Mieses",
        "idea": "Chuẩn bị đánh c4"
    },
    "Center Game": {
        "moves": ["e2e4", "d7d5", "d2d4"],
        "description": "Khai cuộc tấn công trung tâm",
        "history": "Khai cuộc cổ điển",
        "idea": "Tấn công d5 ngay"
    },
    "Danish Gambit": {
        "moves": ["c2c3", "d7d5", "d2d4"],
        "description": "Quân đánh bạt của Đan Mạch",
        "history": "Khai cuộc cổ điển",
        "idea": "Đánh bạt để mở"
    },
    "Irregular Openings": {
        "moves": ["g2g4"],
        "description": "Khai cuộc lạ thường",
        "history": "Chơi sáng tạo",
        "idea": "Kiểm soát f5, e5"
    },
    "Grenfeld Defense Extended": {
        "moves": ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "d7d5", "c1g5"],
        "description": "Phòng thủ sắc sảo",
        "history": "Phát triển hiện đại",
        "idea": "Tấn công chi tiết"
    },
    "Sicilian Accelerated": {
        "moves": ["e2e4", "c7c5", "g1f3", "b8c6"],
        "description": "Sicilian nhanh",
        "history": "Phát triển thế kỷ 20",
        "idea": "Tấn công nhanh d4"
    },
    "French Winawer": {
        "moves": ["e2e4", "e7e6", "d2d4", "d7d5", "b1c3", "f8b4"],
        "description": "Biến thể Winawer",
        "history": "Phát triển chi tiết",
        "idea": "Ghim c3, tạo bất lợi"
    },
    "Caro-Kann Advanced": {
        "moves": ["e2e4", "c7c6", "d2d4", "d7d5", "f1c4"],
        "description": "Biến thể nâng cao",
        "history": "Phát triển thế kỷ 20",
        "idea": "Tấn công f7"
    },
    "Open Sicilian": {
        "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4"],
        "description": "Sicilian mở",
        "history": "Phát triển chi tiết",
        "idea": "Tấn công trung tâm"
    },
    "Najdorf Sicilian": {
        "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"],
        "description": "Biến thể Najdorf nổi tiếng",
        "history": "Miguel Najdorf 1940s, yêu thích của Kasparov",
        "idea": "Phòng thủ linh hoạt, b5 sau"
    },
    "Dragon Sicilian": {
        "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "g7g6"],
        "description": "Sicilian Dragon với g6",
        "history": "Phát triển 1950s, hiệp định Karpov",
        "idea": "Phòng thủ tấn công với g6"
    },
    "Sveshnikov Sicilian": {
        "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "e7e5"],
        "description": "Sveshnikov biến thể",
        "history": "Evgeny Sveshnikov 1970s",
        "idea": "e5 sâu sắc"
    },
    "Taimanov Sicilian": {
        "moves": ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "b8c6"],
        "description": "Biến thể Taimanov",
        "history": "Mark Taimanov, yêu thích của Petrosian",
        "idea": "c6 sớm, phòng thủ bền"
    },
    "Rossolimo Variation": {
        "moves": ["e2e4", "c7c5", "g1f3", "b8c6", "f1b5"],
        "description": "Anti-Sicilian biến thể",
        "history": "Lubomir Kavalek phổ biến",
        "idea": "Xn b5, tránh Sicilian lý thuyết"
    },
    "Alapin Sicilian": {
        "moves": ["e2e4", "c7c5", "c2c3"],
        "description": "Anti-Sicilian 2.c3",
        "history": "Sergei Alapin, yêu thích của Karpov",
        "idea": "Bảo vệ d4, d5 sâu"
    },
    "English Opening": {
        "moves": ["c2c4"],
        "description": "Khai cuộc Anh, dấu hiệu dấu hiệu",
        "history": "Henry Bird 1850s",
        "idea": "Kiểm soát d5 từ xa"
    },
    "Bird Opening": {
        "moves": ["f2f4"],
        "description": "Bird Opening kiểm soát e5",
        "history": "Henry Bird 19th century",
        "idea": "Kiểm soát e5, f5"
    },
    "Polish Opening": {
        "moves": ["b2b4"],
        "description": "Polish Opening b4",
        "history": "Sokolsky 1950s",
        "idea": "Kiểm soát c5, a4 mở"
    },
    "Orangutan Opening": {
        "moves": ["b2b4"],
        "description": "Sokolsky Opening",
        "history": "Aleksei Sokolsky",
        "idea": "Cách tiếp cận lạ"
    },
    "Atypical Opening": {
        "moves": ["h2h4"],
        "description": "h4 Khai cuộc lạ",
        "history": "Chơi sáng tạo",
        "idea": "Kiểm soát g5, phát triển"
    },
    "Nimzo-Indian Advanced": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"],
        "description": "Nimzo-Indian nâng cao",
        "history": "Aaron Nimzowitsch, yêu thích Kasparov",
        "idea": "Bất đối xứng, c3 khó"
    },
    "King's Indian Attack": {
        "moves": ["g1f3", "d7d5", "c2c4"],
        "description": "Khai cuộc tấn công King's Indian",
        "history": "Bobby Fischer, Karpov",
        "idea": "Phát triển linh hoạt"
    },
    "Fianchetto Opening": {
        "moves": ["b2b3"],
        "description": "Fianchetto Trắng",
        "history": "Phát triển thế kỷ 20",
        "idea": "Fianchetto g2, kiểm soát Long diagonal"
    },
    "Sokolsky's Gambit": {
        "moves": ["b2b4", "e7e5", "b4b5"],
        "description": "Gambit Sokolsky",
        "history": "Aleksei Sokolsky",
        "idea": "Tấn công e5 với b5"
    },
    "Orangutan Gambit": {
        "moves": ["b2b4", "e7e5", "a2a3"],
        "description": "Biến thể Orangutan",
        "history": "Phát triển lạ",
        "idea": "a3, chuẩn bị c4"
    },
    "Ware Opening": {
        "moves": ["a2a4"],
        "description": "Ware Opening a4",
        "history": "Preston Ware",
        "idea": "Chuẩn bị a5, kiểm soát cạnh"
    },
    "Mieses Opening": {
        "moves": ["d2d3"],
        "description": "Mieses d3",
        "history": "Jacques Mieses",
        "idea": "Kiểm soát e4, phát triển linh hoạt"
    },
    "Andreasson Opening": {
        "moves": ["c2c3"],
        "description": "Andreasson c3",
        "history": "Phát triển ít phổ biến",
        "idea": "Chuẩn bị d4, bảo vệ"
    },
    "Dunst Opening": {
        "moves": ["c2c3"],
        "description": "Dunst System c3",
        "history": "Siegbert Tarrasch yêu thích",
        "idea": "Chuẩn bị d4 với bảo vệ"
    },
    "Budapest Defense": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e5"],
        "description": "Budapest Defense gambit",
        "history": "Phát triển Hungary, Szabo",
        "idea": "e5 gambit, tấn công thiều hụt"
    },
    "Benko Gambit Accepted": {
        "moves": ["d2d4", "g8f6", "c2c4", "c7c5", "d4c5"],
        "description": "Benko Gambit chấp nhận",
        "history": "Pal Benko 1960s",
        "idea": "Phòng thủ sắc sảo với c5"
    },
    "Benoni Defense Main": {
        "moves": ["d2d4", "g8f6", "c2c4", "c7c5"],
        "description": "Benoni Defense lý thuyết",
        "history": "Aron Nimzowitsch",
        "idea": "c5, tấn công d4"
    },
    "Colle System": {
        "moves": ["d2d4", "g8f6", "f2f3"],
        "description": "Colle System chiến thuật",
        "history": "Edgar Colle 1920s",
        "idea": "e4, e3 chuẩn bị, phát triển bền"
    },
    "London System": {
        "moves": ["d2d4", "g8f6", "f2f3", "c7c6", "c2c3"],
        "description": "London System d4",
        "history": "Phát triển hiện đại, Grivas phổ biến",
        "idea": "d4, e3, c3, e4, f4, f3 chuỗi nước"
    },
    "Catalan Closed": {
        "moves": ["d2d4", "g8f6", "c2c4", "e7e6", "g2g3", "d7d5"],
        "description": "Catalan đóng chặt",
        "history": "Aron Nimzowitsch, Kasparov",
        "idea": "Fianchetto g3, Long diagonal"
    },
    "Reti Opening Main": {
        "moves": ["g1f3", "d7d5", "c2c4", "d5c4"],
        "description": "Reti Opening lý thuyết",
        "history": "Richard Reti 1920s",
        "idea": "f3, c4, kiểm soát trung tâm từ xa"
    },
}

# Teaching mode data - Học khai cuộc
TEACHING_OPENINGS = {
    "Italian Game": {
        "steps": [
            ("e2e4", "Nước 1: e4 - Kiểm soát trung tâm, mở đường tốt Vua"),
            ("e7e5", "Nước 2: e5 - Đối phương cũng kiểm soát trung tâm"),
            ("g1f3", "Nước 3: Nf3 - Phát triển mã, tấn công e5"),
            ("b8c6", "Nước 4: Nc6 - Phòng thủ e5, phát triển"),
            ("f1c4", "Nước 5: Bc4 - Tấn công f7 yếu! Trọng tâm của Italian"),
        ],
        "summary": "Italian Game tấn công f7 yếu qua Bc4"
    },
    "Spanish Opening (Ruy Lopez)": {
        "steps": [
            ("e2e4", "e4 - Kiểm soát trung tâm"),
            ("e7e5", "e5 - Phòng thủ cân bằng"),
            ("g1f3", "Nf3 - Tấn công e5"),
            ("b8c6", "Nc6 - Phòng thủ e5"),
            ("f1b5", "Bb5 - GHIM quân mã c6! Ép Đen phải quyết định"),
        ],
        "summary": "Ruy Lopez là khai cuộc sâu sắc nhất"
    },
    "Sicilian Defense": {
        "steps": [
            ("e2e4", "e4 - Trắng kiểm soát trung tâm"),
            ("c7c5", "c5 - Đen tấn công d4 thay vì e5!"),
        ],
        "summary": "Sicilian là phòng thủ tấn công chính của Đen"
    },
}

def get_opening_by_moves(moves):
    if len(moves) < 2:
        return None, None

    for name, data in OPENINGS.items():
        opening_moves = data['moves']
        if len(moves) >= len(opening_moves) and moves[:len(opening_moves)] == opening_moves:
            return name, data

    return None, None

def get_all_openings():
    return OPENINGS

def get_teaching_data(opening_name):
    """Get teaching steps for an opening"""
    return TEACHING_OPENINGS.get(opening_name, None)
