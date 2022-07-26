# Importing Libraries
import numpy as np
import math
import copy
#import vg
import vector3d.vector as vector
import vector3d.point as v3dpt
import matplotlib.pyplot as plt
from matplotlib import projections

import itertools
import pandas as pd
import seaborn as sns

# Defining Functions

# Way to calculate norm/euclidean dist
def distance(coord, pallet_anchor):
  dist = []
  dist.append(coord)
  dist.append(pallet_anchor)
  return np.linalg.norm(dist)


# Calculate Vector Angle

# Angle IN XY plane # rechecked - correct way to calculate angle in XY plane [are we getting negative values?]
def angle_xy_sin(a, c):
  if (a[1] - c[1]) == 0:
    #n = 1
    return np.arctan(0)
  else:
    n = (a[1] - c[1])
    return abs(np.arctan(((a[0] - c[0])/n)))



# Angle IN YZ plane  # rechecked - correct way to calculate angle in YZ plane
def angle_xz_cos(a, c):
  hypo = np.sqrt(np.square(a[0] - c[0]) + np.square(a[1] - c[1]))
  if hypo == 0:
    #n = 1
    return np.deg2rad(90)
  else: # arctan((a[2]-c[2])/np.sqrt((a[0]-c[0])**2 + (a[1]-c[1])**2)
    
    #return abs(np.arctan(((a[0] - c[0])/n))) # correction - should be XZ and not YZ
    Z = a[2] - c[2]
    
    return abs(np.arctan(Z/hypo)) # rechecked calculation - correct



# Change in Lux due to vector angle - visualized in the form of the beam being blocked wrt angle
# Subtract theta = incident angle to get the relative angle bw LED and pallet face pts

def compare_w_beam_angle_xz (lux, angle, beam_angle):

  if abs(angle) < (beam_angle/2):
    if abs(angle) > (beam_angle/4):
      return lux/2
    if abs(angle) < (beam_angle/4):
      return lux
  

def compare_w_beam_angle_xy (lux, angle, beam_angle, theta):

  if abs(angle - theta) < (beam_angle/2):
    if abs(angle - theta) > (beam_angle/4):
      return lux/2
    if abs(angle - theta) < (beam_angle/4):
      return lux
  

def beam_angle_block(angle_xy, angle_xz, beam_angle, lux, theta):

  # 2 components - with XZ plane and XY plane
  # XZ plane - reference plane - needs to be shifted
  # XY plane - needs to be referenced with the incident angle (have an array of points with [x,y, z = LED])
  bigger_angle = 0
  if angle_xy < angle_xz:
    bigger_angle = angle_xz

    if bigger_angle < (beam_angle/2):
      lux_xz = compare_w_beam_angle_xz(lux, angle_xz, beam_angle)*np.cos(angle_xz)
      lux_xy = compare_w_beam_angle_xy(lux_xz, angle_xy, beam_angle, theta)*np.sin(angle_xy)

      return lux_xy


    else:

      #print("Bigger angle_xz > beam/2 = ", np.rad2deg(bigger_angle))

      return 0
  
  else:
    bigger_angle = angle_xy

    if bigger_angle < (beam_angle/2):
      lux_xz = compare_w_beam_angle_xz(lux, angle_xz, beam_angle)*np.cos(angle_xz)
      lux_xy = compare_w_beam_angle_xy(lux_xz, angle_xy, beam_angle, theta)*np.cos(angle_xy)

      return lux_xy


    else:

      #print("Bigger angle_xy > beam/2 = ", np.rad2deg(bigger_angle))

      return 0


  
  


  #lux_xy = lux_xy*np.cos(angle_xy)
  #lux_yz = lux_yz*np.cos(angle_yz)




# Final lux calculation, including beam angle calculation

def lux_angle(lux, a, c, beam_angle, theta):
  angle_xy = angle_xy_sin(a,c) 
  #print("a = ", a)
  #print("c = ", c)
  #print("angle_xy = ", np.rad2deg(angle_xy))
  angle_xz = angle_xz_cos(a,c) 
  #print("angle_xz = ", np.rad2deg(angle_xz))
  lux_ac = beam_angle_block(angle_xy, angle_xz, beam_angle, lux, theta)
  
  return lux_ac

####################### functions defined #################################

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

