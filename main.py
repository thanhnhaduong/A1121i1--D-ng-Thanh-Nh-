#!/usr/bin/env python3
"""
♟ CHESS MASTER - Optimized Version
"""

import sys
import tkinter as tk
from gui_optimized import ChessGUI

def check_dependencies():
    missing = []
    try:
        import chess
    except ImportError:
        missing.append("python-chess")

    try:
        from stockfish import Stockfish
    except ImportError:
        missing.append("stockfish")

    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        print(f"Install: pip install {' '.join(missing)}")
        return False
    return True

if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)

    root = tk.Tk()
    gui = ChessGUI(root)
    gui.draw_board()
    root.mainloop()
