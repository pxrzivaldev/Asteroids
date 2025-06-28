from circleshape import *
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity*dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        rand_angle = random.uniform(20, 50)
        vec_1 = self.velocity.rotate(rand_angle)
        vec_2 = self.velocity.rotate(-rand_angle)
        size_1 = self.radius - ASTEROID_MIN_RADIUS
        size_2 = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, size_1)
        new_asteroid_1.velocity = vec_1 * 1.2
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, size_2)
        new_asteroid_2.velocity = vec_2 * 1.2

