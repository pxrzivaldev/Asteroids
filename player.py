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
        self.thrusting_backwards = False
        self.thrusting_forwards = False
        self.angular_velocity = 0  

    def triangle(self):
        front = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + front * self.radius
        b = self.position - front * self.radius - right
        c = self.position - front * self.radius + right
        return [a, b, c]
    
    def thrust_flame(self):
        front = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 2.5

        base_center = self.position - front * self.radius * 1.2
        left = base_center - right
        right_point = base_center + right
        tip = self.position - front * self.radius * 2
        return [left, right_point, tip]
    
    def left_rotation_flame(self):
        front = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)

        base = self.position + front * self.radius + right * self.radius * 0.4
        left = base + right * 6
        tip = base + front * 8

        return [base, left, tip]

    def right_rotation_flame(self):
        front = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)

        base = self.position + front * self.radius - right * self.radius * 0.4
        right_pt = base - right * 6
        tip = base + front * 8

        return [base, right_pt, tip]
    
    def thrust(self, dt):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.thrusting_backwards:
            direction *= -0.5
        self.velocity += direction * PLAYER_ACCELERATION * dt    

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

        if self.thrusting_backwards:
            self.thrusting_left = True
            self.thrusting_right = True
        if self.thrusting_forwards:
            pygame.draw.polygon(screen, "orange", self.thrust_flame())
        if self.thrusting_left:
            pygame.draw.polygon(screen, "orange", self.left_rotation_flame())
        if self.thrusting_right:
            pygame.draw.polygon(screen, "orange", self.right_rotation_flame())

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.thrusting_forwards = False
        self.thrusting_backwards = False
        self.thrusting_left = False
        self.thrusting_right = False

        if self.shoot_cd > 0:
            self.shoot_cd-=1*dt

        if keys[pygame.K_a]:
            self.angular_velocity -= PLAYER_ANGULAR_ACCELERATION * dt
            self.thrusting_left = True
        if keys[pygame.K_d]:
            self.angular_velocity += PLAYER_ANGULAR_ACCELERATION * dt
            self.thrusting_right = True
        if keys[pygame.K_w]:
            self.thrusting_forwards = True
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.thrusting_backwards = True
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
        front = pygame.Vector2(0, 1).rotate(self.rotation)
        vec2 = self.position + front*self.radius
        shot = Shot(vec2.x, vec2.y)
        shot.velocity = front * SHOT_SPEED + self.velocity
