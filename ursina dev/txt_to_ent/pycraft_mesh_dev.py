from random import randint
from ursina import *
from perlin_noise import PerlinNoise
from ursina.prefabs.first_person_controller import FirstPersonController
from nMap import nMap
from file_byte import load, save

app = Ursina()

noise = PerlinNoise(octaves=1,seed=int(99))
map_name = 'terrain_1.map'
terrainSize = 0 # To be derived from loaded map data :)
td = {} # Terrain dictionary.
# quad = load_model('stretch_hex.obj')
# dungeon = Entity(model=Mesh(), texture='grass_64_hex_tex.png')
quad = load_model('block.obj')
dungeon = Entity(model=Mesh(), texture='block_texture.png')
dungeon2 = Entity(model=Mesh(), texture='block_texture2.png')
model = dungeon.model
model2 = dungeon2.model

def genPerlin(_x, _z):
    y = 0
    freq = 64
    amp = 32      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 64
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)
    return y

def urizen(_map_name, load_terrain=True):
    global td
    if load_terrain==True:
        td = load(_map_name)
    # Derive terrain size. Position subject.
    terrainSize = floor(math.sqrt(len(td)))
    subject.z = terrainSize*0.5
    subject.x = terrainSize*0.5
    for z in range(terrainSize):
        for x in range(terrainSize):
            if load_terrain==False:
                y = floor(genPerlin(x,z))
                y += sin(x)*0.5
                td[str(x)+'_'+str(z)] = y    
            else:
                y = td.get(str(x)+'_'+str(z))
                cc = nMap(y,-32,32,0.32,0.84)
                cc += randint(1,100)/100
                if randint(1,2)!=1:
                    model.colors.extend((Vec4(cc,cc,cc,1),) * len(quad.vertices))
                    model.vertices.extend([Vec3(x,y,z)+v for v in quad.vertices])
                else:
                    model2.colors.extend((Vec4(cc,cc,cc,1),) * len(quad.vertices))
                    model2.vertices.extend([Vec3(x,y,z)+v for v in quad.vertices])
    if load_terrain==False:
        save(_map_name, td)
    else:
        model.uvs = (quad.uvs) * (terrainSize * terrainSize)
        model.generate()
        model2.uvs = (quad.uvs) * (terrainSize * terrainSize)
        model2.generate()

subject = FirstPersonController()
subject.y = 100
subject.gravity = 0.0
subject.cursor.visible=False
window.color=color.cyan
scene.fog_color = color.cyan
scene.fog_density = 0.01

# False saves terrain to file; True plays!
urizen(map_name,True)
minimap_scale = 0.02
uri = duplicate(dungeon)
uri.texture='white_cube'
uri.color=color.rgba(0,200,200,255)
uri.scale *= minimap_scale
uri.origin = (subject.position +
                        subject.camera_pivot.up * 2 + 
                        subject.camera_pivot.forward * 5)
uri.set_position(uri.origin)
uri.always_on_top=True

# NB Mark inherits scale from uri, the minimap.
mark = Entity(model='sphere',color=color.red)
mark.parent=uri
mark.scale *= 8
mark.always_on_top=True

counter=0
def update():
    global counter
    counter+=1
    # Minimap.
    uri.set_position(   subject.position +
                        subject.camera_pivot.up * 2 + 
                        subject.camera_pivot.forward * 5)
    # Red minimap subject pos marker.
    uri.y += math.sin(counter*0.1)*0.25
    adjustPos = floor(math.sqrt(len(td)))*0.5
    mark.set_position(  uri.position+
                        Vec3(-adjustPos,0,-adjustPos)*minimap_scale+
                        subject.position*minimap_scale+
                        subject.down*2)
    try:
        target_y = 2 + td.get(str(floor(subject.x))+'_'+str(floor(subject.z)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: 
        subject.x = adjustPos
        subject.z = adjustPos
app.run()