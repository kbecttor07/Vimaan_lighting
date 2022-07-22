# Importing Libraries
import numpy as np
import math
import copy
#import vg
import vector3d.vector as vector
import vector3d.point as v3dpt
import matplotlib.pyplot as plt
from matplotlib import projections

# Defining Functions

# Way to calculate norm/euclidean dist
def distance(coord, pallet_anchor):
  dist = []
  dist.append(coord)
  dist.append(pallet_anchor)
  return np.linalg.norm(dist)

# Calculate Vector Angle

def angle_xy_sin(a, c):
  if (a[1] - c[1]) == 0:
    n = 1
  else:
    n = (a[1] - c[1])
  return np.arctan(((a[0] - c[0])/n))

def angle_yz_cos(a, c):
  if (a[2] - c[2]) == 0:
    n = 1
  else:
    n = (a[2] - c[2])
  return np.arctan(((a[1] - c[1])/n))

# Change in Lux due to vector angle

def beam_angle_block(angle_xy, angle_yz, beam_angle, lux):
  lux_xy = lux_yz = lux/2
  if angle_xy < (beam_angle/2):
    if angle_xy > (beam_angle/4):
      lux_xy = lux/4
    if angle_xy < (beam_angle/4):
      lux_xy = lux/2
  else:
    #print("Angle_xy > beam_angle/2 => lux_xy = 0 ---- angle_xy = ", angle_xy)
    lux_xy = 0
  if angle_yz < (beam_angle/2):
    if angle_yz > (beam_angle/4):
      lux_yz = lux/4
    if angle_yz < (beam_angle/4):
      lux_yz = lux/2
  else:
    #print("Angle_yz > beam_angle/2 => lux_yz = 0 ---- angle_yz = ", angle_yz)
    lux_yz = 0
  lux = lux_xy + lux_yz
  return lux

# Final lux calculation, including beam angle calculation
def lux_angle(lux, a, c, beam_angle):
  angle_xy = angle_xy_sin(a,c)
  angle_yz = angle_yz_cos(a,c)
  lux_c = beam_angle_block(angle_xy, angle_yz, beam_angle, lux)
  if lux_c < 0:
    print("lux<0, lux = ", lux)
    print("Reset to 0")
    lux_c = 0
  return lux_c*np.cos(angle_yz_cos(a,c))*np.sin(angle_xy_sin(a,c))


# Pallet_anchor is the midpoint of the pallet face at the starting position
pallet_anchor = [0,0,0]


# Generate Pallet Face Coordinates
# ^Z, >y

# Input height and width, generate pts from -h/2 to h/2 and -w/2 and w/2 => can choose to generate pallet either both ways from origin or one-way
# Use h/2 // w/2 or h//w based on this
height_pallet = int(input("Height of pallet (in mm) = "))
ht_2 = int(height_pallet/2)
width_pallet = int(input("Width of pallet (in mm) = "))
wd_2 = int(width_pallet/2)

# Initialize Pallet

pallet = [pallet_anchor]

# Create pallet

for z in range(0, height_pallet, 5):
  for y in range(0, width_pallet, 5):
    pallet.append([0,y,z])
#print("Pallet = ", pallet)
print("# of pallet pts = ", len(pallet))


# Create arc for incident angle

# input incident angle and depending on the input, generate the x and y

incident_angle = float(input("Input an angle between 20* and 60* = "))

theta = (np.pi/180)*incident_angle

radius = float(input("Euclidean Distance from Global origin (in mm) = "))

x = radius * np.cos(theta)
y = radius * np.sin(theta)

# the z will depend on # of LED, but for angle calculation we'll presume z=0
z = 0

coord = [x,y,z]

#print("Coordinate = ", coord)


# Generate array of LEDs

num_LEDs = int(input("Number of LEDs in the array = "))
dist_bw_LEDs = float(input("Distance between each LED (in mm) = "))
LED_arr = []
for i in range(0,num_LEDs):
  coord[2] = i*dist_bw_LEDs
  #print("Z_i = ", coord[2])
  LED_arr.append(copy.deepcopy(coord))
  #print(LED_arr[i])
#print("LED_arr = ", LED_arr)


# Calculating illumination at Pallet face

# Initialize lux_at_face
lux_at_face = np.zeros(len(pallet))

init_lux = int(input("Enter init_lux at a particular dist (in mm): init_lux = ")) # 6000 lux at 2ft = 609.6mm, 11 deg lens # Can also make this a variable that the user inputs
init_lux_dist = float(input("init_lux_dist (in mm) = "))
beam_angle = np.deg2rad(int(input("Input beam angle in degrees = ")))
print("Beam angle in radian = ", beam_angle)

# Distance contribution
for pt in range(len(pallet)):
  for LED in range(len(LED_arr)):
    dist = distance(LED_arr[LED], pallet[pt])
    lux_dist = init_lux*((init_lux_dist/dist)**2) #*np.cos(theta)
    lux = lux_angle(lux_dist, LED_arr[LED], pallet[pt], beam_angle)
    if lux<0:
      #print("lux = ", lux)
      #print("lux_dist = ", lux_dist)
      #print("LED_arr[LED] idx = ", LED)
      #print("pallet[pt] idx = ", pt)
      lux = 0

    lux_at_face[pt] += lux

print("lux at face = ", lux_at_face)


# Extract Y/Z coordinate pts
Y = []
Z = []

for i in range(len(pallet)):
  Y.append(pallet[i][1])
  Z.append(pallet[i][2])

Y = np.array(Y)
Z = np.array(Z)

# Graphssss
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#import numpy as np
from pylab import *

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#import numpy as np

x = Y
y = Z
z = lux_at_face

fig = plt.figure(figsize=(6, 6))
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot()
ax.scatter(x, y, z, linewidths=1, alpha=.1, edgecolor='k', color = 'green')
color_map = cm.ScalarMappable(cmap=cm.Greens)
color_map.set_array(lux_at_face)
plt.colorbar(color_map)
ax.set_title("Heatmap")
ax.set_xlabel('Y-axis')
ax.set_ylabel('Z-axis')
#ax.set_zlabel('Lux')

plt.show()