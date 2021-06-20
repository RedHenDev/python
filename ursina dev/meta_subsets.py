"""
June 19 2021 Mac -- meta subset system begun. Working!
"""

from ursina import *  
import numpy as nn
import time
import random as ra

from perlin_noise import PerlinNoise

from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.color = color.rgb(0,111,184)
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = False
window.show_ursina_splash = True
# window.render_mode = 'wireframe'

scene.fog_density = .01
scene.fog_color = color.rgb(0,222,222)

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.speed = 6

#  Original position of subject etc.
subject.y = 12
subject.x = 0
subject.z = 0

# For tracking subject's movement and position
# against the Perlin Noise terrain.
prevX = 0
prevZ = 0

# Perlin noise setup.
noise = PerlinNoise(octaves=4,seed=99)
amp = 24
freq = 128
terrainWidth = 50
terrainDepth = 1

grassTex = load_texture('grass_mono.png')
patternTex = load_texture('grass_14.png')
monoTex = load_texture('mono64.png')
monoStrokeTex = load_texture('mono64Stroke.png')
wireTex = load_texture('wireframe.png')

stepSound = Audio('step.ogg',autoplay=False,loop=False)

pickAxe = Entity(model='Diamond-Pickaxe.obj',
            texture='Diffuse.png',
            x=1,y=1,z=1.6,scale=0.06,rotation_x=90,
            rotation_y=45,
            parent=subject)

creeps = Entity(model='creeper',
                texture='creeper.png',
                x=22,y=-3,z=26,
                scale=0.1)

