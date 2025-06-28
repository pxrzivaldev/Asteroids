from circleshape import *
from constants import *
from shot import *
import math

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cd = 0
        self.thrusting = False
        self.reverse = False
        self.angular_velocity = 0  

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def thrust_flame(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 2.5

        base_center = self.position - forward * self.radius * 1.2
        left = base_center - right
        right_point = base_center + right
        tip = self.position - forward * self.radius * 2
        return [left, right_point, tip]
    
    def thrust(self, dt):
        self.thrusting = True
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.reverse:
            direction *= -0.5
        self.velocity += direction * PLAYER_ACCELERATION * dt    

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        if self.thrusting:
            if self.reverse:
                pass
            else:
                pygame.draw.polygon(screen, "orange", self.thrust_flame())

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.thrusting = False
        self.reverse = False
        if self.shoot_cd > 0:
            self.shoot_cd-=1*dt

        if keys[pygame.K_a]:
            self.angular_velocity -= PLAYER_ANGULAR_ACCELERATION * dt
        if keys[pygame.K_d]:
            self.angular_velocity += PLAYER_ANGULAR_ACCELERATION * dt
        if keys[pygame.K_w]:
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.reverse=True
            self.thrust(dt)
        if keys[pygame.K_SPACE]:
            if self.shoot_cd <= 0:
                self.shoot()
                self.shoot_cd = SHOOT_COOLDOWN
        
        self.angular_velocity = max(-PLAYER_MAX_ANGULAR_VELOCITY, min(self.angular_velocity, PLAYER_MAX_ANGULAR_VELOCITY))
        self.angular_velocity *= pow(PLAYER_ANGULAR_DRAG, dt)
        if abs(self.angular_velocity) < ANGULAR_THRESHOLD:
            self.angular_velocity = 0
        self.rotation += self.angular_velocity * dt * 100
        self.position += self.velocity * dt

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        vec2 = self.position + forward*self.radius
        shot = Shot(vec2.x, vec2.y)
        shot.velocity = forward * SHOT_SPEED + self.velocity
