"""
file_byte.py
20.10.21
Open a file from main.py's dir and 
either load() or save() data as bytes.
"""
def save(_fileName, _payload):
    import pickle, sys, os

    # Open main module directory for correct file.
    # sys.arg is  a list of arguments passed to
    # command line, where [0] is name of the script.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(_fileName, 'wb') as f:
        pickle.dump(_payload, f)

def load(_fileName):
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(_fileName, 'rb') as f:
        return pickle.load(f)