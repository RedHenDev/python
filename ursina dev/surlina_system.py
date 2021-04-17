""" Solar system? """


from ursina import *
import numpy as nn

from ursina.prefabs.first_person_controller import FirstPersonController

x = 0

def input(key):
    if key == 'q' or key == 'escape':
        mouse.visible = True
        subject.enabled = False
        quit()

def update():
    global x
    sun.rotation_y += 10 * time.dt
    x += 0.01
    sun.y = (nn.sin(x) * 0.7) 

app = Ursina()

window.color = color.cyan

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),scale=3,texture='2k_sun')
ground = Entity(model="cube",color=color.green,scale=(1000,1,1000),collider='mesh')

ground.y = -10

EditorCamera()
#subject = FirstPersonController()
app.run()
