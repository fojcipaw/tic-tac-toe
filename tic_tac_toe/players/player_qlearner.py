'''
Created on 15 kwi 2022

@author: fojcjpaw, inspired by https://github.com/rfeinman/tictactoe-reinforcement-learning/
'''
import collections
import numpy as np
import random

from players.player_abstract import PlayerAbstract

class PlayerQlearner(PlayerAbstract):
    def __init__(self, player_path):
        PlayerAbstract.__init__(self, player_path)
        # Agent parameters
        self.alpha = 0.5
        self.gamma = 0.9
        self.eps = 0.1
        self.eps_decay = 0.
        self.show_inner_states = False
        
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        
        # Keep a list of reward received at each episode
        self.rewards = []
    
    def update(self, prev_state, new_state, prev_action, new_action, reward):
        """Perform the Q-Learning update of Q values."""
        # Update Q(prev_state,prev_action)
        if new_state is not None:
            # hold list of Q values for all new_action,new_state pairs. We will access the max later
            possible_actions = self.__get_possible_actions(new_state)
            Q_options = [self.Q[action][new_state] for action in possible_actions]
            # update
            self.Q[prev_action][prev_state] += self.alpha*(reward + self.gamma*max(Q_options) - self.Q[prev_action][prev_state])
        else:
            # terminal state update
            self.Q[prev_action][prev_state] += self.alpha*(reward - self.Q[prev_action][prev_state])

        # add reward to rewards list
        self.rewards.append(reward)
    
    def __get_possible_actions(self, state):
        return [action for action in self.actions if state[action[0]*3 + action[1]] == '-']
    
    def get_action(self, state, gui):
        """Select an action given the current game state."""
        # Only consider the allowed actions (empty board spaces)
        possible_actions = self.__get_possible_actions(state)
        if random.random() < self.eps:
            # Random choose.
            action = possible_actions[random.randint(0,len(possible_actions)-1)]
        else:
            try:
                # Greedy choose.
                values = np.array([self.Q[a][state] for a in possible_actions])
                # Find location of max
                ix_max = np.where(values == np.max(values))[0]
                if len(ix_max) > 1:
                    # If multiple actions were max, then sample from them
                    ix_select = np.random.choice(ix_max, 1)[0]
                else:
                    # If unique max action, select that one
                    ix_select = ix_max[0]
                action = possible_actions[ix_select]
            except Exception as e:
                print("Exception: "+str(e))
                print(":-(")

        # update epsilon; geometric decay
        self.eps *= (1.-self.eps_decay)

        return action
    
    def iter_inner_state_on_field(self, state, possible_actions):
        if not self.show_inner_states:
            return
        l = [self.Q[a][state] for a in possible_actions]
        for index,value in enumerate(l):
            row = possible_actions[index][0]
            col = possible_actions[index][1]
            yield (row,col,value)
