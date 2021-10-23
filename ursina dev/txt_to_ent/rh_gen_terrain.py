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
from numpy import floor, sqrt

def genPerlin(_x, _z):
    _seed = (ord('l'))
    noise1 = PerlinNoise(octaves=1,seed=_seed)
    noise2 = PerlinNoise(octaves=3,seed=_seed)
    noise3 = PerlinNoise(octaves=6,seed=_seed)
    noise4 = PerlinNoise(octaves=12,seed=_seed)

    y = 0
    freq = 128
    amp = 32 
    y += ((noise1([_x/freq,_z/freq]))*amp)
    amp = 16
    y += ((noise2([_x/freq,_z/freq]))*amp)
    amp = 8
    y += ((noise3([_x/freq,_z/freq]))*amp)
    amp = 1
    y += ((noise4([_x/freq,_z/freq]))*amp)

    return y

terrainObject = None
terrainS = None
terrainB = None

def genTerrain(x,z):
    block = terrainB
    terrainSize = terrainS
    model = terrainObject.model

    y = floor(genPerlin(x,z))
    # print(y)
    # td[str(x)+'_'+str(z)] = y    
            
    # y = _td.get(str(x)+'_'+str(z))
    cc = nMap(y,-32,32,0.32,0.84)
    cc += randint(1,100)/100
    # if randint(1,2)!=1:
    model.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
    model.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])
    # else:
    #     model2.colors.extend((Vec4(cc,cc,cc,1),) * len(block.vertices))
    #     model2.vertices.extend([Vec3(x,y,z)+v for v in block.vertices])

    model.uvs = (block.uvs) * (terrainSize * terrainSize)
    # model.generate()
    # model2.uvs = (block.uvs) * (terrainSize * terrainSize)
    # model2.generate()
    return y
    
def regen():
    model = terrainObject.model
    block = terrainB
    terrainSize = terrainS
    
    model.uvs = (block.uvs) * (terrainSize * terrainSize)
    model.generate()

def loadMap(_map_name):
    global terrainObject, terrainS, terrainB
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

    model.uvs = (block.uvs) * (terrainSize * terrainSize)
    model.generate()
    model2.uvs = (block.uvs) * (terrainSize * terrainSize)
    model2.generate()

    terrainObject = dungeon
    terrainB = block
    terrainS = terrainSize

    return _td