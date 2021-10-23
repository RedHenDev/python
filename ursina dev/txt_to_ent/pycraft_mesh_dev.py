from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from rh_gen_terrain import loadMap, genTerrain, regen

app = Ursina()

subject = FirstPersonController()
subject.y = 32
subject.x = 32
subject.z = 32
subject.gravity = 0.0
subject.cursor.visible=False
window.color=color.cyan
scene.fog_color = color.cyan
scene.fog_density = 0.01

map_name = 'terrain_1.map'
td = {} # Terrain dictionary.
td = loadMap(map_name)
"""
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
"""
def paintTerrain():
    x = subject.x + 9 * math.sin(math.radians(subject.rotation_y))
    z = subject.z + 9 * math.cos(math.radians(subject.rotation_y))
    x = math.floor(x)
    z = math.floor(z)
    newT = False
    width = 12
    for j in range(-width,width):
        for k in range(-width,width):
            if td.get(str(x+j)+'_'+str(z+k))==None:
                newT = True
                td[str(x+j)+'_'+str(z+k)]=genTerrain(x+j,z+k)
    # Only generate model if new terrain to be built.
    if newT==True:
        regen()    

def input(key):
    if key=='g':
        paintTerrain()

counter=0
def update():
    global counter
    counter+=1
    if counter%32==0:
        paintTerrain()
    """
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
    """
    try:
        target_y = 2 + td.get(str(floor(subject.x+0.5))+'_'+str(floor(subject.z)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: 
        subject.y=subject.y
app.run()