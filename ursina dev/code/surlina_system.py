""" Solar system? """

from ursina import *
import numpy as nn
import random as ra
import math

from noise import pnoise2

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

x = 0

def input(key):
    if key == 'q' or key == 'escape': 
        locked = False
        exit()

def update():
    global x
    sun.rotation_y += 10 * time.dt
    x += 0.01
    sun.y += (nn.sin(x) * 0.7)

    #for p in planets:
      #  p.rotation()
        #p.bob()



class Planet:
    def __init__(this, radius, colour):
        this.ent = Entity(model="sphere",color=colour,
                          scale=radius,texture='2k_moon')
        this.rotSpeed = ra.randint(20,100) * 0.1

    def rotation(this):
        this.ent.rotation_y += this.rotSpeed * time.dt
        if this.ent.rotation_y > 10 and this.ent.rotation_y < 14:
            this.ent.color = color.random_color()

    def bob(this):
        global x
        this.ent.y += (nn.sin(this.ent.rotation_y) * this.ent.scale.x * 0.01)


class Block:
    def __init__(this, _scale):
        this.ent = Entity(model="cube",color=color.white,
                          scale=_scale,texture='grass_12.png')

app = Ursina()

window.color = color.rgb(184,0,184)

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),scale=12,
             texture='2k_sun')
sun.y = 222

#ground = Entity(model="cube",color=color.green,scale=(1000,1,1000),collider='mesh')
#ground.y = -10

#pivot = Entity()
#DirectionalLight(parent=scene,y=2,z=3,shadows=True)

planets = []

blocks = []

for i in range(800):
    #bub = Planet(ra.randint(3,14), color.white)
    bub = Block(1)
    whatShade = ra.randint(11,255)
    bub.ent.color=color.rgb(whatShade,whatShade,whatShade)
    #bub.ent.x = ra.randint(-100,100)
    #bub.ent.y = ra.randint(-100,100)
    #bub.ent.z = ra.randint(-100,100)
    bub.ent.x = math.floor(i/20)
    bub.ent.z = (i % 20)
    freq = 32
    amp = 12
    bub.ent.y = math.floor(pnoise2(9999+bub.ent.x/freq,-99987+bub.ent.z/freq)* amp)
    bub.ent.collider='cube'
    #bub.ent.shader = lit_with_shadows_shader
    #planets.append(bub)
    blocks.append(bub)
    

#EditorCamera()
#Sky()
#scene.fog_density = .1
subject = FirstPersonController(model='sphere')
subject.gravity = 0.5
subject.y = 64
subject.x = 5
subject.z = 5
app.run()
