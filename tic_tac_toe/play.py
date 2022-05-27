#!/usr/bin/python3
'''
Created on 15 kwi 2022

@author: fojcjpaw
'''
import argparse
from base.game import Game
from players.player_qlearner import PlayerQlearner
from players.player_human_qlearner import PlayerHumanQlearner
from players.player_human import PlayerHuman

class Play:
    """
    Start class to play a game
    """
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.game = Game(self.player_1, self.player_2)
    
    def start(self):
        """
        The function starts the game
        """
        self.game.start()
    
    def save(self):
        """
        Save objects of players
        """
        self.player_1.save()
        self.player_2.save()
    
    def is_gui(self):
        """
        True if gui is shown
        """
        return self.game.is_gui()

def get_player(player_name, file_name):
    """
    Factory function to get a player based of player_name,
    player if file_name exist is loaded.
    """
    if player_name == "Human":
        player = PlayerHuman()
    elif player_name == "Qlearner":
        player = PlayerQlearner.load(file_name)
        player.show_inner_states = False
    elif player_name == "HumanQlearner":
        player = PlayerHumanQlearner.load(file_name)
        player.show_inner_states = True
    else:
        player = None
    return player
    
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe.")
    parser.add_argument("-p1", "--player_first", default="Human", type=str,
                        help="define first player (Human, Qlearner, HumanQlearner)")
    parser.add_argument("-p2", "--player_second", default="Qlearner", type=str,
                        help="define second player (Human, Qlearner, HumanQlearner")
    parser.add_argument("-n", "--number_of_games", default=1, type=int,
                        help="define number of games (in case no Human)")
    args = parser.parse_args()
    
    play = Play(get_player(args.player_first,'records/qlearner_player_1.pkl'), get_player(args.player_second,'records/qlearner_player_2.pkl'))
    
    if play.is_gui():
        play.start()
    else:
        for i in range(0,args.number_of_games):
            play.start()
    
    play.save()