import numpy as np
import math
import copy
#import vg
import vector3d.vector as vector
import vector3d.point as v3dpt
import matplotlib.pyplot as plt
from matplotlib import projections

# Way to calculate norm/euclidean dist
def distance(coord, pallet_anchor):
  dist = []
  dist.append(coord)
  dist.append(pallet_anchor)
  return np.linalg.norm(dist)

def angle_xy_sin(a, c):
  return np.arctan(((a[0] - c[0])/(a[1] - c[1])))

def angle_yz_cos(a, c):
  return np.arctan(((a[1] - c[1])/(a[2] - c[2])))

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
      lux = lux/4
    if angle_yz < (beam_angle/4):
      lux_yz = lux/2
  else:
    #print("Angle_yz > beam_angle/2 => lux_yz = 0 ---- angle_yz = ", angle_yz)
    lux_yz = 0
  lux = lux_xy + lux_yz
  return lux

def lux_angle(lux, a, c, beam_angle):
  angle_xy = angle_xy_sin(a,c)
  angle_yz = angle_yz_cos(a,c)
  lux = beam_angle_block(angle_xy, angle_yz, beam_angle, lux)
  return lux*np.cos(angle_yz_cos(a,c))*np.sin(angle_xy_sin(a,c))

# Pallet_anchor is the midpoint of the pallet face at the starting position
pallet_anchor = [0,0,0]

#dist_moved = vel*dt
#pallet

# Generate Pallet Face Coordinates
# ^Z, >y

# Input height and width, generate pts from -h/2 to h/2 and -w/2 and w/2
height_pallet = int(input("Height of pallet (in mm) = "))
ht_2 = int(height_pallet/2)
width_pallet = int(input("Width of pallet (in mm) = "))
wd_2 = int(width_pallet/2)

#pallet_start = [pallet_anchor[0]+int(input("starting point of the pallet = ")), 0,0]

pallet = [pallet_anchor]

# create pallet
for z in range(0, height_pallet, 5):
  for y in range(0, width_pallet, 5):
    pallet.append([0,y,z])
#print("Pallet = ", pallet)
print("# of pallet pts = ", len(pallet))

# Create arc for incident angle

# input incident angle and depending on the input, generate the x and y

incident_angle = float(input("Input an angle between 20* and 60* = "))

theta = (np.pi/180)*incident_angle

radius = float(input("Euclidean Distance from Pallet (in mm) = "))

x = radius * np.cos(theta)
y = radius * np.sin(theta)
# the z will depend on # of LED, but for angle calculation we'll presume z=0
z = 0

#theta = np.linspace(-np.pi/6, np.pi/6, 100)
#theta
#radius = input()
#x = radius * np.cos(theta)
#y = radius * np.sin(theta)

#print("X = ", x)
#print("Y = ", y)

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
lux_at_face = np.zeros(len(pallet))
init_lux = 6000 # at 2ft = 609.6mm, 11 deg lens
beam_angle = np.deg2rad(int(input("Input beam angle in degrees = ")))
print("Beam angle in radian = ", beam_angle)

# Distance contribution
for pt in range(len(pallet)):
  for LED in range(10):
    dist = distance(LED_arr[LED], pallet[pt])
    lux_dist = 6000*((609.6/dist)**2) #*np.cos(theta)
    lux = lux_angle(lux_dist, LED_arr[LED], pallet[pt], beam_angle)
    lux_at_face[pt] += lux

print("lux at face = ", lux_at_face)



# 3D Heatmap in Python using matplotlib

# to make plot interactive
#%matplotlib

# 3D Heatmap in Python using matplotlib

# to make plot interactive
#%matplotlib 

# importing required libraries
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#import numpy as np
from pylab import *

# creating a dummy dataset
#x = np.random.randint(low=100, high=500, size=(1000,))
#y = np.random.randint(low=300, high=500, size=(1000,))
#z = np.random.randint(low=200, high=500, size=(1000,))
#colo = [x + y + z]

# Extract Y/Z coordinate pts
Y = []
Z = []

for i in range(len(pallet)):
  Y.append(pallet[i][1])
  Z.append(pallet[i][2])

Y = np.array(Y)
Z = np.array(Z)

# creating figures
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# setting color bar
color_map = cm.ScalarMappable(cmap=cm.Greens)
color_map.set_array(lux_at_face)

# creating the heatmap
img = ax.scatter(Y, Z, lux_at_face, marker='s',
				s=200, color='green')
plt.colorbar(color_map)

# adding title and labels
ax.set_title("3D Heatmap")
ax.set_xlabel('Y-axis')
ax.set_ylabel('Z-axis')
ax.set_zlabel('Lux')
ax.invert_xaxis()

# displaying plot
plt.show()


# Global position input for the LED array - Euc dist from pallet - input()
# Linear dist moved by the pallet = input()
# change plot to a 2d heatmap