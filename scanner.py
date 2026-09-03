import pygame


class Beam:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def draw(self, screen):
        pygame.draw.line(
            screen,
            (0, 255, 0),
            self.start,
            self.end,
            2
        )