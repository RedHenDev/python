from ursina import *

# inventory=Panel()
# inventory=Entity(model='quad',parent=camera.ui)
# inventory.color=color.dark_gray
# inventory.scale=0.1
# inventory.scale_x*=9
# inventory.origin=(0,4.5)

# hLighter=Entity(model='quad',parent=camera.ui)
# hLighter.color=color.black
# hLighter.scale=0.088
# hLighter.origin=(4.5,5.1)

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=(window.windowed_size.y/9)/window.windowed_size.y
# print(f'Window size is {window.windowed_size.y}')
hotbar.scale_x=0.8
hotbar.y=-0.5 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.light_gray

minerals =  {   'grass' : (8,7),
                'soil' : (10,7),
                'stone' : (8,5),
                'concrete' : (9,6),
                'ice' : (9,7),
                'snow' : (8,6),
                'ruby' : (9,6,Vec4(1,0,0,1))
            }
# Create iterable list from dictionary keys (not values).
mins = list(minerals.keys())

class hotspot(Entity):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.dark_gray
        # Why 10 here instead of 9? Weird.
        this.scale=hotbar.scale_x/10.3
        this.y=-0.5+(hotbar.scale_y*0.5)

class item_icon(Entity):
    def __init__(this,blockType='grass'):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.blockType=blockType

        this.color=color.white
        # And why 10 instead of 9?
        this.scale=hotbar.scale_x/10.3
        # WHy 0.54?
        this.y=-0.5+(hotbar.scale_y*0.5)
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        # (32/(this.texture.width))  
        this.setup_texture()

    def setup_texture(this):
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        basemod=load_model('block.obj')
        cb=copy(basemod.uvs)
        # print(len(cb.uvs))
        del cb[:-33]
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        this.rotation_z=180
    
    def setup_color(this):
        # Do we have a color element on the list?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]

# Test hotspots.
hs=[]
for i in range(9):
    e = hotspot()
    e.x = (-4.5*e.scale_x) + ((e.scale_x+0.01) * i)
    hs.append(e)
hs[0].color=color.lime
gs = []
for i in range(9):
    e = item_icon(mins[i%len(mins)])
    e.x = (-4.5*e.scale_x) + ((e.scale_x+0.01) * i)
    e.setup_color()
    e.scale*=0.9
    gs.append(e)


def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True

    
    if key=='r':
        # Just cycle through possible blocks, 'len(mins)'.
        subject.blockTnum=(subject.blockTnum+1)%(len(mins))
        for h in hs: 
            h.color=color.dark_gray
        hs[subject.blockTnum].color=color.lime
        