"""
Minecraft-like terrain from mesh
30/10/21
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import abs
from rh_mesh_terrain import MeshTerrain

app = Ursina()

map_name = 'terrain_6.map'
terrain = MeshTerrain(map_name)

subject = FirstPersonController()
subject.y = 99
subject.x = 0
subject.z = 0
subject.gravity = 0.0
subject.cursor.visible=False
subject.speed = 6
# window.color=color.cyan
scene.fog_color = color.pink
scene.fog_density = 0.02
Sky(color=color.pink)

def new_terrain_gen_orig():
    radius = 16
    x = subject.x + radius * math.sin(math.radians(subject.rotation_y))
    z = subject.z + radius * math.cos(math.radians(subject.rotation_y))
    pos = Vec2(x,z)
    terrain.subPos = pos
    terrain.reset_swirl()

new_terrain_gen_orig()

def input(key):
    if key=='g':
        new_terrain_gen_orig()

    # terrain_input(key,subject,td, vd)

counter=0
preVpos = subject.position
def update():
    from fh_mining import build_tool_entity
    global counter, preVpos

    counter+=1
    # How quickly to generate new terrain.
    if counter%3==0:
        terrain.paintTerrain()
        # build_tool_entity(subject,camera,td)
        
        # Disable and enable individual subsets
        # according to distance from subject.
        # check_subset(subject)
    if  abs(subject.position.x - preVpos.x) > 8 or \
        abs(subject.position.z - preVpos.z) > 8:
        new_terrain_gen_orig()
        preVpos = subject.position

    try:
        target_y = 2 + terrain.td.get(str(floor(subject.x+0.5))+'_'+str(floor(subject.z+0.5)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: 
        subject.y=subject.y
app.run()