import pickle, os

sgroup = 'Group'
snew = 'New'
sdeleted = 'Deleted'

empty_func = lambda : None

def save_obj(obj, fname):
    pickle.dump(obj,open(fname,"wb"))

def load_obj(fname):
    if exists(fname):
        return pickle.load(open(fname, "rb"))
    return None

def exists(path):
    return os.path.exists(path)