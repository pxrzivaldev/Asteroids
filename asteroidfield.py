import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),  # from left to right
            lambda y: pygame.Vector2(
                -ASTEROID_MAX_RADIUS - SCREEN_WIDTH / 2,
                (y * SCREEN_HEIGHT) - SCREEN_HEIGHT / 2,
            ),
        ],
        [
            pygame.Vector2(-1, 0),  # from right to left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS - SCREEN_WIDTH / 2,
                (y * SCREEN_HEIGHT) - SCREEN_HEIGHT / 2,
            ),
        ],
        [
            pygame.Vector2(0, 1),  # from top to bottom
            lambda x: pygame.Vector2(
                (x * SCREEN_WIDTH) - SCREEN_WIDTH / 2,
                -ASTEROID_MAX_RADIUS - SCREEN_HEIGHT / 2,
            ),
        ],
        [
            pygame.Vector2(0, -1),  # from bottom to top
            lambda x: pygame.Vector2(
                (x * SCREEN_WIDTH) - SCREEN_WIDTH / 2,
                SCREEN_HEIGHT + ASTEROID_MAX_RADIUS - SCREEN_HEIGHT / 2,
            ),
        ],
    ]

    def draw(self, screen, offset):
        edge_color = (100, 255, 100)  # Light green
        edge_thickness = 2

        for direction, position_func in self.edges:
            # Use t=0 and t=1 to get the start and end points of each edge
            start = position_func(0) - offset
            end = position_func(1) - offset

            pygame.draw.line(screen, edge_color, start, end, edge_thickness)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(ASTEROID_MIN_INITIAL_SPEED, ASTEROID_MAX_INITIAL_SPEED)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)