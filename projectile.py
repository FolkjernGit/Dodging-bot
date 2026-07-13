import pygame
import random

class Projectile:
    def __init__(self, position, velocity, color, radius):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.radius = radius

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
        


def random_projectile(target, screen_size):
    width, height = screen_size
    speed = 3

    if random.choice((True, False)):
        position = pygame.Vector2(random.randrange(width), random.choice((0, height)))
    else:
        position = pygame.Vector2(random.choice((0, width)), random.randrange(height))

    velocity = (pygame.Vector2(target) - position).normalize() * speed
    return Projectile(position, velocity, (255, 0, 0), 10)