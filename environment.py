from typing import Optional
import gymnasium as gym
from gymnasium.wrappers import FlattenObservation

import game

"""
An environment for the blackjack game using OpenAI Gymnasium
"""

class Environment(gym.Env):

    def __init__(self, deck: list[tuple[str, str]], game: game.Game):
        self.deck = deck
        self.game = game

        # What the agent is aware of
        self.observation_space = gym.spaces.Dict(
            {
                "score": gym.spaces.Discrete(22),
                "dealer score": gym.spaces.Discrete(22), #
                "soft ace": gym.spaces.Discrete(2), #Soft ace can be a 0 or a 1
                "count": gym.spaces.Int(-100,100), #Count can be anywhere between -100 thru +100
            }
        )

        # The action space is the set of actions that
        self.action_space = gym.spaces.Discrete(3)
        self._action_to_decision: dict[int, str] = {0: "S", 1: "H", 2: "D"}

    # I don't know if this is even necessary
    def _get_obs(self) -> dict:
        return {
            "score": self.game.player.currentScore,
            "dealer score": self.game.dealer.currentScore,
            "soft ace": 1 if self.game.player.soft_ace else 0,
            "count": self.game.count
		}

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> None:

        super().reset(seed=seed)
        self.game = game.Game(game.Player)
        self.game.player.bet=0.0
        self.game.player.money=1000.0
        self.game.player.soft_ace=False

        return self._get_obs


    def step(self, action: int, bet: int = 0):
        actionStr = self._action_to_decision[action]

        if actionStr == "H":
            self.game.hit(self.game.player)
        elif actionStr == "D":
            self.game.doubleDown(self.game.player)
        elif actionStr == "S":
            self.game.dealerAction()

        reward = 0
        done=False #done signals to main if the step is complete
        if self.game.is_over:
            reward = self.game.player.bet if self.game.player.currentScore > self.game.dealer.currentScore and self.game.player.currentScore <= 21 else -1 * self.game.player.bet
            done=True
        
        observation = self._get_obs()

        return observation, reward, self.game.is_over, False, {}
