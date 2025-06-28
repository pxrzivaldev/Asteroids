# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():

    def restart_game():
        pygame.sprite.Group.empty(updatable)
        pygame.sprite.Group.empty(drawable)
        pygame.sprite.Group.empty(asteroids)
        pygame.sprite.Group.empty(shots)

        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        Shot.containers = (shots, updatable, drawable)

        player = Player(x, y)
        asteroidfield = AsteroidField()

        return player, asteroidfield

    print("Starting Asteroids!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #init Groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #init Clock
    clock = pygame.time.Clock()
    dt = 0
    
    #Player instance
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    Player.containers = (updatable, drawable)
    player = Player(x, y)

    #Asteroid
    Asteroid.containers = (asteroids, updatable, drawable)
    
    #AsteroidField
    AsteroidField.containers = (updatable)
    asteroidfield = AsteroidField()

    #Shots
    Shot.containers = (shots, updatable, drawable)

    player_alive = False
    game_over = False
    while True:
        if player_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
        
            dt = clock.tick(60) / 1000

            screen.fill((0,0,0),rect=None, special_flags=0)

            for thing in drawable:
                thing.draw(screen)
        
            for thing in updatable:
                thing.update(dt)
        
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
            clock.tick(60)
        elif game_over:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

            # Optional: Add "Press R to Retry"
            font_small = pygame.font.SysFont(None, 36)
            subtext = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            screen.blit(subtext, (screen.get_width() // 2 - subtext.get_width() // 2, screen.get_height() // 2 + 60))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_r]:
                game_over = False
                player_alive = True
                player, asteroidfield = restart_game()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_e]:
                game_over = False
        else:
            # Clear the screen
            screen.fill((0, 0, 0))  # or your background color
            for thing in drawable:
                thing.draw(screen)

            # Finalize drawing
            font_small = pygame.font.SysFont(None, 36)
            subtext = font_small.render("Press R to Start or Q to Quit", True, (255, 255, 255))
            screen.blit(subtext, (screen.get_width() // 2 - subtext.get_width() // 2, screen.get_height() // 2 + 60))
            pygame.display.flip()


            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if keys[pygame.K_r]:
                game_over = False
                player_alive = True
                player, asteroidfield = restart_game()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
    

    


if __name__ == "__main__":
    main()