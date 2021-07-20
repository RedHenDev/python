"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
Working! 23 June 2021 :)
13th July 2021 -- new infinite system working! 'soul-swirl'.
14th July 2021 -- Octaves, combing subsets. Some optimisation.

15th To DO

0) DONE Try tweaking optimizations to match subSwirl performance. DONE
1) EQUIVALENT DONE Try using subswirl vector movement instead of polar co-ordinates.
1.1) Better algorithm, which moves from subject pos outward, to find edge of terrain,
then begins generating from there? Also, could combine this with more sophisticated
'phase' algorithm for block-by-block swirling (can be nested in a loop to do more than
one block each update cycle).
2) DONE [2 top most looks great] Reduce Octave complexity -- perhaps just 2 instead of the 4? DONE
2.1) DONE Complete optimizations so that we have silky 60fps -- combine subsets into
larger List of terrains. How is subSwirl achieving this? DONE
2.2) DONE Need to match subset number to terrainLimit. And look over to make sure legit.
2.3) EQUIVALENT DONE [seems to be working fine -- but try doing explicitly?] Shall we create subsets on the fly? So that we can destroy them? Else aren't we combining into older subsets?
3) Create Nether/cave.
4) Attempt vertices deletion/repositioning...
5) DONE! WORKS! Try using a custom model with texture -- see if uv map works!
"""

from random import randint
from ursina import *  
# from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
from numpy import cos
from numpy import sin
from numpy import radians
from numpy import pi
import time
from perlin_noise import PerlinNoise  
from subjective_controller import *
from nMap import nMap

app = Ursina()

window.color = color.rgb(0,222,244)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,211,255)
scene.fog_density = 0.01

# blockMod = load_model('block.obj')
# blockTex = load_texture('block_texture.png')
blockMod = load_model('new_hex.obj')
blockTex = load_texture('grass_64_hex_tex.png')

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
    global rad, radLimit, origin, theta
    global terrainLimit, cs
            
    generateShell()

    if  abs(subject.z - prevZ) >= 1 or \
        abs(subject.x - prevX) >= 1:
        prevZ = subject.z
        prevX = subject.x
        # Reset swirling settings...?
        rad = 0
        theta = 0
        swirling=1*canSwirl
        origin=subject.position

    if time.time() - prevTime > subSpeed:
        for i in range(perCycle):
            genSub()
        
        # -4 since needs to happened before we begin this
        # process, else we don't see toolTip!
        if (cs) >= terrainLimit-4:
            comboTip.enabled=False
            # We disable the toolTip first, so that its
            # messages don't overlap.
            comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + ' subsets of #' + 
                    str(len(terrains)) + ' terrain!',
                    background_color=color.lime)
            comboTip.enabled=True
            
        prevTime = time.time()

def finishTerrain():
    global terrains, cs
    
    for s in subsets:
        s.parent=terrains[-1]
    terrains[-1].combine(auto_destroy=False)
    # Create new empty terrain ready for next combination.
    terrains.append(Entity(texture=blockTex))
    # Current subset back to 0.
    cs = 0

noise = PerlinNoise(octaves=1,seed=99)

terrains = []
terrains.append(Entity(texture=blockTex))
terrainLimit = 420 # How many subsets before combining.
comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + 'subsets of #' + 
                    str(len(terrains)) + ' terrain!')
comboTip.enabled=False

subsets = []
numSubCubes = 32 # def=16Number of cubes per subset.
subSpeed = 0.02 # def=0.02How long before new cubes added to terrain?
perCycle = 64    # def=16How many cubes positioned per update?
radLimit = 999   # def=128How far a radius before swirling off?
cs = 0 # Current subset.
bsf = 0 # Blocks so far.
for i in range(terrainLimit):
    bud = Entity()
    bud.texture=blockTex
    bud.disable()
    subsets.append(bud)
subCubes = []
for i in range(numSubCubes):
    bud = Entity(model=blockMod,scale=0.58,
                scale_y=0.67,scale_z=2,
                texture=blockTex)
    # Add random rotation to help diversify the texture.
    # randRot=random.randint(0,3)
    # bud.rotation_y = 90*randRot
    bud.rotation_x=-90 # To correct for Blender orientation.
    bud.disable()
    subCubes.append(bud)

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
    """
    freq = 12
    amp = 11
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 1
    amp = 3
    y += ((noise([_x/freq,_z/freq]))*amp)
    """
    return floor(y)

rad = 0
theta = 45
def genSub():
    global theta, rad, swirling, radLimit
    global cs, bsf, numSubCubes
    global origin, terrainLimit
    if swirling==-1: return
    # Is there already a terrain block here?
    x = floor(origin.x + rad * cos(radians(theta)))
    z = floor(origin.z + rad * sin(radians(theta)))
    x += z%2*0.5
    if subDic.get('x'+str(x)+'z'+str(z))!='i':
        subCubes[bsf].enable()
        subCubes[bsf].parent=subsets[cs]
        subDic['x'+str(x)+'z'+str(z)]='i'
        subCubes[bsf].x = x
        subCubes[bsf].z = z
        y = subCubes[bsf].y = getPerlin(x,z)
        g = nMap(y,-16,16,0,220) + randint(-20,20)
        subCubes[bsf].color = color.rgb(g,g,g)
        # Time to combine cubes into subset?
        # NB. we need to start bsf again at zero.
        # And, to iterate to next subset.
        # We disable the cube now, since its job
        # is done. For performance.
        subCubes[bsf].disable()
        bsf+=1
        if bsf==numSubCubes:
            subsets[cs].combine(auto_destroy=False)
            subsets[cs].enable()
            cs+=1
            bsf=0
            if cs==terrainLimit:
                finishTerrain()
                comboTip.enabled=False
    else:
        pass
        # If we are here, then we are trying to place
        # a terrain block where one already exists.
        # print('already block at ' + 'x'+str(x)+'z'+str(z))
        # rad+=0.5
        
    # Swirl to next hexagonal terrain position.
    if rad==0:
        theta=45
        rad=0.5
    else: theta+=45/rad
    if theta >= 360:
        theta=45/rad
        rad += 0.5
        if rad > radLimit:
            swirling=-1
            rad=0

shellies = []
shellWidth = 3 # Best performance and physics.
for i in range(shellWidth*shellWidth):
    bud = Entity(model=blockMod,scale=0.6,
    scale_z=1.33,collider='box')
    bud.visible=False
    shellies.append(bud)

def generateShell():
    global shellWidth
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + 
                            subject.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + 
                            subject.z - 0.5*shellWidth)
        shellies[i].y = getPerlin(x,z)

subject = SubjectiveController()
subject.cursor.visible = False
subject.gravity = 0.2
subject.speed = 4
subject.step_height = 1
subject.x = subject.z = 0
subject.y = 64 # Drop height! Allows some terrain to gen :)
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