import pygame as p
import random as ra
from math import floor
from numba import jit

p.init()

WIDTH=700
HEIGHT=700
step=1

canvas=p.display.set_mode((WIDTH,HEIGHT))

canvas.fill((255,255,255))

running=True
zoom=2000

# @numba.njit(fastmath=True)
# @jit
def render():
    global zoom
    for x in range(WIDTH):
        for y in range(HEIGHT):
            dx = a = (x - (WIDTH*0.5))/zoom-0.12
            dy = b = (y - (HEIGHT*0.5))/zoom-0.86
            # zoom*=1.04
            for i in range(1,200,step):
                d = (a*a)-(b*b)+dx
                H = d > 200
                b = 2*(a*b)+dy
                a = d
                if (H):
                    r=255/200*i*3
                    if r > 255: r =255
                    c=(r,0,200/255*i*0.5)
                    canvas.set_at((x,y),c)
                    # p.draw.rect(canvas,c,(x,y,step,step))
                    break
    p.display.update()

render()

while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running=False
    # render()
    # p.time.delay(3000)

    

p.quit()