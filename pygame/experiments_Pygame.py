
import pygame as p
import random

p.init()

WIDTH = 640
HEIGHT = 480

canvas = p.display.set_mode((WIDTH, HEIGHT))

fillColour = (200,0,222)

canvas.fill(fillColour)

gameSpeed = 1000

x = random.randint(0, WIDTH)
y = random.randint(0, HEIGHT)

def input():
    global y, x
    # Get List of keys.
    keys = p.key.get_pressed()
    if keys[p.K_UP]:
        y -= 2
    if keys[p.K_DOWN]:
        y += 2

    # Mouse position.
    mouseP = p.mouse.get_pos()
    mouseX = mouseP[0]
    mouseY = mouseP[1]

    # Chase mouse.
    if mouseX < x:
        x -= 42
    else: x += 42
    if mouseY < y:
        y -= 42
    else: y += 42

running = True

while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    p.time.delay(gameSpeed)

    canvas.fill(fillColour)

    """
    x += random.randint(-1,1)
    y += random.randint(-1,1)
    """
    input()

    p.draw.rect(canvas, (0,0,0) , (x-21, y-21, 42, 42))

    p.display.flip()

p.quit()
