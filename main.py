# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import *

def main():
    print("Starting Asteroids!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    
    #Player instance:
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    player = Player(x, y)

    num = 1
    while num > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        screen.fill((0,0,0),rect=None, special_flags=0)
        player.draw(screen)


        pygame.display.flip()
        clock.tick(60)


    #print(f"Screen width: {SCREEN_WIDTH}")
    #print(f"Screen height: {SCREEN_HEIGHT}")
    


if __name__ == "__main__":
    main()