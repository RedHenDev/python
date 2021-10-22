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
quad = load_model('stretch_hex.obj')
dungeon = Entity(model=Mesh(), texture='grass_64_hex_tex.png')
# quad = load_model('block.obj')
# dungeon = Entity(model=Mesh(), texture='block_texture.png')
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

def urizen(_map_name, load_terrain=True):
    global td
    if load_terrain==True:
        td = load(_map_name)
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
                model.colors.extend((Vec4(cc,cc,cc,1),) * len(quad.vertices))
                model.vertices.extend([Vec3(x+z%2*0.5,y,z)+v for v in quad.vertices])
    if load_terrain==False:
        save(_map_name, td)
    else:
        model.uvs = (quad.uvs) * (terrainSize * terrainSize)
        model.generate()

subject = FirstPersonController()
subject.z = 64
subject.x = 64
subject.y = 100
subject.gravity = 0.0
subject.cursor.visible=False
window.color=color.cyan
scene.fog_color = color.cyan
scene.fog_density = 0.01

# False saves terrain to file; True plays!
urizen('hexizen_128.map',True)
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
    uri.y += sin(counter*0.1)*0.25
    # uri.rotation_y += 0.25
    mark.set_position(  uri.position+
                        Vec3(-64,0,-64)*minimap_scale+
                        subject.position*minimap_scale+
                        subject.down*2)
    # mark.x += minimap_scale*math.sin(math.radians(uri.rotation_y))
    # mark.z += minimap_scale*math.cos(math.radians(uri.rotation_y))
    try:
        target_y = 2 + td.get(str(floor(subject.x))+'_'+str(floor(subject.z)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: subject.y = subject.y
app.run()