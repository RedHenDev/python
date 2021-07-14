"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
Working! 23 June 2021 :)

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
from numpy import cos
from numpy import sin
from numpy import radians
import time
from perlin_noise import PerlinNoise  
from subjective_controller import *
from nMap import nMap

app = Ursina()

window.color = color.rgb(0,222,244)
window.exit_button.visible = False

prevTime = time.time()

# scene.fog_color = color.rgb(0,10,222)
# scene.fog_density = 0.02

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')

def input(key):
    global swirling, canSwirl
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': 
        swirling*=-1
        canSwirl*=-1

def update():
    global prevZ, prevX, prevTime, subsets
    global subSpeed, perCycle
    global swirling, comboTip
    global rad, radLimit, origin
            
    generateShell()

    if  abs(subject.z - prevZ) >= 1 or \
        abs(subject.x - prevX) >= 1:
        prevZ = subject.z
        prevX = subject.x
        # Reset swirling settings...?
        rad = 0
        swirling=1*canSwirl
        origin=subject.position

    # Safety net, in case of glitching through terrain.
    # if subject.y < -100:
    #     subject.y = floor((noise([subject.x/freq,
    #     subject.z/freq]))*amp)+4
    #     subject.land()

    if time.time() - prevTime > subSpeed:
        for i in range(perCycle):
            newGen()
            # genSub()
        prevTime = time.time()

noise = PerlinNoise(octaves=1,seed=99)

terrains = []
terrains.append(Entity(model=None))
terrainLimit = 888 # How many subsets before combining.
comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + 'subsets of #' + 
                    str(len(terrains)) + ' terrain!')
comboTip.enabled=False

subsets = []
numSubCubes = 32 # def=32Number of cubes per subset.
subSpeed = 0.0 # def=0How long before new cubes added to terrain?
perCycle = 8    # def=8How many cubes positioned per update?
radLimit = 32   # def=64How far a radius before swirling off?
cs = 0 # Current subset.
bsf = 0 # Blocks so far.
for i in range(999):
    bud = Entity(model=None)
    bud.texture=monoTex
    bud.disable()
    subsets.append(bud)
subCubes = []
for i in range(numSubCubes):
    bud = Entity(model='cube',scale_y=2)
    # Add random rotation to help diversify the texture.
    # randRot=random.randint(1,4)
    # bud.rotation_y = 90*randRot
    # randRot=random.randint(1,4)
    # bud.rotation_z = 90*randRot
    bud.disable()
    subCubes.append(bud)

currentSubset = 0
swirling = 1 # Are we generating terrain?
canSwirl = 1 # Are we allowed to turn on swirling?

# Dictionary for recording whether terrain blocks exist
# at location specified in key.
subDic = {}

def getPerlin(_x,_z):
    y = 0
    freq = 64
    amp = 42      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 32
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)       
    freq = 12
    amp = 11
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 1
    amp = 3
    y += ((noise([_x/freq,_z/freq]))*amp)
    return floor(y)


rad = 0
theta = 0
thetaDir = 1 # Which way are we swirling?
swished = 0  # When swished twice, we increment rad.
def genSub():
    global theta, rad, swirling, radLimit
    global cs, bsf, numSubCubes
    global swished, thetaDir, origin
    if swirling==-1: return
    # Is there already a terrain block here?
    x = round(origin.x + rad * cos(radians(theta)))
    z = round(origin.z + rad * sin(radians(theta)))
    if subDic.get('x'+str(x)+'z'+str(z))!='i':
        subCubes[bsf].enable()
        subCubes[bsf].parent=subsets[cs]
        subDic['x'+str(x)+'z'+str(z)]='i'
        # print(subDic)
        subCubes[bsf].x = x
        subCubes[bsf].z = z
        y = subCubes[bsf].y = getPerlin(x,z)
        r = 0
        b = 0
        g = nMap(y,-16,16,0,255)
        subCubes[bsf].color = color.rgb(r,g,b)

        # Time to combine cubes into subset?
        # NB. this will 'destroy' its child cubes,
        # so we need to start bsf again at zero.
        # And, to iterate to next subset.
        subCubes[bsf].disable()
        bsf+=1
        if bsf==numSubCubes:
            subsets[cs].combine(auto_destroy=False)
            subsets[cs].enable()
            cs+=1
            bsf=0
    else:
        pass
        #print('already block at ' + 'x'+str(x)+'z'+str(z))
        #rad+=1
        
    # Swirl to next terrain position.
    theta-=(128/((rad+1)*3.14))*thetaDir
    if theta <= -360: 
        theta = 0
        rad += 1
        if rad > radLimit:
            swirling=-1
            rad=1
    
def newGen():
    global theta, rad, swirling, radLimit
    global cs, bsf, numSubCubes
    global swished, thetaDir, origin
    if swirling==-1: return
    # Is there already a terrain block here?
    x = floor(origin.x - radLimit + rad)
    z = floor(origin.z + 12)
    if subDic.get('x'+str(x)+'z'+str(z))!='i':
        subCubes[bsf].enable()
        subCubes[bsf].parent=subsets[cs]
        subDic['x'+str(x)+'z'+str(z)]='i'
        # print(subDic)
        subCubes[bsf].x = x
        subCubes[bsf].z = z
        y = subCubes[bsf].y = getPerlin(x,z)
        r = 0
        b = 0
        g = nMap(y,-16,16,0,255)
        subCubes[bsf].color = color.rgb(r,g,b)

        # Time to combine cubes into subset?
        # NB. this will 'destroy' its child cubes,
        # so we need to start bsf again at zero.
        # And, to iterate to next subset.
        subCubes[bsf].disable()
        bsf+=1
        if bsf==numSubCubes:
            subsets[cs].combine(auto_destroy=False)
            subsets[cs].enable()
            cs+=1
            bsf=0
    else:
        pass
        # origin.z+=1
        rad = 0
        #print('already block at ' + 'x'+str(x)+'z'+str(z))
        #rad+=1
        
    # Swirl to next terrain position.
    rad+=1
    if rad==radLimit*2:
        origin.z-=1
        rad=0

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',scale_y=2,collider='box')
    bud.visible=False
    shellies.append(bud)

def generateShell():
    global shellWidth, amp, freq
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + 
                            subject.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + 
                            subject.z - 0.5*shellWidth)
        shellies[i].y = getPerlin(x,z)

subject = SubjectiveController()
subject.cursor.visible = False
subject.gravity = 0.2
subject.speed = 3
subject.step_height = 1
subject.x = subject.z = 0
subject.y = 12
prevZ = subject.z
prevX = subject.x
origin = subject.position

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=3.1,
                texture='chicken.png',
                double_sided=True,
                collider='mesh')

generateShell()

app.run()