import gymnasium as gym
from gymnasium.wrappers import FlattenObservation

import game

"""
An environment for the blackjack game using OpenAI Gymnasium
"""

class Environment(gym.Env):
	
	def __init__(self, deck: list[tuple[str,str]], player: game.Player):
		self.deck = deck
		self.player = player

		self.observation_space = gym.spaces.Dict(
			{
				"hand": gym.spaces.Tuple(),
				"dealer hand": gym.spaces.Tuple()
			}
		)

		# The action space is the set of actions that 
		self.action_space = gym.spaces.Discrete(3)
		self._action_to_decision: dict[int, str] = {
			0: "S",
			1: "H",
			2: "D"
		}

