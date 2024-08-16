#i dont really like this atm so im not using it

try:
    image = pygame.image.load('assets/bg.png')
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()
    
scaled_image = pygame.transform.scale(image, (window_width, window_height))


def draw_background(surface):
    surface.blit(scaled_image, (0, 0))



        window.fill((0, 0, 0))
    draw_background(window)