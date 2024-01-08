# Programmer: 
# Description: 

# Import and initialize the pygame library
import pygame
from pygame.locals import *
pygame.init()

# Import functions for drawing gridlines and using sprites
from pygame_grid import make_grid
from ucc_sprite import Sprite

### SET UP GLOBAL CONSTANTS HERE
WIDTH = 640
HEIGHT = 480
BACKGROUND_COLOR = "#444444"
FONT_COLOR = "#6aa84f"
GAME_OVER_COLOR = "crimson"
PAUSED_COLOR = "gold"
START_TIME = 30

# Create and open a pygame screen with the given size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
grid = make_grid()

# Set the title of the pygame screen
pygame.display.set_caption("Frogger")

# Create a clock to keep track of time
clock = pygame.time.Clock()

# Group to hold all of the active sprites
all_sprites = pygame.sprite.LayeredUpdates()

### SET UP YOUR GAME HERE

# Load the images

background_image = pygame.image.load("streets.png")

start_button_image = pygame.image.load("start.png")
start_button_image = pygame.transform.rotozoom(start_button_image, 0, 0.75)
pause_button_image = pygame.image.load("pause.png")
pause_button_image = pygame.transform.rotozoom(pause_button_image, 0, 0.75)
exit_button_image = pygame.image.load("exit.png")
exit_button_image = pygame.transform.rotozoom(exit_button_image, 0, 0.75)

bus_image = pygame.image.load("bus.png")
bus_image = pygame.transform.rotozoom(bus_image, 0, 0.3)
car_image = pygame.image.load("redcar.png")
car_image = pygame.transform.rotozoom(car_image, 0, 0.3)
cruiser_image = pygame.image.load("police.png")
cruiser_image = pygame.transform.rotozoom(cruiser_image, 0, 0.12)
taxi_image = pygame.image.load("taxi.png")
taxi_image = pygame.transform.rotozoom(taxi_image, 0, 0.3)

frog_image = pygame.image.load("frog.png")


# Sprites for the buttons
start_button = Sprite(start_button_image)
start_button.center = (WIDTH / 3, 450)
start_button.add(all_sprites)

pause_button = Sprite(pause_button_image)
pause_button.center = (WIDTH / 3, 450)

exit_button = Sprite(exit_button_image)
exit_button.center = (2 * WIDTH / 3, 450)
exit_button.add(all_sprites)

# Sprites for the vehicles
vehicles = pygame.sprite.Group()

bus = Sprite(bus_image)
bus.center = (WIDTH / 2, 186)

car = Sprite(car_image)
car.center = (3 * WIDTH / 4, 140)
car.direction = 180

cruiser = Sprite(cruiser_image)
cruiser.center = (WIDTH / 4, 292)

taxi = Sprite(taxi_image)
taxi.center = (2 * WIDTH / 3, 340)
taxi.direction = 180

# Sprite for the frog which is control by the user
frog = Sprite(frog_image)
frog.midbottom = (WIDTH / 2, 410)

# Sprite which displays the time remaining
baloo_font_small = pygame.font.Font("Baloo.ttf", 36)
time_left = START_TIME
timer = Sprite(baloo_font_small.render(f"{time_left}", True, FONT_COLOR))
timer.center = (2 * WIDTH / 3, 30)
timer.add(all_sprites)

# Sprite which displays the score
points = 0
score = Sprite(baloo_font_small.render(f"{points}", True, FONT_COLOR))
score.center = (WIDTH / 3, 30)
score.add(all_sprites)

# Sprite with GAME OVER message
baloo_font_large = pygame.font.Font("Baloo.ttf", 72)
game_over = Sprite(baloo_font_large.render("GAME OVER", True, GAME_OVER_COLOR))
game_over.center = (WIDTH / 2, HEIGHT / 2)

# Sprite with PAUSED message
paused = Sprite(baloo_font_large.render("PAUSED", True, PAUSED_COLOR))
paused.center = (WIDTH / 2, HEIGHT / 2)


# Create a timer event for the countdown
COUNTDOWN_EVENT = pygame.event.custom_type()


### DEFINE HELPER FUNCTIONS

