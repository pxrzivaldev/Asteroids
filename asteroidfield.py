import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def draw(self, screen, offset):
        edge_color = (100, 255, 100)  # light green for visibility
        edge_thickness = 2
        # Top edge
        pygame.draw.line(screen, edge_color, (0 - offset.x, 0 - offset.y), (SCREEN_WIDTH - offset.x, 0 - offset.y), 2)
        # Bottom edge
        pygame.draw.line( screen, edge_color, (0 - offset.x, SCREEN_HEIGHT - offset.y), (SCREEN_WIDTH - offset.x, SCREEN_HEIGHT - offset.y),2)
        # Left edge
        pygame.draw.line(
            screen,
            edge_color,
            (0 - offset.x, 0 - offset.y),
            (0 - offset.x, SCREEN_HEIGHT - offset.y),
            2
        )
        # Right edge
        pygame.draw.line(
            screen,
            edge_color,
            (SCREEN_WIDTH - offset.x, 0 - offset.y),
            (SCREEN_WIDTH - offset.x, SCREEN_HEIGHT - offset.y),
            2
        )

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