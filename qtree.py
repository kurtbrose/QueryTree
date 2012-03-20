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

def build(data, get_children):
    '''
    Main entry point; when passed a root piece of data and a function that
    knows how to fetch the child data, will build up a Query-able tree of Nodes
    attached to that data.
    '''
    root = Node(None, [], data)
    todo = [root]
    while len(todo) > 0:
        cur = todo.pop()
        for d in get_children(cur.data):
            cur.child_nodes.append(Node(cur, [], d))
        todo.extend(cur.child_nodes)
    return root

def _node_walk(node, predicate):
    todo = [node]
    matches = Matches()
    while len(todo) > 0:
        node = todo.pop()
        if predicate(node.data):
            matches.items.append(node)
        todo.extend(node.children)
    return matches

class Node(object):
    __slots__ = ("parent", "child_nodes", "data")
    
    def __init__(self, parent, child_nodes, data):
        self.parent = parent
        self.child_nodes = child_nodes
        self.data = data
    
    def attr(self, k): return getattr(data, k, None)
    
    def children(self, predicate):
        return [c for c in self.child_nodes if predicate(c)]
    
    def closest(self, predicate):
        'Searches up the tree for the first parent which matches'
        cur = self
        while not predicate(cur):
            cur = cur.parent
            if cur is None:
                break
        return cur
    
    def find(self, predicate):
        return _node_walk(self, predicate)
    
    def __repr__(self):
        return "Node(data="+repr(self.data)+")"

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
                p.child_nodes.insert(p.index(i)+1, Node(p, [], data))
        return self #todo: should this modify the current Match set?
    
    def append(self, data):
        for i in self.items:
            i.child_nodes.append(Node(i.parent, [], data))
        return self #todo: return a different Match set?
    
    def attr(self, k):
        return [i.attr(k) for i in self.items]
    
    def children(self, predicate=None):
        if predicate is None:
            return Matches(sum([i.child_nodes for i in self.items], []))
        return Matches(sum([i.children(predicate) for i in self.items], []))
    
    def data(self):
        '''
        After the query is "done", re-extract the data items.
        '''
        return [i.data for i in self.items]
    
    def each(self, f):
        return [f(i.data) for i in self.items]
    
    def empty(self):
        for i in self.items:
            i.child_nodes = []
    
    def find(self, predicate):
        return Matches(sum([i.find(predicate).items for i in self.items], []))
    
    def filter(self, predicate):
        return Matches([i for i in self.items if predicate(i.data)])
    
    def __repr__(self):
        return "Matches("+repr(self.items)+")"
    
####a bunch of predicates

def empty(node):
    'predicate for selecting nodes with no children'
    return len(node.child_nodes) == 0

def even(node):
    'predicate for selecting the even numbered elements'
    