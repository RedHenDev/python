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

from ursina import Entity, color, math

bte=Entity(model='cube',color=color.rgba(1,1,1,0.1),scale=1.01)
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
    
def mine_action(subject, td, subsets, model, vd):
    global bte
    print('mining!')
    
    
    wv = vd.get(str(int(bte.x))+'_'+str(int(bte.z)))
    # del subsets[wv[0]].model.vertices[wv[1]:wv[1]+36]
    for v in range(wv[1]+1,wv[1]+36):
        subsets[wv[0]].model.vertices[v][1]=-999
    subsets[wv[0]].model.generate()

    # wv = vd.get(str(int(bte.x))+'_'+str(int(bte.z)))
    # for v in range(wv,wv+36): 
    #     model.vertices[v][1] = 999
    # model.generate()