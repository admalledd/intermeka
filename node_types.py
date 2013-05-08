class list_node(object):
    def __init__(self,title,sub_nodes):
        self.title=title
        self.sub_nodes=sub_nodes
        self.index=0

    def get_all(self,depth=0):
        '''recurse into sub-nodes and yield the node and depth'''
        for node in self.sub_nodes:
            yield node,depth
            if isinstance(node, list_node):
                for sub in node.get_all(depth+1):
                    yield sub
    def __repr__(self):
        return '<list_node("%s")?>'%self.title

class functer_node(object):
    def __init__(self,title,func):
        self.title=title
        self.func=func
    def call(self):
        self.func()
    def __repr__(self):
        return '<functer_node("%s")?>'%self.title
