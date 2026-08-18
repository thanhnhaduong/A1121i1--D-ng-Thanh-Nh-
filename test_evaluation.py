#!/usr/bin/env python3
"""
Test evaluation logic to verify Good/Bad/Blunder ratings
"""

import chess
from chess_engine import ChessGame, MoveEvaluation

def test_move_evaluation():
    """Test move evaluation with specific positions"""
    game = ChessGame()

    print("=" * 70)
    print("TEST: Move Evaluation Logic")
    print("=" * 70)

    # Test 1: Normal opening moves
    print("\n✅ Test 1: Normal Opening Moves")
    moves = ["e2e4", "c7c5", "g1f3"]  # 1.e4 c5 2.Nf3
    for move in moves:
        result = game.make_move(move)
        if result and game.evaluation_history:
            last = game.evaluation_history[-1]
            eval_obj = last['evaluation']
            before = last['eval_before']
            after = last['eval_after']
            change = after - before if before and after else 0

            # Flip for black if needed
            if len(game.move_history) % 2 == 0:
                change = -change

            print(f"  Move: {move}")
            print(f"    Before: {before/100:+.2f} | After: {after/100:+.2f} | Change: {change/100:+.2f}")
            print(f"    Evaluation: {eval_obj}")

    # Test 2: Blunder move (if possible)
    print("\n✅ Test 2: Looking for Bad Moves")
    test_board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    test_game = ChessGame()
    test_game.board = test_board
    test_game.move_history = ["e2e4"]
    test_game.stockfish.set_fen_position(test_board.fen())

    eval_bad = test_game.get_evaluation()
    print(f"  Position eval: {eval_bad/100:+.2f}" if eval_bad else "  Eval: N/A")

    # Test 3: Check flip logic
    print("\n✅ Test 3: Perspective Flip Logic")
    print("  After white move (len=odd): don't flip")
    print("  After black move (len=even): flip")
    print(f"  Current move_history len: {len(game.move_history)}")
    print(f"  Should flip for next move: {len(game.move_history) % 2 == 0}")

    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)

if __name__ == "__main__":
    test_move_evaluation()
