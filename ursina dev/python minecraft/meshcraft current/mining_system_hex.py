from ursina import Entity, color, floor, Vec3
# Build Tool Entity (aka 'bte').
# bte = Entity(model='block.obj',color=color.rgba(1,1,0,0.4))
# *** HEX
bte = Entity(model='stretch_hex.obj',color=color.rgba(1,1,0,0.4))
bte.scale=1.1
bte.origin_y+=0.05

def highlight(pos,cam,td):
    for i in range(1,132):
        # Adjust for player's height!
        wp=pos+Vec3(0,1.86,0)+cam.forward*(i*0.5)
        # This trajectory is close to perfect!
        # If we can hit perfection...one day...?
        x = round(wp.x)
        y = floor(wp.y)
        z = round(wp.z)
        # *** HEX
        bte.x = x + 0.5 * (z % 2 == 0)
        bte.y = y
        bte.z = z
        whatT=td.get((x,y,z))
        if whatT!=None and whatT!='g':
            bte.visible = True
            break
        else:
            bte.visible = False

def mine(td,vd,subsets,_numVertices):
    if not bte.visible: return

    wv=vd.get((floor(bte.x),floor(bte.y),floor(bte.z)))
    
    # Have we got a block highlighted? If not, return.
    if wv==None: return
    # ***
    for i in range(wv[1]+1,wv[1]+(_numVertices+1)):
        subsets[wv[0]].model.vertices[i][1]+=999
    
    subsets[wv[0]].model.generate()

    # g for gap in terrain. And wipe vd entry.
    td[ (floor(bte.x),floor(bte.y),floor(bte.z))]='g'
    vd[ (floor(bte.x),floor(bte.y),floor(bte.z))] = None
    
    return (bte.position, wv[0])