import unittest
from CheckersGame import Checkers, Player, OutofTurn, InvalidSquare, InvalidPlayer


class TestCheckersGame(unittest.TestCase):
    """
    Contains unit tests for Checkers game
    """
    def test_regular_piece_move(self):
        """
        Testing moves for regular pieces

        Rubric conditions being tested:
            Updates the board correctly - Line 22 and Line 32
        """
        game = Checkers()

        game.create_player("Adam", "White")
        game.create_player("Lucy", "Black")

        game.play_game("Lucy", (5, 6), (4, 7))
        self.assertEqual(game._board, [[None,'White',None,'White',None,'White',None,'White'],
                       ['White',None,'White',None,'White',None,'White',None],
                       [None,'White',None,'White',None,'White',None,'White'],
                       [None,None,None,None,None,None,None,None],
                       [None,None,None,None,None,None,None,"Black"],
                       ['Black',None,'Black',None,'Black',None,None,None],
                       [None,'Black',None,'Black',None,'Black',None,'Black'],
                       ['Black',None,'Black',None,'Black',None,'Black',None]])

        game.play_game("Adam", (2, 1), (3, 0))
        self.assertEqual(game._board, [[None,'White',None,'White',None,'White',None,'White'],
                                       ['White',None,'White',None,'White',None,'White',None],
                                       [None,None,None,'White',None,'White',None,'White'],
                                       ["White",None,None,None,None,None,None,None],
                                       [None,None,None,None,None,None,None,"Black"],
                                       ['Black',None,'Black',None,'Black',None,None,None],
                                       [None,'Black',None,'Black',None,'Black',None,'Black'],
                                       ['Black',None,'Black',None,'Black',None,'Black',None]])

    def test_regular_piece_captures(self):
        """
        Test that play_game returns correct number of captured pieces

        Rubric conditions being tested:
            play_game returns pieces being captured - Line 57 and 59
        """
        game = Checkers()
        game.create_player("Adam", "White")
        game.create_player("Lucy", "Black")

        game.play_game("Lucy", (5, 6), (4, 7))
        game.play_game("Adam", (2, 1), (3, 0))
        game.play_game("Lucy", (4, 7), (3, 6))
        game.play_game("Adam", (2, 5), (4, 7))
        game.play_game("Lucy", (5, 2), (4, 3))
        self.assertEqual(game.play_game("Adam", (3, 0), (4, 1)), 0)
        game.play_game("Lucy", (5, 0), (3, 2))
        self.assertEqual(game.play_game("Adam", (2, 3), (4, 1)), 1)

    def test_regular_piece_double_jump(self):
        """
        Test if there is a double jump option that the turn does not change

        Rubric conditions being tested:
            play_game returns pieces being captured - Line 76 and 77
            out of turn - player A makes a capture move adn then tries to move a
                different piece that is non-capture - Line 86
        """
        game = Checkers()
        game.create_player("Adam", "White")
        game.create_player("Lucy", "Black")

        game.play_game("Lucy", (5, 6), (4, 7))
        game.play_game("Adam", (2, 1), (3, 0))
        self.assertEqual(game.play_game("Lucy", (4, 7), (3, 6)), 0)
        self.assertEqual(game.play_game("Adam", (2, 5), (4, 7)), 1)
        game.play_game("Lucy", (5, 2), (4, 3))
        game.play_game("Adam", (3, 0), (4, 1))
        game.play_game("Lucy", (5, 0), (3, 2))
        game.play_game("Adam", (2, 3), (4, 1))
        game.play_game("Lucy", (4, 3), (3, 4))
        game.play_game("Adam", (1, 4), (2, 3))
        game.play_game("Lucy", (6, 7), (5, 6))
        game.play_game("Adam", (2, 3), (4, 5))
        with self.assertRaises(OutofTurn):
            game.play_game("Adam", (4, 1), (5, 2))

    def test_switch_to_king(self):
        """
        Rubric conditions being tested:
            Regular piece switch to King piece - Line 121
            updated king count - Line 122
            get_checker_detail returns right info - Line 121
            get_checker_details - raises Invalid Square if square not on board - Line 123
        """
        game = Checkers()
        player_1 = game.create_player("Adam", "White")
        game.create_player("Lucy", "Black")

        game.play_game("Lucy", (5, 6), (4, 7))
        game.play_game("Adam", (2, 1), (3, 0))
        game.play_game("Lucy", (4, 7), (3, 6))
        game.play_game("Adam", (2, 5), (4, 7))
        game.play_game("Lucy", (5, 2), (4, 3))
        game.play_game("Adam", (3, 0), (4, 1))
        game.play_game("Lucy", (5, 0), (3, 2))
        game.play_game("Adam", (2, 3), (4, 1))
        game.play_game("Lucy", (4, 3), (3, 4))
        game.play_game("Adam", (1, 4), (2, 3))
        game.play_game("Lucy", (6, 7), (5, 6))
        game.play_game("Adam", (2, 3), (4, 5))
        game.play_game("Adam", (4, 5), (6, 7))

        game.play_game("Lucy", (5, 4), (4, 5))
        game.play_game("Adam", (1, 2), (2, 3))
        game.play_game("Lucy", (6, 5), (5, 6))
        game.play_game("Adam", (4, 7), (6, 5))
        game.play_game("Lucy", (7, 6), (5, 4))
        game.play_game("Adam", (6, 7), (7, 6))
        self.assertEqual(game.get_checker_details((7, 6)), "White_king")
        self.assertEqual(player_1.get_king_count(), 1)
        with self.assertRaises(InvalidSquare):
            game.get_checker_details((8, 6))


