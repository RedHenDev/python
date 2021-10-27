"""
Mining module
Tues 26th Oct 2021

Can we integrate this with the pycraft_mesh_dev?
I think it will be called by rh_terrain_gen.py
but perhaps from input() of main pycraft_mesh_dev module.
rh_terrain will thus just have a shell function passing
us straight through and collecting the subject and td
objects as it goes.
"""

from ursina import Entity, color, duplicate, math

bte=Entity(model='cube',color=color.white,scale=1.01)
# bte.always_on_top=True
bte.pos = bte.position

def build_tool_entity(subject,camera,td):
    global bte
    radius = 1
    max = 5
    best = None
    # Iterate until nearest block found in
    # front of subject.
    while radius < max:
        origin = subject.position
        origin.y +=2
        where = (   origin + 
                    camera.forward * radius)
        bte.x = (math.floor(where.x+0.5))
        bte.z = (math.floor(where.z+0.5))
        try:
            bte.y = td.get( str(int(bte.x))+'_'+
                            str(int(bte.z)))+0.5
            radius+=1
            best = bte.y
        except:
            radius+=1
            if best!=None: bte.y = best
    
def mine_action(subject, td, subsets, model):
    global bte
    print('mining?')
    print(td.get(   str(int(math.floor(bte.x)))+'_'+
                    str(int(math.floor(bte.z)))))
    
    e = duplicate(bte)
    e.color=color.cyan
    # e.always_on_top=True

    totalV = 0
    vChange = False
        
    for v in model.vertices:
        # Is the vertex close enough to
        # where we want to mine (bte position)?
        if (v[0] >=bte.x - 0.5 and
            v[0] <=bte.x + 0.5 and
            v[1] >=bte.y - 0.5 and
            v[1] <=bte.y + 0.5 and
            v[2] >=bte.z - 0.5 and
            v[2] <=bte.z + 0.5):
            # Yes!
            #v[1] -= 1
            # Move vertex high into air to
            # give illusion of being destroyed.
            # model.colors[:] = color.rgba(0,0,0,0)
            # Note that we have made change.
            # Gather average height for cave dic.
            vChange = True
            totalV += 1
            # The mystery of 36 vertices!! :o
            # print('tV= ' + str(totalV))
            if totalV==36: break
    
    # if vChange == True:
        # model.generate()



"""
# Our real mining of the terrain :)
        # Iterate over all the subsets that we have...
        totalV = 0
        for s in range(len(this.subsets)):
            vChange = False
            
            for v in this.subsets[s].model.vertices:
                # Is the vertex close enough to
                # where we want to mine (bte position)?
                if (v[0] >=this.bte.x - 0.5 and
                    v[0] <=this.bte.x + 0.5 and
                    v[1] >=this.bte.y - 0.5 and
                    v[1] <=this.bte.y + 0.5 and
                    v[2] >=this.bte.z - 0.5 and
                    v[2] <=this.bte.z + 0.5):
                    # Yes!
                    #v[1] -= 1
                    # Move vertex high into air to
                    # give illusion of being destroyed.
                    v[1] = 9999
                    # Note that we have made change.
                    # Gather average height for cave dic.
                    vChange = True
                    totalV += 1
                    # The mystery of 36 vertices!! :o
                    # print('tV= ' + str(totalV))
                    if totalV==36: break
            
            if vChange == True:

                # Now we need to spawn a new cube below
                # the bte's position -- if no cube or
                # gap there already.
                # Next, spawn 4 cubes to create illusion
                # of more layers -- if each position is
                # neither a gap nor a place where terrain
                # already is.
                # Record new gap on dictionary.
                this.tDic[  'x'+str(this.bte.x)+
                            'y'+str(this.bte.y)+
                            'z'+str(this.bte.z)] = 'gap'
                this.mineSpawn()
                # Now that we've spawned what (if anything)
                # we need to, update subset model. Done.
                this.subsets[s].model.generate()
                this.builds.combine()
                return
"""