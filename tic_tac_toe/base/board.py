'''
Created on 15 kwi 2022

@author: fojcjpaw
'''
import itertools
class Board:
    def __init__(self):
        self.board_xy=(((0,0),(0,1),(0,2)),
                       ((1,0),(1,1),(1,2)),
                       ((2,0),(2,1),(2,2)))
        self.reset()
        self.player_1_mark = "X"
        self.player_2_mark = "O"
    
    def reset(self):
        """
        Reset to the initial states
        """
        self.board=[['-','-','-',],
                   ['-','-','-',],
                   ['-','-','-',]]
        
        self.count = 0
        self.winning_line = None
    
    def get_player_1_mark(self):
        """
        Return "X"
        """
        return self.player_1_mark

    def get_player_2_mark(self):
        """
        Return "O"
        """
        return self.player_2_mark
    
    def state(self):
        """
        Return the board state
        """
        return self.board
    
    def get_winning_line(self):
        """
        Returns the winning line in format:
        ((row1,col1),(row2,col2),(row3,col3)):        
        """
        return self.winning_line
    
    def apply_action(self,action,mark):
        self.board[action[0]][action[1]] = mark
        self.count += 1
    
    def available_moves(self):
        for row, col in itertools.product(range(3), range(3)):
            if self.board[row][col] == "-":
                yield (row, col)
    
    def get_state_key(self):
        """
        Converts 2D list representing the board state into a string key
        for that state. Keys are used for Q-value hashing.
        """
        key = ''
        for row in self.board:
            for elt in row:
                key += elt
        return key
    
    def __has_3_in_a_line(self, line):
        return all(x == self.player_1_mark for x in line) | all(x == self.player_2_mark for x in line)

    def __has_3_in_row(self):
        for x in range(3):
            if self.__has_3_in_a_line(self.board[x]):
                self.winning_line = self.board_xy[x]
                return True
        return False

    def __has_3_in_col(self):
        for y in range(3):
            if self.__has_3_in_a_line([i[y] for i in self.board]):
                self.winning_line = [i[y] for i in self.board_xy]
                return True
        return False

    def __has_3_diag_left_up_right_down(self):
        if self.__has_3_in_a_line([self.board[i][i] for i in range(3)]):
            self.winning_line = [self.board_xy[i][i] for i in range(3)]
            return True
        return False

    def __has_3_diag_left_down_right_up(self):
        if self.__has_3_in_a_line([self.board[2 - i][i] for i in range(3)]):
            self.winning_line = [self.board_xy[2 - i][i] for i in range(3)]
            return True
        return False
    
    def is_game_over(self):
        """ Returns:
            -1: game continue
            0: draw
            1: player/player_qlearner won
        """        
        if self.count < 5:
            return -1 # game continue, no possibility to win
        
        is_end = (self.__has_3_in_row() |
                  self.__has_3_in_col() |
                  self.__has_3_diag_left_up_right_down() |
                  self.__has_3_diag_left_down_right_up())
        
        if is_end:
            return 1 #player/player_qlearner won
        
        if self.count == 9:
            return 0 #draw
        
        return -1 # game continue