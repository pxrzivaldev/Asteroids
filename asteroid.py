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
        offset = self.velocity.normalize().rotate(90) * (self.radius - ASTEROID_MIN_RADIUS)
        new_asteroid_1 = Asteroid(self.position.x + offset.x, self.position.y + offset.y, size_1)
        new_asteroid_1.velocity = vec_1 * 1.2
        new_asteroid_2 = Asteroid(self.position.x - offset.x, self.position.y - offset.y, size_2)
        new_asteroid_2.velocity = vec_2 * 1.2

    def a_a_collision(self, other):

        # ---- Position Correction to resolve overlap ----
        delta_pos = self.position - other.position
        distance = delta_pos.length()

        if distance == 0:
            # If exactly overlapping, give small random push
            delta_pos = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            distance = 1e-3

        overlap = self.radius + other.radius - distance
        if overlap > 0:
                    correction = delta_pos.normalize() * (overlap / 2)
                    self.position += correction
                    other.position -= correction

        rel_vel = self.velocity - other.velocity
        rel_speed = rel_vel.length()
        normal = (self.position - other.position).normalize()

        # Elastic collision response
        m1, m2 = self.radius**2, other.radius**2
        u1, u2 = self.velocity, other.velocity

        # Projection of velocities on the normal
        u1n = normal.dot(u1)
        u2n = normal.dot(u2)
        # Elastic collision formula (1D along normal)
        v1n = (u1n * (m1 - m2) + 2 * m2 * u2n) / (m1 + m2)
        v2n = (u2n * (m2 - m1) + 2 * m1 * u1n) / (m1 + m2)
        # Update velocities along the normal, keep tangential unchanged
        delta_v1 = normal * (v1n - u1n)
        delta_v2 = normal * (v2n - u2n)
        self.velocity += delta_v1
        other.velocity += delta_v2
        # Optional: Split smaller asteroid if collision is intense
        if rel_speed > SPLIT_VELOCITY_THRESHOLD:
            if self.radius < other.radius:
                self.split()
            elif other.radius < self.radius:
                other.split()