for z in range(-ht_2, ht_2, 5):
  for y in range(-wd_2, wd_2, 5):
    pallet.append([0,y,z])
#print("Pallet = ", pallet)
print("# of pallet pts = ", len(pallet))


# Create arc from pallet anchor for incident angle

# input incident angle and depending on the input, generate the x and y

incident_angle = float(input("Input an angle between 20* and 60* = "))

theta = (np.pi/180)*incident_angle

radius = float(input("Euclidean Distance from Pallet Anchor (in mm) = "))

x = radius * np.cos(theta)
y = radius * np.sin(theta)

# the z will depend on # of LED, but for angle calculation we'll presume z=0
z = 0

coord = [x,y,z]

#print("Coordinate = ", coord)


# Generate array of LEDs

num_LEDs = int(input("Number of LEDs in the array = "))
num_LEDs_2 = int(num_LEDs/2)
dist_bw_LEDs = float(input("Distance between each LED (in mm) = "))
LED_arr = []

# Add ref_arr for the calculation of incident angle
#incident_ang_ref_arr = []
#ref_coord = pallet_anchor

for i in range(-num_LEDs_2,num_LEDs_2):
  coord[2] = i*dist_bw_LEDs                 # to get coordinate of LED
  #ref_coord[2] = i*dist_bw_LEDs             # to get corresponding coordinate for incident angle on pallet
  #print("Z_i = ", coord[2])
  LED_arr.append([x,y,i*dist_bw_LEDs])
  #incident_ang_ref_arr.append(copy.deepcopy(ref_coord))
  #print(LED_arr[i])
#print("LED_arr = ", LED_arr)


# Calculating illumination at Pallet face

# Initialize lux_at_face
lux_at_face = np.zeros(len(pallet))
print("Enter init_lux at a particular dist (in mm): ")
init_lux = int(input("init_lux = ")) # 6000 lux at 2ft = 609.6mm, 11 deg lens # Can also make this a variable that the user inputs
init_lux_dist = float(input("init_lux_dist (in mm) = "))
beam_angle = np.deg2rad(int(input("Input beam angle in degrees = ")))
print("Beam angle in radian = ", beam_angle)

# Distance contribution
for pt in range(len(pallet)):
  for LED in range(len(LED_arr)):
    dist = distance(LED_arr[LED], pallet[pt])
    lux_dist = init_lux*((init_lux_dist/dist)**2) 

    #print("Lux_dist = ", lux_dist)
    #print("LED = ", LED_arr[LED])
    #print("Pallet_pt = ", pallet[pt])
    
    # Get angle contribution and final projections

    lux = lux_angle(lux_dist, LED_arr[LED], pallet[pt], beam_angle, theta)
    if lux<0:
      #print("lux = ", lux)
      #print("lux_dist = ", lux_dist)
      #print("LED_arr[LED] idx = ", LED)
      #print("pallet[pt] idx = ", pt)
      lux = 0

    lux_at_face[pt] += lux

print("lux at face = ", lux_at_face)

############################### Make graphs #######################################

# Extract Y/Z coordinate pts
Y = []
Z = []

for i in range(len(pallet)):
  Y.append(pallet[i][1])
  Z.append(pallet[i][2])

Y = np.array(Y)
Z = np.array(Z)



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import numpy as np

#from mpl_toolkits.mplot3d import Axes3D
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

################## SNS HEATMAP ########################

# Create pandas DataFrame to hold pallet grid points and lux values
pallet_lux_df = pd.DataFrame(pallet, columns=['pallet_x_pt', 'pallet_y_pt', 'pallet_z_pt'])
# Insert empty columns for lux contribution from individual LEDs and the beam masked contribution


# Insert an empty column for total lux from all LEDs

pallet_lux_df[f'total_led_lux'] = 0

for idx in range(len(lux_at_face)):
    pallet_lux_df['total_led_lux'][idx] = lux_at_face[idx]

pallet_lux_df = pallet_lux_df.drop(index = [0])

# Visualize total led lux without beam masks
fig, ax = plt.subplots(figsize=(20, 15))
df = pallet_lux_df.pivot('pallet_z_pt', 'pallet_y_pt', 'total_led_lux')
sns.heatmap(data=df, ax=ax)
ax.invert_yaxis()
print("plot now")
plt.show()
#zd = input("input")
