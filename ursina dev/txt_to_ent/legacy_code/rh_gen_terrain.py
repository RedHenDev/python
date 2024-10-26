"""
Generate terrain via mesh.
rh_gen_terrain.py

Idea2: we only need td in main module...so perhaps
all that this function needs access to is td? I.e.
all the terrain entity objects will belong to this
module itself?
"""
from os import unsetenv
from ursina import *
from perlin_noise import PerlinNoise
from file_byte import load
from nMap import nMap
from random import randint, randrange
from numpy import floor, sqrt, abs

_seed = (ord('j')+ord('o'))
# terrain_3.map
# _seed = (ord('l'))
# noise1 = PerlinNoise(octaves=1,seed=_seed)
# noise2 = PerlinNoise(octaves=3,seed=_seed)
# noise3 = PerlinNoise(octaves=6,seed=_seed)
# noise4 = PerlinNoise(octaves=12,seed=_seed)
# terrain_3.map ?
# noise1 = PerlinNoise(octaves=3,seed=_seed)
# noise2 = PerlinNoise(octaves=6,seed=_seed)
# noise3 = PerlinNoise(octaves=12,seed=_seed)

# terrain_5.map
noise = PerlinNoise(octaves=5,seed=_seed)

def genPerlin(_x, _z):
    y = 0

    # For terrain_4.map
    # freq = 256
    # amp = 112 
    # y += ((noise1([_x/freq,_z/freq]))*amp)
    # amp = 56
    # y += ((noise2([_x/freq,_z/freq]))*amp)
    # amp = 8
    # y += ((noise3([_x/freq,_z/freq]))*amp)
    # amp = 1
    # y += ((noise4([_x/freq,_z/freq]))*amp)

    # terrain_3.map
    # freq = 256
    # amp = 64 
    # y += ((noise1([_x/freq,_z/freq]))*amp)
    # amp = 12
    # y += ((noise2([_x/freq,_z/freq]))*amp)
    # amp = 1
    # y += ((noise3([_x/freq,_z/freq]))*amp)

    # terrain_6.map
    # freq=300
    # amp=32
    # y += ((noise([_x/freq,_z/freq]))*amp)

    # y+= math.sin(_x)*0.5-0.5
    # y+= math.cos(_z)*0.5-0.5

    # Just a setting -- no map file :)
    freq=444
    amp=32
    y += ((noise([_x/freq,_z/freq]))*amp)

    y+= math.sin(_x)*0.5-0.5
    # y+= math.cos(_z)*0.5-0.5

    return y

terrainObject = None
terrainS = None
terrainB = None

subsets = []
currentSubset = 0

# For new position of subset.
currentVec = 0
iterations = 0
toIterate = 1
changes = -1
subPos = Vec2(32,32)
swirlVecs = [
    Vec2(0,0),
    Vec2(0,1),
    Vec2(1,0),
    Vec2(0,-1),
    Vec2(-1,0)
]

def mine(subject,td,vd):
    from fh_mining import mine_action
    mine_action(subject,td,subsets,terrainObject.model,vd)

def terrain_input(key,subject,td,vd):
    if key=='left mouse up':
        mine(subject,td,vd)

def check_subset(subject):
    for s in subsets:
        if (abs(s.pos.x - subject.x)>128 or 
            abs(s.pos.y - subject.z)>128):
            # print('ghost')
            s.disable()
        else:
            # print('zombie')
            s.enable()

def set_subPos(pos):
    subPos.x = pos.x
    subPos.y = pos.y

def reset_swirl():
    global currentVec, iterations, toIterate, changes
    currentVec = 0
    iterations = 0
    toIterate = 1
    changes = -1

def swirl():
    global iterations,toIterate,currentVec,changes
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

def swirl_pos(subWidth):
    # Translate position of subset, according to
    # current vector.
    subPos.x += (swirlVecs[currentVec].x*subWidth)
    subPos.y += (swirlVecs[currentVec].y*subWidth)
    return subPos

def setup_subsets():
    global subsets
    if len(subsets)!=0: return
    
    for i in range(512):
        e = Entity(model=Mesh(),texture='texture_atlas_3.png')
        # *** adjust scale of texture.
        e.texture_scale*=64/e.texture.width
        e.pos = Vec2(0,0)
        subsets.append(e)