def nMap(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

# Building functions etc.
class B:
    GRASS = color.rgb(0,200,0)
    STONE = color.rgb(255,255,255)
    WOOD = color.rgb(150,75,0)
buildColour = B.STONE
jojo = Entity(  model='cube',
                collider=None,
                texture=wireTex,
                color=B.STONE)
buildMode = -1 # Toggle with 'f'
def projectBuilder():
    global buildColour
    jojo.position = (subject.position +
                    Vec3(camera.forward * 2))
    jojo.x = nn.round(jojo.x)
    jojo.y = nn.floor(jojo.y)
    jojo.z = nn.round(jojo.z)
    jojo.y+=2
    jojo.color=buildColour

def input(key):
    global buildMode, buildColour, stepSound
    if key == 'q' or key == 'escape': 
        exit()
    if key == 'g': subject.position = Vec3(100,32,100)
    if key == 'f': 
        buildMode *= -1 # Toggle build mode.  
    if key == '1': buildColour = B.GRASS
    if key == '2': buildColour = B.STONE
    if key == '3': buildColour = B.WOOD 
    if key == 'left mouse up' and buildMode==1:
        projectBuilder()
        e = duplicate(jojo)
        e.collider = 'box'
        e.texture=grassTex
        e.color=buildColour
        e.shake(duration=0.5,speed=0.01)
        stepSound.pitch = ra.randrange(8,9)*0.1
        stepSound.length = 0.1
        stepSound.play()
    elif key == 'right mouse up' and buildMode==1:
        e = mouse.hovered_entity
        if e and e.visible==True:
            destroy(e)

def update():
    global prevX, prevZ, ghostTime, ghostDone
    if  nn.abs(nn.floor(subject.z)-nn.floor(prevZ)) >= 1 or \
        nn.abs(nn.floor(subject.x)-nn.floor(prevX)) >= 1 or \
        nn.abs(subject.x-prevX)+nn.abs(subject.z-prevZ) >= 1:
        prevX = subject.x
        prevZ = subject.z
        if stepSound.playing == False:
            stepSound.pitch = ra.random()+0.7
            stepSound.play()
        generateShell()
    
    if buildMode==1:
        projectBuilder()
    else: jojo.y = -9999 # Hide jojo.

    # Continue to build 10K terrain!
    if ghostDone == False and time.time() - ghostTime > 0.25:
        generateSubset()
        # Update timeStamp AFTER generation of subset!
        ghostTime = time.time() 

    # Control creeper. Look at subject; cancel out pitch.
    creeps.look_at(subject)
    creeps.rotation_x = 0

# Ghost-terrain. Parent to subets.
ghost = Entity(model=None,collider=None)

# Our physical terrain object. Parent to blocks.
shell = Entity(model=None,collider=None)
shell.visible = False

# Generate pool of cubes for urizen shell.
blocks = []
blocksWidth = 5
for i in range(blocksWidth*blocksWidth):
    bub = Entity(model='cube',
    collider=None,parent=shell,visible=False)
    blocks.append(bub)

# Cubes to populate each subset.
gblocks = []
subWidth = terrainWidth
for i in range(subWidth*terrainDepth):
    bud = Entity(model='cube',collider=None)
    gblocks.append(bud)
# Empty entity for each subset-gblocks combine.
# In turn, all subsets combined into ghost at end of process.
subsets = []
si = 0 # Current subset index. As we work across terrain.
subsDone = False
totNumSubs = int((terrainWidth*terrainWidth)/subWidth)
for i in range(totNumSubs):
    bud = Entity(model=None,collider=None)
    bud.parent=ghost
    bud.texture=patternTex 
    subsets.append(bud)

# Combine all subsets.
def generateGhost():
    global ghostDone
    application.pause()
    # subject.y += 12 # Prevent fall glitch.
    # subject.gravity = 0
    ghost.combine(auto_destroy=True)
    # Inherit colour from gblocks :)
    ghost.texture=grassTex
    ghost.collider=None
    ghostDone=True
    application.resume()
    # subject.gravity = 0.5
    

# Terrain data.
urizenData = []
for i in range (terrainWidth*terrainWidth):
    # NB. This was reversed in previous non-subset version.
    x = nn.floor(i/terrainWidth)
    z = nn.floor(i%terrainWidth)
    y = (noise([x/freq,z/freq])* amp)
    y = nn.floor(y)
    urizenData.append(y)

def generateShell():
    global terrainWidth, blocksWidth
    for i in range(blocksWidth*blocksWidth):
        x = blocks[i].x = nn.floor(subject.x + (i/blocksWidth))-1
        z = blocks[i].z = nn.floor(subject.z + (i%blocksWidth))-1
        # Check index. If out of range, return to default
        # shell position.
        indi = int((x*terrainWidth)+z)
        if  x >= terrainWidth or \
            z >= terrainWidth or \
            x < 0 or \
            z < 0 or \
            indi >= len(urizenData)-1: 
                blocks[i].y = -5
        
        else:   blocks[i].y = urizenData[indi]

    shell.model = None
    shell.combine(auto_destroy=False)
    shell.collider = 'mesh'
    # shell.texture = patternTex
    # shell.visible = True

gbi = 0 # Current index. I.e., of created ghostblock so far.
ghostTime = 0 # Time stamp for when to generate new subset.
ghostDone = False
def generateSubset():
    global gbi, si, terrainWidth, subWidth, subsDone, ghostDone, terrainDepth
    global totNumSubs, terrainDepth
    # Safety catches...
    if subsDone: return
    if gbi >= len(urizenData)-1: 
        if ghostDone == False:
            generateGhost()
        return
    # Iterate from current index to index + (subWidth-1).
    # Currently, a strip of 100...
    for i in range(gbi,gbi+subWidth):
        x = gblocks[i-gbi].x = nn.floor(i/terrainWidth)
        z = gblocks[i-gbi].z = nn.floor(i%terrainWidth)
        # Check index. If out of range, return to default
        # subset position. NB Not sure we need this anymore?
        indi = int((x*terrainWidth)+z)
        y = gblocks[i-gbi].y = urizenData[indi]
        # To compute Perlin on the fly...
        # y = gblocks[i-gbi].y = nn.floor(noise([x/freq,z/freq])* amp)
        # I could iterate here for layers...
        # for j in range(terrainDepth):
        #     gblocks[i-gbi+subWidth*j].x = x   # Layers...
        #     gblocks[i-gbi+subWidth*j].z = z
        #     gblocks[i-gbi+subWidth*j].y = y - (j+1)
        #     gblocks[i-gbi+subWidth*j].parent=subsets[si]

        gblocks[i-gbi].collider=None
        gblocks[i-gbi].parent=subsets[si]
        # Set colour for each block against height.
        yy = y
        yy += ra.randrange(-2,2)
        r = g = b = 0
        if yy < 5:
            r = nMap(yy,0,5,100,164) + ra.randrange(-10,10)
        elif yy < 10:
            g = nMap(yy,5,10,164,200) + ra.randrange(-10,10)
        else:
            r = 200 + ra.randrange(-10,10)
            g = 200 + ra.randrange(-10,10)
            b = 200 + ra.randrange(-10,10)
        gblocks[i-gbi].color = color.rgb(r,g,b)
    
    # If finished all subsets...
    # First combine gblocks into this final
    # subset, then signal to generate combined ghost.
    # Else combine without destroying and
    # increment si and gbi for next subset.
    if gbi >= len(urizenData)-1:
        subsets[si].combine(auto_destroy=True)
        subsDone = True 
        generateGhost()
    else: 
        subsets[si].combine(auto_destroy=False)
        gbi += subWidth # Increment to new ghost block index.
        subsets[si].collider = None
        if si >= totNumSubs: subsDone = True
        else: si += 1  # Increment to next subset index.

#  Let's gooooo!
generateShell()

app.run()