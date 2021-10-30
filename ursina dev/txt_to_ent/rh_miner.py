from ursina import Entity, color, math

class Miner:
    def __init__(this,_subject,_camera,_td,_vd,_subsets):
        this.bte=Entity(model='cube',
                        color=color.rgba(1,1,1,0.1),
                        scale=1.01)

        this.subject = _subject
        this.camera = _camera
        this.td = _td
        this.vd = _vd
        this.subsets = _subsets

    def build_tool_entity(this):
        radius = 1
        max = 5
        best = None
        # Iterate until nearest block found forward.
        while radius < max:
            origin = this.subject.position
            origin.y +=2
            where = (   origin + 
                        this.camera.forward * radius)
            this.bte.x = (math.floor(where.x+0.5))
            this.bte.z = (math.floor(where.z+0.5))
            try:
                this.bte.y = this.td.get( 
                                str(int(this.bte.x))+'_'+
                                str(int(this.bte.z)))+0.5
                radius+=1
                best = this.bte.y
            except:
                radius+=1
                if best!=None: this.bte.y = best
        
    def mine(this):
        x = str(int(this.bte.x))
        z = str(int(this.bte.z))
        wv = this.vd.get(x+'_'+z)
        for v in range(wv[1]+1,wv[1]+37):
            this.subsets[wv[0]].model.vertices[v][1]-=1
        this.subsets[wv[0]].model.generate()

        this.td[x+'_'+z] -= 1