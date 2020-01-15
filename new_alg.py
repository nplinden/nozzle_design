from Nozzle import *
import time

#Limits of the canva
length_limit=50
height_limit=20

#Geometry parameters
theta_top =18.375
theta_step_num=10
theta_bottom = 0.375
#physical parameters
throat_mach = 1
throat_radius=1

#Defining the angles with which to start the calculation
theta_list = np.linspace(theta_bottom,theta_top,theta_step_num)
theta_list = [i * 2 * pi / (360) for i in  theta_list]
#Creating initial angles at sharp throat
seed = [ Node(0,throat_radius,i,1,nu=i) for i in theta_list ]
floor = Wall(0,0,0)
gen=[]

wall = [seed[-1]]


####################     Computing    ######################
seg = []
wall_seg = []

gen.append(seed.copy())
new_gen=[]
new_gen.append(gen[0][0].interWall(floor,length_limit,height_limit))
seg.append(Segment(gen[0][0],new_gen[-1]))
for node in gen[0][1:]:
    new_gen.append(node.interKm(new_gen[-1],length_limit,height_limit))
    seg.append(Segment(node,new_gen[-1]))
    seg.append(Segment(new_gen[-1],new_gen[-2]))
gen.append(new_gen.copy())
for i in range(1,theta_step_num):
    new_gen=[]
    new_gen.append(gen[i][1].interWall(floor,length_limit,height_limit))
    seg.append(Segment(gen[i][1],new_gen[-1]))
    for node in gen[i][2:]:
        new_gen.append(node.interKm(new_gen[-1],length_limit,height_limit))
        seg.append(Segment(node,new_gen[-1]))
        seg.append(Segment(new_gen[-1],new_gen[-2]))
    gen.append(new_gen.copy())

for generation in gen[1:] :
    last_node = generation[-1]
    wall_candidate = last_node.findRoof(wall)
    wall.append(wall_candidate)
    wall_seg.append(Segment(wall[-1],wall[-2]))
    seg.append(Segment(wall[-1],last_node))
 

####################     Graphing    ######################
plt.figure()
ax=plt.subplot(111)
for segment in seg :
    segment.graphSegment(ax)
for segment in wall_seg:
    segment.graphSegment(ax,'bo-')
#ax.set_xlim(-0.05,3)
#ax.set_ylim(-0.05,1.05)
ax.grid()
ax.set_aspect('equal')
plt.show()

