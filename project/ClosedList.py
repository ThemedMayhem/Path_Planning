from Node import *

class ClosedList():

    def __init__(self):
        self.elements = dict()


    def __iter__(self):
        return iter(self.elements)


    def __len__(self):
        return len(self.elements)


    def AddNode(self, item : Node):
        '''
        AddNode is the method that inserts the node to CLOSED
        '''
        self.elements.update({(item.i, item.j): item})


    def WasExpanded(self, item : Node):
        '''
        WasExpanded is the method that checks if a node has been expanded
        '''
        return (item.i, item.j) in self.elements