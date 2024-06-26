"""
Mesh terrain builder.
Saves to .map file.
Map file can then be loaded to
generate a terrain.

Notes for dev

It would be nice to also communicate the
perlin details along with the map info.
"""
from random import randint
from ursina import *
from perlin_noise import PerlinNoise
from nMap import nMap
from file_byte import load, save

# app = Ursina()

terrainSize = 128
mapName = 'terrain_6.map'
td = {} # Terrain dictionary.
# quad = load_model('stretch_hex.obj')
# dungeon = Entity(model=Mesh(), texture='grass_64_hex_tex.png')
# quad = load_model('block.obj')
# dungeon = Entity(model=Mesh(), texture='block_texture.png')
# model = dungeon.model

_seed = (ord('j')+ord('o'))
# New style, as per perlin-noise module example.
# noise1 = PerlinNoise(octaves=3,seed=_seed)
# noise2 = PerlinNoise(octaves=6,seed=_seed)
# noise3 = PerlinNoise(octaves=9,seed=_seed)
# noise4 = PerlinNoise(octaves=12,seed=_seed)

noise = PerlinNoise(octaves=6,seed=_seed)

def genPerlin(_x, _z):
    y = 0
    # New style, as per perlin-noise module example.
    # freq = 256
    # amp = 64 
    # y += ((noise1([_x/freq,_z/freq]))*amp)
    # amp = 12
    # y += ((noise2([_x/freq,_z/freq]))*amp)
    # amp = 1
    # y += ((noise3([_x/freq,_z/freq]))*amp)
    # amp = 1
    # y += ((noise4([_x/freq,_z/freq]))*amp)

    freq=300
    amp=32
    y += ((noise([_x/freq,_z/freq]))*amp)

    y+= math.sin(_x)*0.5-0.5
    y+= math.cos(_z)*0.5-0.5

    return y

def urizen(_map_name, load_terrain=False):
    global td
    if load_terrain==True:
        td = load(_map_name)
    for z in range(terrainSize):
        for x in range(terrainSize):
            if load_terrain==False:
                y = floor(genPerlin(x,z))
                
                td[str(x)+'_'+str(z)] = y    
            else:
                y = td.get(str(x)+'_'+str(z))
                cc = nMap(y,-32,32,0.32,0.84)
                cc += randint(1,100)/100
                model.colors.extend((Vec4(cc,cc,cc,1),) 
                                        * len(quad.vertices))
                # For hexagonal terrain blocks.
                # model.vertices.extend([Vec3(x+z%2*0.5,y,z)
                model.vertices.extend([Vec3(x,y,z)
                                        +v for v in quad.vertices])
    if load_terrain==False:
        save(_map_name, td)
    else:
        model.uvs = (quad.uvs) * (terrainSize * terrainSize)
        model.generate()

# subject = FirstPersonController()
# subject.z = 64
# subject.x = 64
# subject.y = 100
# subject.gravity = 0.0
# subject.cursor.visible=False
# window.color=color.cyan
# scene.fog_color = color.cyan
# scene.fog_density = 0.01

# False saves terrain to file; True plays!
urizen(mapName,False)
print("map " + mapName + " saved :)")
# def update():
    # try:
    #     target_y = 2 + td.get(str(floor(subject.x))+'_'+str(floor(subject.z)))
    #     subject.y = lerp(subject.y, target_y, 0.1)
    # except: subject.y = subject.y
# app.run()