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
from inventory_system import *
# *** - move from bottom of module.
from mob_system import *
"""
NB - RED workspace is private PREP.
NB - BLUE is TUTORIAL code!
Adventures
1) 'Snap' behaviour for items. DONE :D
2) Number keys select building block type. DONE :)
3) Make an inventory panel.

Notes for vid 16
i) Correcting colour - DONE (except for stain bug - see vi)
ii) Saving blockType correctly - DONE
ii+) from 't' to not None and not 'g' (in bump_system, building, etc.) - DONE
ii+) record blockType in td only at end of genBlock() - DONE
iii) Map-name const at start of save_load_system - DONE
iv) fixPos() at instantiation of hotspots - DONE!

Tut 17 notes
i) inventory panel creation; toggle behaviour, static method - DONE
ii) Investigate colour staining bug - DONE
ii+) Solve colour staining - DONE :D
ii) ? - Earthquakes :o - DONE :D

Tut 18 notes
i) mined block particles - pick-up for inventory - DONE
ii) trees? Rocks?! (VID 20?)
iii) Note on ursina update and fix! 4.1.1 - DONE

Tut 19 adventure plans!
0) eye-level correction - DONE
0.1) more efficient highlight call - DONE
0.2) empty-subject hands, then no build - DONE
i) colour bug for e.g. ruby collectible - DONE - UNDONE?!
ii) picking up behaviour  - DONE
iii) sounds for picking up item - DONE
iv) text for stacking info on inventory DONE
iv+) stacking behaviour on inventory DONE
v) destroy collectibles if lifespan expires - DONE

Tut 20
i) ui aspect ratio bug DONE
ii) collectible colour bug DONE
iii) inventory items stay put when clicked DONE
iv) saw a panda -- DONE
v) created simple stack system DONE 

Tut 21
i) BUG item text remaining when it shouldn't - DONE
i.i) BUG items of different kinds overlapping... DONE
i.ii) Item stack text update upon collection. - DONE
iii) TREES :) - DONE

Tut 22
i) deplete stack number when building :) - DONE

Tut 23 * TREE SPECIAL *
0.i) refactor rara (random module clash) - DONE
ii) Trees minable - DONE
ii.i) Tree texture(s) - DONE -> grass transparency :) 'BUG'
ii.ii) Tree perlin distribution - DONE
iii) FOV to 63 - DONE (corrected for dash effect)
iv) location co-ords as Text on screen DONE 

Tut 24
i) audio - pickups as member property
ii) Rocks -> replace random stone placements
iii) tree placement wiggle
iv) prevent tree crown clash

**To Do List**
) audio as member property of collectible class
) Refactor the current-blockType (building) mechanism.
) Write an 'empty' function to empty a hotspot.
) Giant rocky outcrops?!
) Text background (e.g. for location text)
) Ui hotspot spacing (refactor)
) Bump system - sticking to trees, and climbing them...
) minimap?
) BUG glitching through terrain bc trees
"""
window.color = color.rgb(0,200,225)

# no sky
# indra = Sky()
# indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
# closer to Minecraft height of subject?
subject.height=1.62
subject.camera_pivot.y=subject.height
subject.frog=False # For jumping...
subject.runSpeed=12
subject.walkSpeed=4
subject.blockType=None
# ***
tool=Entity(model='Diamond-Pickaxe.obj',
            texture='diamond_axe_tex.png',
            parent=camera,
            always_on_top=True)
tool.z = 3
tool.x=1.6
tool.rotation_x = 90
tool.rotation_z = 90
tool.rotation_y=-33
tool.y=-0.6
tool.scale=0.07

camera.dash=20 # Rate at which fov changes when running.
# *** - set in inventory.py
# window.fullscreen=True
origFOV=camera.fov=70 # 63 is 'correct' Minecraft? 70 default.
# camera.clip_plane_far=60
# print(camera.clip_plane_far) # 10K!
# window.vsync=False

# *** inv items passed in here?
terrain = MeshTerrain(subject,camera)
# snowfall = SnowFall(subject)
# How do you at atmospheric fog?
scene.fog_density=(-1,75) # 75.
# scene.fog_color=indra.color
scene.fog_color=window.color # color.white
scene.fog_density=(-1,99)
scene.fog_color=window.color # color.white
# *** False to enable huge terrain at start.
generatingTerrain=True

# Generate our terrain 'chunks'.
# *** default 4 for debugging. 128 takes 30seconds-ish.
# *** 512 took under 3mins.
for i in range(4):
    terrain.genTerrain()
# For loading in a large terrain at start.
# loadMap(subject,terrain)

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)
sound_ON = True

pX = subject.x
pZ = subject.z

def input(key):
    # *** earthquake and sound
    global generatingTerrain, earthquake_ON, sound_ON
    terrain.input(key)
    if key=='q': earthquake_ON = not earthquake_ON
    if key=='o': sound_ON = not sound_ON
    if key=='g':
        generatingTerrain = not generatingTerrain
    # Jumping...
    if key=='space': subject.frog=True
    # Saving and loading...
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)

    # Inventory access.
    inv_input(key,subject,mouse)
    
    # ***
    # scene.fog_density=(-1,99)
    # scene.fog_color=window.color # color.white
    

count=0
earthcounter=0
earthquake_ON=False
def update():
    global count, pX, pZ, earthcounter, origFOV

    # Highlight terrain block for mining/building...  
    terrain.update()

    # Handle mob ai.
    mob_movement(grey, subject.position, terrain.td)

    count+=1
    # ***
    if count >= 1:
        
        # count=4
        # Generate terrain at current swirl position.
        # ***
        if generatingTerrain:
            terrain.genTerrain()
            # 12
            # for i in range(4):
            #     terrain.genTerrain()
                
    

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if sound_ON:
            if subject.y > 4:
                if snow_audio.playing==False:
                    snow_audio.pitch=ra.random()+0.25
                    snow_audio.play()
            elif grass_audio.playing==False:
                grass_audio.pitch=ra.random()+0.7
                grass_audio.play()
    
    # *******
    #  Earthquake experiment!
    if earthquake_ON:
        earth_amp=0.1
        earth_freq=0.5
        earthcounter+=earth_freq
        for h in terrain.subsets:
            h.y = (math.sin(terrain.subsets.index(h) + 
                            earthcounter)*earth_amp)#*time.dt
    # *******

    # Walk on solid terrain, and check wall collisions.
    bumpWall(subject,terrain)
    # Running and dash effect.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        # *** - default fov
        if camera.fov>origFOV:
            camera.fov-=camera.dash*4*time.dt
            if camera.fov<origFOV:camera.fov=origFOV

app.run()