import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass


    def update(self, dt):
        # sub-classes must override
        pass

    
    def check_collision(self, other):
        dist = self.radius + other.radius
        return self.position.distance_squared_to(other.position) <= dist*dist
        
    """
    def check_collision(self, other):
        dist = self.radius + other.radius
        delta = self.position - other.position
        dist_sq = delta.length_squared()
        radius_sum_sq = dist * dist
        if dist_sq <= radius_sum_sq:
            if dist_sq == 0:
                # Avoid divide-by-zero
                normal = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                distance = 1e-6
            else:
                # Use Newton-Raphson method for sqrt approximation
                # Initial guess
                approx_sqrt = 0.5 * (dist_sq + dist_sq / dist_sq)
                for i in range(3):
                    approx_sqrt = 0.5 * (approx_sqrt + dist_sq / approx_sqrt)
                distance = approx_sqrt
                inv_distance = 1.0 / distance
                normal = delta * inv_distance  # Normalized vector
            # Approximate overlap
            overlap = dist - distance
            correction = normal * (overlap / 2)
            self.position += correction
            other.position -= correction
            return True

        return False
        """