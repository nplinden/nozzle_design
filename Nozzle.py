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
                 theta_top,
                 theta_step_num,
                 theta_bottom=0.375):
        self.length_limit       = length_limit
        self.height_limit       = height_limit
        self.throat_radius      = throat_radius
        self.throat_pressure    = throat_pressure
        self.throat_temperature = throat_temperature
        self.throat_mach        = throat_mach
        self.air_gas_constant   = air_gas_constant
        self.mass_flow          = mass_flow
        self.g                  = g

        #Calculating total temp and pressure from (T/P) at the throat
        self.temp_totale = self.throat_temperature*(1+(self.g-1)*0.5*self.throat_mach*self.throat_mach)
        self.p_totale = self.throat_pressure*pow((1+(self.g-1)*0.5*self.throat_mach*self.throat_mach),self.g/(self.g-1))

        #Defining the angles with which to start the calculation
        self.theta_list = np.linspace(theta_bottom,theta_top,theta_step_num)
        self.theta_list = [i * 2 * pi / (360) for i in  self.theta_list]





        #Creating intial angles at sharp throat
        self.seed = [ Node(0,self.throat_radius,i,1,nu=i) for i in self.theta_list ]
        floor = Wall(0,0,0)
        plt.figure()
        self.wall = [self.seed[-1]]
        gen = self.seed.copy()
        self.seg=[]

        #computing the first point with the right values to initiate calculation
        new = self.seed[0].interWall(floor,self.length_limit,self.height_limit)
        new.thet = self.seed[0].thet
        new.nu = new.thet
        new.recalculate()
        self.seed[0].link_down = True
        gen.append(new)
        self.seg.append(Segment(self.seed[0],new))

        #Expanding the characteristics fan
        for initNode in gen :
            candidate_list = []

            if not(initNode.link_down) and initNode.y != 0 :

                #checking for intersection with x-axis
                wall_candidate = initNode.interWall(floor,self.length_limit,self.height_limit)
                if isinstance(wall_candidate,Node) :
                    candidate_list.append([wall_candidate,floor])

                #checking for intersections with all characteristics
                for targetNode in gen :
                    if targetNode != initNode and targetNode.link_up ==False :
                            fan_candidate = initNode.interKm(targetNode,self.length_limit,self.height_limit)
                            if isinstance(fan_candidate,Node) :
                                if fan_candidate.x > targetNode.x and fan_candidate.x > initNode.x :
                                    candidate_list.append( [fan_candidate,targetNode] )

            #selecting the closest candidate
            if candidate_list != []:
                selected_candidate = initNode.selectClosestNode(candidate_list)
                gen.append(selected_candidate[0])
                self.seg.append(Segment(initNode,selected_candidate[0]))
                if isinstance(selected_candidate[1],Node):
                    self.seg.append(Segment(selected_candidate[1],selected_candidate[0]))
                initNode.link_down = True

                for i in gen :
                    if i == selected_candidate[1]:
                        i.link_up = True

        #Computing the nozzle's shape
        for initNode in gen :
            if not(initNode.link_up) :
                inter= initNode.findRoof(self.wall)
                self.wall.append(inter)
                self.seg.append(Segment(initNode,inter))
        for i in gen :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        for i in self.seed :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        for i in self.wall :
            i.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)

        #self.fan contains node on the nozzle contour
        self.fan=[i for i in gen if i.x != 0]



    def graph(self):
            # plt.figure()
            nozzle_ax = plt.subplot(111)
            nozzle_ax.plot([i.x for i in self.wall],[i.y for i in self.wall],'b-')
            nozzle_ax.plot([i.x for i in self.wall],[-i.y for i in self.wall],'b-')

            for i in self.fan :
                i.graphNode(nozzle_ax,'ko')
            for i in self.seg :
                i.graphSegment(nozzle_ax)

            nozzle_ax.set_aspect('equal')
            nozzle_ax.grid()
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
