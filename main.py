from Nozzle import *
import time
from CoolProp.CoolProp import PropsSI
from packages.Htable import *
t0 = time.process_time()
#Limits of the canva
lengthLimit=50
heightLimit=20

#Geometry parameters
exit_mach = 2.157194624
#throatAngle =18.75
throatAngleStep =10
# throatMinAngle = 0.375

#physical parameters
tankPressure= 10e5 #Pa
tankTemperature = 573 #K
airGasConstant = 287.05 #J.kg-1.K-1
massFlow = 4 #kg.s-1
gamma = 1.4
noz = Nozzle(
        ntype = "expansion",
        tank_pressure = tankPressure,
        tank_temperature = tankTemperature,
        air_gas_constant = airGasConstant,
        mass_flow = massFlow,
        g = gamma,
        exit_mach = exit_mach,
        theta_step_num = throatAngleStep
        )

#noz.save_contour()
#noz.save_data(display)
t1 = time.process_time()
#noz.graph(show_seg=True)
t2 = time.process_time()
#print(t1-t0)
#print(t2-t0)


def gamma(p,t):
	return PropsSI("CPMASS", "P", p, "T", t, "Air")/PropsSI("CVMASS", "P", p, "T", t, "Air")

#for i in noz.wall :
        #print(i)
#print(noz.temp_totale)
#print(noz.p_totale)
