"""
Saving and loading a terrain 'map'.
"""

mapName='november_test_1.land'

def saveMap(_subPos, _td):
    import os, sys, pickle

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(mapName, 'wb') as f:

        map_data = [_subPos, _td]

        pickle.dump(map_data, f)

        map_data.clear()

def loadMap(_subject,_terrain):
    import os, sys, pickle
    from ursina import destroy

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open(mapName, 'rb') as f:
        map_data = pickle.load(f)

    # Empty out current terrain objects.
    for s in _terrain.subsets:
        destroy(s)
    _terrain.td={}
    _terrain.vd={}
    _terrain.subsets=[]
    _terrain.setup_subsets()
    # *** from 1 to 0
    _terrain.currentSubset=0
    # Without copy?
    _terrain.td=map_data[1]
    # Iterate over terrain dictionary and
    # if we find blockType then generate a block.
    # Note this means we'll lose colour info etc.
    i = 0 # Which subset to build block on?
    for key in _terrain.td:
        whatT=_terrain.td.get(key)
        if whatT!=None and whatT!='g':
            x = key[0]
            y = key[1]
            z = key[2]
            if i>=len(_terrain.subsets)-1:
                i=0
            _terrain.genBlock(x,y,z,subset=i,gap=False,blockType=whatT)
            i+=1

    # And reposition subject according to saved map.
    _subject.position=map_data[0]
    # Reset swirl engine.
    _terrain.swirlEngine.reset( _subject.position.x,
                                _subject.position.z)
    # Regenerate subset models, so that we can see terrain.
    for s in _terrain.subsets:
        s.model.generate()