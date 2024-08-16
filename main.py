import pygame
import sys
import random

pygame.init()

def run(screen=None):
    print('[main] run')

    if not screen:
        pygame.init()
        screen = pygame.display.set_mode((window_width, window_height))


# window creation
window_width, window_height = 1920, 1080
window = pygame.display.set_mode((window_width, window_height))

pygame.font.init()
font = pygame.font.SysFont('Arial', 60)

class Button():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, button_width, button_height)
        self.pressed = False  
    def draw(self, surface):
        
        color = self.color2 if self.pressed else self.color1
        pygame.draw.rect(surface, color, self.rect)


# bottom buttons
button_width = 100
button_height = 40
button_spacing = 20


bar_height = 10
bar_color = (255, 0, 0)


total_buttons = 4
total_width = total_buttons * button_width + (total_buttons - 1) * button_spacing
start_x = (window_width - total_width) // 2

start_y = window_height - button_height - bar_height - 20

button_color1 = (192, 192, 192)
button_color2 = (255, 255, 255)


buttons = [
    Button(start_x + i * (button_width + button_spacing), 
           start_y, 
           button_color1, button_color2, key)
    for i, key in enumerate([
        pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n
    ])
]

# music initialization
# TODO: make this so i can pick a song

pygame.mixer.music.load('songs/2night.mp3')
pygame.mixer.music.play(-1)


# falling notes
class Note:
    def __init__(self, x, y, color, key):
        self.x = x
        self.y = y
        self.color = color
        self.key = key
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, button_width, button_height))
    
    def update(self):
        self.y += 10 

notes = []
note_timer = 0
hit_message = None
miss_message = None

BPM = 130
beat_duration = 60000 / BPM


# note generation (needs to be changed once i can come up with a system that i can create my own charts with right now its completely RNG and barely works)
def generate_notes():
    global note_timer
    if note_timer % int(beat_duration / 2) == 0:  # Generate notes every half-beat
        key = random.choice([pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n])
        x_pos = next(button.x for button in buttons if button.key == key)
        notes.append(Note(x_pos, 0, (0, 255, 0), key))
    note_timer += 1

# this is for the hit and miss text at the top of the screen
def check_note_hits():
    global notes, hit_message, message_timer
    to_remove = []
    for note in notes:
        if note.y > start_y and note.y < start_y + button_height:
            for button in buttons:
                if button.key == note.key and button.pressed:
                    to_remove.append(note)
                    hit_message = "HIT"
                    message_timer = pygame.time.get_ticks()
                    print("Hit detected!")
                    break
    for note in to_remove:
        notes.remove(note)

def check_note_expiration():
    global notes, miss_message, message_timer
    to_remove = [note for note in notes if note.y > window_height]
    if to_remove:
        miss_message = "MISS"
        message_timer = pygame.time.get_ticks()
        print("Miss detected!")
    for note in to_remove:
        notes.remove(note)

def render_text(surface, text, position, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            for button in buttons:
                if event.key == button.key:
                    button.pressed = True
        elif event.type == pygame.KEYUP:
            for button in buttons:
                if event.key == button.key:
                    button.pressed = False

    generate_notes()
    check_note_hits()
    check_note_expiration()

    for note in notes:
        note.update()

    window.fill((0, 0, 0))
    
    for button in buttons:
        button.draw(window)

    bar_rect = pygame.Rect(start_x, start_y + button_height + 10, total_width, bar_height)
    pygame.draw.rect(window, bar_color, bar_rect)
    
    for note in notes:
        note.draw(window)


# this is for the terminal itll display the HIT/MISS messages
    if hit_message or miss_message:
        current_time = pygame.time.get_ticks()
        if current_time - message_timer < 500:
            if hit_message:
                render_text(window, hit_message, (window_width // 2 - 100, 50), (0, 255, 0))
                print("Displaying HIT message.")
            elif miss_message:
                render_text(window, miss_message, (window_width // 2 - 100, 50), (255, 0, 0))
                print("Displaying MISS message.")
        else:
            hit_message = None
            miss_message = None

    pygame.display.update()
    clock.tick(60)

# current shit that needs done soon:

# figure out a way to make my own charts i saw a video of a similar concept that uses text files but it kinda looks shitty and hard to use
# make it so charting can have hold notes
# make the health bar work
# figure out what i want the quirk of the game to be
# put a multiplier counter and accuracy % display somwhere on screen
# basic main menu
# possibly change the UI
# extra options for customization