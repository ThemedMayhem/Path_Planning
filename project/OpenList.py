from Node import *

class OpenList():

    def __init__(self):
        self.elements = dict()
        self.sortF = dict()


    def __iter__(self):
        return iter(self.elements)


    def __len__(self):
        return len(self.elements)


    def isEmpty(self):
        return self.__len__() == 0

    def GetBestNode(self, *args):
        mn = min(self.sortF)
        k = self.sortF[mn][0]
        if (len(self.sortF[mn])) == 1:
            self.sortF.pop(mn)
        else:
            self.sortF.update({mn: self.sortF[mn][1:]})
        best = self.elements.pop(k)
        return best

    def AddNode(self, node : Node, *args):
        el = self.elements.get((node.i, node.j))
        if el:
            if el.g > node.g:
                mn = el.F
                self.elements[(node.i, node.j)] = Node(node.i, node.j, node.g, node.h, node.F, node.parent)
                self.sortF[mn].remove((node.i, node.j))
                if (len(self.sortF[mn]) == 0):
                    self.sortF.pop(mn)

                if self.sortF.get(node.F):
                    self.sortF.update({node.F: self.sortF[node.F] + [(node.i, node.j)]})
                else:
                    self.sortF.update({node.F: [(node.i, node.j)]})
            return
        self.elements.update({(node.i, node.j): node})

        if self.sortF.get(node.F):
            self.sortF.update({node.F: self.sortF[node.F] + [(node.i, node.j)]})
        else:
            self.sortF.update({node.F: [(node.i, node.j)]})
        return
