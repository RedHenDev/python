"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
Working! 23 June 2021 :)

We could also generate a load of subsets at start -- to
prevent need of generating these entities on the fly.
This would also mean we have to be a bit more sophisticated
when combining new subsets into terrain mesh...
Tried it. Not successful. No clear gains. But -- perhaps I
did something wrong.

Yeah, I should probably call this 'DeathCraft'. I.e. running
fast...and red mist?

"""

from random import randrange
from ursina import * 
# from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
import time
from perlin_noise import PerlinNoise  
from subjective_controller import *
from nMap import nMap

app = Ursina()

window.color = color.rgb(0,211,222)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,255)
scene.fog_density = 0.01

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')

def input(key):
    global swirling
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': swirling*=-1

def update():
    global prevZ, prevX, prevTime, subsets, terrainLimit
    global subArea, subSpeed
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            generateShell()

    # Safety net, in case of glitching through terrain.
    if subject.y < -amp:
        subject.y = floor((noise([subject.x/freq,
        subject.z/freq]))*amp)+3
        subject.disable()   # To reset physics...
        subject.enable()

    if time.time() - prevTime > subSpeed:
        generateSubswirl()
        
        # if len(subsets) == terrainLimit:
        #     finishTerrain()
        prevTime = time.time()

noise = PerlinNoise(octaves=24,seed=99)
amp = 24
freq = 664
terrain = Entity(model=None,collider=None)
terrain.texture = monoTex
terrainLimit = 300 # How many subsets before combining.
subWidth = 4
subSpeed = 0.04
subArea = subWidth*subWidth
subsets = []
subCubes = []
currentSubset = 0
swirling = 1 # Are we generating terrain?

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
    if swirling==-1: return
    global currentVec, iterations, changes, subArea
    global subPos, toIterate, swirlVecs

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
        g = nMap(y,0,amp/2,64,255)
        subCubes[i].color = color.rgb(0,g,0)
    
    subsets[-1].combine(auto_destroy=False)
    subsets[-1].texture = monoTex

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
    bud.scale_y=4
    # bud.disable()
    subCubes.append(bud)
    
terrain.texture = monoTex
def finishTerrain():
    global subsets, terrain, currentSubset

    # Since subsets will be destroyed, reparent subcubes.
    for sc in subCubes:
        sc.parent = scene

    terrain.combine()
    
    # Make sure our subset list is empty, since its
    # entities have just been destroyed.
    subsets = []
    
shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',scale_y=4,collider='box')

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

subject = SubjectiveController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.speed = 6
subject.step_height = 1
subject.x = subject.z = subWidth*0.5
subject.y = amp+3
prevZ = subject.z
prevX = subject.x

disp = Entity(model='quad',parent=camera.ui,
scale_y=0.1,scale_x=1,y=-0.3,
color=color.rgba(0,0,255,111))

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=3.1,
                texture='chicken.png',
                double_sided=True,
                collider='mesh')

generateShell()

app.run()