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
    global rad
            
    generateShell()

    if  abs(subject.z - prevZ) >= 4 or \
        abs(subject.x - prevX) >= 4:
        prevZ = subject.z
        prevX = subject.x
        # Reset swirling settings...?
        rad = 0

    # Safety net, in case of glitching through terrain.
    if subject.y < -amp:
        subject.y = floor((noise([subject.x/freq,
        subject.z/freq]))*amp)+4
        subject.land()

    if time.time() - prevTime > subSpeed:
        genSub()
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
subSpeed = 0
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
subDic = {}

def getPerlin(_x,_z):
    global amp, freq
    return floor((noise([_x/freq,_z/freq]))*amp)

rad = 0
theta = 0
def genSub():
    global theta, rad, swirling
    if swirling==-1: return
    # Is there already a terrain block here?
    x = round(subject.x + rad * cos(radians(theta)))
    z = round(subject.z + rad * sin(radians(theta)))
    if subDic.get(str(x)+str(z))==None:
        bud = Entity(   model='cube',
                    texture=grassStrokeTex)
        subDic['x'+str(x)+'z'+str(z)]='i'
        print(subDic)
        bud.x = x
        bud.z = z
        y = bud.y = getPerlin(x,z)
        bud.color = color.rgb(0,
                    nMap(y,0,amp,64,255),200)
    
    # Swirl to next terrain position.
    theta-=90/((rad+1)*3.14)
    if theta <= -360: 
        theta = 0
        rad += 1





    
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

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=3.1,
                texture='chicken.png',
                double_sided=True,
                collider='mesh')

generateShell()

app.run()