def gen_subset(x,z):
    from random import random
    global currentSubset
    block = terrainB   # Model with which we mould blocks. 
    subsets[currentSubset].enable()
    model = subsets[currentSubset].model
    
    # Record position of subset.
    # For checking distance...
    subsets[currentSubset].pos.x = x
    subsets[currentSubset].pos.y = z

    y = floor(genPerlin(x,z))   
    cc = nMap(y,-32,32,0.32,0.84)
    cc += randint(1,100)/100
    model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
    model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])
    # *** UVs
    tilesX = 2
    tilesY = 1
    # colX from left.
    # rowY from top.
    if z > 10:
        colX = 1
        rowY = 2
    else: 
        colX = 1
        rowY = 1
    uu = tilesX/colX
    uv = tilesY*rowY 

    model.uvs.extend([Vec2(8,7)+u for u in block.uvs])
    
    # for i in range(1,3):
    #     model.vertices.extend([Vec3(x,y-i,z)+v for v in block.vertices])
    
    vob = (currentSubset,len(model.vertices)-37)
    return y, vob

def subset_regen(_width):
    global currentSubset
    model = subsets[currentSubset].model
    block = terrainB
    # ***
    # These now generate in gen_subset (i.e. texture atlas).
    # model.uvs += (block.uvs) * _width
    # Mesh.project_uvs(model)
    model.generate()

def next_subset():
    global currentSubset
    currentSubset += 1
    if currentSubset == len(subsets)-1:
        currentSubset = 0
        # subsets[0].model.clear(regenerate=False) 
        print('used all subsets')
    # Perhaps clear subset here?
    # Well, academic since we actually want
    # to find the subset furthest away and behind player?

def genTerrain(x,z):
    block = terrainB
    model = terrainObject.model
    y = floor(genPerlin(x,z))   
    cc = nMap(y,-32,32,0.32,0.84)
    cc += randint(1,100)/100
    model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
    model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])

    return y

def regen(_width):
    model = terrainObject.model
    block = terrainB
    model.uvs += (block.uvs) * _width
    model.generate()

"""
For use when not loading terrain from file.
"""
def setup_terrain():
    global terrainObject, terrainS, terrainB
    setup_subsets()

    terrainSize = 0 # To be derived from loaded map data :)
    block = load_model('block.obj')
    # dungeon = Entity(model=Mesh(),texture='block_texture.png')
    dungeon = Entity(model=Mesh(),texture='texture_atlas_1.png')
    
    dungeon2 = Entity(model=Mesh(),texture='block_texture2.png')

    terrainObject = dungeon
    terrainB = block
    terrainS = terrainSize

    # *** debug
    # print(terrainB.uvs)

def loadMap(_map_name):
    global terrainObject, terrainS, terrainB

    setup_subsets()

    terrainSize = 0 # To be derived from loaded map data :)
    block = load_model('block.obj')
    dungeon = Entity(model=Mesh(),texture='block_texture.png')
    dungeon2 = Entity(model=Mesh(),texture='block_texture2.png')
    model = dungeon.model
    model2 = dungeon2.model

    _td={}
    _td = load(_map_name)
    vd = {}
    vCount = 0 # To track vertices to vd. See below.
    # Derive terrain size. Position subject.
    terrainSize = int(floor(sqrt(len(_td))))
    print(terrainSize)
    for z in range(terrainSize):
        for x in range(terrainSize):
            
            # For saving...
            # y = floor(genPerlin(x,z))
            # td[str(x)+'_'+str(z)] = y    
            
            y = _td.get(str(x)+'_'+str(z))
            cc = nMap(y,-32,32,0.32,0.84)
            cc += randint(1,100)/100
            if randint(2,2)!=1:
                model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
                model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])
            else:
                model2.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
                model2.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])
            # Keep track of vertex id for mining :)
            vd[str(x)+'_'+str(z)] = vCount
            vCount+=36
            # This is used when mining -
            # knowing which vertices in the model to remove.

            # for i in range(1,3):
            #     model.vertices.extend([Vec3(x,y-i,z)+v for v in block.vertices])

    model.uvs = (block.uvs) * (terrainSize * terrainSize)
    model.generate()
    model2.uvs = (block.uvs) * (terrainSize * terrainSize)
    model2.generate()

    terrainObject = dungeon
    terrainB = block
    terrainS = terrainSize

    return _td, vd