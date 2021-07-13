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

13th July 2021 -- infinite system working!
Basically, we subswirl around the player's position, the
player having moved 10 blocks. Maybe we should make this
a new number...a higher number.
Also, we check whether a block already exists before
setting its Perlin position, disabling it and moving to
next subCube if it does -- i.e. for when player backtracks
over terrain they've already visited.
Optimizing by combining whole of terrain would be nice...
Maybe a List of terrains, where we combine 1K subsets at
a go or something? DONE

To Do...

0) Would be nice to use 3 or 4 proper octaves...

1) Reset subset count (for determining when to combine into
a terrain) somehow once we have triggered new swirl pos.
Or rather -- more sophisticated counter as per when
subject has approached edge of generated area so far --
so that a good amount of terrain surrounds them, before
stopping swirling. This could be independent of the
combination of terrains, which is really a separate issue?
Essentially, we always want swirling enabled when subject
is not surrounded by enough terrain.

2) Bug with floating terrain artefact once combining terrain.
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
scene.fog_density = 0.02

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')

def input(key):
    global swirling
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': swirling*=-1

def update():
    global prevZ, prevX, prevTime, subsets, terrainLimit
    global subArea, subSpeed, toIterate, subPos
    global changes, iterations, swirling, comboTip
            
    generateShell()

    if  abs(subject.z - prevZ) >= 10 or \
        abs(subject.x - prevX) >= 10:
        prevZ = subject.z
        prevX = subject.x
        # Reset swirling settings...
        toIterate = 1
        iterations = 0
        changes = -1
        # Center on subject position...
        subPos = Vec2(  floor(subject.x),
                        floor(subject.z))
        swirling = 1
        comboTip.enabled=False
        

    # Safety net, in case of glitching through terrain.
    if subject.y < -amp:
        subject.y = floor((noise([subject.x/freq,
        subject.z/freq]))*amp)+4
        subject.land()

    if time.time() - prevTime > subSpeed:
        generateSubswirl()
        if (len(subsets)) >= terrainLimit-4:
            comboTip.enabled=False
            comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + ' subsets of #' + 
                    str(len(terrains)) + ' terrain!')
            comboTip.enabled=True
        if len(subsets) == terrainLimit:
            finishTerrain()
            comboTip.enabled=False
            swirling=-1
        prevTime = time.time()

noise = PerlinNoise(octaves=24,seed=99)
amp = 24
freq = 664
terrains = []
terrains.append(Entity(model=None))
terrainLimit = 888 # How many subsets before combining.
comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + 'subsets of #' + 
                    str(len(terrains)) + ' terrain!')
comboTip.enabled=False
subWidth = 6
subSpeed = 0.05
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
# Dictionary for recording whether terrain blocks exist
# at location specified in key.
subDic = {
    "0.0,0.0": '0'
}

def generateSubswirl():
    if swirling==-1: return
    global currentVec, iterations, changes, subArea
    global subPos, toIterate, swirlVecs

    sub = Entity(model=None,parent=terrains[0])
    subsets.append(sub)

    # Translate position of subset, according to
    # current vector.
    subPos.x += (swirlVecs[currentVec].x*subWidth)
    subPos.y += (swirlVecs[currentVec].y*subWidth)

    # Make sure we have created a new block, else
    # later on here don't bother calling the
    # costly combine method...
    createdSomeTerrain = False

    for i in range(subArea):
        x = subCubes[i].x = floor(i/subWidth) + subPos.x
        z = subCubes[i].z = floor(i%subWidth) + subPos.y
        # Check if already terrain block here...
        if subDic.get(str(x)+'-'+str(z))=='0': 
            subCubes[i].disable()
            continue
        # No block already here, so we can create one :)
        subCubes[i].enable()
        createdSomeTerrain = True
        # Record this block in dictionary.
        subDic[str(x)+'-'+str(z)]='0'
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[-1]
        g = nMap(y,0,amp/2,64,255)
        subCubes[i].color = color.rgb(0,g,0)
    
    if createdSomeTerrain==True:
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
    bud.scale_y=4   # This must match ghost terrain.
    subCubes.append(bud)

def finishTerrain():
    global subsets, terrains, currentSubset, swirling
    # Since subsets will be destroyed, reparent subcubes.
    for sc in subCubes:
        sc.parent = scene

    terrains[-1].texture = monoTex
    terrains[-1].combine()
    # Create new empty terrain ready for next combination.
    terrains.append(Entity(model=None))
    
    # Make sure our subset list is empty, since its
    # entities have just been destroyed.
    subsets *= 0
    
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
subject.speed = 4
subject.step_height = 1
subject.x = subject.z = subWidth*0.5
subject.y = amp+6
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