#### test to walk through a whole game, split up to test at various checkpoint.

    def test_out_of_turn(self):
        """
        Rubric conditions being tested:
            Out of turn - non capture move and player tries to move again - Line 140
        """
        whole_game = Checkers()
        Player1 = whole_game.create_player("Adam", "White")
        Player2 = whole_game.create_player("Lucy", "Black")

        whole_game.play_game("Lucy", (5, 4), (4, 3))
        # Not your turn
        with self.assertRaises(OutofTurn):
            whole_game.play_game("Lucy", (5, 6), (4, 7))

        whole_game.play_game("Adam", (2, 5), (3, 6))
        whole_game.play_game("Lucy", (4, 3), (3, 4))
        self.assertEqual(whole_game.game_winner(), "Game has not ended")
        whole_game.play_game("Adam", (2, 3), (4, 5))

    def test_exceptions_1(self):
        """
        Testing calling game_winner function
        Testing if destination square is not on the board
        Testing what happens if player tried to move a regular piece more than one spot
        Testing what will happen if Player A plays a capturing move and then Player A tries to
            play a non-capturing move

        Rubric conditions being tested:
            in play_game - raises Invalid square if the square does not exist - Lines 173, Line 175
            in play_game - raises Invalid square if player tries to move opponent's square - Line 177
            out of turn - Player A plays a capturing move and then Player A
                tries to play a non-capturing move with same piece - Line 192
        """
        whole_game = Checkers()
        Player1 = whole_game.create_player("Adam", "White")
        Player2 = whole_game.create_player("Lucy", "Black")

        whole_game.play_game("Lucy", (5, 4), (4, 3))
        whole_game.play_game("Adam", (2, 5), (3, 6))
        whole_game.play_game("Lucy", (4, 3), (3, 4))
        self.assertEqual(whole_game.game_winner(), "Game has not ended")
        whole_game.play_game("Adam", (2, 3), (4, 5))
        whole_game.play_game("Lucy", (5, 6), (3, 4))
        whole_game.play_game("Adam", (2, 1), (3, 2))
        with self.assertRaises(InvalidSquare):
            whole_game.play_game("Lucy", (5, 0), (4, 8))
        with self.assertRaises(InvalidSquare):
            whole_game.play_game("Lucy", (5, 0), (-1, 1))
        with self.assertRaises(InvalidSquare):
            whole_game.play_game("Lucy", (3, 2), (5, 0))
        with self.assertRaises(InvalidSquare):
            whole_game.play_game("Lucy", (4, 1), (3, 2))

        whole_game.play_game("Lucy", (5, 0), (4, 1))
        whole_game.play_game("Adam", (3, 2), (5, 0))
        whole_game.play_game("Lucy", (5, 2), (4, 1))
        whole_game.play_game("Adam", (1, 4), (2, 3))
        whole_game.play_game("Lucy", (4, 1), (3, 0))
        # invalid move
        # with self.assertRaises(InvalidSquare):
        #     whole_game.play_game("Adam", (2, 3), (5, 6))
        whole_game.play_game("Adam", (2, 3), (4, 5))
        # out of turn
        with self.assertRaises(OutofTurn):
            whole_game.play_game("Adam", (4, 5), (5, 6))

    def testing_exceptions_2(self):
        """
        Testing invalid player
        Testing Regular piece turning into King piece then checking King count
        Testing king capture move
        testing tripple king capture behavior and updated board
        Testing capturing a king ad updating the king pieces count
        Testing King double jump
        Testing game_winner()

        Rubric conditions being tested:
            InvalidPlayer Exception - Line 221
            play_game returns pieces being captured for King move - Line 248
            play_game returns pieces being captures for _triple_king - Line 277
            king player turning into triple king player - Line 261
            check updated king and triple king count - Lines 244, 245, 262-265
            get_capture_pieces_count - Line 249, 250, 278, 279, 304, 305
            game_winner returns "Game not done" when no winner - Line 296
            game_winner return winner when game is over - Line 316
        """
        whole_game = Checkers()
        Player1 = whole_game.create_player("Adam", "White")
        Player2 = whole_game.create_player("Lucy", "Black")

        whole_game.play_game("Lucy", (5, 4), (4, 3))
        whole_game.play_game("Adam", (2, 5), (3, 6))
        with self.assertRaises(InvalidPlayer):
            whole_game.play_game("Adriaan", (2, 5), (3, 6))
        whole_game.play_game("Lucy", (4, 3), (3, 4))
        whole_game.play_game("Adam", (2, 3), (4, 5))
        whole_game.play_game("Lucy", (5, 6), (3, 4))
        whole_game.play_game("Adam", (2, 1), (3, 2))
        whole_game.play_game("Lucy", (5, 0), (4, 1))
        whole_game.play_game("Adam", (3, 2), (5, 0))
        whole_game.play_game("Lucy", (5, 2), (4, 1))
        whole_game.play_game("Adam", (1, 4), (2, 3))
        whole_game.play_game("Lucy", (4, 1), (3, 0))
        whole_game.play_game("Adam", (2, 3), (4, 5))
        whole_game.play_game("Lucy", (6, 5), (5, 6))
        whole_game.play_game("Adam", (1, 2), (2, 3))
        whole_game.play_game("Lucy", (6, 3), (5, 4))
        whole_game.play_game("Adam", (1, 0), (2, 1))
        whole_game.play_game("Lucy", (5, 6), (3, 4))
        # # should be invalid move        ##NOT WORKING AS EXPECTED
        whole_game.play_game("Lucy", (3, 4), (1, 2))
        whole_game.play_game("Adam", (0, 3), (1, 4))

        whole_game.play_game("Lucy", (1, 2), (0, 3))
        self.assertEqual(whole_game._board[0][3], "Black_king")
        self.assertEqual(Player1.get_king_count(), 0)
        self.assertEqual(Player2.get_king_count(), 1)

        whole_game.play_game("Adam", (1, 4), (2, 3))
        self.assertEqual(whole_game.play_game("Lucy", (0, 3), (4, 7)), 1) # testing king capture move
        self.assertEqual(Player1.get_captured_pieces_count(), 3)
        self.assertEqual(Player2.get_captured_pieces_count(), 4)

        whole_game.play_game("Adam", (2, 3), (3, 4))
        whole_game.play_game("Lucy", (4, 7), (5, 6))
        whole_game.play_game("Adam", (0, 5), (1, 4))
        whole_game.play_game("Lucy", (7, 4), (6, 3))
        whole_game.play_game("Adam", (1, 6), (2, 5))
        whole_game.play_game("Lucy", (5, 6), (6, 5))
        whole_game.play_game("Adam", (3, 4), (4, 3))

        whole_game.play_game("Lucy", (6, 5), (7, 4))
        self.assertEqual(whole_game._board[7][4], "Black_Triple_King")
        self.assertEqual(Player1.get_king_count(), 0)
        self.assertEqual(Player2.get_king_count(), 0)
        self.assertEqual(Player1.get_triple_king_count(), 0)
        self.assertEqual(Player2.get_triple_king_count(), 1)

        whole_game.play_game("Adam", (1, 4), (2, 3))
        whole_game.play_game("Lucy", (3, 0), (1, 2))
        whole_game.play_game("Adam", (2, 3), (3, 2))
        whole_game.play_game("Lucy", (1, 2), (0, 3))
        self.assertEqual(Player1.get_king_count(), 0)
        self.assertEqual(Player2.get_king_count(), 1)
        whole_game.play_game("Adam", (4, 3), (5, 2))
        whole_game.play_game("Lucy", (0, 3), (3, 6))
        whole_game.play_game("Adam", (3, 2), (4, 1))

        self.assertEqual(whole_game.play_game("Lucy", (7, 4), (3, 0)), 2)
        self.assertEqual(Player1.get_captured_pieces_count(), 3)
        self.assertEqual(Player2.get_captured_pieces_count(), 8)
        self.assertEqual(whole_game._board, [[None, 'White', None, None, None, None, None, 'White'],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, 'White'],
                            ['Black_Triple_King', None, None, None, None, None, 'Black_king', None],
                            [None, None, None, None, None, None, None, None],
                            ['White', None, None, None, 'Black', None, None, None],
                            [None, 'Black', None, 'Black', None, None, None, 'Black'],
                            ['Black', None, 'Black', None, None, None, 'Black', None]])

        whole_game.play_game("Adam", (2, 7), (4, 5))
        self.assertEqual(Player2.get_king_count(), 0)
        self.assertEqual(Player2.get_triple_king_count(), 1)
        whole_game.play_game("Lucy", (5, 4), (3, 6))
        whole_game.play_game("Adam", (0, 1), (1, 2))
        whole_game.play_game("Lucy", (6, 1), (5, 2))
        whole_game.play_game("Adam", (5, 0), (6, 1))
        self.assertEqual(whole_game.game_winner(), "Game has not ended")
        whole_game.play_game("Lucy", (7, 2), (5, 0))
        whole_game.play_game("Adam", (0, 7), (1, 6))
        whole_game.play_game("Lucy", (3, 6), (2, 7))
        whole_game.play_game("Adam", (1, 6), (2, 5))

        whole_game.play_game("Lucy", (3, 0), (0, 3))
        whole_game.play_game("Lucy", (0, 3), (3, 6))  # double jump
        self.assertEqual(Player1.get_captured_pieces_count(), 4)
        self.assertEqual(Player2.get_captured_pieces_count(), 12)

        self.assertEqual(whole_game._board, [[None, None, None, None, None, None, None, None],
                                    [None, None, None, None, None, None, None, None],
                                    [None, None, None, None, None, None, None, 'Black'],
                                    [None, None, None, None, None, None, 'Black_Triple_King', None],
                                    [None, None, None, None, None, None, None, None],
                                    ['Black', None, 'Black', None, None, None, None, None],
                                    [None, None, None, 'Black', None, None, None, 'Black'],
                                    ['Black', None, None, None, None, None, 'Black', None]])

        self.assertEqual(whole_game.game_winner(), "Lucy")  # should be Lucy


if __name__ == '__main__':
    unittest.main(exit=False)