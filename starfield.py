import pygame
import math
import random
from constants import *


STAR_DENSITY = 0.2  # Chance of a star in a cell
STAR_COLOR = (255, 255, 255)

def consistent_random(x, y, seed=42):
    """Deterministically generate a pseudo-random number for a given grid cell."""
    random.seed((x * 73856093) ^ (y * 19349663) ^ seed)
    return random.random()

def generate_star_in_cell(cell_x, cell_y):
    if consistent_random(cell_x, cell_y) < STAR_DENSITY:
        # Offset star slightly inside the cell
        local_x = consistent_random(cell_x, cell_y + 1) * CELL_SIZE
        local_y = consistent_random(cell_x + 1, cell_y) * CELL_SIZE
        return pygame.Vector2(cell_x * CELL_SIZE + local_x,
                              cell_y * CELL_SIZE + local_y)
    return None

class Starfield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.visible_stars = []

    def update(self, cam_pos):
        print("update")
        self.visible_stars = []

        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2
        min_x = int((cam_pos.x - half_w) // CELL_SIZE) - 1
        max_x = int((cam_pos.x + half_w) // CELL_SIZE) + 1
        min_y = int((cam_pos.y - half_h) // CELL_SIZE) - 1
        max_y = int((cam_pos.y + half_h) // CELL_SIZE) + 1

        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                star_pos = generate_star_in_cell(cx, cy)
                if star_pos:
                    self.visible_stars.append(star_pos)

    def draw(self, screen, camera_pos):
        for star in self.visible_stars:
            screen_pos = star - camera_pos + pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            pygame.draw.circle(screen, STAR_COLOR, (int(screen_pos.x), int(screen_pos.y)), 2)

