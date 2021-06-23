"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
Working! 23 June 2021 :)

We could also generate a load of subsets at start -- to
prevent need of generating these entities on the fly.
This would also mean we have to be a bit more sophisticated
when combining new subsets into terrain mesh...

"""

from operator import sub
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
    global prevZ, prevX, prevTime, subsets, terrainArea
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
        generateShell()
    
    # Safety net, in case of glitching through terrain.
    if subject.y < -amp:
        subject.y = floor((noise([subject.x/freq,
        subject.z/freq]))*amp)+3

    if time.time() - prevTime > 0.5:
        prevTime = time.time()
        generateSubswirl()
        if currentSubset == terrainArea-1:
            finishTerrain()

noise = PerlinNoise(octaves=3,seed=2021)
amp = 32
freq = 100
terrain = Entity(model=None,collider=None)
terrainArea = 100
subWidth = 5
subArea = subWidth*subWidth
subsets = []
subCubes = []
currentSubset = 0


# Generate all subsets now, before running app, so that
# we run more smoothly, not having to instantiate entities
# on the fly.
for i in range(terrainArea):
    sub = Entity(model=None,collider=None)
    sub.disable()
    subsets.append(sub)

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
    global subPos, toIterate, swirlVecs, currentSubset

    # sub = Entity(model=None,parent=terrain)
    # subsets.append(sub)

    # Translate position of subset, according to
    # current vector.
    subPos.x += (swirlVecs[currentVec].x*subWidth)
    subPos.y += (swirlVecs[currentVec].y*subWidth)

    for i in range(subArea):
        x = subCubes[i].x = floor(i/subWidth) + subPos.x
        z = subCubes[i].z = floor(i%subWidth) + subPos.y
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[currentSubset]
        r = randrange(142,244)
        subCubes[i].color = color.rgb(r,0,0)
        subCubes[i].visible = False
    
    subsets[currentSubset].texture = monoTex
    subsets[currentSubset].combine(auto_destroy=False)
    subsets[currentSubset].parent = terrain

    currentSubset+=1

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
    bud.disable()
    subCubes.append(bud)
    

terrainFinished = False
terrain.texture = grassStrokeTex
def finishTerrain():
    global terrainFinished, subsets, terrain, subCubes
    global currentSubset
    
    # for sc in subCubes:
    #     sc.parent = scene
    
    terrain.combine(auto_destroy=False)
    
    # for ss in subsets:
        # ss.model = None
        # ss.parent = scene
    currentSubset=0
    
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
subject.x = subject.z = 0
subject.y = amp+3
prevZ = subject.z
prevX = subject.x

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=7.1,
                texture='chicken.png',
                double_sided=True)

generateShell()

app.run()