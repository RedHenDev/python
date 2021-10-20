from random import randint
from ursina import *
from perlin_noise import PerlinNoise
from ursina.prefabs.first_person_controller import FirstPersonController
from nMap import nMap
from file_byte import load, save

app = Ursina()

noise = PerlinNoise(octaves=1,seed=int(99))
terrainSize = 128
td = {} # Terrain dictionary.
quad = load_model('block.obj')
dungeon = Entity(model=Mesh(), texture='block_texture')
model = dungeon.model

def genPerlin(_x, _z):
    y = 0
    freq = 64
    amp = 32      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 64
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)

    return y

def urizen(_td):
    for z in range(terrainSize):
        for x in range(terrainSize):
            # y = floor(genPerlin(x,z))
            y = _td.get(str(x)+'_'+str(z))
            # td[str(x)+'_'+str(z)] = y
            model.vertices.extend([Vec3(x,y,z)+v for v in quad.vertices])
            cc = nMap(y,0,64,0.4,0.9)
            cc += randint(1,100)/100
            model.colors.extend((Vec4(cc,cc,cc,1),) * len(quad.vertices))
    # save('urizen_1.map', td)
    model.uvs = (quad.uvs) * (terrainSize * terrainSize)
    model.generate()

subject = FirstPersonController()
subject.z = 32
subject.x = 32
subject.y = 100
subject.gravity = 0.0

td = load('urizen_1.map')
urizen(td)

def update():
    target_y = 2 + td.get(str(floor(subject.x))+'_'+str(floor(subject.z)))
    subject.y = lerp(subject.y, target_y, 0.1)
app.run()