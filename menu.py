import pygame
import main

def run(screen=None):
    print('[menu] run')

    if not screen:
        pygame.init()
        screen = pygame.display.set_mode((window_width, window_height))

        window_width, window_height = 1920, 1080

    mainloop(screen)

def mainloop(screen):
    print('[menu] mainloop')

    running = True
    while running:

        print('running menu ...')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # skip rest of code
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    main.run(screen)  # run game

        screen.fill((255,0,0))
        pygame.display.flip()


if __name__ == '__main__':
    run()