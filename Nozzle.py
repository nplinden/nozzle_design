from math import *
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from variousFunctions import *
from Node import *
from Segment import *
from Wall import *
import csv

class Nozzle :

    def __init__(self,
                 length_limit,
                 height_limit,
                 throat_radius,
                 throat_pressure,
                 throat_temperature,
                 throat_mach,
                 air_gas_constant,
                 mass_flow,
                 g,
                 theta_bottom,
                 theta_top,
                 theta_step):
        self.length_limit       = length_limit
        self.height_limit       = height_limit
        self.throat_radius      = throat_radius
        self.throat_pressure    = throat_pressure
        self.throat_temperature = throat_temperature
        self.throat_mach        = throat_mach
        self.air_gas_constant   = air_gas_constant
        self.mass_flow          = mass_flow
        self.g                  = g
        self.theta_bottom       = theta_bottom
        self.theta_top          = theta_top
        self.theta_step         = theta_step

        self.temp_totale = self.throat_temperature*(1+(self.g-1)*0.5*self.throat_mach*self.throat_mach)
        self.p_totale = self.throat_pressure*pow((1+(self.g-1)*0.5*self.throat_mach*self.throat_mach),self.g/(self.g-1))
        self.theta_list = np.arange(self.theta_bottom,self.theta_top+self.theta_step,self.theta_step)

        self.theta_list = [i * 2 * pi / (360) for i in  self.theta_list]
        number_of_points = (self.theta_top-self.theta_bottom)/self.theta_step
        ylist = [(thet/self.theta_top)*self.throat_radius for thet in self.theta_list]
        self.seed = [Node(0,self.throat_radius,self.theta_list[i],1,nu=self.theta_list[i]) for i in range(len(self.theta_list))]

        #initializing things
        floor = Wall(0,0,0)
        plt.figure()
        ax=plt.subplot(111)
        self.wall = [self.seed[-1]]
        gen = self.seed.copy()
        seg=[]

        #computing the first point with the right values to initiate calculation
        new = self.seed[0].interWall(floor,self.length_limit,self.height_limit)
        new.thet = self.seed[0].thet
        new.nu = new.thet
        new.recalculate()
        self.seed[0].link_down = True
        gen.append(new)
        seg.append(Segment(self.seed[0],new))

        #Expanding the characteristics fan
        for initNode in gen :
            interNode_down = []

            if not(initNode.link_down) and initNode.y != 0 :
                if initNode.interWall(floor,self.length_limit,self.height_limit) != False :
                    interNode_down.append([initNode.interWall(floor,self.length_limit,self.height_limit),floor])
                for targetNode in gen :
                    if targetNode != initNode :
                        if targetNode.link_up ==False :
                            if initNode.interKm(targetNode,self.length_limit,self.height_limit) != False :
                                if initNode.interKm(targetNode,self.length_limit,self.height_limit).x > targetNode.x and initNode.interKm(targetNode,self.length_limit,self.height_limit).x > initNode.x :
                                    interNode_down.append( [initNode.interKm(targetNode,self.length_limit,self.height_limit),targetNode] )

            if interNode_down != []:
                gen.append(initNode.selectClosestNode(interNode_down)[0])
                seg.append(Segment(initNode,initNode.selectClosestNode(interNode_down)[0]))
                if isinstance(initNode.selectClosestNode(interNode_down)[1],Node):
                    seg.append(Segment(initNode.selectClosestNode(interNode_down)[1],initNode.selectClosestNode(interNode_down)[0]))

                initNode.link_down = True

                for i in gen :
                    if i == initNode.selectClosestNode(interNode_down)[1]:
                        i.link_up = True



        self.seg = seg
        #Computing the nozzle's shape
        segWall = []
        for initNode in gen :
            if not(initNode.link_up) :
                inter= initNode.findRoof(self.wall)
                self.wall.append(inter)
                segWall.append(Segment(self.wall[-2],inter))
                seg.append(Segment(initNode,inter))
        for i in gen :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        for i in self.seed :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        for i in self.wall :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)

        self.fan=[]
        for i in gen :
            if i.x != 0:
                self.fan.append(i)

        self.wallx = [i.x for i in self.wall]
        self.wally = [i.y for i in self.wall]


    def graph(self):
            # plt.figure()
            ax = plt.subplot(111)
            ax.plot(self.wallx,self.wally,'b-')
            ax.plot(self.wallx,[-i for i in self.wally],'b-')

            for i in self.fan :
                i.graphNode(ax,'ko')
            for i in self.seg :
                i.graphSegment(ax)

            ax.set_aspect('equal')
            ax.grid()
            plt.show()

    def Printseed(self):
        print('{:^75s}'.format('******Initial points******'))
        for i in self.seed:
            print(i)

    def save_contour(self,result_path='results/',catia=False):
        if catia :
            with open(result_path+'contour_catia.csv', mode='w',newline='') as csv_file:
                fieldnames = ['X','Y','Z']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

                # writer.writeheader()
                writer.writerow({'X':'StartLoft','Y':'','Z':''})
                writer.writerow({'X':'StartCurve','Y':'','Z':''})
                for i in self.wall :
                    writer.writerow({'X': str(i.x).replace('.',','), 'Y': str(i.y).replace('.',','),'Z':'0'})
                writer.writerow({'X':'EndCurve','Y':'','Z':''})
                writer.writerow({'X':'EndLoft','Y':'','Z':''})
                writer.writerow({'X':'End','Y':'','Z':''})
        else :
            with open(result_path+'contour.csv', mode='w',newline='') as csv_file:
                fieldnames = ['X','Y']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

                writer.writeheader()
                for i in self.wall :
                    writer.writerow({'X': str(i.x).replace('.',','), 'Y': str(i.y).replace('.',',')})

    def save_data(self,selection=[],result_path='results/'):
        with open(result_path+'nodes.csv', mode='w',newline='') as csv_file:
            fieldnames = ['']+selection
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerow({'':'SEED'})
            for node in self.seed :
                dict = {'':''}
                for prop in selection :
                    dict[prop] = str(node.attrDict[prop]).replace('.',',')
                writer.writerow(dict)
            writer.writerow({'':'FAN'})
            for node in self.fan :
                dict = {'':''}
                for prop in selection :
                    dict[prop] = str(node.attrDict[prop]).replace('.',',')
                writer.writerow(dict)
            writer.writerow({'':'CONTOUR'})
            for node in self.wall :
                dict = {'':''}
                for prop in selection :
                    dict[prop] = str(node.attrDict[prop]).replace('.',',')
                writer.writerow(dict)

    def misc(self):
        return
