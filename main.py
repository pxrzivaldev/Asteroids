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

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()



    clock = pygame.time.Clock()
    dt = 0

    
    #Player instance:
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    Player.containers = (updatable, drawable)

    player = Player(x, y)
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        dt = clock.tick(60) / 1000

        screen.fill((0,0,0),rect=None, special_flags=0)

        for thing in drawable:
            thing.draw(screen)
        
        for thing in updatable:
            thing.update(dt)
        

        pygame.display.flip()
        
        clock.tick(60)



    #print(f"Screen width: {SCREEN_WIDTH}")
    #print(f"Screen height: {SCREEN_HEIGHT}")
    


if __name__ == "__main__":
    main()