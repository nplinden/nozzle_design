from math import *
import matplotlib.pyplot as plt
from variousFunctions import HallFunction, machAngle
from Node import Node

def cotan(x) : return 1/tan(x)
thet_1 = 9 * 2*pi/360
nu_1 = 21.75 *2*pi/360
m_1 = 1.84
mu_1 = 32.9*2*pi/360
x_1 = 0.1
r_1 = 0.05
P1 = Node(x_1,r_1,thet_1,m_1)
print(P1.nu)
print(P1.mu)
thet_2 = 3 * 2*pi/360
nu_2 = 21.75 *2*pi/360
m_2 = 1.84
mu_2 = 32.9*2*pi/360
x_2 = 0.1
r_2 = 0.025
P2 = Node(x_2,r_2,thet_2,m_2)


thet_3 = 0.5*(P1.thet+P2.thet)
r_3 = 0.5*(P1.y+P2.y)
m_3 = 0.5*(P1.mach+P2.mach)
nu_3 =0.5*(P1.nu+P2.nu)
mu_3 = machAngle(P1.mach)
x_3 = max(P1.x,P2.x)
#Premiere convergence de theta3
delta = [1,1,1,1,1,1]
previous_step = [1,1,1,1,1,1]
while max(delta) > 1e-10 :
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

plt.figure()
ax = plt.subplot(111)
ax.plot([P1.x,P2.x,P3.x],[P1.y,P2.y,P3.y],'bo')
plt.show()
