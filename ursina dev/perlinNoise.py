""" Perlin noise experiments """

from ursina import *
import numpy as nn
import random as ra
import math

#from pnoise import pnoise2
from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController
#from ursina.shaders import lit_with_shadows_shader


sunY = 0

def input(key):
    if key == 'q' or key == 'escape': 
        locked = False
        exit()
    if key == 'g':
        generateChunk(  subject.x,
                        subject.z)

def update():
    global sunY
    sun.rotation_y += 10 * time.dt
    sunY += 0.01
    sun.y += (nn.sin(sunY) * 2.8) * time.dt
    #for b in blocks:
    #    b.update()

class Block:
    def __init__(this, _scale):
        this.ent = Entity(model="cube",color=color.white,
                          scale=_scale,texture='grass_12.png')
        this.origColor = this.ent.color

    def update(this):
        if this.ent.hovered:
            this.ent.color = color.lime
        else: this.ent.color = this.origColor


app = Ursina()

window.color = color.rgb(0,111,184)

sun = Entity(model="sphere",color=color.rgba(222,200,0,200),
                scale=12,
                texture='2k_sun')
sun.y = 22
sun.x = 1990
sun.z = 1990

#ground = Entity(model="cube",color=color.green,scale=(1000,1,1000),collider='mesh')
#ground.y = -10

#pivot = Entity()
#DirectionalLight(parent=scene,y=2,z=3,shadows=True)



# Perlin noise setup.
noise = PerlinNoise(octaves=3,seed=1)

# Our terrain objects.
#urizen = Entity()
urizen2 = Entity()

blocks = []

for i in range(400):
    bub = Block(1)
    bub.ent.parent = urizen2
    blocks.append(bub)

# Terrain data.
urizenData = []
for i in range (25000): 
    x = 1984 + math.floor(i/500)
    z = 1984 + math.floor(i % 500)
    freq = 64
    amp = 12
    y = (noise([x/freq,z/freq])* amp)
    urizenData.append(math.floor(y))

def generateChunk(_ox, _oz):
    for i in range(400):
        #bub = blocks[i]
        whatShade = ra.randint(100,122)
        blocks[i].ent.color=color.rgb(0,whatShade,0)
        blocks[i].origColor = blocks[i].ent.color
        blocks[i].ent.x = math.floor(_ox + math.floor(i/20))
        blocks[i].ent.z = math.floor(_oz + math.floor(i % 20))
        freq = 64
        amp = 12
        blocks[i].ent.y = urizenData[int(((blocks[i].ent.x-1984)*500)+
        blocks[i].ent.z-1984)]
        #blocks[i].ent.parent = urizen2
    
    for b in blocks:
        b.ent.enable()
    urizen2.combine(auto_destroy=False)
    for b in blocks:
        b.ent.disable()
    urizen2.collider = 'mesh'
    urizen2.texture = 'grass_14.png'

generateChunk(1984,1984)

"""
for i in range(100):
    bub = Block(1)
    whatShade = ra.randint(100,122)
    bub.ent.color=color.rgb(whatShade,
    whatShade,whatShade)
    bub.origColor = bub.ent.color
    bub.ent.x = 1984 + math.floor(i/10)
    bub.ent.z = 1984 + math.floor(i % 10)
    freq = 64
    amp = 12
    #bub.ent.scale_y = 10
    #bub.ent.y = math.floor(noise([bub.ent.x/freq,bub.ent.z/freq])* amp)
    bub.ent.y = urizenData[int(((bub.ent.x-1984)*500)+
    bub.ent.z-1984)]
    #bub.ent.collider='cube'
    bub.ent.parent = urizen
    
    #destroy(bub.ent)
    #blocks.append(bub)

urizen.combine()
urizen.collider = 'mesh'
urizen.texture = 'grass_14.png'
"""



#EditorCamera()
#Sky()
scene.fog_density = .03
scene.fog_color = color.rgb(0,111,184)
subject = FirstPersonController(model='cube')
subject.gravity = 0.5
subject.y = 32
subject.x = 1989
subject.z = 1989
app.run()