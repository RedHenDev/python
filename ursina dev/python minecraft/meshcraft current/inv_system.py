from ursina import *

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=(window.windowed_size.y/9.8)/window.windowed_size.y
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

class item_panel(Entity):
    def __init__(this,cols=9,rows=3):
        super().__init__()
        this.model='quad'
        this.ratio=rows/cols
        this.cols=cols
        this.rows=rows 
        # NB y is 1/3 of x. I.e. rows v cols.
        this.scale=0.8
        this.scale_y*=this.ratio
        this.parent=camera.ui
        this.trays=[Vec2(x,y) for x in range(this.cols) for y in range(this.rows)]
        this.texture='white_box.png'
        this.texture_scale=(this.cols,this.rows)
    
    def update(this):
        pass

ite=item_panel()

class hotspot(Entity):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.dark_gray
        # Why 10 here instead of 9? Weird.
        this.scale=hotbar.scale_x/10.3
        this.y=-0.5+(hotbar.scale_y*0.5)

class item_icon(Draggable):
    def __init__(this,blockType='grass'):
        super().__init__()
        this.model='quad'
        this.parent=ite # Let's try this...
        this.blockType=blockType

        this.color=color.white
        # And why 10 instead of 9?
        this.scale_x = this.parent.scale_x/9
        this.scale_y = this.parent.scale_y
        # WHy 0.54?
        # this.y=-0.5+(hotbar.scale_y*0.5)
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        # (32/(this.texture.width))  
        this.setup_texture()

    def drop(this):
        print(9*5*this.x*this.parent.scale.x*this.parent.ratio)
        print(3*5*this.y*this.parent.ratio)

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

test_item = item_icon()

# Test hotspots.
# hs=[]
# for i in range(9):
#     e = hotspot()
#     e.x = (-4.5*e.scale_x) + ((e.scale_x+0.01) * i)
#     e.scale*=1.2
#     hs.append(e)
# hs[0].color=color.white
# gs = []
# for i in range(9):
#     e = item_icon(mins[i%len(mins)])
#     e.x = (-4.5*e.scale_x) + ((e.scale_x+0.01) * i)
#     e.setup_color()
#     e.scale*=1.08
#     e.lock_x=e.lock_y=1
#     gs.append(e)

def inv_input(key,subject,mouse):
    global gs
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
        # for di in gs:
        #     di.lock_x=di.lock_y=0
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True
        # for di in gs:
        #     di.lock_x=di.lock_y=1

    if key=='r':
        # Just cycle through possible blocks, 'len(mins)'.
        subject.blockTnum=(subject.blockTnum+1)%(len(mins))
        # for h in hs: 
        #     h.color=color.dark_gray
        # hs[subject.blockTnum].color=color.white