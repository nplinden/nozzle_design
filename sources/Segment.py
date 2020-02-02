import matplotlib.pyplot as plt

class Segment:
    
    def __init__(self,firstNode,secondNode):
        self.x0 = firstNode.x
        self.y0 = firstNode.y
        self.x1 = secondNode.x
        self.y1 = secondNode.y
        
    def graphSegment(self,ax,style='ko--') :
        ax.plot([self.x0,self.x1],[self.y0,self.y1],style)
