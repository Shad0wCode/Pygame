import pygame
import math
import random


# Load screen and images

pygame.init()
window = pygame.display.set_mode((640, 640))

levi_original = pygame.image.load("levi.png")
jaw_titan__original = pygame.image.load("jaw_titan.png")
beast_titan_original = pygame.image.load("beast_titan.png")
rock_original = pygame.image.load("rock.png")
scale_factor_levi = 0.8
scale_factor_jaw = 0.8
scale_factor_beast = 0.8
scale_factor_rock = 0.6
levi_scaled = pygame.transform.scale(levi_original, (int(levi_original.get_width() * scale_factor_levi), int(levi_original.get_height() * scale_factor_levi)))
jaw_scaled = pygame.transform.scale(jaw_titan__original, (int(jaw_titan__original.get_width() * scale_factor_jaw), int(jaw_titan__original.get_height() * scale_factor_jaw)))
beast_scaled = pygame.transform.scale(beast_titan_original, (int(beast_titan_original.get_width() * scale_factor_beast), int(beast_titan_original.get_height() * scale_factor_beast)))
rock_scaled = pygame.transform.scale(rock_original, (int(rock_original.get_width() * scale_factor_rock), int(rock_original.get_height() * scale_factor_rock)))

# Instantiate initial position of images
levi_x = 0
levi_y = 640-levi_scaled.get_height()
jaw_x = 0
jaw_y = 0
beast_x = 0
beast_y = 0
rock_x = 0 + beast_scaled.get_width()/2
rock_y = 0 + beast_scaled.get_height()

# Define Levi's initial health points
levi_health = 5
beast_velocity = 2

# Create a font object for rendering text
font = pygame.font.Font(None, 36)

to_right = False
to_left = False

clock = pygame.time.Clock()

# Runtime events
while True:
    for event in pygame.event.get():
        # When key is pressed, movement continues as long as key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
        # When the key is not pressed, movement stops
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
        if event.type == pygame.QUIT:
            exit()

    # Moving Levi with keyboard
    if to_right:
        levi_x += 4
    if to_left:
        levi_x -= 4

    # Move the beast titan
    beast_x += beast_velocity

    # Reverse direction if beast titan reaches the edge of the screen
    if beast_velocity > 0 and beast_x + beast_scaled.get_width() >= window.get_width():
        beast_velocity = -beast_velocity
    elif beast_velocity < 0 and beast_x <= 0:
        beast_velocity = -beast_velocity
    
    rock_y += 4

    # Check if the rock has gone beyond the bottom of the screen
    if rock_y > window.get_height():
        # Reset rock position (make it disappear) and set it to start from beast_titan's position
        rock_y = beast_scaled.get_height()
        rock_x = beast_x + (beast_scaled.get_width() - rock_scaled.get_width()) / 2  # Align rock with beast_titan

    # Rock collision with Levi logic
    # Check for collision between Levi and the rock
    levi_rect = levi_scaled.get_rect(topleft=(levi_x, levi_y))
    rock_rect = rock_scaled.get_rect(topleft=(rock_x, rock_y))
    if levi_rect.colliderect(rock_rect):
        print("Levi is hit by the rock!")
        levi_health -= 1  # Decrease Levi's health
        if levi_health <= 0:
            print("Game over!")  # Game over logic
            exit()
        # Reset rock position (make it disappear)
        rock_y = beast_scaled.get_height()
        #rock_x = random.randint(0, window.get_width() - rock_scaled.get_width())  # Randomize rock's horizontal position
        rock_x = beast_x + (beast_scaled.get_width() - rock_scaled.get_width()) / 2

    # Refresh window with new positions
    window.fill((0, 0, 0))
    window.blit(levi_scaled, (levi_x, levi_y))
    window.blit(beast_scaled, (beast_x, beast_y))
    window.blit(rock_scaled, (rock_x, rock_y))

    # Render health points text
    health_text = font.render(f"Health: {levi_health}", True, (255, 255, 255))
    window.blit(health_text, (500, 10))

    pygame.display.flip()

    #x += velocity
    #if velocity > 0 and x+levi_scaled.get_width() >= 640:
    #    velocity = -velocity
    #if velocity < 0 and x <= 0:
    #   velocity = -velocity  

    # Runs 60 times the loop per second
    clock.tick(60)