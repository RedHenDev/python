from ursina import Entity, color, math
from ursina.vec3 import Vec3

class Miner:
    def __init__(this,_subject,_camera,_td,_vd,_subsets):
        this.bte=Entity(model='cube',
                        color=color.rgba(1,1,0,0.4),
                        scale=1.01)

        this.subject = _subject
        this.camera = _camera
        this.td = _td
        this.vd = _vd
        this.subsets = _subsets

    def build_tool_entity(this):
        import numpy as np
        # I need to incorporate y here! ***
        radius = 0.1
        max = 5
        this.bte.position = best = Vec3(0,-999,0)
        # Iterate until nearest block found forward.
        while radius < max:
            origin = this.subject.position
            origin.y = math.floor(origin.y+1)
            where = (   origin + 
                        this.camera.forward * radius)
            x = (np.round(where.x))
            y = (np.round(where.y+0.5))
            z = (np.round(where.z))
            try:
                what = this.td.get( 
                                str(int(x))+'_'+
                                str(int(y))+'_'+
                                str(int(z)))
                best = Vec3(x,y+0.5,z)
            except:
                pass
            radius+=1
            if what=='t':
                this.bte.position = best

    def mine(this):
        from ursina import Vec2
        x = str(math.floor(this.bte.x))
        y = str(math.floor(this.bte.y))
        z = str(math.floor(this.bte.z))
        
        wv = this.vd.get(x+'_'+y+'_'+z)
        wt = this.td.get(x+'_'+y+'_'+z)
        ob = this.td.get(x+'_'+str(int(y)-1)+'_'+z)

        # First, remove block and add new block below site.
        if wt == 't' and ob == None:
            for v in range(wv[1]+1,wv[1]+37):
                this.subsets[wv[0]].model.vertices[v][1]+=999
            # New block will be added upon return...

            # Update dictionaries.
            this.td[x+'_'+y+'_'+z] = 'g'
            # Protect upper pos from spawned wall.
            # *** Need to detect dig trajectory and
            # do these 'protections' properly.
            # Using a try: except: due to sporadic KeyError.
            try:
                a = this.td[x+'_'+str(int(y)+1)+'_'+z]
                if a==None:
                    this.td[x+'_'+str(int(y)+1)+'_'+z] = 'g'
            except:
                this.td[x+'_'+str(int(y)+1)+'_'+z] = 'g'
            this.vd[x+'_'+y+'_'+z] = None
            """
            # Record vertices tuple on return. 
            # First, which subset. Second, vertex index.
            """
            # Spawn terrain walls?
            # Return centre-point to rh_mesh_terrain.
            return (int(x),int(y),int(z),wv[0])
        elif wt == 't' and ob != None:
            for v in range(wv[1]+1,wv[1]+37):
                this.subsets[wv[0]].model.vertices[v][1]+=999
            this.subsets[wv[0]].model.generate()
            # Update dictionaries.
            this.td[x+'_'+y+'_'+z] = 'g'
            # Protect upper pos from spawned wall.
            # *** Need to detect dig trajectory and
            # do these 'protections' properly.
            # Using a try: except: due to sporadic KeyError.
            try:
                a = this.td[x+'_'+str(int(y)+1)+'_'+z]
                if a==None:
                    this.td[x+'_'+str(int(y)+1)+'_'+z] = 'g'
            except:
                this.td[x+'_'+str(int(y)+1)+'_'+z] = 'g'
            this.vd[x+'_'+y+'_'+z] = None
            # Return dig epicentre and subset index.
            return (int(x),int(y),int(z),wv[0])
        else: 
            print('No dice, grandma')
            return False