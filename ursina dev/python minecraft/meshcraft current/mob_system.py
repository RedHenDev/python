# Mobs deserve their own mobule :)

from ursina import *

grey = FrameAnimation3d('panda_walk_',fps=1)
# ***
grey.texture='panda_texture'
grey.position = Vec3(0,-2.9,10)
grey.turnSpeed = 1
grey.speed = 1
grey.a=True

# Can we find Vincent?!
vincent = Entity(model='chicken.obj',scale=1)
vincent.texture='chicken.png'
vincent.z = 16
vincent.y = 8
vincent.rotation_y=180
vincent.turnSpeed = 0.1
vincent.speed = 0.1
vincent.a=False

def mob_movement(mob, subPos, _td):
    # First, turn towards target...
    # BUG wiggle walk when aligned with subject?
    tempOR = mob.rotation_y
    mob.lookAt(subPos)
    #***
    if mob.a:
        mob.rotation = Vec3(0,mob.rotation.y+180,0)
    else: mob.rotation = Vec3(0,mob.rotation.y,0)
    mob.rotation_y = lerp(tempOR,mob.rotation_y,mob.turnSpeed*time.dt)

    # Now move mob towards target...
    # How close can they approach?
    intimacyDist = 3
    # How far away from target?
    dist = subPos-mob.position
    # Magnitude of distance from target examined...
    if dist.length() > intimacyDist:
        # ***
        if mob.a:
            # Approach target...
            mob.position -= mob.forward * mob.speed * time.dt
            mob.resume() # Animation.
            mob.is_playing=True
        else:
            # Approach target...
            mob.position += mob.forward * mob.speed * time.dt
    else:
        if mob.a:
            mob.pause() # Animation.
            mob.is_playing=False

    terrain_walk(mob, _td)

def terrain_walk(mob, _td):
    # Check mob hasn't fallen off the planet ;)

    if mob.y < -100:
        mob.y = 100
        print("I've fallen off!")

    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    for i in range(-step,step):
        whatT1=_td.get((x,y+i,z))
        if whatT1!=None and whatT1!='g':
            whatT2=_td.get((x,y+i+1,z))
            if whatT2!=None and whatT2!='g':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        mob.y = lerp(mob.y, target, 6 * time.dt)
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt
