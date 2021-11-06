"""
Terrain generation by mesh class
30/10/21
"""
from ursina import *
from rh_perlin_noise import PerlinTerrain
from rh_miner import Miner

class MeshTerrain:
    def __init__(this,_subject,_camera):
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        
        # Dictionaries.
        # td for location, vd for vertices and mining. 
        this.td = {}
        this.vd = {}

        # Should we be generating new terrain?
        this.generating = True

        this.subsets = []
        this.subsetNum = 512
        this.subWidth = 4
        this.currentSubset = 0
        this.totalCubes = this.subWidth*this.subWidth

        this.perlin = PerlinTerrain()
        this.miner = Miner( _subject,_camera,
                            this.td,this.vd,
                            this.subsets)

        # For tracking amount of blocks in each
        # subset. See paintTerrain().
        this.countCubes = 0

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
            # Used in checking terrain dist from subject.
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

    def gen_block(this,x,y,z,subsetNum,tex='grass'):
        from random import randint
        from nMap import nMap
        # subsets[currentSubset].enable()
        model = this.subsets[subsetNum].model
        
        # Record position of subset.
        # For checking distance...
        # this.subsets[this.currentSubset].pos.x = this.subsets[this.currentSubset].x
        # this.subsets[this.currentSubset].pos.y = this.subsets[this.currentSubset].z

        # y = floor(this.genPerlin(x,z))   
        cc = nMap(y,-32,32,0.32,0.84)
        cc += randint(1,100)/100
        model.colors.extend((   Vec4(cc,cc,cc,1),) * 
                                len(this.block.vertices))
        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # *** UVs - NB. scale of texture must be adjusted.
        if tex=='grass':
            what_tile_x = 8
            what_tile_y = 7
        elif tex=='soil':
            what_tile_x = 10
            what_tile_y = 7
        elif tex=='grey_stone':
            what_tile_x = 8
            what_tile_y = 5
        elif tex=='snow':
            what_tile_x = 8
            what_tile_y = 6
            # Counting from top left to bottom right.
        uu = what_tile_x
        uv = what_tile_y
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])
        # model.uvs.extend([Vec2(8,7) + u for u in this.block.uvs])

        # Record cube on terrain dictionary td.
        this.td[str(x)+'_'+str(y)+'_'+str(z)] = 't'
        # Record which subset and index of first vertex
        # on vd dictionary for Mining.
        vob = (subsetNum,len(model.vertices)-37)
        this.vd[str(x)+'_'+str(y)+'_'+str(z)] = vob
        # return vob
    
    """
    def set_texture(this,tex,model=None,uvs=None):
        if model==None and uvs==None: return
        # *** UVs - NB. scale of texture must be adjusted.
        if tex=='grass':
            what_tile_x = 8
            what_tile_y = 7
        if tex=='soil':
            what_tile_x = 10
            what_tile_y = 7
        if tex=='grey_stone':
            what_tile_x = 8
            what_tile_y = 5
            # Counting from top left to bottom right.
        uu = what_tile_x
        uv = what_tile_y
        if uvs==None:
            model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])
            return
    """    
            


    def subset_regen(this):
        # These now generate in gen_subset (i.e. texture atlas).
        # model.uvs += (block.uvs) * this.subWidth*this.subWidth*4
        this.subsets[this.currentSubset].model.generate()

    def next_subset(this):
        this.currentSubset += 1
        if this.currentSubset >= len(this.subsets)-1:
            this.currentSubset = 0 
            print('used all subsets')
            # this.generating=False

    def genPerlin(this,x,z):
        return this.perlin.findHeight(x,z,False)

    def gen_walls(this,epicentre):
        if epicentre==False: return

        # If we are here, then epicentre must
        # be a Vec3 -- i.e. the xyz co-ord of
        # cube just mined.
        m = epicentre[3] # Which subset.
        # North wall:
        x = math.floor(epicentre[0])
        y = math.floor(epicentre[1])
        z = math.floor(epicentre[2]+1)
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='soil')
        # South wall:
        x = math.floor(epicentre[0])
        y = math.floor(epicentre[1])
        z = math.floor(epicentre[2]-1)
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='soil')
        # East wall:
        x = math.floor(epicentre[0]+1)
        y = math.floor(epicentre[1])
        z = math.floor(epicentre[2])
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='soil')
        # West wall:
        x = math.floor(epicentre[0]-1)
        y = math.floor(epicentre[1])
        z = math.floor(epicentre[2])
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='soil')
        # Upper wall:
        x = math.floor(epicentre[0])
        y = math.floor(epicentre[1]+1)
        z = math.floor(epicentre[2])
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='soil')
        # Lower wall:
        x = math.floor(epicentre[0])
        y = math.floor(epicentre[1]-1)
        z = math.floor(epicentre[2])
        if this.td.get(str(x)+'_'+str(y)+'_'+str(z))==None:
            this.gen_block(x,y,z,m,tex='grey_stone')
        
        # Regenerate subset's model with spawned walls :)
        this.subsets[m].model.generate()

    def terrain_input(this,key):
        if key=='left mouse up':
            this.gen_walls(this.miner.mine())
        if key=='g':
            this.generating = not this.generating
    
    def new_swirl_origin(this,x,z,rot,rad=16):
        rot = math.radians(rot)
        x += rad * math.sin(rot)
        z += rad * math.cos(rot)
        pos = Vec2(x,z)
        this.subPos = pos
        this.reset_swirl()

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
                y = floor(this.genPerlin(x+j,z+k))
                if this.td.get(str(x+j)+'_'+str(y)+'_'+str(z+k))==None:
                    newT = True
                    this.countCubes+=1
                    
                    # Biomes.
                    if x+j > 10:
                        tex = 'grey_stone'
                    else: tex = 'grass'
                    if y > 5: tex = 'snow'
                    this.gen_block(x+j,y,z+k,this.currentSubset,tex)

                    # Create extra below! ***
                    # this.gen_block(x+j,y-1,z+k,this.currentSubset)
                    # this.countCubes+=1

                    # Protect surface from spawned walls.
                    # Mark all as a 'gap'.
                    this.td[str(x+j)+'_'+str(y+1)+'_'+str(z+k)]='g'

        # Only generate model if new terrain to be built.
        if newT==True:
            if this.countCubes>=this.totalCubes:
                this.countCubes=0
                # this.subset_regen(this.totalCubes*2)
                this.subset_regen()
                this.next_subset()