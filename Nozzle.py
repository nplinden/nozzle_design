from math import *
from packages.Ftable import *
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from variousFunctions import *
from Node import *
from Segment import *
from Wall import *
import csv
from CoolProp.CoolProp import PropsSI
from packages.Htable import *
import time
class Nozzle :

    def __init__(self,
                physics,
                geometry,
                results):
        t0 = time.time()
        self.physics = physics
        self.geometry = geometry
        self.results = results

        self.check()
        self.initialize()
        self.draw()
        self.compute()
        if self.results['display_tables'] : self.display()
        if self.results['display_figure'] : self.graph()
        t1 = time.time()
        self.comp_time = t1 - t0
        self.charac['comp_time'] = self.comp_time

####################     Computing    ######################

    def check(self) :
        self.tank_pressure = self.physics['tank_pressure']
        self.tank_temperature = self.physics['tank_temperature']
        self.throat_mach = 1
        self.air_gas_constant = self.physics['specific_gas_constant']
        self.mass_flow = self.physics['mass_flow']
        self.g = self.physics['gamma']
        if 'exit_mach' in self.physics :
            self.exit_mach = self.physics['exit_mach']
        if 'exit_pressure' in self.physics :
            self.exit_pressure = self.physics['exit_pressure']
        self.theta_step_num = self.geometry['step_number']
        self.ntype = self.geometry['nozzle_type']
        if self.ntype == 'minimal' :
            self.theta_bottom = self.geometry['initial_angle']

    def initialize(self) :
        if self.ntype=='expansion' :

            #Calculating the throat's area and radius
            rho=PropsSI("D","P",self.tank_pressure,"T",self.tank_temperature,"Air")
            throat_surf = self.mass_flow/(rho*sqrt(self.g*self.air_gas_constant*self.tank_temperature))
            self.throat_radius =sqrt(throat_surf/pi)

            #Calculating total temp and pressure from (T/P) at the throat
            self.temp_totale = self.tank_temperature*(1+(self.g-1)*0.5*0)
            self.p_totale = self.tank_pressure*pow((1+(self.g-1)*0.5*0*0),self.g/(self.g-1))

            #calculating the final expansion angle
            if 'exit_mach' in self.physics :
                desired_mach = self.exit_mach
            elif 'exit_pressure' in self.physics :
                desired_mach = sqrt((2/(self.g-1))*(pow(self.p_totale/self.exit_pressure,(self.g-1)/self.g)-1))
                self.exit_mach = desired_mach
            self.theta_top = 360/(2*pi)*PMfunction(desired_mach,self.g)/2

            #Creating the circle for the expansion region's slope
            theta = np.linspace(-pi/2, 1.5*pi, 1000)
            y0 = self.throat_radius
            x1 = 1.0*y0
            r=x1/sin(self.theta_top*2*pi/360)
            y1=r+y0-r*cos(self.theta_top*2*pi/360)
            x_circle = 0
            y_circle = y0+r
            x=r*np.cos(theta)+x_circle
            y = r*np.sin(theta)+y_circle
            val = [[x[i],y[i]] for i in range(len(x)) if 0<=x[i]<=x1 and y[i]<=y1]
            valbis = [[x[i],y[i]] for i in range(len(x)) if 0>=x[i] or x[i]>=x1 or y[i]>=y1]
            xbis = [i[0] for i in valbis]
            ybis = [i[1] for i in valbis]
            x = [i[0] for i in val]
            y = [i[1] for i in val]
            #creating the nozzle's initial points
            x_seed = np.linspace(x1/25,x1,self.theta_step_num)
            theta_seed = [asin(i/r) for i in x_seed]
            y_seed = [r+y0-r*cos(i) for i in theta_seed]
            nu_seed = theta_seed.copy()
            mach_seed = [HallFunction(i) for i in nu_seed]
            self.seed = [Node(x_seed[i],y_seed[i],theta_seed[i],mach_seed[i],nu_seed[i]) for i in range(len(x_seed))]
            self.floor = Wall(0,0,0)
            self.wall = self.seed.copy()
            self.xlim = 1000*self.throat_radius
            self.ylim = 1000*self.throat_radius

        if self.ntype=='minimal':


            rho=PropsSI("D","P",self.tank_pressure,"T",self.tank_temperature,"Air")
            throat_surf = self.mass_flow/(rho*sqrt(self.g*self.air_gas_constant*self.tank_temperature))
            self.throat_radius =sqrt(throat_surf/pi)
            #Calculating total temp and pressure from (T/P) at the throat
            self.temp_totale = self.tank_temperature*(1+(self.g-1)*0.5*0)
            self.p_totale = self.tank_pressure*pow((1+(self.g-1)*0.5*0*0),self.g/(self.g-1))


            #calculating the final expansion angle
            if 'exit_mach' in self.physics :
                desired_mach = self.exit_mach
            elif 'exit_pressure' in self.physics :
                desired_mach = sqrt((2/(self.g-1))*(pow(self.p_totale/self.exit_pressure,(self.g-1)/self.g)-1))
                self.exit_mach = desired_mach

            self.theta_top = PMfunction(desired_mach,self.g)/2
            self.theta_top *= 360/(2*pi)
            #Defining the angles with which to start the calculation
            self.theta_list = np.linspace(self.theta_bottom,self.theta_top,self.theta_step_num)
            self.theta_list = [i * 2 * pi / (360) for i in  self.theta_list]
            #Creating intial angles at sharp throat
            self.seed = [ Node(0,self.throat_radius,i,1,nu=i) for i in self.theta_list ]
            self.floor = Wall(0,0,0)
            self.wall = [self.seed[-1]]
            self.xlim = 1000*self.throat_radius
            self.ylim = 1000*self.throat_radius
    def draw(self):
        seg = []
        wall_seg = []
        gen = []
        gen.append(self.seed.copy())
        new_gen=[]
        new_gen.append(gen[0][0].interWall(self.floor,self.xlim,self.ylim))
        seg.append(Segment(gen[0][0],new_gen[-1]))
        for node in gen[0][1:]:
            new_gen.append(node.interKm(new_gen[-1],self.xlim,self.ylim))
            seg.append(Segment(node,new_gen[-1]))
            seg.append(Segment(new_gen[-1],new_gen[-2]))
        gen.append(new_gen.copy())
        for i in range(1,self.theta_step_num):
            new_gen=[]
            new_gen.append(gen[i][1].interWall(self.floor,self.xlim,self.ylim))
            seg.append(Segment(gen[i][1],new_gen[-1]))
            for node in gen[i][2:]:
                new_gen.append(node.interKm(new_gen[-1],self.xlim,self.ylim))
                seg.append(Segment(node,new_gen[-1]))
                seg.append(Segment(new_gen[-1],new_gen[-2]))
            gen.append(new_gen.copy())
        for generation in gen[1:] :
            last_node = generation[-1]
            wall_candidate = last_node.findRoof(self.wall)
            self.wall.append(wall_candidate)
            wall_seg.append(Segment(self.wall[-1],self.wall[-2]))
            seg.append(Segment(self.wall[-1],last_node))
        self.gen=gen
        self.seg=seg
        self.wall_seg=wall_seg

        for i, generation in enumerate(self.gen) :
            for j, node in enumerate(generation) :
                node.gen_id = i
                node.node_id = j+1

    def compute(self) :
        for node in self.wall :
            node.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        for generation in self.gen :
            for node in generation :
                node.compute_therm_parameters(self.temp_totale,self.p_totale,self.g)
        self.area_ratio = self.wall[-1].y/self.wall[0].y
        self.charac = {
                'area_ratio' : self.area_ratio ,
                'exit_mach' : self.wall[-1].mach ,
                'exit_pressure' : self.wall[-1].p ,
                }
    

    def display(self) :
        init = [
                ['Type de tuyère', str(self.ntype)],
                ['Rayon du col', '{:.5g}'.format(self.throat_radius)],
                ['Débit massique (kg/s)', str(self.mass_flow)],
                ['Température totale (K)', str(self.tank_temperature)],
                ['Pression totale (bar)', str(self.tank_pressure*1e-5)],
                ['Constante des gaz parfaits (J/kg/K)', str(self.air_gas_constant)],
                ['Vitesse de sortie (Mach)','{:.3g}'.format(self.exit_mach)],
                ['Angle du divergent (deg)', '{:.3g}'.format(self.theta_top)],
                ['Nombre de pas d\'angle', str(self.theta_step_num)],
                ]
        init_table = Htable(init)
        table = Ftable()
        pressure = [node.p for generation in self.gen for node in generation]
        temperature = [node.temp for generation in self.gen for node in generation]
        y = [node.y*1000 for generation in self.gen for node in generation]
        x = [node.x*1000 for generation in self.gen for node in generation]

        table.set_title('Les points du maillage de caractéristiques')

        table.add_col([node.gen_id+0.01*node.node_id for generation in self.gen for node in generation],'Id')
        table.add_col([node.x*1000 for generation in self.gen for node in generation],'x (mm)')
        table.add_col([node.y*1000 for generation in self.gen for node in generation],'y (mm)')
        table.add_col([node.p for generation in self.gen for node in generation],'pression (Pa)')
        table.add_col([node.temp for generation in self.gen for node in generation],'Température (K)')
        table.disp()

        table_contour = Ftable()
        table_contour.set_title('Les points du contour de la tuyère')
        table_contour.add_col([node.x*1000 for node in self.wall],'x (mm)')
        table_contour.add_col([node.y*1000 for node in self.wall],'y (mm)')
        table_contour.add_col([node.p for node in self.wall],'pression (Pa)')
        table_contour.add_col([node.temp for node in self.wall],'Température (K)')
        table_contour.add_col([node.mach for node in self.wall],'Mach')
        table_contour.disp()
        return


    def graph(self,show_seg=True):
            plt.figure()
            nozzle_ax = plt.subplot(111)
            nozzle_ax.plot([i.x for i in self.wall],[i.y for i in self.wall],'b-')
            # nozzle_ax.plot([i.x for i in self.wall],[-i.y for i in self.wall],'b-')
            if show_seg :
                for i in self.seg :
                    i.graphSegment(nozzle_ax)
            nozzle_ax.plot([0,self.wall[-1].x],[0,0],'k:')

            nozzle_ax.set_aspect('equal')
            nozzle_ax.grid()
            plt.show()

    def iterate(physics,geometry,results) :
        iteration = []
        for parameter in physics.keys() :
            if type(physics[parameter]) is list :
                iterande = parameter 
                iter_list = physics[parameter]
                iteration_dic = physics.copy()
                for value in iter_list :
                    iteration_dic[iterande] = value
                    iteration.append(Nozzle(iteration_dic,geometry,results))

        for parameter in geometry.keys() :
            if type(geometry[parameter]) is list :
                iterande = parameter
                iter_list = geometry[parameter]
                iteration_dic = geometry
                for value in iter_list :
                    iteration_dic[iterande] = value
                    iteration.append(Nozzle(physics,iteration_dic,results))
        if 'iter_out_param' in results.keys() :
            for i, noz in enumerate(iteration) :
                if results['display_figure'] : noz.graph()
                print(f'{iter_list[i]}, {noz.charac[results["iter_out_param"]]}')
        return iteration

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


