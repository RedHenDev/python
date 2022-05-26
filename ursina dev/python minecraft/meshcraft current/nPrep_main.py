from ursina import *
# Instantiate ursina here, so that textures can be
# loaded without issue in other modules :)
app = Ursina()

from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap, loadMap
# from inventory_system import *
# ***
from new_inv import *

window.color = color.rgb(0,0,0)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.height=1.86
subject.frog=False # For jumping...
subject.runSpeed=20
subject.walkSpeed=4
camera.dash=10 # Rate at which fov changes when running.
window.fullscreen=False

terrain = MeshTerrain(subject,camera)
# snowfall = SnowFall(subject)
# How do you at atmospheric fog?
scene.fog_density=(0,75)
# scene.fog_color=indra.color
scene.fog_color=color.white
generatingTerrain=True

# Generate our terrain 'chunks'.
for i in range(64):
    terrain.genTerrain()
# For loading in a large terrain at start.
# loadMap(subject,terrain)

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

def input(key):
    global generatingTerrain
    terrain.input(key)
    if key=='g':
        generatingTerrain = not generatingTerrain
    # Jumping...
    if key=='space': subject.frog=True
    # Saving and loading...
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)

    # Inventory access.
    inv_input(key,subject,mouse)

count = 0
# ***
earthquake=0
def update():
    global count, pX, pZ, earthquake

    # Highlight terrain block for mining/building...
    terrain.update(subject.position,camera)

    # Handle mob ai.
    mob_movement(grey, subject.position, terrain.td)

    count+=1
    if count == 32:
        
        count=0
        # Generate terrain at current swirl position.
        if generatingTerrain:
            terrain.genTerrain()
            # for i in range(4):
            #     terrain.genTerrain()
                
    # ***
    # # Crazy subset wave...
    # if mouse.locked:
    #     for s in terrain.subsets:
    #         s.y = math.sin(terrain.subsets.index(s) + earthquake*0.5)*0.1
    #     earthquake+=1   

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=ra.random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=ra.random()+0.7
            grass_audio.play()
    
    # Walk on solid terrain, and check wall collisions.
    bumpWall(subject,terrain)
    # Running and dash effect.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        if camera.fov>90:
            camera.fov-=camera.dash*4*time.dt
            if camera.fov<90:camera.fov=90

from mob_system import *

app.run()