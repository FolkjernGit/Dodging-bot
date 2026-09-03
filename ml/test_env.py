import pygame
from enviroment import DodgeEnv
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

env = DodgeEnv(screen)

observation = env.reset()

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # random AI
    action = random.randint(0, 3)

    observation, reward, done = env.step(action)

    env.render()

    if done:
        print("Died, resetting")
        observation = env.reset()

pygame.quit()