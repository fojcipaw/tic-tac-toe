'''
Created on 15 kwi 2022

@author: fojcjpaw
'''
from base.board import Board
from base.gui import GUI

class Game:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = Board()
        self.gui = GUI(self.board)
        
        self.is_gui_needed = (self.player_1.is_gui_needed() |
                              self.player_2.is_gui_needed())
    
    def is_gui(self):
        "True if gui is shown"
        return self.is_gui_needed
    
    def apply_action(self, action, mark):
        """
        Applies an action (move)
        """
        self.board.apply_action(action, mark)
        self.gui.apply_action(action, mark)
        print(action,mark)
    
    def set_winner(self, player_win, player_fail, player_win_mark, player_fail_mark, reward):
        """
        Set appropriate counters and print result of the game
        """
        self.winner = ""
        print("----------------")
        if reward == 0:            
            player_win.set_counter_draws()
            player_fail.set_counter_draws()
            print("Game over, result: DRAW")
        else:            
            self.winner = player_win_mark
            player_win.set_counter_winnings()
            player_fail.set_counter_losers()            
            print("Game over, winner is: ", player_win_mark)
        
        print("Summary: ")
        print("(", player_win_mark, ") winnings=", player_win.counter_winnings,
              ", loosers=", player_win.counter_losers, ", draws=", player_win.counter_draws,sep="")
        print("(", player_fail_mark, ") winnings=", player_fail.counter_winnings,
              ", loosers=", player_fail.counter_losers, ", draws=", player_fail.counter_draws,sep="")
        print("----------------")
            

    def gui_update_field_by_inner_state(self, agent, state):
        """
        It shows inner states of player on the board
        """
        inner_states = agent.iter_inner_state_on_field(state, list(self.board.available_moves()))
        if inner_states != None:
            self.gui.update_field([a for a in inner_states])
    
    def start(self):
        """
        Start function with main loop
        """
        self.board.reset()
        
        state_1_prev = None
        state_1_new = None
        action_1_prev = None
        action_1_new = None
        
        state_2_prev = None
        state_2_new = None
        action_2_prev = None
        action_2_new = None
            
        while True:
            state_1_new = self.board.get_state_key()
            action_1_new = self.player_1.get_action(state_1_new, self.gui)
            self.gui_update_field_by_inner_state(self.player_1, state_1_new)
            self.apply_action(action_1_new,self.board.get_player_1_mark())
            
            reward = self.board.is_game_over()
            if reward != -1:
                self.player_1.update(state_1_prev, None, action_1_prev, None, 1 * reward)
                self.player_2.update(state_2_prev, None, action_2_prev, None, -1 * reward)
                self.set_winner(self.player_1, self.player_2, self.board.get_player_1_mark(), self.board.get_player_2_mark(), reward)
                break

            if state_1_prev is not None:
                self.player_1.update(state_1_prev, state_1_new, action_1_prev, action_1_new, 0)
            state_1_prev = state_1_new
            action_1_prev = action_1_new
        
            state_2_new = self.board.get_state_key()
            action_2_new = self.player_2.get_action(state_2_new, self.gui)
            self.gui_update_field_by_inner_state(self.player_2, state_2_new)
            self.apply_action(action_2_new,self.board.get_player_2_mark())
            
            reward = self.board.is_game_over()
            if reward != -1:
                self.player_1.update(state_1_prev, None, action_1_prev, None, -1 * reward)
                self.player_2.update(state_2_prev, None, action_2_prev, None, 1 * reward)
                self.set_winner(self.player_2, self.player_1, self.board.get_player_2_mark(), self.board.get_player_1_mark(), reward)
                break
            
            if state_2_prev is not None:
                self.player_2.update(state_2_prev, state_2_new, action_2_prev, action_2_new, 0)
            state_2_prev = state_2_new
            action_2_prev = action_2_new
      
        if self.is_gui_needed:
            if self.gui.finish(self.winner):
                self.start()