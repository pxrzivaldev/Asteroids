import pygame
from constants import *

class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.position = - pygame.math.Vector2((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.player_tracking: Player | None = None
        self.target_position = - pygame.math.Vector2((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.rate = 5

    def set_position(self, position):
        self.target_position = position - pygame.math.Vector2((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    
    def set_target(self, player):
        self.player_tracking = player

    def update(self, dt):
        if self.player_tracking:
            self.set_position(self.player_tracking.position)
        self.position += (self.target_position - self.position) * dt * self.rate