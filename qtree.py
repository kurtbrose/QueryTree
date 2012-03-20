'''
The idea is to create a SuperTree with jQuery like functionality on arbitrary
data.

The key is, chain and accept a selector function in place of css.

Here are some jQuery methods that could be implemented:
add() -- adds to the set of matched elements

Nodes should only be in one place -- one parent;
just point multiple nodes to the same data...

append, appendTo... not sure what to do with these

'''
import collections

class Node(object):
    __slots__ = ("parent", "children", "data")
    
    def __init__(self, parent, children, data):
        self.parent = parent
        self.children = children
        self.data = data
        
    def appendTo(self, ): pass

class Matches(collections.MutableSequence):
    __slots__ = ("items",)
    
    def __init__(self, items=None):
        self.items = items if items is not None else []
    
    def     __len__(self)      : return self.items.__len__()
    def      insert(self, i, x): self.items.insert(i, x)
    def __delitem__(self, i)   : self.items.__delitem__(i)
    def __setitem__(self, i, x): self.items.__setitem__(i, x)
    def __getitem__(self, i):
        if isinstance(i, slice):
            return Matches(self.items.__getitem__(i))
        return self.items.__getitem__(i)
    
    def extend(self, values): self.items.extend(values)
    def __add__(self, other): return Matches(self.items + other.items)
    #before I go off on an orgy of operator overloading, lets make sure we have something useful here...
    
    #implementing jQuery methods....
    #don't need add -- __add__ and __iadd__ have this covered already
    
    def after(self, data):
        for i in self.items:
            for p in i.parents:
                p.children.insert(p.index(i)+1, Node(p, [], data))
        return self #todo: should this modify the current Match set?
    
    def append(self, data):
        for i in self.items:
            i.children.append(Node(i.parent, [], data))
        return self #todo: return a different Match set?
    
    
