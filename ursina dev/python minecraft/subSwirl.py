"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
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
scene.fog_density = 0.02

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')

def input(key):
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': generateSubswirl()

def update():
    global prevZ, prevX, prevTime
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
        generateShell()
    
    # Safety net, in case of glitching through terrain.
    if subject.y < -amp:
        subject.y = floor((noise([subject.x/freq,
        subject.z/freq]))*amp)+2

    if time.time() - prevTime > 0.33:
        prevTime = time.time()
        # generateSubswirl()

noise = PerlinNoise(octaves=4,seed=2021)
amp = 32
freq = 100
terrain = Entity(model=None,collider=None)
terrainWidth = 200
subWidth = 8
subArea = subWidth*subWidth
subsets = []
subCubes = []
sci = 0 # subCube index.
currentSubset = 0

# For new position of subset.
currentVec = 0
iterations = 0
toIterate = 1
changes = -1
subPos = Vec2(0,0)
swirlVecs = [
    Vec2(0,0),
    Vec2(0,1),
    Vec2(1,0),
    Vec2(0,-1),
    Vec2(-1,0)
]

def generateSubswirl():
    global currentVec, iterations, changes, subArea
    global subPos, toIterate, swirlVec

    sub = Entity(model=None,parent=terrain)
    subsets.append(sub)

    # Translate position of subset, according to
    # current vector.
    subPos.x += (swirlVecs[currentVec].x*subWidth)
    subPos.y += (swirlVecs[currentVec].y*subWidth)

    for i in range(subArea):
        x = subCubes[i].x = floor(i/subWidth) + subPos.x
        z = subCubes[i].z = floor(i%subWidth) + subPos.y
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[-1]
        b = randrange(188,244)
        subCubes[i].color = color.rgb(0,0,b)
        subCubes[i].visible = False
    
    subsets[-1].combine(auto_destroy=False)
    subsets[-1].texture = grassStrokeTex
    
    # Co-ordinate new vector by iteration around swirl.
    iterations+=1
    if iterations == toIterate:
        currentVec+=1
        if currentVec == len(swirlVecs):
            currentVec = 1
        changes+=1
        iterations = 0
        if changes == 2:
            changes=0
            toIterate+=1

    

# Instantiate our 'ghost' subset cubes.
for i in range(subArea):
    bud = Entity(model='cube')
    subCubes.append(bud)
    

# Instantiate our empty subsets.
# for i in range(int((terrainWidth*terrainWidth)/subWidth)):
#     bud = Entity(model=None)
#     bud.parent = terrain
#     subsets.append(bud)

# def generateSubset():
#     global sci, currentSubset, freq, amp
#     if currentSubset >= len(subsets): 
#         finishTerrain()
#         return
#     for i in range(subWidth):
#         x = subCubes[i].x = floor((i+sci)/terrainWidth)
#         z = subCubes[i].z = floor((i+sci)%terrainWidth)
#         y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
#         subCubes[i].parent = subsets[currentSubset]
#         b = randrange(188,244)
#         subCubes[i].color = color.rgb(0,0,b)
#         subCubes[i].visible = False
    
#     subsets[currentSubset].combine(auto_destroy=False)
#     subsets[currentSubset].texture = grassStrokeTex
#     sci += subWidth
#     currentSubset += 1

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
subject.gravity = 0.0
subject.x = subject.z = 0
subject.y = amp+3 * 2
prevZ = subject.z
prevX = subject.x

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=7.1,
                texture='chicken.png',
                double_sided=True)

generateShell()

app.run()