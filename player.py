import pygame
import math

from ray import Ray



class Player:
    def __init__(self, position, screen):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.color = (255, 255, 255)
        self.radius = 50
        self.ray_length = screen.get_width()*2
        self.alive = True
        self.shielded = False
        self.shield_duration = 0
        self.shield_cooldown = 0
        self.shield_hits = 0
        self.blocked_projectiles = 0
        
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
    
    def get_closest_projectiles(self, projectiles, n):
        sorted_projectiles = sorted(
            projectiles,
            key=lambda p: self.position.distance_to(p.position)
        )

        return sorted_projectiles[:n]
    
    #def get_observation(self, screen):
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
    
    def get_observation(self, projectiles, screen, MAX_PROJECTILE_SPEED):
        observation = []
        
        player_x = (self.position.x / screen.get_width()) * 2 - 1
        player_y = (self.position.y / screen.get_height()) * 2 - 1

        observation.append(player_x)
        observation.append(player_y)
        
        closest = self.get_closest_projectiles(projectiles, 5)

        for projectile in closest:

            offset = projectile.position - self.position
            max_distance = (
                screen.get_width() ** 2 +
                screen.get_height() ** 2
            ) ** 0.5

            distance = offset.length() / max_distance
            distance = max(0, min(1, distance))
            x = offset.x / (screen.get_width() / 2)
            y = offset.y / (screen.get_height() / 2)
            x = max(-1, min(1, x))
            y = max(-1, min(1, y))
            observation.append(x)
            observation.append(y)
            observation.append(distance)
            vx = projectile.velocity.x / MAX_PROJECTILE_SPEED
            vy = projectile.velocity.y / MAX_PROJECTILE_SPEED

            vx = max(-1, min(1, vx))
            vy = max(-1, min(1, vy))

            observation.append(vx)
            observation.append(vy)
        observation.append(
                int(self.shielded)
            )
        while len(closest) < 5:
            observation.extend([0, 0, 1, 0, 0])
            closest.append(None)
        return observation
    
    def move(self, direction, screen):
        self.velocity.update(0, 0)

        if direction == 0:       # up
            self.velocity.y -= self.speed
        elif direction == 1:     # down
            self.velocity.y += self.speed
        elif direction == 2:     # left
            self.velocity.x -= self.speed
        elif direction == 3:     # right
            self.velocity.x += self.speed
        elif direction == 4:     # up-left
            self.velocity.x -= self.speed / math.sqrt(2)
            self.velocity.y -= self.speed / math.sqrt(2)
        elif direction == 5:     # up-right
            self.velocity.x += self.speed / math.sqrt(2)
            self.velocity.y -= self.speed / math.sqrt(2)
        elif direction == 6:     # down-left
            self.velocity.x -= self.speed / math.sqrt(2)
            self.velocity.y += self.speed / math.sqrt(2)
        elif direction == 7:     # down-right
            self.velocity.x += self.speed / math.sqrt(2)
            self.velocity.y += self.speed / math.sqrt(2)
        elif direction == 8:     # stay
            self.velocity.update(0, 0)
        elif direction == 9:
            if self.shield_cooldown == 0:
                self.shielded = True
                self.shield_hits = 1
            
        
        if self.shielded:

            self.shield_duration += 1

            if self.shield_duration >= 60:
                self.shielded = False
                self.shield_duration = 0
                self.shield_cooldown = 300


        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

        self.position += self.velocity

        # keep inside screen
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
    
    def draw_threat_lines(self, screen, projectiles):
        closest = self.get_closest_projectiles(projectiles, 5)

        for projectile in closest:
            pygame.draw.line(
                screen,
                pygame.Color(204,204, 204),
                self.position,
                projectile.position,
                2
            )
