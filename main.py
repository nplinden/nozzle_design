from Nozzle import *
import time
from CoolProp.CoolProp import PropsSI

t0 = time.process_time()
#Limits of the canva
lengthLimit=50
heightLimit=20

#Geometry parameters
throatAngle =25
throatAngleStep =10
# throatMinAngle = 0.375

#physical parameters
throatPressure= 10e5 #Pa
throatTemperature = 1000 #K
throatMach = 1
airGasConstant = 287.05 #J.kg-1.K-1
massFlow = 4 #kg.s-1
gamma = 1.4

#results parameters
display = ['X','Y','mach','thet','nu','mu','T','P']

noz = Nozzle(
        ntype = "expansion",
        length_limit = lengthLimit,
        height_limit = heightLimit,
        throat_pressure = throatPressure,
        throat_temperature = throatTemperature,
        throat_mach = throatMach,
        air_gas_constant = airGasConstant,
        mass_flow = massFlow,
        g = gamma,
        theta_top = throatAngle,
        theta_step_num = throatAngleStep
        )

#noz.save_contour()
#noz.save_data(display)
t1 = time.process_time()
noz.graph(show_seg=True)
t2 = time.process_time()
#print(t1-t0)
#print(t2-t0)


def gamma(p,t):
	return PropsSI("CPMASS", "P", p, "T", t, "Air")/PropsSI("CVMASS", "P", p, "T", t, "Air")

#for i in noz.wall :
        #print(i)
#print(noz.temp_totale)
#print(noz.p_totale)
