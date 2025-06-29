from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen, offset: pygame.Vector2):
        pygame.draw.circle(screen, "white", self.position - offset, self.radius)

    def update(self, dt):
        self.position += self.velocity*dt