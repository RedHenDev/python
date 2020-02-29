
import pygame as p
import random

p.init()

WIDTH = 640
HEIGHT = 480

canvas = p.display.set_mode((WIDTH, HEIGHT))

fillColour = (200,0,222)

canvas.fill(fillColour)

x = random.randint(0, WIDTH)
y = random.randint(0, HEIGHT)

running = True

while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False

    p.time.delay(1)

    canvas.fill(fillColour)

    x += random.randint(-1,1)
    y += random.randint(-1,1)

    p.draw.rect(canvas, (0,0,0) , (x, y, 42, 42))

    p.display.update()

p.quit()

