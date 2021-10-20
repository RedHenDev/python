from random import randint
from ursina import *
from perlin_noise import PerlinNoise
from ursina.camera import Camera
from ursina.prefabs.first_person_controller import FirstPersonController
from nMap import nMap
from file_byte import load, save

app = Ursina()

noise = PerlinNoise(octaves=1,seed=int(99))
terrainSize = 128
td = {} # Terrain dictionary.
quad = load_model('basic_hex.obj')
dungeon = Entity(model=Mesh(), texture='grass_64_hex_tex.png')
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
            i=z%2*x
            if load_terrain==False:
                y = floor(genPerlin(x,z))
                td[str(x)+'_'+str(z)] = y    
            else:
                y = td.get(str(x)+'_'+str(z))
                cc = nMap(y,-32,32,0.32,0.84)
                cc += randint(1,100)/100
                model.colors.extend((Vec4(cc,cc,cc,1),) * len(quad.vertices))
                model.vertices.extend([Vec3(x,y,z)+v+Vec3(i,0,0) for v in quad.vertices])
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
urizen('hurizen_128.map',True)
minimap_scale = 0.02
uri = duplicate(dungeon)
uri.texture='white_cube'
# uri.color=color.rgba(200,200,200,200)
uri.scale *= minimap_scale
uri.origin = (subject.position +
                        subject.camera_pivot.up * 2 + 
                        subject.camera_pivot.forward * 5)
uri.set_position(uri.origin)
uri.always_on_top=True

mark = Entity(model='sphere',color=color.red)
# mark.scale *= minimap_scale * 2
# mark.origin = uri.position
mark.parent=uri
mark.scale *= 8
# mark.scale_x *= 3
# mark.scale_z *= 3
mark.always_on_top=True

def update():
    uri.set_position(   subject.position +
                        subject.camera_pivot.up * 2 + 
                        subject.camera_pivot.forward * 5)
    
    mark.set_position(  uri.position+
                        subject.position*minimap_scale+
                        subject.down*2)
    # mark.position=(subject.position*minimap_scale)
    mark.x -= 64
    mark.z -= 64
    # uri.y += sin(uri.rotation_y*0.1)*0.25
    # uri.rotation_y += 0.25
    # mark.rotation_y -= 0.25
    try:
        target_y = 2 + td.get(str(floor(subject.x))+'_'+str(floor(subject.z)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: subject.y = subject.y
app.run()