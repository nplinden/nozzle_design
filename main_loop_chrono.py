from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from CoolProp.CoolProp import PropsSI


fig = plt.figure()
ax = fig.gca(projection='3d')
def get_gamma(p,t):
	return PropsSI("CPMASS", "P", p, "T", t, "Air")/PropsSI("CVMASS", "P", p, "T", t, "Air")
print(get_gamma(100000,573))
# Make data.
P = np.linspace(100000,1000000,10) 
T = np.linspace(273,2000,10)
R = np.sqrt(P**2 + T**2)
g =np.zeros((10,10)) 
for i in range(len(P)):
	for j in range(len(T)):
		g[i][j] = get_gamma(P[i],T[j])
print(g)
# Plot the surface.
T, P = np.meshgrid(T, P)
surf = ax.plot_surface(P*1e-5, T, g, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(1.3, 1.6)
ax.set_title(r'$\gamma$ en fonction de P et de T')
ax.set_ylabel("temperature (K)")
ax.set_xlabel("Pression (Bar)")
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
