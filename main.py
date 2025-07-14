# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from camera import *
from starfield import *
from predictline import *


def main():

    def start_game():
        pygame.sprite.Group.empty(updatable)
        pygame.sprite.Group.empty(drawable)
        pygame.sprite.Group.empty(asteroids)
        pygame.sprite.Group.empty(shots)
        pygame.sprite.Group.empty(cam_updatable)

        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable, drawable)
        Shot.containers = (shots, updatable, drawable)
        Camera.containers = (updatable)
        Starfield.containers = (cam_updatable, drawable)

        player = Player(0, 0)
        asteroidfield = AsteroidField()
        camera = Camera()
        camera.set_target(player)
        starfield = Starfield()

        return player, asteroidfield, camera, starfield

    print("Starting Asteroids!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #init Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    cam_updatable = pygame.sprite.Group()
    
    #init Clock
    clock = pygame.time.Clock()
    dt = 0

    player_alive = False
    game_over = False

    while True:
        if player_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
        
            dt = clock.tick(FPS_LIMIT) / 1000

            screen.fill((0,0,0),rect=None, special_flags=0)

            for thing in updatable:
                thing.update(dt)

            draw_predicted_path(screen, player, camera.position)

            for thing in cam_updatable:
                thing.update(camera.position)

            for thing in drawable:
                thing.draw(screen, camera.position)

            for asteroid in asteroids:
                if asteroid.check_collision(player):
                    print("Game Over!")
                    player_alive = False
                    game_over = True
                for shot in shots:
                    if asteroid.check_collision(shot):
                        asteroid.split()
                        shot.kill()
            pygame.display.flip()
            clock.tick(FPS_LIMIT)
            asteroid_list = asteroids.sprites()
            for i in range(len(asteroid_list)):
                for j in range(i + 1, len(asteroid_list)):
                    a1 = asteroid_list[i]
                    a2 = asteroid_list[j]
                    if a1.check_collision(a2):
                        a1.a_a_collision(a2)

        elif game_over:
            screen.fill((0, 0, 0))
            for thing in drawable:
                thing.draw(screen, camera.position)
            font = pygame.font.Font('font/Expansiva_bold.ttf', 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

            # Optional: Add "Press R to Retry"
            font_small = pygame.font.Font('font/CreatoDisplay-Medium.ttf', 36)
            subtext0 = font_small.render("Press E - Main Menu", True, (255, 255, 255))
            subtext1 = font_small.render("Press R - Restart", True, (255, 255, 255))
            subtext2 = font_small.render("Press Q - Quit", True, (255, 255, 255))
            screen.blit(subtext0, (screen.get_width() // 2 - subtext0.get_width() // 2, screen.get_height() // 2 + 30))
            screen.blit(subtext1, (screen.get_width() // 2 - subtext1.get_width() // 2, screen.get_height() // 2 + 60))
            screen.blit(subtext2, (screen.get_width() // 2 - subtext2.get_width() // 2, screen.get_height() // 2 + 90))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_r]:
                game_over = False
                player_alive = True
                player, asteroidfield, camera, starfield = start_game()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_e]:
                game_over = False
            clock.tick(FPS_LIMIT)
        else:
            screen.fill((0, 0, 0))

            # Finalize drawing
            font_small = pygame.font.Font('font/CreatoDisplay-Medium.ttf', 36)
            subtext = font_small.render("Press R to Start or Q to Quit", True, (255, 255, 255))
            screen.blit(subtext, (screen.get_width() // 2 - subtext.get_width() // 2, screen.get_height() // 2 + 60))
            pygame.display.flip()


            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if keys[pygame.K_r]:
                game_over = False
                player_alive = True
                player, asteroidfield, camera, starfield = start_game()
            if keys[pygame.K_q]:
                pygame.quit()
            clock.tick(FPS_LIMIT)

if __name__ == "__main__":
    main()