import pygame

def start_menu():

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True  # Return True if Enter key is pressed to start the game
        if event.type == pygame.QUIT:
            exit()
    return False  # Return False if the game is not started yet

# Load screen and images

pygame.init()

window_x = 850
window_y = 850
window = pygame.display.set_mode((window_x, window_y))

start_menu_image = pygame.image.load("start_menu.png")
scale_factor_start_menu_image = 1
start_menu_scaled = pygame.transform.scale(start_menu_image, (int(start_menu_image.get_width() * scale_factor_start_menu_image), int(start_menu_image.get_height() * scale_factor_start_menu_image)))

levi_original = pygame.image.load("levi.png")
jaw_titan__original = pygame.image.load("jaw_titan.png")
beast_titan_original = pygame.image.load("beast_titan.png")
rock_original = pygame.image.load("rock.png")
slash_original = pygame.image.load("slash.png")
scale_factor_levi = 0.8
scale_factor_jaw = 0.8
scale_factor_beast = 0.8
scale_factor_rock = 0.6
scale_factor_slash = 0.1
levi_scaled = pygame.transform.scale(levi_original, (int(levi_original.get_width() * scale_factor_levi), int(levi_original.get_height() * scale_factor_levi)))
jaw_scaled = pygame.transform.scale(jaw_titan__original, (int(jaw_titan__original.get_width() * scale_factor_jaw), int(jaw_titan__original.get_height() * scale_factor_jaw)))
beast_scaled = pygame.transform.scale(beast_titan_original, (int(beast_titan_original.get_width() * scale_factor_beast), int(beast_titan_original.get_height() * scale_factor_beast)))
rock_scaled = pygame.transform.scale(rock_original, (int(rock_original.get_width() * scale_factor_rock), int(rock_original.get_height() * scale_factor_rock)))
slash_scaled = pygame.transform.scale(slash_original, (int(slash_original.get_width() * scale_factor_slash), int(slash_original.get_height() * scale_factor_slash)))

# Instantiate initial position of images
levi_x = 0
levi_y = window_y-levi_scaled.get_height()
jaw_x = 0
jaw_y = 0
beast_x = window_x/2
beast_y = 0
rock_x = beast_x + beast_scaled.get_width()/2
rock_y = 0 + beast_scaled.get_height()
slash_x = -100 # initial position for the slash outside the screen
slash_y = -100 # initial position for the slash outside the screen

# Define Game features
START_MENU = 0
PLAYING = 1
game_state = START_MENU

levi_health = 5
beast_health = 5
beast_velocity = 4
slash_velocity = -10

# Create a font object for rendering text
font = pygame.font.Font(None, 28)
start_menu_font = pygame.font.Font(None, 40)

to_right = False
to_left = False
slash_pressed = False
slash_on_screen = False

clock = pygame.time.Clock()

# Runtime events
while True:
    if game_state == START_MENU:
        window.blit(start_menu_scaled, (0, 0))
        # Start menu text
        start_menu_text = start_menu_font.render(f"Press enter to start!", True, (255, 255, 255))
        window.blit(start_menu_text, (window_x/2, 10))
        if start_menu():
            game_state = PLAYING
    elif game_state == PLAYING:
        for event in pygame.event.get():
            # When key is pressed, movement continues as long as key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    to_left = True
                if event.key == pygame.K_RIGHT:
                    to_right = True
                # Hit enabled with space key
                if event.key == pygame.K_SPACE:
                    if not slash_on_screen:
                        slash_pressed = True
                        slash_on_screen = True
                        slash_x = levi_x + levi_scaled.get_width() // 2
                        slash_y = levi_y
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
            levi_x += 9
        if to_left:
            levi_x -= 9

        # Move slash/hit image when space is pressed
        if slash_pressed:
            slash_y += slash_velocity
            slash_on_screen = True 

        # Move the beast titan
        beast_x += beast_velocity

        # Reverse direction if beast titan reaches the edge of the screen
        if beast_velocity > 0 and beast_x + beast_scaled.get_width() >= window.get_width():
            beast_velocity = -beast_velocity
        elif beast_velocity < 0 and beast_x <= 0:
            beast_velocity = -beast_velocity
        
        rock_y += 10

        # Check if the rock has gone beyond the bottom of the screen
        if rock_y > window.get_height():
            # Reset rock position (make it disappear) and set it to start from beast_titan's position
            rock_y = beast_scaled.get_height()
            rock_x = beast_x + (beast_scaled.get_width() - rock_scaled.get_width()) / 2  # Align rock with beast_titan

        # Check if the slash has gone beyond the top of the screen
        if slash_y < 0:
            # Make slash position disappear
            slash_y = -100  # Set y-coordinate outside the screen
            slash_x = -100  # Set x-coordinate outside the screen 
            slash_on_screen = False
            slash_pressed = False

        # Rock collision with Levi logic
        # Check for collision between Levi and the rock
        # pygame.Rect is used to create a rectangle object with custom dimensions.Generates 4 parameters as following:
            # left: The x-coordinate of the left edge of the rectangle.
            # top: The y-coordinate of the top edge of the rectangle.
            # width: The width of the rectangle.
            # height: The height of the rectangle.     
        levi_rect = pygame.Rect(levi_x + 20, levi_y + 20, levi_scaled.get_width() - 40, levi_scaled.get_height() - 40)
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

        # Slash collision with Beast Titan logic
        beast_rect = pygame.Rect(beast_x, beast_y, beast_scaled.get_width(), beast_scaled.get_height())
        slash_rect = slash_scaled.get_rect(topleft=(slash_x, slash_y))
        if beast_rect.colliderect(slash_rect):
            print("Beast is hit with slash!")
            beast_health -= 1 # Decrease beast titan health
            if beast_health <= 0:
                print("You won!") # Game over logic
                exit()
            # Reset slash position (make it disappear)
            slash_y = -100  # Set y-coordinate outside the screen 
            slash_x = -100  # Set x-coordinate outside the screen

        # Levi can slash back

        # Refresh window with new positions
        window.fill((0, 0, 0))
        window.blit(levi_scaled, (levi_x, levi_y))
        window.blit(beast_scaled, (beast_x, beast_y))
        window.blit(rock_scaled, (rock_x, rock_y))
        window.blit(slash_scaled, (slash_x, slash_y))

        # Render health points text for levi
        levi_text = font.render(f"Levi HP: {levi_health}", True, (255, 255, 255))
        window.blit(levi_text, (500, 10))
        # Render health points text for beast
        beast_text = font.render(f"Beast HP: {beast_health}", True, (255, 255, 255))
        window.blit(beast_text, (500, 30))

    pygame.display.flip()

        #x += velocity
        #if velocity > 0 and x+levi_scaled.get_width() >= 640:
        #    velocity = -velocity
        #if velocity < 0 and x <= 0:
        #   velocity = -velocity  

        # Runs 60 times the loop per second
    clock.tick(60)