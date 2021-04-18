""" Solar system? """

from ursina import *
import numpy as nn
import random as ra

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

x = 0

def input(key):
    if key == 'q' or key == 'escape':
        mouse.visible = True
        #subject.enabled = False
        quit()

def update():
    global x
    sun.rotation_y += 10 * time.dt
    x += 0.01
    sun.y = (nn.sin(x) * 0.7)

    for p in planets:
        p.rotation()
        p.bob()

class Planet:
    def __init__(this, radius, colour):
        this.ent = Entity(model="sphere",color=colour,scale=radius,texture='2k_moon')
        this.rotSpeed = ra.randint(20,100) * 0.1

    def rotation(this):
        this.ent.rotation_y += this.rotSpeed * time.dt

    def bob(this):
        global x
        this.ent.y += (nn.sin(this.ent.rotation_y) * this.ent.scale.x * 0.01)

app = Ursina()

window.color = color.rgb(184,0,184)

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),scale=12,texture='2k_sun')
#ground = Entity(model="cube",color=color.green,scale=(1000,1,1000),collider='mesh')
#ground.y = -10

#pivot = Entity()
#DirectionalLight(parent=pivot,y=2,z=3,shadows=True)

planets = []

for i in range(100):
    bub = Planet(ra.randint(3,14), color.white)
    whatShade = ra.randint(11,255)
    bub.ent.color=color.rgb(whatShade,whatShade,whatShade)
    bub.ent.x = ra.randint(-100,100)
    bub.ent.y = ra.randint(-100,100)
    bub.ent.z = ra.randint(-100,100)
    #bub.ent.shader = lit_with_shadows_shader
    planets.append(bub)
    

EditorCamera()
#Sky()
#subject = FirstPersonController()
app.run()
