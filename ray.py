import pygame

from logic import point_to_line_distance


class Ray:
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length
        self.distance = 1.0

    def get_end_position(self, position):
        direction = pygame.Vector2(1, 0).rotate(self.angle)
        return position + direction * self.length
    
    def update(self, position, projectiles):

        self.distance = 1.0

        end = self.get_end_position(position)

        for projectile in projectiles:

            distance = point_to_line_distance(
                projectile.position,
                position,
                end
            )

            if distance < projectile.radius:

                hit_distance = (
                    position.distance_to(projectile.position)
                    / self.length
                )

                self.distance = min(
                    self.distance,
                    hit_distance
                )
    
    def draw(self, screen, position):
        end = self.get_end_position(position)

  
        if self.distance < 1.0:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0) 

        pygame.draw.line(
            screen,
            color,
            position,
            end,
            2
        )

