from math import *
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt



def PMfunction(M,g=1.4): #computes the Prandtl-Meyer function (nu) for given M and gamma (1.4 by default)
    c1 = sqrt( (g+1)/(g-1) )
    c2 = atan( sqrt( ( (g-1)*(M*M-1) )/(g+1) ) )
    c3 = atan( sqrt(M*M-1) )
    return c1*c2-c3


def machAngle(M): #computes the Mach angles for a given Mach number
    return asin(1/M)

#units conversion
def radToDeg(alpha): return(alpha*(180/np.pi))
def degToRad(alpha): return(alpha*(np.pi/180))

def centerNode(nu0,g=1.4):
    #center nodes have a fixed flow angle of 0, therefore on these nodes nu0 is equal to the flow angle (theta) of the preceding node, we look for the root of the Prandtl-Meyer function minus nu0 to compute the Mach number and then the Mach angle. This gives us the slope of the next characteristic line. The function return the Mach number and the Mach ange in both rads and degs.
    f = lambda x : PMfunction(x,g)-nu0
    mach0 = fsolve(f,1)
    mu0 = machAngle(mach0)
    return [mach0,mu0,radToDeg(mu0)]


def m_from_nu(nu0,g=1.4):
    f = lambda x : PMfunction(x,g)-nu0
    mach0 = fsolve(f,1)
    return mach0[0]

def A_from_M(M,A0=0.02010619298297468,g=1.4) :
    c1 = pow(1+0.5*(g-1)*M*M,0.5*(g+1)/(g-1))
    c2 = pow(0.5*(g+1),0.5*(g+1)/(g-1))
    return (A0 * c1) / (M * c2)

def R_from_A(A) :
    return sqrt(A/pi)


def internalNode(nu1,thet1,nu2,thet2):
    #Internal, non-center nodes are defined by the intersection of two characteristic lines (A C+ and a C- line). We write parameters refering to the C- line with a 1 and parameters refering to the C+ line with a 2)
    K1 = thet1 + nu1
    K2 = thet2 - nu2
    thetNode = 0.5*(K1+K2)
    nuNode = 0.5*(K1-K2)
    f = lambda x : PMfunction(x,g)-nuNode
    machNode = fsolve(f,1)
    muNode = machAngle(machNode)
    return [thetNode,nuNode,machNode,muNode]


#print(centerNode(0.1576))
#print(centerNode(0.078889))
#print(centerNode(0.11825))
