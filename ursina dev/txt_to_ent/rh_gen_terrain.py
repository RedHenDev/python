"""
Generate terrain via mesh.
rh_gen_terrain.py

Idea2: we only need td in main module...so perhaps
all that this function needs access to is td? I.e.
all the terrain entity objects will belong to this
module itself?
"""
from ursina import *
from perlin_noise import PerlinNoise
from file_byte import load
from nMap import nMap
from random import randint
from numpy import floor, sqrt, abs

_seed = (ord('l'))
noise1 = PerlinNoise(octaves=1,seed=_seed)
noise2 = PerlinNoise(octaves=3,seed=_seed)
noise3 = PerlinNoise(octaves=6,seed=_seed)
noise4 = PerlinNoise(octaves=12,seed=_seed)

def genPerlin(_x, _z):
    y = 0
    freq = 256
    amp = 112 
    y += ((noise1([_x/freq,_z/freq]))*amp)
    amp = 56
    y += ((noise2([_x/freq,_z/freq]))*amp)
    amp = 8
    y += ((noise3([_x/freq,_z/freq]))*amp)
    amp = 1
    y += ((noise4([_x/freq,_z/freq]))*amp)

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

def check_subset(subject):
    for s in subsets:
        if (abs(s.pos.x - subject.x)>256 or 
            abs(s.pos.y - subject.z)>256):
            print('ghost')
            # s.disable()
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
        e = Entity(model=Mesh(),texture='block_texture.png')
        e.pos = Vec2(0,0)
        subsets.append(e)

def gen_subset(x,z):
    global currentSubset
    block = terrainB   # Model with which we mould blocks. 
    subsets[currentSubset].enable()
    model = subsets[currentSubset].model
    
    # Record position of subset.
    subsets[currentSubset].pos.x = x
    subsets[currentSubset].pos.y = z

    y = floor(genPerlin(x,z))   
    cc = nMap(y,-32,32,0.32,0.84)
    cc += randint(1,100)/100
    model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
    model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])

    # for i in range(1,3):
    #     model.vertices.extend([Vec3(x,y-i,z)+v for v in block.vertices])

    return y

def subset_regen(_width):
    global currentSubset
    model = subsets[currentSubset].model
    block = terrainB
    model.uvs += (block.uvs) * _width
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
            if randint(1,2)!=1:
                model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
                model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])
            else:
                model2.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
                model2.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])

            # for i in range(1,3):
            #     model.vertices.extend([Vec3(x,y-i,z)+v for v in block.vertices])


    model.uvs = (block.uvs) * (terrainSize * terrainSize)
    model.generate()
    model2.uvs = (block.uvs) * (terrainSize * terrainSize)
    model2.generate()

    terrainObject = dungeon
    terrainB = block
    terrainS = terrainSize

    return _td