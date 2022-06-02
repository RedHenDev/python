"""Subject terrain collisions -- i.e. not ghosting
through walls etc."""

from ursina import Vec3, held_keys, time, lerp

def bumpWall(subject,terrain):
    blockFound=False
    step = 2
    jumpHeight = 3
    height = subject.height
    x = round(subject.x)
    z = round(subject.z)
    y = round(subject.y)
    # Simple wall collision detection.
    # Front and Back.
    # inF is location of block ahead, behind, side, etc.
    def checkBump(inF):
        for i in range(1,step+1):
            whatT=terrain.td.get(  (round(inF.x),
                                round(inF.y+i),
                                round(inF.z)) )
            if whatT!='g' and whatT!=None:
                return True
        return False
    # In front...
    # Also check diagonal left and right...
    howClose=0.55
    rPos=Vec3(x,y,z)
    subFor=subject.forward
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.left*howClose*0.5) or
        checkBump(bDir+subject.right*howClose*0.5)):
        held_keys['w'] = 0
    # Behind...
    bDir=rPos-subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.left*howClose*0.5) or
        checkBump(bDir+subject.right*howClose*0.5)):
        held_keys['s'] = 0
    # Left...
    subFor=subject.left
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.forward*howClose*0.5) or
        checkBump(bDir+subject.back*howClose*0.5)):
        held_keys['a'] = 0
    # Right...
    bDir=rPos-subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.forward*howClose*0.5) or
        checkBump(bDir+subject.back*howClose*0.5)):
        held_keys['d'] = 0
        
    # Walking on the terrain itself.
    for i in range(-2,step):
        # ***
        whatT=terrain.td.get((x,y+i,z))
        if whatT!='g'and whatT!=None:
            whatT1=terrain.td.get((x,y+i+1,z))
            if whatT1!='g'and whatT1!=None:
                # Also check any blocks above, still within stepping range.
                target = y+i+height+1
                blockFound=True
                break
            # Stomach height?
            whatT2=terrain.td.get((x,y+i+2,z))
            if whatT2!='g'and whatT2!=None:
                target = y+i+height+2
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        subject.y = lerp(subject.y, target, 6 * time.dt)
        # We are grounded -- so can jump...
        if subject.frog is True:
            subject.frog=False
            subject.y+=jumpHeight
    else:
        # Gravity fall :<
        subject.y -= 9.8 * time.dt