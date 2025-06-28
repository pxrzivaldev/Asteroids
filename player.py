from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cd = 0
        

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def thrust(self, dt, reverse=False):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        if reverse:
            direction *= -0.5
        self.velocity += direction * PLAYER_ACCELERATION * dt    

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.shoot_cd > 0:
            self.shoot_cd-=1*dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.thrust(dt, reverse=True)
        if keys[pygame.K_SPACE]:
            if self.shoot_cd <= 0:
                self.shoot()
                self.shoot_cd = SHOOT_COOLDOWN
        
        self.position += self.velocity * dt

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        vec2 = self.position + forward*self.radius
        shot = Shot(vec2.x, vec2.y)
        shot.velocity = forward * SHOT_SPEED + self.velocity
