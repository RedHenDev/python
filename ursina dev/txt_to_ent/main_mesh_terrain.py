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
subject.x = 32
subject.z = 32
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
    # if counter%3==0:
    if terrain.generating:
            terrain.paintTerrain()
    if counter==3:
        counter=0
        terrain.miner.build_tool_entity()
        
        # Disable and enable individual subsets
        # according to distance from subject.
        # check_subset(subject)
    if  abs(subject.x - preVpos.x) > 6 or \
        abs(subject.z - preVpos.z) > 6:
        terrain.new_swirl_origin(   subject.x,
                                    subject.z,
                                    subject.rotation_y,
                                    4)
        preVpos = subject.position
    
    step_height = 3
    foundBlock = False
    for i in range(-step_height,step_height,1):
        if terrain.td.get(str(floor(subject.x+0.5))+
                        '_'+str(floor(subject.y+0.5)+i)+
                        '_'+str(floor(subject.z+0.5)))\
                        =='t': 
            target_y = floor(subject.y+0.5)+i
            foundBlock = True
            break
    if foundBlock==False:
        subject.y -= 19.8 * time.dt
    else:
        subject.y = lerp(subject.y, target_y+2, 9*time.dt)
    
app.run()