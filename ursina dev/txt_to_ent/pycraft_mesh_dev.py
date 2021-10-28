from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from rh_gen_terrain import loadMap, swirl, swirl_pos, reset_swirl, gen_subset, set_subPos, next_subset, subset_regen
from rh_gen_terrain import check_subset, terrain_input
from numpy import abs

"""
Some notes about how this mess works:
Perlin must be co-ordinated with the map_builder that
contributed the loaded terrain at start.

This module controls how wide each subset will be
and how often created and after how many steps
a new origin for the swirling terrain to be
generated.

rh_gen_terrain controls how many subsets and
when to use the first on the list again etc
(at present 24th Oct 2021 this is not organised
really at all) - what we really need is to turn off
subsets behind the player, on again if in front.
So, subsets also need to record their location in
a dictionary. Now, this won't work until we sort
out the above issue of subsets being reused by
new terrain generation resulting in subsets being
giant dispersed things.

The reason for subsets is precisely for being able
to turn off and on for 60fps over giant terrains.
Also, for rapid generation of terrain (although
this seems to be more a matter of balancing
size of new chunks etc (see details above)). Oh, meaning
that we might just as well do without subsets and
add new 'chunks' to existing single terrain entity.

Seems to work well with a large 256 size terrain
and subset of size 8x8, 512 subsets, radius of 16
for projected subset start pos ahead of subject,
painting terrain every 5 frames, and resetting start pos
after subject moving more than 8 units.

Another thing we need to look at is diversity of
terrain texture, i.e. using the dual/multiple entity
system that has been proven to work. Second, we
need to test out mining.

But right now I just want to test running this without
the subsets hack. Yeah, was waaaaay too slow.
"""

app = Ursina()

subject = FirstPersonController()
subject.y = 99
subject.x = 128
subject.z = 128
subject.gravity = 0.0
subject.cursor.visible=False
subject.speed = 6
# window.color=color.cyan
scene.fog_color = color.cyan
scene.fog_density = 0.02
Sky(color=color.cyan)

def new_terrain_gen_orig():
    radius = 16
    x = subject.x + radius * math.sin(math.radians(subject.rotation_y))
    z = subject.z + radius * math.cos(math.radians(subject.rotation_y))
    pos = Vec2(0,0)
    pos.x = x
    pos.y = z
    # pos = Vec2(subject.x,subject.z)
    set_subPos(pos)
    reset_swirl()

map_name = 'terrain_6.map'
td = {} # Terrain dictionary.
vd = {} # Vertex dictionary.
td, vd = loadMap(map_name)
# Position subject at centre of given map.
subject.x = math.sqrt(len(td))*0.5
subject.z = subject.x
new_terrain_gen_orig()
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

    terrain_input(key,subject,td, vd)

counter=0
preVpos = subject.position
def update():
    from fh_mining import build_tool_entity
    global counter, preVpos

    counter+=1
    # How quickly to generate new terrain.
    if counter%3==0:
        paintTerrain()
        # Disable and enable individual subsets
        # according to distance from subject.
        check_subset(subject)
    if  abs(subject.position.x - preVpos.x) > 8 or \
        abs(subject.position.z - preVpos.z) > 8:
        new_terrain_gen_orig()
        preVpos = subject.position

    build_tool_entity(subject,camera,td)
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
        target_y = 2 + td.get(str(floor(subject.x+0.5))+'_'+str(floor(subject.z+0.5)))
        subject.y = lerp(subject.y, target_y, 0.1)
    except: 
        subject.y=subject.y
app.run()