from constants import *
from player import *

def draw_predicted_path(screen, player, offset, color=(0, 255, 255)):
    position = player.position
    velocity = player.velocity
    acceleration = player.acceleration
    angle = player.rotation
    angular_velocity = player.angular_velocity

    steps = 60
    dt_step = 0.05
    points = []

    current_pos = pygame.Vector2(position)
    current_vel = pygame.Vector2(velocity)
    current_angle = angle

    for i in range(steps):
        dt = dt_step
        current_vel += acceleration * dt
        current_pos += current_vel * dt
        current_angle += angular_velocity * dt
        points.append((int(current_pos.x - offset.x), int(current_pos.y - offset.y)))

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 1)