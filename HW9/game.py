import random
import time
# legal moves in this order: right, left, up, down, NNE, NNW, SSE, SSW
legal_moves = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)] 


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    
    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def is_drop_phase(self, state):
        total_pieces = sum(row.count('b') + row.count('r') for row in state)
        return total_pieces < 8
    
    def succ(self, state):
        
        succ_states = []
                
        # drop phase
        if self.is_drop_phase(state) is False:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        new_state = [row[:] for row in state] # get deep copy of state
                        new_state[row][col] = self.my_piece # drop correct piece in this open spot
                        succ_states.append(new_state)
        # open play
        else:
            for row in range(5):
                for col in range(5):
                    for dr,dc in legal_moves:
                        new_row, new_col = row + dr, col + dc # test all possible moves
                        # test if valid move
                        # i.e. in bounds and no piece currently
                        if 0 <= new_row <= 4 and 0 <= new_col <= 4 and state[new_row][new_col] == ' ':
                            new_state = [row[:] for row in state] # get deep copy
                            new_state[new_row][new_col] = self.my_piece
                            new_state[row][col] = ' '
                            succ_states.append(new_state)
        return succ_states
    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        # if self.is_drop_phase(state):
        #     best_move = (random.randint(0,4), random.randint(0,4))
        # else:
        best_score = float('-inf')
        depth = 1
        succ_states = self.succ(state)
        for succ_state in succ_states:
            score = self.max_value(succ_state, depth -1)
            if score > best_score:
                best_score = score
                best_move = self.get_move_from_states(state, succ_state)
        return best_move
    
    # def get_move_from_states(self, old_state, new_state):
    #     for row in range(5):
    #         for col in range(5):
    #             if old_state[row][col] == ' ' and new_state[row][col] == self.my_piece:
    #                 return [(row, col)]  # Tuple of the location to place the piece

    #     # If no move found (should not reach here)
    #     return None
    
    def get_move_from_states(self, old_state, new_state):
        drop_phase = self.is_drop_phase(old_state)

        for row in range(5):
            for col in range(5):
                if old_state[row][col] == ' ' and new_state[row][col] == self.my_piece:
                    destination = (row, col)
                    if not drop_phase and sum(1 for row in old_state for cell in row if cell == self.my_piece) >= 4:
                        # Relocation move: find the source location of the piece
                        for r in range(5):
                            for c in range(5):
                                if old_state[r][c] == self.my_piece and new_state[r][c] == ' ':
                                    source = (r, c)
                                    return (destination, source)  # Return source and destination as a tuple
                    # Placement move: return only the destination location
                    return (destination,)

        # If no move found, return a tuple indicating it's a drop move
        return ((0, 0),)  # Ensure move is returned as a tuple

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    
                    return 1 if state[row][col] == self.my_piece else -1
                             
        # TODO: check / diagonal wins
        for row in range(3):
            for col in range(2,5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    
                    return 1 if state[row][col] == self.my_piece else -1
                
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row+1][col] == state[row+1][col+1]:
                    
                    return 1 if state[row][col] == self.my_piece else -1
        #print("!")
        return 0 # no winner yet
    
    def heuristic_game_value(self, state):
        succ_states = self.succ(state)
        if(self.game_value(state) != 0 or i == ' ' for i in enumerate(state)):
            return self.game_value(state)
        
        total_score = 0
        num_successors = 0
        
        for succ_state in succ_states:
            score = self.heuristic_game_value(succ_state)
            total_score += score
            num_successors += 1
            
        
        if num_successors > 1:
            avg_score = (float) (total_score / num_successors)
            
            return avg_score
        else:
            return 0.5
            
    def max_value(self, state, depth):
        if self.game_value(state) != 0 or depth == 0:
            return self.heuristic_game_value(state)
        
        best_score = float('-inf')
        
        for succ_state in self.succ(state):
            score = self.min_value(succ_state, depth - 1)
            best_score = max(score, best_score)
            
        return best_score
            
    def min_value(self, state, depth):
        if self.game_value(state) != 0 or depth == 0:
            return self.heuristic_game_value(state)

        best_score = float('inf')
        
        for succ_state in self.succ(state):
            score = self.max_value(succ_state, depth - 1)
            best_score = min(best_score, score)
            
        return best_score
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0
    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
