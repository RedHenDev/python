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
            origin.y = math.floor(origin.y)
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
            if what!=None and what!='g':
                this.bte.position = best

    def mine(this):
        x = str(int(this.bte.x))
        y = str(int(this.bte.y))
        z = str(int(this.bte.z))
        wv = this.vd.get(x+'_'+y+'_'+z)
        for v in range(wv[1]+1,wv[1]+37):
            this.subsets[wv[0]].model.vertices[v][1]-=1

        # Spawn terrain walls?

        this.subsets[wv[0]].model.generate()

        this.td[x+'_'+y+'_'+z] = 'g'
        this.td[x+'_'+str(int(y)-1)+'_'+z] = 't'