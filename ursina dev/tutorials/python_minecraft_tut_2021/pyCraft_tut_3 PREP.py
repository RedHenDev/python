"""
Minecraft in Python, with Ursina, tut 3 PREP ONLY
"""

from random import randrange
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
import time
from perlin_noise import PerlinNoise  

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,200,211)
scene.fog_density = 0.04

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('grass_mono.png')

def input(key):
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': generateSubset()

def update():
    global prevZ, prevX, prevTime
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
        generateShell()

    if time.time() - prevTime > 0.25:
        prevTime = time.time()
        generateSubset()

noise = PerlinNoise(octaves=2,seed=2021)
amp = 24
freq = 100
terrain = Entity(model=None,collider=None)
terrainWidth = 100
subWidth = int(terrainWidth/2)
subsets = []
subCubes = []
sci = 0 # subCube index.
currentSubset = 0

# Instantiate our 'ghost' subset cubes.
for i in range(subWidth):
    bud = Entity(model='cube')
    subCubes.append(bud)

# Instantiate our empty subsets.
for i in range(int((terrainWidth*terrainWidth)/subWidth)):
    bud = Entity(model=None)
    bud.parent = terrain
    subsets.append(bud)

def generateSubset():
    global sci, currentSubset, freq, amp
    if currentSubset >= len(subsets): 
        finishTerrain()
        return
    for i in range(subWidth):
        x = subCubes[i].x = floor((i+sci)/terrainWidth)
        z = subCubes[i].z = floor((i+sci)%terrainWidth)
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[currentSubset]
        r = randrange(100,200)
        subCubes[i].color = color.rgb(r,0,0)
        subCubes[i].visible = False
    
    subsets[currentSubset].combine(auto_destroy=False)
    subsets[currentSubset].texture = grassStrokeTex
    sci += subWidth
    currentSubset += 1

terrainFinished = False
def finishTerrain():
    global terrainFinished
    if terrainFinished==True: return
    terrain.combine()
    terrainFinished = True
    subject.y = 64
    terrain.texture = monoTex


# for i in range(terrainWidth*terrainWidth):
#     bud = Entity(model='cube',color=color.green)
#     bud.x = floor(i/terrainWidth)
#     bud.z = floor(i%terrainWidth)
#     bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
#     bud.parent = terrain

# terrain.combine()
# terrain.collider = 'mesh'
# terrain.texture = grassStrokeTex

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',collider='box')
    bud.visible=False
    shellies.append(bud)

def generateShell():
    global shellWidth, amp, freq
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + 
                            subject.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + 
                            subject.z - 0.5*shellWidth)
        shellies[i].y = floor((noise([x/freq,z/freq]))*amp)




subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.x = subject.z = 25
subject.y = 32
prevZ = subject.z
prevX = subject.x

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=7.1,
                texture='chicken.png',
                double_sided=True)

generateShell()

app.run()