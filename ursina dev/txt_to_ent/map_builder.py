"""
Mesh terrain builder.
Saves to .map file.
Map file can then be loaded to
generate a terrain.
"""
from random import randint
from ursina import *
from perlin_noise import PerlinNoise
from nMap import nMap
from file_byte import load, save

# app = Ursina()

noise = PerlinNoise(octaves=1,seed=int(19882211))
terrainSize = 128
mapName = 'mapBuild_test_2.map'
td = {} # Terrain dictionary.
# quad = load_model('stretch_hex.obj')
# dungeon = Entity(model=Mesh(), texture='grass_64_hex_tex.png')
# quad = load_model('block.obj')
# dungeon = Entity(model=Mesh(), texture='block_texture.png')
# model = dungeon.model

def genPerlin(_x, _z):
    y = 0
    freq = 64
    amp = 32      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 64
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)
    return y

def urizen(_map_name, load_terrain=False):
    global td
    if load_terrain==True:
        td = load(_map_name)
    for z in range(terrainSize):
        for x in range(terrainSize):
            if load_terrain==False:
                y = floor(genPerlin(x,z))
                y += math.sin(x)*0.5
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