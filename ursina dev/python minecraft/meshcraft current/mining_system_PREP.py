# from ursina import Entity, color, floor, Vec3
# ***
from ursina import *
bte = Entity(model='block.obj',color=color.rgba(1,1,0,0.4))
bte.scale=1.1
# Adjust for model offset.
bte.origin_y+=0.05
bp = Entity(model='block.obj',texture='ursina_wink_0001')
bp.texture_scale=0.25
# bp.origin_y-=5.1
# bp.scale=0.11

def highlight(pos,cam,td):
    for i in range(1,32):
        # Adjust for player's height!
        wp=pos+Vec3(0,1.86,0)+cam.forward*(i*0.5)
        # This trajectory is close to perfect!
        # If we can hit perfection...one day...?
        x = round(wp.x)
        y = floor(wp.y)
        z = round(wp.z)
        bte.x = x
        bte.y = y # ***
        bte.z = z
        if td.get((x,y,z))!=None and \
            td.get((x,y,z))[0]!='g':
            bte.visible = True
            # ***
            bp.visible = True
            break
        else:
            bte.visible = False
            # ***
            bp.visible = False

def mine(td,vd,subsets):
    if not bte.visible: return
    # ***
    wv=vd.get((int(bte.x),int(bte.y),int(bte.z)))
    
    # Have we got a block highlighted? If not, return.
    if wv==None: return
    
    # Deleting the vertices (and colours) not a solution!
    # Try it out!
    # del subsets[wv[0]].model.vertices[wv[1]+1:wv[1]+37]
    # del subsets[wv[0]].model.colors[wv[1]+1:wv[1]+37]
    for i in range(wv[1]+1,wv[1]+37):
        # Make invisible?
        subsets[wv[0]].model.colors[i][3]=0.5
        # subsets[wv[0]].model.vertices[i][1]+=999
    
    # This is called outside, so redundant here.
    # subsets[wv[0]].model.generate()

    # Nice idea? Nope. Well, idea is to move just this
    # block to full transparency, not the whole subset.
    # But advantage would be that we don't have to 
    # generate the model!
    # subsets[wv[0]].texture_scale*=2

    # g for gap in terrain. And wipe vd entry.
    # ***
    td[ (int(bte.x),int(bte.y),int(bte.z))]=['g',None]
    vd[ (int(bte.x),int(bte.y),int(bte.z))] = None

    return (bte.position, wv[0])