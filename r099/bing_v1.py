import pygame
import sys
import os

# get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the screen size and background color
WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)

# Define the sprite image and its size
SPRITE = current_dir + "/33HU.gif"
SPRITE_WIDTH = 50
SPRITE_HEIGHT = 50

# Define the initial position and speed of the sprite
x = WIDTH / 2 - SPRITE_WIDTH / 2
y = HEIGHT / 2 - SPRITE_HEIGHT / 2
speed_x = 0
speed_y = 0

# Initialize pygame and create the screen and clock objects
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load the sprite image and create a rectangle object for it
sprite = pygame.image.load(SPRITE)
sprite_rect = sprite.get_rect()
sprite_rect.center = (x, y)

# Start the game loop
while True:
    # Fill the screen with the background color
    screen.fill(BACKGROUND)

    # Check for events such as keyboard input or window closing
    for event in pygame.event.get():
        # If the user presses the X button on the window, exit the loop
        if event.type == pygame.QUIT:
            sys.exit()
        # If the user presses a key, change the speed of the sprite accordingly
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x = -5
            elif event.key == pygame.K_RIGHT:
                speed_x = 5
            elif event.key == pygame.K_UP:
                speed_y = -5
            elif event.key == pygame.K_DOWN:
                speed_y = 5
        # If the user releases a key, stop the sprite from moving in that direction
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                speed_y = 0

    # Update the position of the sprite based on its speed and check for boundaries
    x += speed_x
    y += speed_y

    if x < 0:
        x = 0
    elif x > WIDTH - SPRITE_WIDTH:
        x = WIDTH - SPRITE_WIDTH

    if y < 0:
        y = 0
    elif y > HEIGHT - SPRITE_HEIGHT:
        y = HEIGHT - SPRITE_HEIGHT

    # Update the rectangle object of the sprite with its new position
    sprite_rect.center = (x, y)

    # Draw the sprite on the screen
    screen.blit(sprite, sprite_rect)

    # Update the display and set the framerate to 60 FPS
    pygame.display.flip()
    clock.tick(60)