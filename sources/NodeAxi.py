from math import *
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from sources.variousFunctions import HallFunction, PrandtlFunction, machAngle
class Node:
    #On définit la classe node qui se caractérise par :
    #   la position (x,y) du noeud
    #   le flow angle theta du noeud
    #   le mach number du noeud
    #On en déduit les paramètres :
    #   le mach angle du noeud
    #   l'angle de Prandl-Meyer du noeud
    #   la valeur de K- sur le noeud
    #   la valeur de K+ sur le noeud
    def __init__(self,x,y,thet,mach,nu=False):
        self.gen_id=0
        self.node_id = 0
        self.x = x
        self.y = y
        self.thet = thet
        if nu == False :
            self.mach = mach
            self.nu = PrandtlFunction(mach)
        else :
            self.mach = HallFunction(nu)
            self.nu = nu
        self.mu = asin(1/self.mach)
        self.Km = self.thet+self.nu
        self.Kp = self.thet-self.nu
        self.CpSlope = tan(self.thet+self.mu)
        self.CmSlope = tan(self.thet-self.mu)
        if self.x == 0 :
            self.link_up = True
        else :
            self.link_up = False
        self.link_down= False
        self.temp_totale = 0
        self.p_totale = 0
        self.temp = 0
        self.p = 0
        self.attrDict ={
            "X":self.x,
            "Y":self.y,
            "thet":self.thet*(360/(2*pi)),
            "nu":self.nu*(360/(2*pi)),
            "mu":self.mu*(360/(2*pi)),
            "mach":self.mach,
            "T":self.temp,
            "P":self.p*1e-5,
        }

    def recalculate(self):
        self.mach = HallFunction(self.nu)
        self.mu = asin(1/self.mach)
        self.Km = self.thet+self.nu
        self.Kp = self.thet-self.nu
        self.CpSlope = tan(self.thet+self.mu)
        self.CmSlope = tan(self.thet-self.mu)
        self.link = False
        if self.x == 0 :
            self.link_up = True
        else :
            self.link_up = False
        self.link_down= False

    def __str__(self):
        thet = self.thet*(360/(2*pi))
        nu = self.nu*(360/(2*pi))
        mu = self.mu*(360/(2*pi))
        Km = self.Km*(360/(2*pi))
        Kp = self.Kp*(360/(2*pi))
        listing = '{:3s}{:<5.2f}'.format('X = ', self.x)
        listing += '{:3s}{:<5.2f}'.format('| Y = ',self.y)
        listing += '{:3s}{:<6.3f}'.format('| Theta = ',thet)
        listing += '{:3s}{:<6.3f}'.format('| nu = ',nu)
        listing += '{:3s}{:<6.3f}'.format('| mu = ',mu)
        listing += '{:3s}{:<5.2f}'.format('| Mach = ',self.mach)
        #listing += '{:3s}{:<5.2f}'.format('| Temp = ',self.temp)
        #listing += '{:3s}{:<5.2f}'.format('| pressure = ',self.p*1e-5)
        #optional prints
        #listing += '{:3s}{:<5.2f}'.format('| Km = ',Km)
        #listing += '{:3s}{:<5.2f}'.format('| Kp = ',Kp)
        listing += '{:3s}{:5.2f}'.format('| CpSlope = ',self.CpSlope)
        listing += '{:3s}{:5.2f}'.format('| CmSlope = ',atan(self.CmSlope)*360/(2*pi))
        return listing


    def graphNode(self,ax,style='o'):
        ax.plot(self.x,self.y,style)
        return

    def intersect(self,node,xlim,ylim):
        def cotan(x) : return 1/tan(x)
        thet_1 = self.thet
        nu_1 = self.nu
        mu_1 = self.mu
        x_1 = self.x
        r_1 = self.y
        thet_2 = node.thet

        nu_2 = node.nu
        mu_2 = node.mu
        x_2 = node.x
        r_2 = node.y

        
        thet_3 = 0.5*(self.thet+node.thet)
        r_3 = 0.5*(self.y+node.y)
        m_3 = 0.5*(self.mach+node.mach)
        nu_3 =0.5*(self.nu+node.nu)
        mu_3 = machAngle(self.mach)
        x_3 = max(self.x,node.x)

        delta = [1,1,1,1,1,1]
        previous_step = [1,1,1,1,1,1]
        counter=0
        while max(delta) > 1e-10 and counter<100 :
            counter+=1
            print('**************************')
            previous_step[0]=thet_3
            previous_step[1]=nu_3
            previous_step[2]=m_3
            previous_step[3]=mu_3
            previous_step[4]=x_3
            previous_step[5]=r_3
            d = 1
            while d > 1e-10 :
                t = thet_3
                thet_3 = 0.5*(thet_1+thet_2+nu_1-nu_2+( (r_3-r_1)*(r_3-r_2)/(r_3*r_3*(m_3*m_3-1-cotan(thet_3)*cotan(thet_3)))))
                d = abs(t-thet_3)/t
            print('thet_3 =',thet_3)
            #Premiere convergence de nu 3
            nu_3 = 0.5*(thet_1-thet_2+nu_1+nu_2+( (r_3-r_1)*(r_3-r_2)/(r_3*r_3*(m_3*m_3-1-cotan(thet_3)*cotan(thet_3)))))
            m_3 = HallFunction(nu_3)
            mu_3 = machAngle(m_3)
            print('nu_3 =',nu_3)
            print('m_3 =',m_3)
            print('mu_3 =',mu_3)
            #Premiere convergence de x_3
            x_3 = (r_2-r_1+tan(thet_1-mu_1)*x_1-tan(thet_2+mu_2)*x_2)/(tan(thet_1-mu_1)-tan(thet_2+mu_2))
            print('x_3 =',x_3)

            #premiere convergence de r_3
            r_3 = r_1 +(x_3-x_1)*tan(thet_1-mu_1)
            print('r_3 =',r_3)
            delta[0]=(previous_step[0]-thet_3)/previous_step[0]
            delta[1]=(previous_step[1]-nu_3)/previous_step[1]
            delta[2]=(previous_step[2]-m_3)/previous_step[2]
            delta[3]=(previous_step[3]-mu_3)/previous_step[3]
            delta[4]=(previous_step[4]-x_3)/previous_step[4]
            delta[5]=(previous_step[5]-r_3)/previous_step[5]
            print(delta)
        P3 = Node(x_3,r_3,thet_3,m_3)
        if max(delta)<= 1e-10 : return P3
        else : return False

    def findAxis(self,wall,xlim,ylim,limit=False):
        #Cette méthode trouve la position de l'intersection d'une caractéristique avec l'axe de la tuyère
        ywall =  wall.y + wall.c*(self.x-wall.x)
        if limit == False : limit = xlim
        if self.y > wall.y + wall.c*(self.x-wall.x):
            a = self.CmSlope
            b = self.y - a*self.x
            c = wall.c
            d = wall.y - c*wall.x
            if a != c and b != d :
                x = (d-b)/(a-c)
                y = round(a*x+b,5)
                if self.x <= x <= xlim and 0 <= y < ylim:
                    nu = self.Km
                    M = HallFunction(nu)
                    return Node(x,y,0,M)
        elif self.y < wall.y + wall.c*(self.x-wall.x):
            a = self.CpSlope
            b = self.y - a*self.x
            c = wall.c
            d = wall.y - c*wall.x
            if a != c and b != d :
                x = (d-b)/(a-c)
                y = round(a*x+b,5)
                if self.x <= x <= limit and 0 <= y <= ylim:
                    theta = atan(wall.c)
                    nu = theta - self.Kp
                    M = HallFunction(nu)
                    return Node(x,y,theta,M)
        return False



    def findContour(self,wallList) :
        #Cette méthode calcule la position de l'intersection d'une caractéristique avec le contour de la tuyère
        targetWall = wallList[-1]
        thet_intersect = self.thet
        thet_contour = targetWall.thet
        avg_slope = 0.5*( thet_contour + thet_intersect )

        a = self.CpSlope
        b = self.y - a*self.x

        c = tan(avg_slope)
        d = targetWall.y - c*targetWall.x

        if a != c and b != d :
            x = (d-b)/(a-c)
            y = a*x+b
        return Node(x,y,thet_intersect,self.mach)





    def distanceNode(self,node):
        return sqrt((self.x-node.x)**2 + (self.y-node.y)**2)

    def selectClosestNode(self,nodeList) :
        closestNode = nodeList[0]
        for node in nodeList :
            if self.distanceNode(node[0]) <= self.distanceNode(closestNode[0]) :
                closestNode = node

        return closestNode

    def compute_therm_parameters(self,temp_totale,p_totale,g):
        self.temp_totale = temp_totale
        self.p_totale = p_totale
        self.g = g
        self.temp = self.temp_totale / (1+0.5*self.mach*self.mach*(self.g-1))
        self.p = self.p_totale * pow(self.temp/self.temp_totale,self.g/(self.g-1))

        self.attrDict ={
            "X":self.x,
            "Y":self.y,
            "thet":self.thet*(360/(2*pi)),
            "nu":self.nu*(360/(2*pi)),
            "mu":self.mu*(360/(2*pi)),
            "mach":self.mach,
            "T":self.temp,
            "P":self.p*1e-5,
        }

