from perlin_PREP import Perlin
from ursina import *
from swirl_engine import SwirlEngine
from mining_system_PREP import *
from building_system_PREP import *
# ***
import random as ra
from inv_system import mins, minerals
# ***
from config import six_cube_dirs

class MeshTerrain:
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam

        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 64
        
        # Must be even number! See genTerrain()
        this.subWidth = 8 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        # Instantiate our subset Entities.
        this.setup_subsets()

    def setup_subsets(this):
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        epi = mine(this.td,this.vd,this.subsets)
        if epi != None:
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    # ***
    def update(this):
        highlight(  this.subject.position,
                    this.camera,this.td,
                    this.subject.height)
        # Blister-mining!
        if bte.visible==True:
            # Build site indicator...
            # temp=checkBuild( bte.position,this.td,
            #                     this.camera.forward,
            #                     this.subject.position+Vec3(0,this.subject.height,0),
            #                     bp)
            if held_keys['shift'] and held_keys['left mouse']:
                this.do_mining()
            # for key, value in held_keys.items():
            #     if key=='left mouse' and value==1:
            #         this.do_mining()

    def input(this,key):
        if key=='left mouse up' and bte.visible==True:
            this.do_mining()
        # Building :)
        # ***
        # if key=='right mouse up' and bp.visible==True:
        if key=='right mouse up' and bte.visible==True:
            # ***
            bsite = checkBuild( bte.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0),
                                bp)
            if bsite!=None:
                this.genBlock(bsite.x,bsite.y,bsite.z,subset=0,blockType=mins[this.subject.blockTnum])
                # print(mins[this.subject.blockTnum])
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        # ***
        # Avoid lazy import - place at top of module.
        # from config import six_cube_dirs
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        
        for i in range(0,6):
            np = epi + six_cube_dirs[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')


    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        
        # ***
        # This is where we used to record td.

        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            dot = this.td.get(key)
            if dot is None:
                this.td[key]=['g',subset]

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-37)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

        # *** New colour system.
        # Do we have a color element on the list?
        if len(minerals[blockType]) > 2:
            # print(minerals[blockType][2])
            model.colors.extend((minerals[blockType][2],)*
                                    this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = ra.random()-0.5
            model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                    this.numVertices)

        # ***
        uu = minerals[blockType][0]
        uv = minerals[blockType][1]
        
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])
        
        # Record terrain in dictionary :)
        dot = [blockType,subset]
        this.td[(floor(x),floor(y),floor(z))] = dot
        # Also, record gap above this position to
        # correct for spawning walls after mining.

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if this.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None:
                    # ***
                    if ra.random() > 0.86:
                        mineralType='stone'
                    else: mineralType='grass'
                    if y > 2:
                        mineralType='snow'
                    this.genBlock(x+k,y,z+j,blockType=mineralType)

        # *** Normals...etc. experiments...
        # this.subsets[this.currentSubset].model.generate_normals()
        # this.subsets[this.currentSubset].model.colorize()
        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()