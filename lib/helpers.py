'''a few random helper functions and their sources'''

#http://stackoverflow.com/questions/9730648/merge-a-nested-dictionary-default-values
#for merging json config files (start with default, then each more local version)
import types 
def merge(x,y):
    # store a copy of x, but overwrite with y's values where applicable         
    merged = dict(x,**y)

    xkeys = x.keys()

    # if the value of merged[key] was overwritten with y[key]'s value           
    # then we need to put back any missing x[key] values                        
    for key in xkeys:
        # if this key is a dictionary, recurse                                  
        if type(x[key]) is types.DictType and y.has_key(key):
            merged[key] = merge(x[key],y[key])

    return merged