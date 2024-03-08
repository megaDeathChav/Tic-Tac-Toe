import unittest
from GameStatus_5120 import GameStatus

class TestGameStatus(unittest.TestCase):
    def test_is_terminal(self):
        # Test a game that is not over
        game_state = GameStatus([[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)
        self.assertEqual(game_state.is_terminal(), (False, None))

        # Test a game that is over with a draw
        game_state = GameStatus([[1, -1, 1], [-1, 1, -1], [1, -1, 1]], False)
        self.assertEqual(game_state.is_terminal(), (True, 'Human'))

        # Test a game that is over with a win for the human player
        game_state = GameStatus([[1, 1, 1], [0, -1, 0], [0, 0, -1]], False)
        self.assertEqual(game_state.is_terminal(), (True, 'Human'))

        # Test a game that is over with a win for the AI player
        game_state = GameStatus([[-1, -1, -1], [0, 1, 0], [0, 0, 1]], True)
        self.assertEqual(game_state.is_terminal(), (True, 'AI'))

    def test_get_moves(self):
        # Test a game with all cells empty
        game_state = GameStatus([[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)
        self.assertEqual(game_state.get_moves(), [(i, j) for i in range(3) for j in range(3)])

        # Test a game with some cells filled
        game_state = GameStatus([[1, 0, -1], [0, 1, 0], [-1, 0, 1]], True)
        self.assertEqual(game_state.get_moves(), [(0, 1), (1, 0), (1, 2), (2, 1)])

    def test_get_scores(self):
        # Test a game with no winner
        game_state = GameStatus([[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)
        self.assertEqual(game_state.get_scores(), 0)

        # Test a game with a draw
        game_state = GameStatus([[1, -1, 1], [-1, 1, -1], [1, -1, 1]], False)
        self.assertEqual(game_state.get_scores(), 2)

        # Test a game with a win for the human player
        game_state = GameStatus([[1, 1, 1], [0, -1, 0], [0, 0, -1]], False)
        self.assertEqual(game_state.get_scores(), 1)

        # Test a game with a win for the AI player
        game_state = GameStatus([[-1, -1, -1], [0, 1, 0], [0, 0, 1]], True)
        self.assertEqual(game_state.get_scores(), -1)

    def test_get_new_state(self):
        # Test a game with a move for the human player
        game_state = GameStatus([[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)
        new_state = game_state.get_new_state((0, 0))
        self.assertEqual(new_state.board_state, [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertEqual(game_state.turn_O, False)


if __name__ == '__main__':
    unittest.main()