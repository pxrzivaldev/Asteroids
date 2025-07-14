import pygame
from constants import *

class HudElement(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.screen_pos = pygame.Vector2(x, y)

    def draw(self, screen):
        pass


    def update(self, dt):
        pass
