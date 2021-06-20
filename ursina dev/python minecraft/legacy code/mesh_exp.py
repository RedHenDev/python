from ursina import *

app = Ursina()

def input(key):
    if key=='q' or key=='escape':
        quit()

def update():
    e.rotation_y += 0.1

window.color = color.rgb(255,0,255)
e = Entity(model='sphere')

app.run()