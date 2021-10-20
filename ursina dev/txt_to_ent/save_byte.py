"""
save_byte.py
20.10.21
Save a file to main.py's dir; data written as bytes.
"""
def save(_fileName, _payload):
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(_fileName, 'wb') as f:
        pickle.dump(_payload, f)