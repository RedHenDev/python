
import pygame as p
import random

# Initialize pygame (needed here so can work on different platforms).
p.init()

# Canvas display dimensions.
WIDTH = 1024
HEIGHT = 812

# Create our pygame 'surface' - I'll call this window display a 'canvas'.
canvas = p.display.set_mode((WIDTH, HEIGHT))

# Canvas background colour.
fillColour = (random.randint(70,255),0,random.randint(70,255))

# Delay in milliseconds at start of Update Loop.
gameSpeed = 100


# Dealing with key presses and mouse position etc.
def input():

    # Get List of keys.
    keys = p.key.get_pressed()

    if keys[p.K_UP]:
        temp = "I do nothing"
        # Do something

    # Mouse position.
    mouseP = p.mouse.get_pos()
    mouseX = mouseP[0]
    mouseY = mouseP[1]

# Update loop running?
running = True

# Update loop.
while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    # Delay (ms) before each frame/update.
    p.time.delay(gameSpeed)

    # Repaint canvas background colour.
    canvas.fill(fillColour)

    # Get input and apply behaviour etc.
    input()

    
    # Refresh canvas.
    p.display.flip()

# If we reach here, Update Loop ended. Exit time.
p.quit()
