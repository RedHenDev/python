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
mins=list(minerals.keys())

class item_panel(Entity):
    def __init__(this,cols=9,rows=3):
        super().__init__()
        this.model='quad'
        this.texture='white_box.png'
        this.parent=camera.ui
        this.cols=cols
        this.rows=rows
        this.texture_scale=(this.cols,this.rows)
        this.scale=(this.cols/10,this.rows/10)
        this.origin=(-0.5,0.5)
        this.x=this.scale_x*-0.5
        this.y=this.scale_y*0.5
        this.trays=[Vec2(x,y) for x in range(this.cols) for y in range(this.rows)]
        
        
    
    def update(this):
        pass

ite=item_panel()

class item_icon(Draggable):
    def __init__(this,blockType='grass'):
        super().__init__()
        this.model='quad'
        this.parent=ite # Let's try this...
        this.scale_x=1/(this.parent.texture_scale[0]*1.2)
        this.scale_y=1/(this.parent.texture_scale[1]*1.2)
        this.origin=(-0.5*1.2,0.5*1.2)
        
        this.blockType=blockType
        this.color=color.white

        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width  
        this.setup_texture()

    def drop(this):
        print(f"x={this.x},y={this.y}")
        # this.x=int(this.x*10)/10
        # this.y=int(this.y*100)/100
        """
        x=-0.00010246038436889648,y=-0.0009403526782989502
        x=0.11149701476097107,y=-0.3401150405406952
        x=0.2226986289024353,y=-0.6690537929534912
        """
        sv = str(abs(this.x))[2]
        this.x = 0.111*float(sv)

        sv = str(abs(this.y))[2]
        sv = int(round(int(sv))/3)
        print(sv)
        this.y= -sv * 0.33
        # if sv == 0: this.y=0
        # elif sv==1: this.y=-0.34
        # else: this.y=-0.67
        

    def setup_texture(this):
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        # basemod=load_model('block.obj')
        basemod=load_model('quad')
        cb=copy(basemod.uvs)
        # for v in cb:
        #     v=(v[0]*0.25,v[1]*0.25)
        # OK this isn't right -- but gives ok texture.
        # del cb[:-33]
        print(cb)
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        # this.rotation_z=180
    
    def setup_color(this):
        # Do we have a color element on the list?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]

test_item=item_icon()

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