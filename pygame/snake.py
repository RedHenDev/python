
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

# How many milliseconds between each movement of snake?
gameSpeed = 256
timeStamp = p.time.get_ticks()

# *******

# Setup snake object, segments, etc.

# Size of each square segement.
step = 20

# Snake is a List of Lists...(sub-list is x,y position).
# Or -- odd number is x, and next index in list, y.
snake = [WIDTH/2, HEIGHT/2]

# These lines should append a segment above the previously appended segment.
# So, we should be able to plop this pair into a loop.
snake.append(snake[-2])
snake.append(snake[-2] - step)

segNumb = 7
i = 0
while i < segNumb:
    snake.append(snake[-2])
    snake.append(snake[-2] - step)
    i += 1

# Therefore number of segments is half of length of list.
numberOfSegments = len(snake)/2

# Direction of snake. Up down, left and right?
direction = 2

""" _s = snake """
def renderSnake(_s):
    global step
    numberOfSegments = len(snake)/2

    i = 0
    while  numberOfSegments > i:
        i += 1
        # Draw rectangle at x and y position.
        # So first, we need to find index position of current segment (i).
        # Minus 2 because first index starts at ZERO, not ONE.
        iP = (2 * i) - 2
        # Now, we can create position and size tuples for pygame draw.rect() function.
        tPosition = (_s[iP], _s[iP+1])
        tSize = (step, step)
        # Build a tuple from position and size.
        tRect = (tPosition, tSize)
        tColour = (255,255,255)
        p.draw.rect(canvas, tColour, tRect)
        p.draw.rect(canvas, (0,0,0), tRect, 2)


def moveSnake(_s):
    global direction, step

    # Iterate over segments in reverse order.
    # This is the way the information flows.
    i = int(len(_s) - 1)
    while i > 1:
        _s[i] = _s[int(i-2)]
        i -= 1

    # The head segment (uniquely) is directed by the direction variable.
    # We must do this after body segments, since they need the head's
    # current position, not the new position here changed.
    if direction == 1:
        _s[1] -= step
    elif direction == 2:
        _s[1] += step
    elif direction == 3:
        _s[0] -= step
    elif direction == 4:
        _s[0] += step

# *******



# Dealing with key presses and mouse position etc.
def input():
    global direction
    # Get List of keys.
    keys = p.key.get_pressed()

    if keys[p.K_UP]:
        direction = 1
    elif keys[p.K_DOWN]:
        direction = 2
    elif keys[p.K_LEFT]:
        direction = 3
    elif keys[p.K_RIGHT]:
        direction = 4

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

    # Repaint canvas background colour.
    canvas.fill(fillColour)

    # Get input and apply behaviour etc.
    input()

    # Only move our snake after so many milliseconds.
    timeNow = p.time.get_ticks()
    if timeNow - timeStamp >= gameSpeed:
        print("\a", end = "")
        moveSnake(snake)
        timeStamp = p.time.get_ticks()
        
    renderSnake(snake)
    
    # Refresh canvas.
    p.display.flip()

# If we reach here, Update Loop ended. Exit time.
p.quit()
