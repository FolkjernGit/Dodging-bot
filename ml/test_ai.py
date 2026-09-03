import pygame
import torch

from enviroment import DodgeEnv
from model import DodgeModel
from agent import Agent


pygame.init()

screen = pygame.display.set_mode((800, 600))

# environment
env = DodgeEnv(screen)

# model
model = DodgeModel()

# load trained model
model.load_state_dict(
    torch.load("models/best_model.pth")
)

model.eval()


# agent
agent = Agent(model)


# disable randomness
agent.epsilon = 0


# reset
observation = env.reset()

done = False


while not done:

    # AI chooses best action
    action = agent.choose_action(
        observation,
        training=False
    )

    observation, reward, done = env.step(action)


    # render
    env.render()

    pygame.time.delay(30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


print("Game over!")
print("Reward:", reward)
print("Time alive:", env.time_alive)

pygame.quit()