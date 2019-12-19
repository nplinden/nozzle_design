from Nozzle import *
import time
t0 = time.process_time()
#Limits of the canva
lengthLimit=50
heightLimit=20

#Geometry parameters
throatRadius = 1
throatAngle = 18.375
# throatAngleStep = 37
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
T=[]
throatAngleStep = [i for i in range(1,50)]
for angle in throatAngleStep :
    t0=time.process_time()
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
            theta_step_num = angle
            )
    t1 = time.process_time()
    T.append(t1-t0)

plt.figure()
ax=plt.subplot(111)
ax.set_title('Temps de calcul en fonction du nombre de steps')
ax.set_ylabel('Temps de calcul /s')
ax.set_xlabel('Nombre de steps')
ax.plot(throatAngleStep,T,'o--')
plt.show()
print(throatAngleStep)
print(T)
