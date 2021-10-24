from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from rh_gen_terrain import loadMap, swirl, swirl_pos, reset_swirl, gen_subset, set_subPos, next_subset, subset_regen

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
def new_terrain_gen_orig():
    radius = 8
    x = subject.x + radius * math.sin(math.radians(subject.rotation_y))
    z = subject.z + radius * math.cos(math.radians(subject.rotation_y))
    pos = Vec2(0,0)
    pos.x = x
    pos.y = z
    set_subPos(pos)
    reset_swirl()

def paintTerrain():
    width = 4
    pos = swirl_pos(width*2)
    swirl() # Find next position to create terrain.
    x = math.floor(pos.x)
    z = math.floor(pos.y)
    newT = False
    
    for j in range(-width,width):
        for k in range(-width,width):
            if td.get(str(x+j)+'_'+str(z+k))==None:
                newT = True
                # td[str(x+j)+'_'+str(z+k)]=genTerrain(x+j,z+k)
                td[str(x+j)+'_'+str(z+k)]=gen_subset(x+j,z+k)
# Only generate model if new terrain to be built.
    if newT==True:
        # But why 4? - since each width is half a length.
        # Could optimize by precalculating this once.
        # regen(width*width*4)
        subset_regen(width*width*4)
        next_subset()

def input(key):
    if key=='g':
        new_terrain_gen_orig()

counter=0
def update():
    global counter
    counter+=1
    if counter%30==0:
        new_terrain_gen_orig()
        counter=0
    if counter%4==0:
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