'''
Created on 15 kwi 2022

@author: fojcjpaw, inspired by https://github.com/rfeinman/tictactoe-reinforcement-learning/
'''
from players.player_qlearner import PlayerQlearner

class PlayerHumanQlearner(PlayerQlearner):
    @classmethod
    def load(cls, player_path):
        player = PlayerQlearner.load(player_path)
        # Create new b_obj
        this_obj = cls()
        # Copy all values of A to B
        # It does not have any problem since they have common template
        for key, value in player.__dict__.items():
            this_obj.__dict__[key] = value
        return this_obj

    def __init__(self):
        self.show_inner_states = True
    
    def get_action(self, state, gui):
        gui.wait()
        action = gui.get_action()
        while action == None:     
            gui.wait()
            action = gui.get_action()
        gui.update()
        return action
    
    def is_gui_needed(self):
        return True
    
    def save(self):
        pass
