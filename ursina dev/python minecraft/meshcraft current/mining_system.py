from ursina import Entity, color, floor, Vec3
# ***
from collectible_system import *
from math import sin

# Build Tool Entity (aka 'bte').
bte = Entity(model='block.obj',color=color.rgba(1,1,0,0.4))
# *** HEX
# bte = Entity(model='stretch_hex.obj',color=color.rgba(1,1,0,0.4))
bte.scale=1.1
bte.origin_y+=0.05

def highlight(pos,cam,td):
    # *** - since called in update()
    for p in pickups:
        p.rotation_y+=2
        p.y=p.original_y+sin(p.rotation_y/64)*p.scale_y

    for i in range(1,132):
        # Adjust for player's height!
        wp=pos+Vec3(0,1.86,0)+cam.forward*(i*0.5)
        # This trajectory is close to perfect!
        # If we can hit perfection...one day...?
        x = round(wp.x)
        y = floor(wp.y)
        z = round(wp.z)
        bte.x = x
        bte.y = y
        bte.z = z
        whatT=td.get((x,y,z))
        if whatT!=None and whatT!='g':
            bte.visible = True
            break
        else:
            bte.visible = False

def mine(td,vd,subsets,_numVertices,_texture,_model):
    if not bte.visible: return

    # ***
    # Reference vertices dictionary
    # and see if there is a highlighted block here.
    wv=vd.get((floor(bte.x),floor(bte.y),floor(bte.z)))
    
    # Have we got a block highlighted? If not, return.
    if wv==None: return

    # If here - we're mining :)
    # So, present solution is to simply send the 
    # highlighted block's vertices high into the air
    # and thus 'vanishing' them. Also, record 'gap' on
    # terrain dictionary (td) and update vd.
    # *** - _numVertices used instead of magic number 37.
    for i in range(wv[1]+1,wv[1]+(_numVertices+1)):
        subsets[wv[0]].model.vertices[i][1]+=999
    
    # ***
    # First idea: place collectible
    # behaviour here -- or at least
    # call its functions, housing those
    # functions in collectible_system.py?
    """
    So, 1) Here, request new collectible
    object to be placed around bte pos.
    2) record collectible location on
    its own dictionary? Then we can check
    subject position against collectible
    positions. Check could happen whenever
    subject moves? So, C_S's check() called
    from main?
    3) when picked up, add item to available
    place on hotbar. If no available space,
    do not pick up.
    4) First, make pick ups a tiny cube
    spinning with a bit of sine bob.
    
    """
    # 1
    # What blockType are we mining?
    blockType=td.get((floor(bte.x),floor(bte.y),floor(bte.z)))
    print(blockType)
    new_pickable(_model,_texture,blockType,bte.position)
    # ***

    # Generate model so that changes actually visible.
    subsets[wv[0]].model.generate()

    # g for gap in terrain. And wipe vd entry.
    td[ (floor(bte.x),floor(bte.y),floor(bte.z))]='g'
    vd[ (floor(bte.x),floor(bte.y),floor(bte.z))] = None
    
    # NB. wv[0] is the subset index.
    return (bte.position, wv[0])