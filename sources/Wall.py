import matplotlib.pyplot as plt

class Wall:
    
    def __init__(self,x,y,c,b=0,a=0,limit=False):
        self.x = x
        self.y = y
        self.c = c
        self.b = b
        self.a = a
        if limit != False : self.limit = limit


    def graphWall(self,xlim,ylim,style='k-'):
        plt.plot([self.x,self.x+xlim],[self.y,self.y+self.c*xlim],style)
