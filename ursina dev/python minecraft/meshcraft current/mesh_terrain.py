from perlin import Perlin
from ursina import *
import random as raa
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *
from config import six_cube_dirs, minerals, mins
from tree_system import *
from inventory_system import *

class MeshTerrain:
    # * - inventory system items passed in here?
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam

        this.block = load_model('block.obj')
        
        # * HEX ******
        # this.textureAtlas='grass_64_hex_tex_2.png'
        # this.block = load_model('stretch_hex.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 1024 #*** 1024 new default
        
        # Must be even number! See genTerrain()
        # 20 was experiment.
        this.subWidth = 6 # *** 2 for new default
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        # For the main terrain?
        this.perlin = Perlin()
        # And for our new terrain features :)
        this.tree_noise=PerlinNoise(
                octaves=32,
                seed=2022)
        this.tree_freq=64
        this.tree_amp=128

        # Instantiate our subset Entities.
        this.setup_subsets()

    def setup_subsets(this):
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
    
    def plantStone(this,_x,_y,_z):
        # We want to use perlin and perhaps co-ordinates
        # to determine how much stone to lay.
        # Let's try linear interpolation?
        
        # y_interp = lerp(_z,10,0.5)
        # print(y_interp)
        # if y_interp > 1:
        #     # Laying terrain will change blockType to 'stone'.
        #     return True

        # noise=PerlinNoise(
        #         octaves=32,
        #         seed=2022)
        # freq=64
        # amp=128
        y=this.tree_noise(([_x/this.tree_freq,_z/this.tree_freq]))*this.tree_amp
        # print(y)
        if y > 64:
            this.genBlock(_x,_y+1,_z,
                blockType='ruby')
            # for i in range(int(y/28)):
            #     this.genBlock(_x,_y+1+i,_z,
            #     blockType='ruby')
            return False
        if y > 34:
            return True

        # Laying terrain will assume grass, not stone.
        return False

    def plantTree(this,_x,_y,_z):
        # ***
        # k=((floor(_x),floor(_y),floor(_z)))
        # wb=this.td.get(k)
        # if wb!=None and wb!='g': return

        ent=TreeSystem.genTree(_x,_z)
        if ent==0: return
        # *** - disrupt grid.
        wiggle=floor(sin(_z*_x)*3)
        # print(wiggle)
        # Adjust to wiggled position height.
        _y = 1+floor(this.perlin.getHeight(_x+wiggle,_z+wiggle))
        # Trunk.
        # ***
        treeH=int(ent*7)
        # **** Surely I ought to define this at 
        # Initilization?
        # noise=PerlinNoise(
        #         octaves=32,
        #         seed=2022)
        # freq=64
        # amp=128
        
        # print(y)
        
        for i in range(treeH):
            this.genBlock(_x+wiggle,_y+i,_z+wiggle,
                blockType='wood')
            by=this.tree_noise(([_x/this.tree_freq,_z/this.tree_freq,_y+i]))*this.tree_amp
            if by > 34:
                this.genBlock(_x+wiggle+1,_y+i,_z+wiggle,
                blockType='foliage')
                this.genBlock(_x+wiggle,_y+i,_z+wiggle-1,
                blockType='foliage')
                this.genBlock(_x+wiggle-1,_y+i,_z+wiggle,
                blockType='foliage')
                this.genBlock(_x+wiggle,_y+i,_z+wiggle+1,
                blockType='foliage')
        # Crown.
        for t in range(-2,3):
            for tt in range(4):
                for ttt in range(-2,3):
                    this.genBlock(_x+t+wiggle,_y+treeH+tt,_z+ttt+wiggle,
                    blockType='foliage')
                    
    def do_mining(this):
        epi = mine( this.td,this.vd,this.subsets,
                    this.numVertices,this.textureAtlas,
                    this.subject)
        if (epi!=None and epi[2]!='wood' and
            epi[2]!='foliage'):
            # Don't generate walls around trees!
            # Epi[0] is bte position (Vec3).
            # Epi[1] is subset index.
            # Epi[2] is blockType.
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    def update(this):
        # *** return blockTpe! see end of highlight()!
        b = highlight(  this.subject.position,
                        this.subject.height,
                        this.camera,this.td)
        
        # Blister-mining!
        if bte.visible==True and mouse.locked==True:
            if held_keys['shift'] and held_keys['left mouse']:
                this.do_mining()
            # for key, value in held_keys.items():
            #     if key=='left mouse' and value==1:
            #         this.do_mining()

    def input(this,key):
        if key=='left mouse up' and bte.visible==True and mouse.locked==True:
            this.do_mining()
        # Building :)
        # *** - empty-handed?
        if this.subject.blockType==None: return
        if key=='right mouse up' and bte.visible==True and mouse.locked==True:
            bsite = checkBuild( bte.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0))
            if bsite!=None:
                # *** - tut22
                # *** do genBlock beforehand, to avoid
                # Nonetype error with subject.blockType.
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),
                    subset=0,blockType=this.subject.blockType)
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
                # ***
                for h in hotspots:
                    # Am I highlighted? I.e. my colour black?
                    if h.color==color.black:
                        h.stack-=1
                        h.item.update_stack_text()
                        if h.stack<=0:
                            destroy(h.item)
                            h.occupied=False
                            h.stack=0
                            h.t.text=""
                            this.subject.blockType=None
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for call to genBlock?
        
        for i in range(0,6):
            np = epi + six_cube_dirs[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')

    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass',layingTerrain=False):
        # Clash protection.
        key=((floor(x),floor(y),floor(z)))
        if (this.td.get(key)!=None and 
            this.td.get(key)!='g'): return

        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        # ****** HEX
        """
        hex_z=z
        if z % 2 == 0:
            x+=0.5
        """

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])

        # Does the dictionary entry for this blockType
        # hold colour information? If so, use it :)
        if len(minerals[blockType])>2:
            # Decide random tint for colour of block :)
            c = raa.random()-0.5
            # Grab the Vec4 colour data :)
            ce=minerals[blockType][2]
            # Adjust each colour channel separately to
            # ensure that hard-coded RGB combination is maintained.
            model.colors.extend(    (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                    this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = raa.random()-0.5
            model.colors.extend(    (Vec4(1-c,1-c,1-c,1),)*
                                    this.numVertices)

        # This is the texture atlas co-ord for grass :)
        uu=minerals[blockType][0]
        uv=minerals[blockType][1]
        # ***
        """
        # HEX
        uu=0
        uv=0
        """

        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

        # Record terrain in dictionary :)
        this.td[(floor(x),floor(y),floor(z))] = blockType
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            if this.td.get(key)==None:
                this.td[key]='g'

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-this.numVertices-1)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if (this.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None):
                    # Decide whether to plant tree, rock, etc.
                    bType='grass' # Assume placing grass.
                    if this.plantStone(x+k,y,z+j):
                        bType='stone'
                    # If high enough, cap with snow blocks :D
                    if y > 2:
                        bType='snow'
                    this.genBlock(x+k,y,z+j,blockType=bType,
                                            layingTerrain=True)
                    # Plant a tree?
                    this.plantTree(x+k,y+1,z+j)
                       
        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()