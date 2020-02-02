from math import *
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt



def HallFunction(nu) : #this is an inversion of the prandl-meyer function
    A = 1.3604
    B = 0.0962
    C = -0.5127
    D = -0.6722
    E = -0.3278
    nu_inf = (pi/2)*(sqrt(6)-1)
    y = pow(nu/nu_inf,2/3)
    return (1+A*y+B*y*y+C*y*y*y)/(1+D*y+E*y*y)

def PrandtlFunction(M,g=1.4): #computes the Prandtl-Meyer function (nu) for given M and gamma (1.4 by default)
    c1 = sqrt( (g+1)/(g-1) )
    c2 = atan( sqrt( ( (g-1)*(M*M-1) )/(g+1) ) )
    c3 = atan( sqrt(M*M-1) )
    return c1*c2-c3

def machAngle(M): #computes the Mach angles for a given Mach number
    return asin(1/M)

