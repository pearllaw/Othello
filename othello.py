from collections import namedtuple
from itertools import repeat
from games import Game, alpha_beta_cutoff_search
import interface
import pygame

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

class Othello(Game):
    """Play Othello on 8x8 board, with Black (first player) playing 'B'.
    A state has the player to_move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'B' or 'W'."""
    def __init__(self, h=8, v=8):
        self.h = h
        self.v = v
        # Initialize board with starting pieces
        self.positions = [(x, y) for x in range(h) for y in range(v)]
        board = dict(zip(self.positions, repeat(None)))
        board.update({(3, 3): 'W', (3, 4): 'B', (4, 3): 'B', (4, 4): 'W'})
        self.initial = GameState(to_move='B', utility=0, board=board, moves=[])
        self.gui = interface.Gui()
        self.gui.show_screen(self.initial)
    
    def opponent(self, player):
        """Returns character representation of the player's opponent."""
        return 'W' if player == 'B' else 'B'
    
    def in_bounds(self, x, y):
        """Returns True if (x, y) position is within the board dimensions and 
        False otherwise."""
        return x >= 0 and x < self.h and y >= 0 and y < self.v

    def find_moves(self, move, player, board, direction):
        """Returns (x, y) position that the player can move to or None if the 
        position cannot be moved to."""
        pos = tuple(map(sum, zip(move, direction)))
        if board.get(pos) == player:
            return None
        opponent = self.opponent(player)
        # Get position to move to if not out of bounds and not already occupied by player
        while board.get(pos) == opponent: 
            pos = tuple(map(sum, zip(pos, direction)))
        return None if not self.in_bounds(pos[0], pos[1]) or board.get(pos) == None else pos

    def is_valid(self, move, player, board):
        """Returns True if a move is valid and False otherwise."""
        moves = lambda direction: self.find_moves(move, player, board, direction)
        return board.get(move) == None and any(map(moves, DIRECTIONS))
    
    def any_valid_moves(self, state, player):
        return any(self.is_valid(pos, player, state.board) for pos in self.positions)

    def actions(self, state):
        """Returns list of valid (x, y) moves for a given player"""
        for x in range(self.h):
            for y in range(self.v):
                if self.is_valid((x, y), state.to_move, state.board):
                    state.moves.append((x, y))
        return state.moves

    def flip_disks(self, move, player, board, direction):
        """Flip all disks in the direction until disk of same color is found."""
        position = self.find_moves(move, player, board, direction)
        if not position:
            return
        disk = tuple(map(sum, zip(move, direction))) 
        while disk != position:
            board[disk] = player
            disk = tuple(map(sum, zip(disk, direction)))

    def result(self, state, move):
        """Return game state after player has made their move."""
        board = state.board.copy()
        board[move] = state.to_move
        for d in DIRECTIONS:
            self.flip_disks(move, state.to_move, board, d)
        return GameState(to_move=('W' if state.to_move == 'B' else 'B'), 
            utility=self.compute_utility(state.to_move, board), 
            board=board, moves=[])

    def utility(self, state, player):
        """Returns player's utility."""
        return state.utility 

    def compute_utility(self, player, board):
        """Calculate player's current score"""
        black = white = 0
        opponent = self.opponent(player)
        for pos in self.positions:
            disk = board.get(pos)
            if disk == player: 
                black += 1
            elif disk == opponent:
                white += 1
        return black - white

    def evaluate(self, state):
        """Evaluation function that determines the goodness/value of a 
        position in the current board state."""
        board = state.board
        return self.disk_difference(board) + 1000*self.corners_occupied(board) + 10*self.corner_closeness(board)

    def disk_difference(self, board):
        """Captures difference in disks on the board between B - human player 
        (maximizer) and W - AI (minimizer)."""
        disks = [board.get(square) for square in board] 
        black_disks = sum(1 for d in disks if d == 'B')
        white_disks = sum(1 for d in disks if d == 'W')
        return white_disks - black_disks
    
    def corners_occupied(self, board):
        """Captures how many corners are occupied by each player, evaluates 
        stability since corner disks cannot be flipped by opponent once occupied."""
        b = w = 0

        if board.get((0,0)) == 'B': b += 1
        elif board.get((0,0)) == 'W': w += 1
        if board.get((0,7)) == 'B': b += 1
        elif board.get((0,7)) == 'W': w += 1
        if board.get((7,0)) == 'B': b += 1
        elif board.get((7,0)) == 'W': w += 1
        if board.get((7,7)) == 'B': b += 1
        elif board.get((7,7)) == 'W': w += 1
        return w - b

    def corner_closeness(self, board):
        """Captures how many of each player's disks that are close to a corner.""" 
        w = 0

        for row in range(1,7):
            if board.get((row, 0)) == 'W': w += 1
            if board.get((row, 7)) == 'W': w += 1
        for col in range(2,8):
            if board.get((0, col)) == 'W': w += 1
            if board.get((7, col)) == 'W': w += 1
        return w

    def mobility(self, state):
        """Captures relative difference in mobility (possible moves) for max and 
        min player."""
        opponent = self.opponent(state.to_move)
        opponent_state = GameState(to_move=opponent,
            utility=self.compute_utility(opponent, state.board),
            board=state.board, moves=[])
        black_moves = len(self.actions(state))
        white_moves = len(self.actions(opponent_state))
        if black_moves + white_moves == 0:
            return 0
        else:
            return white_moves
        
    
    def terminal_test(self, state):
        """A state is terminal if it is won or neither player has any valid move."""
        player = state.to_move
        opponent = self.opponent(player)
        return not (self.any_valid_moves(state, player) and self.any_valid_moves(state, opponent))

    def run(self, state):
        """Run the program until terminal state is reached."""
        while True:
            if self.terminal_test(state):
                player = state.to_move
                opponent = self.opponent(player)
                if player == 'B':
                    black = self.compute_utility(player, state.board)
                    white = self.compute_utility(opponent, state.board)
                else:
                    black = self.compute_utility(opponent, state.board)
                    white = self.compute_utility(player, state.board)
                if black > white:
                    winner = 'B'
                elif black < white:
                    winner = 'W'
                else:
                    winner = None
                break
            moves = self.actions(state)
            if len(moves) > 0:
                self.gui.show_valid_moves(moves)
                # Human player
                if state.to_move == 'B':  
                    while True:
                        move = self.gui.get_mouse_event()
                        if move in moves:
                            break
                    state = self.result(state, move) 
                # AI player
                else: 
                    move = alpha_beta_cutoff_search(state, self, 4, None, self.evaluate)
                    state = self.result(state, move)
            self.gui.update(state.board)
        self.gui.score(winner)

if __name__ == '__main__':
    othello = Othello()
    state = othello.initial
    othello.run(state)  
