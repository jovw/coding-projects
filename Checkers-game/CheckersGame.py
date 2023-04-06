class OutofTurn(Exception):
    """
    Will be raised when player is playing out of turn
    Conditions:
        If Player A is makes a non-capturing move and then player A tries to play again
        If player A makes a capture move and makes another move, but it is not the same piece
        If player A makes a capture move, plays the same piece again, but it is not a capture move
    """
    pass


class InvalidSquare(Exception):
    """
    Will be raised if the player is trying to move a piece that is not theirs
    If a player is trying to move apiece that does not exist
    If a player tries to play a square that is not on the board
    """
    pass


class InvalidPlayer(Exception):
    """
    Will be raised if the player name does not exist
    """
    pass


class Checkers:
    """
    Initialized a checkers object that represents tha game as it is being played.
    The class contains information about the board and the players.
    self._board initializes the board when checkers object is created
    """
    def __init__(self):
        """
        Initialized data members for checkers class
        All data members are private
        """
        self._board = [[None, 'White', None, 'White', None, 'White', None, 'White'],
                       ['White', None, 'White', None, 'White', None, 'White', None],
                       [None, 'White', None, 'White', None, 'White', None, 'White'],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       ['Black', None, 'Black', None, 'Black', None, 'Black', None],
                       [None, 'Black', None, 'Black', None, 'Black', None, 'Black'],
                       ['Black', None, 'Black', None, 'Black', None, 'Black', None]]
        self._player = {}
        self._prev_turn_played_by = None
        self._prev_piece_played = None
        self._was_prev_capture = False

    def get_board(self):
        """
        Description: returns the board
        """
        return self._board

    def create_player(self, player_name, piece_color):
        """
        Parameters: player_name and piece_color
        Description: takes player name and piece color. Verifies that the piece color is either Black or White
            Then creates a player object. The objects are stored in the _player dictionary associated with the player
            name.
        Other classes: Player class - to initialize the player
        returns: Player object that has been created
        """
        if piece_color not in ["White", "Black"]:
            raise ValueError("Piece color has to be Black or White")
        player = Player(player_name, piece_color)
        self._player[player_name] = player
        return player

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Parameters: player_name, starting_square_location, destination_square_location
        Description: Square_locations are in tuple forms, (row, col). This method will verify the move and then update
            the board and player information accordingly. A regular, king and triple king piece will be verified
            against their own movement restrictions.

            The following exceptions will be raised:
                OutofTurn: When player tries to move a piece when it is not their turn
                InvalidSquare: If player does not own the piece in square_location, or if square location does not
                    exist on the board.
                InvalidPlayer: If the player_name is not valid

            If the destination piece reaches the end of opponent's side it is promoted as a king on the board.
            If the piece crosses back to its original side it becomes a triple king.
        Other Classes: Player class to updated player information as the game progresses
        Return: number of pieces captured in that round, if none then return 0
        """

        ### Check if the players is valid ###
        if player_name not in self._player.keys():
            raise InvalidPlayer("Player does not exist")

        ### Check that square is on board ###
        self.get_checker_details(destination_square_location)
        self.get_checker_details(starting_square_location)

        ### Set up variables - opponent_player (object), piece, current_player (object), player_piece ###
        opponent_player = None
        for key, value in self._player.items():
            if key != player_name:
                opponent_player = value
        piece = self.get_checker_details(starting_square_location)  # this is the piece at starting location
        current_player = self._player[player_name]
        player_piece = current_player.get_piece_color()

        ### confirm that it is the players piece ###
        if piece is None or not piece.startswith(player_piece) or (piece not in player_piece and player_piece + '_king'
                                                                   not in piece and player_piece + '_Triple_King'
                                                                   not in piece):
            raise InvalidSquare("There is not piece to be played")

        ### Check what piece is being played ###
        ################# TRIPLE KING ##############################
        if piece.endswith("_Triple_King"):
            capture_move = False
            captured_piece_count = None

            # Check if it is a capture move #
            if abs(starting_square_location[0] - destination_square_location[0]) > 1:
                capture_move = True
                captured_piece_count = self.check_king_and_triple_king_piece(current_player,
                                                                             opponent_player, starting_square_location,
                                                                             destination_square_location)

                # updated board #
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                self._board[destination_square_location[0]][destination_square_location[1]] = piece

                # updates player's captured pieces #
                for capture in range(captured_piece_count):
                    current_player.increment_captured_pieces_count()

            # Check for out of turn #
            self.check_if_out_of_turn(player_name, capture_move, starting_square_location, destination_square_location)

            if capture_move is True:
                self._was_prev_capture = True

            # What to do if not capture move and play_game return#
            if not capture_move:
                self._was_prev_capture = False
                # update board #
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                self._board[destination_square_location[0]][destination_square_location[1]] = piece
                return 0
            else:
                return captured_piece_count

        ################# KING ##############################
        elif piece.endswith("_king"):
            capture_move = False

            # check if capture move #
            if abs(starting_square_location[0] - destination_square_location[0]) > 1:
                capture_move = True
                self.check_king_and_triple_king_piece(current_player, opponent_player, starting_square_location,
                                                      destination_square_location)
                # updates board #
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                self._board[destination_square_location[0]][destination_square_location[1]] = piece

                # updates player's captured pieces #
                current_player.increment_captured_pieces_count()

            # check for out of turn #
            self.check_if_out_of_turn(player_name, capture_move, starting_square_location, destination_square_location)

            if capture_move is True:
                self._was_prev_capture = True

            # what to do if not capture move #
            if not capture_move:
                self._was_prev_capture = False
                # confirm move against king rules #
                # if non capture move, can only move one spot, and only diagonally #
                if abs(starting_square_location[0] - destination_square_location[0]) != 1 \
                        and starting_square_location[0] == destination_square_location[0] \
                        and starting_square_location[1] == destination_square_location[1]:
                    raise InvalidSquare("This is an invalid move")

                # updated board #
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                self._board[destination_square_location[0]][destination_square_location[1]] = piece

            # Switching over to a triple king #
            if destination_square_location[0] == 7 or destination_square_location[0] == 0:
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                current_player.decrement_king_count()
                current_player.increment_triple_king_count()
                if destination_square_location[0] == 7 and piece == "Black_king":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "Black_Triple_King"
                elif destination_square_location[0] == 0 and piece == "White_king":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "White_Triple_King"

            # return play_game #
            if not capture_move:
                return 0
            else:
                return 1

        ################# REGULAR ##############################

        else:
            capture_move = False

            # check if a capture move #
            if abs(starting_square_location[0] - destination_square_location[0]) == 2:
                capture_move = True
                self.check_regular_piece(current_player, opponent_player, starting_square_location,
                                         destination_square_location)

                # update board #
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                self._board[destination_square_location[0]][destination_square_location[1]] = piece

                # update player's captured pieces #
                current_player.increment_captured_pieces_count()

            # check if out of turn #
            self.check_if_out_of_turn(player_name, capture_move, starting_square_location, destination_square_location)

            if capture_move is True:
                self._was_prev_capture = True

            # what to do if not captured move #
            if not capture_move:
                self._was_prev_capture = False
                # check moves against regular piece rules #
                start_row = starting_square_location[0]
                start_col = starting_square_location[1]
                end_row = destination_square_location[0]
                end_col = destination_square_location[1]
                # black piece rules #
                # can only move one spot, diagonally and forward #
                if piece == "Black":
                    if (end_row - start_row != -1 and end_row - start_row > -2) or start_row == end_row \
                            or start_col == end_col:
                        raise InvalidSquare("That is an invalid move")
                    else:
                        # update board #
                        self._board[starting_square_location[0]][starting_square_location[1]] = None
                        self._board[destination_square_location[0]][destination_square_location[1]] = piece
                # white piece rules #
                # can only move one spot, diagonally and forward #
                elif piece == "White":
                    if (end_row - start_row != 1 and end_row - start_row > 2) or start_row == end_row \
                            or start_col == end_col:
                        raise InvalidSquare("That is an invalid move")
                    else:
                        # update board #
                        self._board[starting_square_location[0]][starting_square_location[1]] = None
                        self._board[destination_square_location[0]][destination_square_location[1]] = piece

            # how to switch over to a king piece #
            if destination_square_location[0] == 7 or destination_square_location[0] == 0:
                self._board[starting_square_location[0]][starting_square_location[1]] = None
                current_player.increment_king_count()
                if destination_square_location[0] == 7 and piece == "White":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "White_king"
                elif destination_square_location[0] == 0 and piece == "Black":
                    self._board[destination_square_location[0]][destination_square_location[1]] = "Black_king"

            # return play_game #
            if not capture_move:
                return 0
            else:
                return 1

    def check_if_out_of_turn(self, player_name, capture_move,starting_square_location, destination_square_location):
        """
        Parameters: player_name, capture_move (True/False), destination_square_location
        Description: Checks out of turn conditions. If not out of turn, update the prev_player and prev_piece_player
            data members. If out of turn, raise OutofTurn
        Return: True if not out of turn
        """

        if self._prev_turn_played_by == player_name:
            if capture_move is False:
                raise OutofTurn("It is not your turn")
            if self._was_prev_capture is False:
                raise OutofTurn("It is not your turn")
            if starting_square_location != self._prev_piece_played:
                raise OutofTurn("It is not your turn")
        # if self._prev_turn_played_by == player_name and capture_move is False:
        #     # and starting_square_location == self._prev_piece_played:
        #     raise OutofTurn("It is not your turn")
        # if self._prev_turn_played_by == player_name and self._was_prev_capture is False:
        #     raise OutofTurn("It is not your turn")
        # if self._prev_turn_played_by == player_name and starting_square_location != self._prev_piece_played:
        #     raise OutofTurn("It is not your turn")
        else:
            self._prev_turn_played_by = player_name
            self._prev_piece_played = destination_square_location
            return True

    def check_regular_piece(self, current_player, opponent_player, start, end):
        """
        Parameter: current_player, opponent_player, start (square tuple), end (square tuple)
        Description: Checks if the move is a capture move. If not then the InvalidSquare exception is raised.
        Update captured piece on the board to None
            If captured move is either _king or _triple_king update the opponent players _king
            and triple_king count accordingly.
        Other Classes: Player class to update _king and _triple_king count info
        Return: If a capture move then return True
        """
        # get capture piece location info and current player piece info #
        row = (start[0] + end[0]) // 2
        col = (start[1] + end[1]) // 2
        player_piece = current_player.get_piece_color()
        captured_piece = self._board[row][col]
        # check if capture piece is not none and that it is not the player's own piece #
        if self._board[row][col] is None or self._board[row][col].startswith(player_piece):
            raise InvalidSquare("This is an invalid move")
        # update board #
        self._board[row][col] = None
        # update opponent players _king and _triple_king count if needed #
        if captured_piece.endswith("_king"):
            opponent_player.decrement_king_count()
        if captured_piece.endswith("_Triple_King"):
            opponent_player.decrement_triple_king_count()
        return True

    def check_king_and_triple_king_piece(self, current_player, opponent_player, start, end, captured_piece_count=0):
        """
        Parameters: current_player, opponent_player, start, end, captured_pieces_count
        Description: Check if move is a captured piece move. If not raise InvalidSquare exception.
            If it is a capture move:

        Other Classes: Player class to get player information and updated player information
        Return: number of captured pieces
        """
        player_piece = current_player.get_piece_color()
        opponent_piece = "White" if player_piece.startswith("Black") else "Black"
        # Base case to stop recursion #
        if end == start and captured_piece_count != 0:
            return captured_piece_count
        elif end == start and captured_piece_count == 0:
            raise InvalidSquare("This is an invalid move")

        # check row to see if player is moving down the board #
        elif end[0] - start[0] > 0:
            # check col to see if player is moving right on the board #
            if end[1] - start[1] > 0:
                # if opponent piece, update board accordingly #
                if self._board[end[0] - 1][end[1] - 1] == opponent_piece:
                    # update opponent _king and _triple_king count #
                    if self._board[end[0] - 1][end[1] - 1].endswith("_king"):
                        opponent_player.decrement_king_count()
                    if self._board[end[0] - 1][end[1] - 1].endswith("_Triple_King"):
                        opponent_player.decrement_triple_king_count()
                    self._board[end[0] - 1][end[1] - 1] = None
                    # move on to next square #
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] - 1, end[1] - 1), captured_piece_count + 1)
                # if not opponent_piece, nothing to update #
                else:
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] - 1, end[1] - 1), captured_piece_count)
            # check col to see if player ius moving left on board #
            elif end[1] - start[1] < 0:
                # if opponent piece, update board accordingly #
                if self._board[end[0] - 1][end[1] + 1] == opponent_piece:
                    # update opponent _king and _triple_king count #
                    if self._board[end[0] - 1][end[1] + 1].endswith("_king"):
                        opponent_player.decrement_king_count()
                    if self._board[end[0] - 1][end[1] + 1].endswith("_Triple_King"):
                        opponent_player.decrement_triple_king_count()
                    self._board[end[0] - 1][end[1] + 1] = None
                    # move on to next square #
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] - 1, end[1] + 1), captured_piece_count + 1)
                # if not opponent_piece, nothing to update #
                else:
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] - 1, end[1] + 1), captured_piece_count)
        # if the player is moving up on the board #
        else:
            # check col to see if player is moving left on board #
            if end[1] - start[1] < 0:
                # if opponent piece, update board accordingly #
                if self._board[end[0] + 1][end[1] + 1] == opponent_piece:
                    # update opponent _king and _triple_king count #
                    if self._board[end[0] + 1][end[1] + 1].endswith("_king"):
                        opponent_player.decrement_king_count()
                    if self._board[end[0] + 1][end[1] + 1].endswith("_Triple_King"):
                        opponent_player.decrement_triple_king_count()
                    self._board[end[0] + 1][end[1] + 1] = None
                    # move on to next square #
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] + 1, end[1] + 1), captured_piece_count + 1)
                # if not opponent_piece, nothing to update #
                else:
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] + 1, end[1] + 1), captured_piece_count)
            # check col to see if player is moving right on board #
            elif end[1] - start[1] > 0:
                # if opponent piece, update board accordingly #
                if self._board[end[0] + 1][end[1] - 1] == opponent_piece:
                    # update opponent _king and _triple_king count #
                    if self._board[end[0] + 1][end[1] - 1].endswith("_king"):
                        opponent_player.decrement_king_count()
                    if self._board[end[0] + 1][end[1] - 1].endswith("_Triple_King"):
                        opponent_player.decrement_triple_king_count()
                    self._board[end[0] + 1][end[1] - 1] = None
                    # move on to next square #
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] + 1, end[1] - 1), captured_piece_count + 1)
                # if not opponent_piece, nothing to update #
                else:
                    return self.check_king_and_triple_king_piece(current_player, opponent_player, start,
                                                                 (end[0] + 1, end[1] - 1), captured_piece_count)

    def get_checker_details(self, square_location):
        """
        Parameters: square_location
        Description: takes parameter and returns the checker details present in the square_location
            InvalidSquare Exception if the location is not on the board
        Return: None if no piece is present on the location. If there is a piece it will return that piece.
            Black, White, Black_king, White_king, Black_Triple_King or White_Triple_King
        """
        row = square_location[0]
        col = square_location[1]

        if 0 > row or row > 7 or 0 > col or col > 7:
            raise InvalidSquare("Square not on the board")
        if self._board[row][col] is not None:
            return self._board[row][col]
        return None

    def print_board(self):
        """
        Prints out the board
        """
        for row in self._board:
            print(row)
        # print(self._board)

    def game_winner(self):
        """
        Description: Checks if either player has captured 12 pieces.
        Return: If no winner yet return "Game has not ended" else return winner name
        """
        for key, value in self._player.items():
            player = key
            if value.get_captured_pieces_count() == 12:
                return player
        return "Game has not ended"


class Player:
    """
    Player object represents the player in the game
    Contains information about the player. Details get updated as the game is being played.
    """
    def __init__(self, player_name, piece_color):
        """
        Initialized data members for checkers class
        All data members are private
        """
        self._player_name = player_name
        self._piece_color = piece_color
        self._captured_pieces_count = 0
        self._king_pieces_count = 0
        self._triple_king_count = 0

    def get_name(self):
        """
        Will return the name of the player
        """
        return self._player_name

    def get_piece_color(self):
        """
        Will return the piece color for player
        """
        return self._piece_color

    def get_king_count(self):
        """
        will return the amount of king pieces the player has
        """
        return self._king_pieces_count

    def get_triple_king_count(self):
        """
        will return the amount of triple king pieces the player has
        """
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """
        Will return the amount of opponent pieces the player has captured
        """
        return self._captured_pieces_count

    def increment_captured_pieces_count(self):
        """
        Will increase the player's capture pieces
        """
        self._captured_pieces_count += 1

    def increment_king_count(self):
        """
        Increase king count by 1
        """
        self._king_pieces_count += 1

    def decrement_king_count(self):
        """
        decreases king count by 1
        """
        self._king_pieces_count -= 1

    def increment_triple_king_count(self):
        """
        increases triple king count by 1
        """
        self._triple_king_count += 1

    def decrement_triple_king_count(self):
        """
        decreases triple king count by 1
        """
        self._triple_king_count -= 1


def main():
    whole_game = Checkers()
    Player1 = whole_game.create_player("Adam", "White")
    Player2 = whole_game.create_player("Lucy", "Black")

#
    whole_game.play_game("Lucy", (5, 4), (4, 3))
    whole_game.play_game("Adam", (2, 5), (3, 6))
#
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
    # # # should be invalid move        ##NOT WORKING AS EXPECTED
    whole_game.play_game("Lucy", (3, 4), (1, 2))
    whole_game.play_game("Adam", (0, 3), (1, 4))
    #
    whole_game.play_game("Lucy", (1, 2), (0, 3))
    whole_game.play_game("Adam", (1, 4), (2, 3))
    whole_game.play_game("Lucy", (0, 3), (4, 7))  # testing king capture move
#
    whole_game.play_game("Adam", (2, 3), (3, 4))
    whole_game.play_game("Lucy", (4, 7), (5, 6))
    whole_game.play_game("Adam", (0, 5), (1, 4))
    whole_game.play_game("Lucy", (7, 4), (6, 3))
    whole_game.play_game("Adam", (1, 6), (2, 5))
    whole_game.play_game("Lucy", (5, 6), (6, 5))
    whole_game.play_game("Adam", (3, 4), (4, 3))
#
    whole_game.play_game("Lucy", (6, 5), (7, 4))
    whole_game.play_game("Adam", (1, 4), (2, 3))
    whole_game.play_game("Lucy", (3, 0), (1, 2))
    whole_game.play_game("Adam", (2, 3), (3, 2))
    whole_game.play_game("Lucy", (1, 2), (0, 3))
    whole_game.play_game("Adam", (4, 3), (5, 2))
    whole_game.play_game("Lucy", (0, 3), (3, 6))
    whole_game.play_game("Adam", (3, 2), (4, 1))

    whole_game.play_game("Lucy", (7, 4), (3, 0))
#
    whole_game.print_board()
    print('Adam has', Player1.get_captured_pieces_count(), 'black pieces')
    print('Lucy has', Player2.get_captured_pieces_count(), 'white pieces')
    print(whole_game.game_winner())  # should be Lucy
#
#
if __name__ == '__main__':
    main()