"""
load_byte.py
20.10.21
Open a file from main.py's dir and 
return file's data (read as bytes).
"""
def load(_fileName):
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(_fileName, 'rb') as f:
        return pickle.load(f)