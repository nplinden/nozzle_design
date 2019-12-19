from Nozzle import *
#Limits of the canva
lengthLimit=50
heightLimit=20

#Geometry parameters
throatRadius = 1
throatAngle = 18.375
throatAngleStep = 20
# throatMinAngle = 0.375

#physical parameters
throatPressure= 10e5 #Pa
throatTemperature = 573 #K
throatMach = 1
airGasConstant = 287.5 #J.kg-1.K-1
massFlow = 4 #kg.s-1
gamma = 1.4

#results parameters
display = ['X','Y','mach','thet','nu','mu','T','P']

noz = Nozzle(
        length_limit = lengthLimit,
        height_limit = heightLimit,
        throat_radius = throatRadius,
        throat_pressure = throatPressure,
        throat_temperature = throatTemperature,
        throat_mach = throatMach,
        air_gas_constant = airGasConstant,
        mass_flow = massFlow,
        g = gamma,
        theta_top = throatAngle,
        theta_step_num = throatAngleStep
        )

noz.save_contour()
noz.save_data(display)
# noz.graph()
