'''
Created on 16 maj 2022

@author: fojcjpaw
'''
import pickle
import os
from abc import ABC, abstractmethod

class PlayerAbstract(ABC):
    """
    Player abstract (API) for every player in this game.    
    """
    @classmethod
    def load(cls, player_path):
        """
        Load a specific class    
        """
        player = None
        if os.path.isfile(player_path):
            with open(player_path,"rb") as f:
                player = pickle.load(f)
        else:
            player = cls(player_path)
        return player

    def __init__(self, player_path):
        """
        Player_path - path to the file with specific class
        """        
        self.player_path = player_path
        self.counter_draws= 0
        self.counter_winnings = 0
        self.counter_losers = 0
    
    @abstractmethod
    def get_action(self, state, gui):
        """
        Function should return a tuple (row,col)
        about the move
        """ 
        pass
    
    def update(self, prev_state, new_state, prev_action, new_action, reward):
        """
        Used for learning,
        prev_state - previous state of the game
        new_state - new state of the game
        prev_action - the previous action (move)
        new_action - new action (move)
        reward - 0 means no reward, 1, -1 accordingly for win, fail 
        """ 
        pass

    def iter_inner_state_on_field(self, state, possible_actions):
        """
        Generator for each possible action, should return calculated value for each field,
        the value means how good is the move to choose.
        """
        pass
    
    def is_gui_needed(self):
        """
        Should return True when human player is on, when gui should be shown.
        """
        return False
    
    def set_counter_winnings(self):
        """
        Set counter of winnings
        """
        self.counter_winnings += 1
    
    def set_counter_losers(self):
        """
        Set counter of losers
        """
        self.counter_losers += 1
    
    def set_counter_draws(self):
        """
        Set counter of draws
        """
        self.counter_draws += 1
    
    def save(self):
        """ 
        Save object of the class
        """
        if os.path.isfile(self.player_path):
            os.remove(self.player_path)
        f = open(self.player_path, 'wb')
        pickle.dump(self, f)
        f.close()