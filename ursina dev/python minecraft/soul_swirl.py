"""
Minecraft in Python, with Ursina.
New idea for a 'subSwirl' system: June 22 2021.
Working! 23 June 2021 :)
13th July 2021 -- infinite system working!
14th July 2021 -- Octaves, combing subsets. Some optimisation.

15th To DO

0) Try tweaking optimizations to match subSwirl performance. DONE
1) Try using subswirl vector movement instead of polar co-ordinates.
1.1) OR -> better algorithm, which moves from subject pos outward, to find edge of terrain,
then begins generating from there? Also, could combine this with more sophisticated
'phase' algorithm for block-by-block swirling (can be nested in a loop to do more than
one block each update cycle).
2) Reduce Octave complexity -- perhaps just 2 instead of the 4? DONE
2.1) Complete optimizations so that we have silky 60fps -- combine subsets into
larger List of terrains. How is subSwirl achieving this? DONE
2.2) Need to match subset number to terrainLimit. And look over to make sure legit.
3) Create Nether/cave.
4) Attempt vertices deletion/repositioning...
5) Try using a custom model with texture -- see if uv map works!
"""

from random import randint, randrange
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

scene.fog_color = color.rgb(0,211,255)
scene.fog_density = 0.01

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')
blockMod = load_model('block.obj')
blockTex = load_texture('block_texture.png')

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
    global terrainLimit, cs
            
    generateShell()

    if  abs(subject.z - prevZ) >= 10 or \
        abs(subject.x - prevX) >= 10:
        prevZ = subject.z
        prevX = subject.x
        # Reset swirling settings...?
        rad = 0
        swirling=1*canSwirl
        origin=subject.position

    if time.time() - prevTime > subSpeed:
        for i in range(perCycle):
            genSub()
        
        if (cs) >= terrainLimit-4:
            comboTip.enabled=False
            comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + ' subsets of #' + 
                    str(len(terrains)) + ' terrain!')
            comboTip.enabled=True
            
        if cs == terrainLimit-1:
            finishTerrain()
            comboTip.enabled=False
            
        prevTime = time.time()

def finishTerrain():
    global terrains, cs
    # Since subsets will be destroyed, reparent subcubes.
    # Legacy!
    # for sc in subCubes:
    #     sc.parent = scene

    # terrains[-1].texture = blockTex
    terrains[-1].combine(auto_destroy=False)
    # Create new empty terrain ready for next combination.
    terrains.append(Entity(model=None))
    
    # Make sure our subset list is empty, since its
    # entities have just been destroyed.
    # No they haven't! That was legacy...
    #subsets *= 0
    cs = 0

noise = PerlinNoise(octaves=1,seed=99)

terrains = []
terrains.append(Entity(model=None))
terrainLimit = 100 # How many subsets before combining.
comboTip = Tooltip('<pink>Warning! Combining ' + 
                    str(terrainLimit) + 'subsets of #' + 
                    str(len(terrains)) + ' terrain!')
comboTip.enabled=False

subsets = []
numSubCubes = 16 # def=16Number of cubes per subset.
subSpeed = 0.0 # def=0.02How long before new cubes added to terrain?
perCycle = 16    # def=16How many cubes positioned per update?
radLimit = 128   # def=128How far a radius before swirling off?
cs = 0 # Current subset.
bsf = 0 # Blocks so far.
for i in range(100):
    bud = Entity(model=None)
    bud.texture=blockTex
    bud.disable()
    subsets.append(bud)
subCubes = []
for i in range(numSubCubes):
    bud = Entity(model=blockMod,scale_y=1)
    # Add random rotation to help diversify the texture.
    randRot=random.randint(1,4)
    bud.rotation_y = 90*randRot
    # randRot=random.randint(1,4)
    # bud.rotation_z = 90*randRot
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
theta = 0
thetaDir = 1 # Which way are we swirling?
swished = 0  # When swished twice, we increment rad.
def genSub():
    global theta, rad, swirling, radLimit
    global cs, bsf, numSubCubes
    global thetaDir, origin
    if swirling==-1: return
    # Is there already a terrain block here?
    x = floor(origin.x + rad * cos(radians(theta)))
    z = floor(origin.z + rad * sin(radians(theta)))
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
        g = nMap(y,-16,16,0,220) + randint(-20,20)
        subCubes[bsf].color = color.rgb(g,g,g)
        

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
    if rad==0:
       theta=0
       rad=0.5
    else: theta+=45/rad
    # theta-=(128/((rad+1)*3.14))*thetaDir
    if theta >= 360: 
        theta = 0
        rad += 0.5
        if rad > radLimit:
            swirling=-1
            rad=0

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',scale_y=1,collider='box')
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