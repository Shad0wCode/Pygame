import pygame

# Constants
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 850
PLAYER_HEALTH = 5
ENEMY_HEALTH = 2
PLAYER_SPEED = 9
ENEMY_SPEED = 4
SLASH_SPEED = 10
ROCK_SPEED = 10

class Player:
    def __init__(self, x, y, health, image):
        self.x = x
        self.y = y
        self.image = image
        self.health = health
        self.left_pressed = False
        self.right_pressed = False
        self.slash = None # Initialize the slash object as none

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_pressed = True
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = True
            elif event.key == pygame.K_SPACE:
                self.slash = Slash(self.x + self.image.get_width() // 2, self.y)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = False

    def move(self):
        if self.left_pressed and self.x > 0:
            self.x -= PLAYER_SPEED
        if self.right_pressed and self.x < WINDOW_WIDTH - self.image.get_width():
            self.x += PLAYER_SPEED

    def attack(self):
        if self.slash:
            self.slash.move()

    def check_collision_with_rock(self, rock):
        # Check for collision between Levi and the rock
        # pygame.Rect is used to create a rectangle object with custom dimensions.Generates 4 parameters as following:
            # left: The x-coordinate of the left edge of the rectangle.
            # top: The y-coordinate of the top edge of the rectangle.
            # width: The width of the rectangle.
            # height: The height of the rectangle.     
        levi_rect = pygame.Rect(self.x + 20, self.y + 20, levi_scaled.get_width() - 40, levi_scaled.get_height() - 40)
        rock_rect = rock_scaled.get_rect(topleft=(rock.x, rock.y))
        if levi_rect.colliderect(rock_rect):
            print("Levi is hit by the rock!")
            self.health -= 1  # Decrease Levi's health
            if self.health <= 0:
                print("Game over!")  # Game over logic
                exit()
            rock.reset_position()
    
class Enemy:
    def __init__(self, x, y, health, speed, image):
        self.x = x
        self.y = y
        self.image = image
        self.health = health
        self.speed = speed
        self.direction = 1 # Initial direction 1 for right, -1 for left

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x + self.image.get_width() >= WINDOW_WIDTH:
            self.direction *= -1

    def attack(self):
        pass

    def check_collision_with_slash(self, slash):
        beast_rect = pygame.Rect(self.x, self.y, beast_scaled.get_width(), beast_scaled.get_height())
        slash_rect = pygame.Rect(slash.x, slash.y, slash_scaled.get_width(), slash_scaled.get_height())
        if beast_rect.colliderect(slash_rect):
            print("Beast is hit by the slash!")
            self.health -= 1  # Decrease Beast's health
            if self.health <= 0:
                print("Game over!")  # Game over logic
                exit()
            slash.reset_position()
    
class Slash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit_pressed = False
        self.image = pygame.image.load("slash.png")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.hit_pressed = True

    def move(self):
        self.y -= SLASH_SPEED

    def reset_position(self):
        # Reset slash position (make it disappear)
        self.x = -100
        self.y = -100

class Rock:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    
    def move(self):
        self.y += ROCK_SPEED
        if self.y > WINDOW_HEIGHT:
            self.y = enemy.y + beast_scaled.get_height()
            self.x = enemy.x + (beast_scaled.get_width() - rock_scaled.get_width()) / 2  # Align rock with beast_titan

    def reset_position(self):
        # Reset rock position (make it disappear)
        rock.y = beast_scaled.get_height()
        #rock.x = random.randint(0, window.get_width() - rock_scaled.get_width())  # Randomize rock's horizontal position
        rock.x = enemy.x + (beast_scaled.get_width() - rock_scaled.get_width()) / 2

def start_menu():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True  # Return True if Enter key is pressed to start the game
        if event.type == pygame.QUIT:
            exit()
    return False  # Return False if the game is not started yet

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

start_menu_image = pygame.image.load("start_menu.png")
scale_factor_start_menu_image = 1
start_menu_scaled = pygame.transform.scale(start_menu_image, (int(start_menu_image.get_width() * scale_factor_start_menu_image), int(start_menu_image.get_height() * scale_factor_start_menu_image)))

levi_original = pygame.image.load("levi.png")
rock_original = pygame.image.load("rock.png")
slash_original = pygame.image.load("slash.png")
beast_titan_original = pygame.image.load("beast_titan.png")
scale_factor_levi = 0.8
scale_factor_beast = 0.9
scale_factor_rock = 0.6
scale_factor_slash = 0.1
levi_scaled = pygame.transform.scale(levi_original, (int(levi_original.get_width() * scale_factor_levi), int(levi_original.get_height() * scale_factor_levi)))
beast_scaled = pygame.transform.scale(beast_titan_original, (int(beast_titan_original.get_width() * scale_factor_beast), int(beast_titan_original.get_height() * scale_factor_beast)))
rock_scaled = pygame.transform.scale(rock_original, (int(rock_original.get_width() * scale_factor_rock), int(rock_original.get_height() * scale_factor_rock)))
slash_scaled = pygame.transform.scale(slash_original, (int(slash_original.get_width() * scale_factor_slash), int(slash_original.get_height() * scale_factor_slash)))


# Define Game features
START_MENU = 0
FIRST_STAGE = 1
SECOND_STAGE = 2
game_state = START_MENU
# Create a font object for rendering text
font = pygame.font.Font(None, 28)
start_menu_font = pygame.font.Font(None, 40)

## TODO: ADD HEALTH BAR INSTEAD OF COUNTING
scale_once_beast = False

clock = pygame.time.Clock()

# Game objects
player = Player(0, WINDOW_HEIGHT-levi_scaled.get_height(), PLAYER_HEALTH, levi_scaled)
enemy = Enemy(WINDOW_WIDTH/2, 0, ENEMY_HEALTH, ENEMY_SPEED, beast_scaled)
rock = Rock(enemy.x + beast_scaled.get_width()/2, 0 + beast_scaled.get_height(), rock_scaled)
slash = Slash(-100, -100)

# Runtime events
running = True
while running:
    if game_state == START_MENU:
        window.blit(start_menu_scaled, (0, 0))
        # Start menu text
        start_menu_text = start_menu_font.render(f"Press enter to start!", True, (255, 255, 255))
        window.blit(start_menu_text, (WINDOW_WIDTH/2, 10))
        if start_menu():
            game_state = FIRST_STAGE
    elif game_state == FIRST_STAGE:
        for event in pygame.event.get():
            # Handle events for the player
            player.handle_event(event)
            if event.type == pygame.QUIT:
                exit()

        # Update Levi's position
        player.move()
        player.attack()
        player.check_collision_with_rock(rock)
        enemy.move()
        enemy.check_collision_with_slash(slash)
        rock.move()
        slash.move()

        ### DISPLAY/VISUALS
        # Refresh window with new positions
        window.fill((0, 0, 0))
        window.blit(levi_scaled, (player.x, player.y))
        window.blit(beast_scaled, (enemy.x, enemy.y))
        window.blit(rock_scaled, (rock.x, rock.y))
        if player.slash:
            window.blit(slash_scaled, (player.slash.x, player.slash.y))

        # Render health points text for levi
        levi_text = font.render(f"Levi HP: {player.health}", True, (255, 255, 255))
        window.blit(levi_text, (700, 10))
        # Render health points text for beast
        beast_text = font.render(f"Beast HP: {enemy.health}", True, (255, 255, 255))
        window.blit(beast_text, (700, 30))

        if player.slash:
        # Draw collision rectangles for visual debugging
            beast_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
            slash_rect = pygame.Rect(player.slash.x, player.slash.y, slash_scaled.get_width(), slash_scaled.get_height())

            pygame.draw.rect(window, (255, 255, 255), beast_rect, 2)  # Red rectangle for beast
            pygame.draw.rect(window, (255, 255, 255), slash_rect, 2)  # Green rectangle for slash

    pygame.display.flip()

    # Runs 60 times the loop per second
    clock.tick(60)