# Function that starts a new game or resumes a paused game
def start ():
    global time_left, points

    # If there is no time left, we need to start a new game
    if time_left == 0:
        time_left = START_TIME
        timer.image = baloo_font_small.render(f"{time_left}", True, FONT_COLOR)
        points = 0
        score.image = baloo_font_small.render(f"{points}", True, FONT_COLOR)
        frog.midbottom = (WIDTH / 2, 410)

    # Show all of the vehicles and start their movement
    bus.speed = 1
    bus.add(all_sprites, vehicles)
    car.speed = 4
    car.add(all_sprites, vehicles)
    cruiser.speed = 6
    cruiser.add(all_sprites, vehicles)
    taxi.speed = 3
    taxi.add(all_sprites, vehicles)

    # Show the frog
    frog.add(all_sprites)

    # Swap the start/pause buttons
    pause_button.add(all_sprites)
    start_button.kill()

    # Remove any message sprites
    game_over.kill()
    paused.kill()

    # Start the countdown timer
    pygame.time.set_timer(COUNTDOWN_EVENT, 1000, time_left)


# Function that pauses a game.  If the timer is up, this function ends the game
def pause ():
    global time_left

    # Show the appropriate message based on the time left
    if time_left > 0:
        paused.add(all_sprites)
    else:
        game_over.add(all_sprites)

    # Stop the vehicles and remove them from the screen
    for vehicle in vehicles:
        vehicle.speed = 0
        vehicle.kill()

    # Remove the frog from the screen
    frog.kill()

    # Swap the start/pause buttons
    start_button.add(all_sprites)
    pause_button.kill()

    # Stop the countdown timer
    pygame.time.set_timer(COUNTDOWN_EVENT, 0)


# Main Loop
running = True
while running:
    # Set the frame rate to 60 frames per second
    clock.tick(60)

    for event in pygame.event.get():
        # Check if the quit (X) button was clicked
        if event.type == QUIT:
            running = False

        ### MANAGE OTHER EVENTS SINCE THE LAST FRAME
            
        # If the countdown timer has went off, decrease the time left
        elif event.type == COUNTDOWN_EVENT:
            time_left -= 1
            timer.image = baloo_font_small.render(f"{time_left}", True, FONT_COLOR)

            # If the timer has expired, end the game
            if time_left == 0:
                pause()
        
        # Check for a mouse click
        elif event.type == MOUSEBUTTONDOWN:
            # If the exit button was clicked on, close the game
            if exit_button.mask_contains_point(event.pos):
                running = False

            # If the start_button was clicked on, start the game
            elif start_button.mask_contains_point(event.pos) and start_button.alive():
                start()

            # If the pause button was clicked on, pause the game
            elif pause_button.mask_contains_point(event.pos) and pause_button.alive():
                pause()

        # Check for a key press
        elif event.type == KEYDOWN:
            # If the space bar was pressed, start/pause the game
            if event.key == K_SPACE:
                if frog.alive():
                    pause()
                else:
                    start()

            # If the escape key was pressed, close the game
            if event.key == K_ESCAPE:
                running = False


    ### MANAGE GAME STATE FRAME-BY-FRAME
    
    # Loop through the vehicles group
    for vehicle in vehicles:
        # If the vehicle goes off the screen, wrap around the to the other side
        if vehicle.left > WIDTH:
            vehicle.right = 0
        elif vehicle.right < 0:
            vehicle.left = WIDTH

        # If the vehicle collides with the frog, take off a point and start again
        if pygame.sprite.collide_mask(vehicle, frog):
            points -= 1
            score.image = baloo_font_small.render(f"{points}", True, FONT_COLOR)
            frog.midbottom = (WIDTH / 2, 410)

    # Get the keys that are currently pressed down and move the frog on WASD
    keys_down = pygame.key.get_pressed()
    if frog.alive():
        # On W key, move the frog up
        if keys_down[K_w]:
            frog.y -= 1

            # If the frog reaches the top grass strip, add a point and start again
            if frog.top <= 70:
                points += 1
                score.image = baloo_font_small.render(f"{points}", True, FONT_COLOR)
                frog.midbottom = (WIDTH / 2, 410)

        # On the S key, move the frog down.  Can't go off the playing area
        if keys_down[K_s] and frog.bottom < 420:
            frog.y += 1

        # On the A key, move the frog left.  Can't go off the playing area
        if keys_down[K_a] and frog.left > 0:
            frog.x -= 1

        # On the D key, move the frog right.  Can't go off the playing area
        if keys_down[K_d] and frog.right < WIDTH:
            frog.x += 1
    

    # Update the sprites' locations
    all_sprites.update()

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_image, (0, 60))

    # Redraw the sprites
    all_sprites.draw(screen)

    # Uncomment the next line to show a grid
    # screen.blit(grid, (0,0))

    # Flip the changes to the screen to the computer display
    pygame.display.flip()

# Quit the program
pygame.quit()
