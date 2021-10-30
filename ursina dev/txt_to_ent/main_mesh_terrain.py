"""
Minecraft-like terrain from mesh
30/10/21
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import abs
from rh_mesh_terrain import MeshTerrain

app = Ursina()

subject = FirstPersonController()
subject.y = 99
subject.x = 4
subject.z = 4
subject.gravity = 0.0
subject.cursor.visible=False
subject.speed = 6
# window.color=color.cyan
scene.fog_color = color.pink
scene.fog_density = 0.02
Sky(color=color.pink)

map_name = 'terrain_6.map'
terrain = MeshTerrain(subject,camera)

def input(key):
    terrain.terrain_input(key)

counter=0
preVpos = subject.position
def update():
    global counter, preVpos

    counter+=1
    # How quickly to generate new terrain.
    if counter%3==0:
        terrain.paintTerrain()
        terrain.miner.build_tool_entity()
        
        # Disable and enable individual subsets
        # according to distance from subject.
        # check_subset(subject)
    if  abs(subject.x - preVpos.x) > 8 or \
        abs(subject.z - preVpos.z) > 8:
        terrain.new_swirl_origin(   subject.x,
                                    subject.z,
                                    subject.rotation_y)
        preVpos = subject.position

    try:
        target_y = 2 + terrain.td.get(str(floor(subject.x+0.5))+'_'+str(floor(subject.z+0.5)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: 
        subject.y=subject.y
app.run()