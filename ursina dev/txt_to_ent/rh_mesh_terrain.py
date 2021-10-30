"""
Terrain generation by mesh class
30/10/21
"""
from ursina import *
from rh_perlin_noise import PerlinTerrain

class MeshTerrain:
    def __init__(this,_map_name):
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        
        this.perlin = PerlinTerrain()

        this.subsets = []
        this.subsetNum = 512
        this.subWidth = 8
        this.currentSubset = 0
        this.totalCubes = this.subWidth*this.subWidth

        # For tracking amount of blocks in each
        # subset. See paintTerrain().
        this.countCubes = 0

        # Dictionaries.
        # td for location, vd for vertices and mining. 
        this.td = {}
        this.vd = {}

        # Controls for swirling terrain.
        this.currentVec = 0
        this.iterations = 0
        this.toIterate = 1
        this.changes = -1
        this.subPos = Vec2(32,32)
        this.swirlVecs = [
            Vec2(0,0),
            Vec2(0,1),
            Vec2(1,0),
            Vec2(0,-1),
            Vec2(-1,0)
        ]

        this.setup_subsets()

    def setup_subsets(this):
        if len(this.subsets)!=0: return
    
        for i in range(this.subsetNum):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            # Adjust scale of texture.
            e.texture_scale*=64/e.texture.width
            e.pos = Vec2(0,0)
            this.subsets.append(e)

    def reset_swirl(this):
        this.currentVec = 0
        this.iterations = 0
        this.toIterate = 1
        this.changes = -1
    
    def swirl(this):
        # Co-ordinate new vector by iteration around swirl.
        this.iterations+=1
        if this.iterations==this.toIterate:
            this.currentVec+=1
            if this.currentVec==len(this.swirlVecs):
                this.currentVec=1
            this.changes+=1
            this.iterations=0
            if this.changes==2:
                this.changes=0
                this.toIterate+=1

    def swirl_pos(this):
        # Translate position of subset, according to
        # current vector.
        this.subPos.x += (  this.swirlVecs[this.currentVec].x *
                            this.subWidth)
        this.subPos.y += (  this.swirlVecs[this.currentVec].y *
                            this.subWidth)
        return this.subPos

    def gen_subset(this,x,z):
        from random import randint
        from nMap import nMap
        # subsets[currentSubset].enable()
        model = this.subsets[this.currentSubset].model
        
        # Record position of subset.
        # For checking distance...
        # this.subsets[this.currentSubset].pos.x = this.subsets[this.currentSubset].x
        # this.subsets[this.currentSubset].pos.y = this.subsets[this.currentSubset].z

        y = floor(this.genPerlin(x,z))   
        cc = nMap(y,-32,32,0.32,0.84)
        cc += randint(1,100)/100
        model.colors.extend((   Vec4(cc,cc,cc,1),) * 
                                len(this.block.vertices))
        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # *** UVs
        tilesX = 2
        tilesY = 1
        # colX from left.
        # rowY from top.
        if z > 10:
            colX = 1
            rowY = 2
        else: 
            colX = 1
            rowY = 1
        uu = tilesX/colX
        uv = tilesY*rowY 
        model.uvs.extend([Vec2(8,7) + u for u in this.block.uvs])

        # Record which subset and index of first vertex
        # on vd dictionary for Mining.
        vob = (this.currentSubset,len(model.vertices)-37)
        return y, vob
    
    def subset_regen(this):
        # These now generate in gen_subset (i.e. texture atlas).
        # model.uvs += (block.uvs) * this.subWidth*this.subWidth*4
        this.subsets[this.currentSubset].model.generate()

    def next_subset(this):
        this.currentSubset += 1
        if this.currentSubset == len(this.subsets)-1:
            this.currentSubset = 0 
            print('used all subsets')

    def genPerlin(this,x,z):
        return this.perlin.findHeight(x,z)
        """
    def mine(this,subject,td,vd):
        from fh_mining import mine_action
        mine_action(subject,td,subsets,terrainObject.model,vd)

    def terrain_input(this,key,subject,td,vd):
        if key=='left mouse up':
            mine(subject,td,vd)
        """
    
    def paintTerrain(this):
        # Find position according to swirl vector...
        pos = this.swirl_pos()
        this.swirl() # Next position to create terrain.
        x = math.floor(pos.x)
        z = math.floor(pos.y)
        newT = False
        wid = floor(this.subWidth * 0.5)
        for j in range(-wid,wid):
            for k in range(-wid,wid):
                if this.td.get(str(x+j)+'_'+str(z+k))==None:
                    newT = True
                    this.countCubes+=1
                    # td[str(x+j)+'_'+str(z+k)]=genTerrain(x+j,z+k)
                    # Actually store the list of vertices on the vd?
                    this.td[str(x+j)+'_'+str(z+k)], \
                    this.vd[str(x+j)+'_'+str(z+k)]= \
                        this.gen_subset(x+j,z+k)
        # Only generate model if new terrain to be built.
        if newT==True:
            if this.countCubes>=this.totalCubes:
                this.countCubes=0
                # this.subset_regen(this.totalCubes*2)
                this.subset_regen()
                this.next_subset()