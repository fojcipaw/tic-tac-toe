'''
Created on 16 maj 2022

@author: fojcjpaw
'''
from players.player_abstract import PlayerAbstract

class PlayerHuman(PlayerAbstract):
    def __init__(self):
        PlayerAbstract.__init__(self, "")
    
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
        