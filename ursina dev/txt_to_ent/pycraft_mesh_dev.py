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

def input(key):
    global td
    if key=='g':
        td[str(32)+'_'+str(64)] =genTerrain(32,64)
        td[str(32)+'_'+str(65)] =genTerrain(32,65)
        td[str(32)+'_'+str(66)] =genTerrain(32,66)
        td[str(32)+'_'+str(67)] =genTerrain(32,67)
        regen()

counter=0
def update():
    global counter
    counter+=1
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
    if counter%1==0:
        try:
            target_y = 2 + td.get(str(floor(subject.x+0.5))+'_'+str(floor(subject.z)))
            subject.y = lerp(subject.y, target_y, 0.1)
        except: 
            pass
        # subject.x = 32
        # subject.z = 32
app.run()