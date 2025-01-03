import gymnasium as gym
import numpy as np
import game
from environment import Environment
from stable_baselines3 import PPO, A2C
import matplotlib.pyplot as plt

def create_blackjack():
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    deck = [(value, suit) for suit in suits for value in values]
    newGame = game.Game()
    return Environment(deck, newGame)

gym.register(
    id="gymnasium_env/CSE368-BlackJack-v0",
    entry_point = create_blackjack,
)

env = gym.make("gymnasium_env/CSE368-BlackJack-v0")

# RL Agent

agent = "A2C"
policy = "MultiInputPolicy"
timesteps = 10_000

model = A2C(policy, env, verbose=1)
model.learn(total_timesteps=timesteps)
del model

average = []
sum = 0
for i in range(len(game.rewardList)):
    sum += game.rewardList[i]
    if i%(timesteps/100) == 0:
        average.append(sum/(timesteps/100))
        sum = 0

# RL Agent Plotting

plt.plot(list(range(len(average))), average, label="RL Agent")
data = np.array(average)
data = data[~np.isnan(data)]
data = data[~np.isinf(data)]
z = np.polyfit(list(range(len(data))), data, 1)
p = np.poly1d(z)
plt.plot(list(range(len(average))), p(list(range(len(average)))), label="RL Linear Trend")

# Random Agent

game.rewardList = []

for i in range(int(timesteps * (4/6))):
    observation, info = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        observation, reward, done, truncated, info = env.step(action)

average = []
sum = 0
for i in range(len(game.rewardList)):
    sum += game.rewardList[i]
    if i%(timesteps/100) == 0:
        average.append(sum/(timesteps/100))
        sum = 0

# Random Agent Plotting

plt.plot(list(range(len(average))), average, label="Random")

z = np.polyfit(list(range(len(average))), average, 1)
p = np.poly1d(z)
plt.plot(list(range(len(average))), p(list(range(len(average)))), label="Random Linear Trend")

plt.xlabel(f"Time steps * {timesteps/100}")
plt.ylabel("Average reward")
plt.title("RL Agent vs Random Selection")
plt.legend()
plt.show()

env.close()
