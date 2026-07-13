import pygame
import math

from ray import Ray



class Player:
    def __init__(self, position, screen):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.color = (1, 0, 0)
        self.radius = 50
        self.ray_length = screen.get_width()*2
        self.alive = True

        ray_count = 16
        ray_length = screen.get_width()*2

        self.rays = []

        for i in range(ray_count):
            angle = i * (360 / ray_count)
            self.rays.append(
                Ray(angle, ray_length)
            )
        
        self.image = pygame.image.load(
            "assets/player.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (self.radius, self.radius)
        )

        self.rect = self.image.get_rect(
            center=self.position
        )
        
    def get_observation(self, screen):
        observation = []

        # player position
        observation.append(self.position.x / screen.get_width())
        observation.append(self.position.y / screen.get_height())

        # ray distances
        for ray in self.rays:
            observation.append(ray.distance)

        # velocity
        observation.append(self.velocity.x)
        observation.append(self.velocity.y)

        # alive status
        observation.append(int(self.alive))
        return observation
    
    
    def move(self, screen):
        keys = pygame.key.get_pressed()

        self.velocity.update(0, 0)
        if keys[pygame.K_w]:
            self.velocity.y -= self.speed
        if keys[pygame.K_s]:
            self.velocity.y += self.speed
        if keys[pygame.K_a]:
            self.velocity.x -= self.speed
        if keys[pygame.K_d]:
            self.velocity.x += self.speed

        self.position += self.velocity
        if self.position.x < self.radius // 2:
            self.position.x = self.radius // 2
        if self.position.x > screen.get_width() - self.radius // 2:
            self.position.x = screen.get_width() - self.radius // 2
        if self.position.y < self.radius // 2:
            self.position.y = self.radius // 2
        if self.position.y > screen.get_height() - self.radius // 2:
            self.position.y = screen.get_height() - self.radius // 2
            

    def draw(self, screen):
        self.rect.center = (round(self.position.x), round(self.position.y))
        screen.blit(self.image, self.rect)
    
    def draw_rays(self, screen):
        for ray in self.rays:
            ray.draw(screen, self.position)