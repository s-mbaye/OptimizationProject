#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:26:46 2023

@author: smbaye
"""

import random

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

# Define the size of the forested area and the probability of a lightning strike occurring at each location
N = 100
lightning_prob = 0.001
# Initialize the wildfire map, with all locations being unburned
wildfire_burnedQ=np.zeros((N,N))
wildfire_map = np.zeros((N,N,3))
# Randomly select a starting location for the wildfire
i,j = random.randint(0,N-1), random.randint(0,N-1)
wildfire_burnedQ[i,j]=1
wildfire_map[i,j] = [1, 1, 0]  # Fire (Yellow)
#Initialize starting point, start at center of the map
aircraft_location=(50,50)
#Initial a home base for the aircraft, start at center of the map
base_location=(50,50)
#Put a flag for whether or not the aircraft is loaded with retardant
aircraft_loaded=1
# The maximum distance an aircraft can move in one timestep
maxflydist = 50
# The radius of extinction when the aircraft is loaded and tries to extinguish
radius = 20


# Create a random map of the forested area, with each location being either trees, grass, or water
forest_map = np.zeros((N,N,3))
for i in range(N):
    for j in range(N):
        r = random.random()
        if r < 0.4:
            forest_map[i,j] = [139/255, 69/255, 19/255]  # Trees (Dark Brown)
            #prob[i,j] = 0.6
        elif r < 0.8:
            forest_map[i,j] = [0, 1, 0]   # Grass (Green)
        else:
            forest_map[i,j] = [0, 0, 1]   # Water (Blue)

# Define a function to simulate wildfire occurrence and spread
def simulate_wildfire(forest_map, lightning_prob, wildfire_map, wildfire_burnedQ):
    #Misty's bug note -- this spreads the wildfire too fast in the southeast direction
    wildfire_burnedQTemp=wildfire_burnedQ;
    wildfire_mapTemp=wildfire_map;
    for i in range(N):
      for j in range(N):
        #if (wildfire_map[i,j] == [1, 1, 0]).all():
        if wildfire_burnedQ[i,j] == 1:
          # Check each neighboring location to see if it catches fire
          for i2 in range(max(0,i-1),min(i+1,N)):
            for j2 in range(max(0,j-1),min(j+1,N)):
              #if (wildfire_map[i2,j2] == [0, 0, 0]).all():
              if wildfire_burnedQ[i2,j2] == 0:
                # Compute the probability of the neighbor catching fire based on the neighbor's terrain type
                if (forest_map[i2,j2] == [139/255, 69/255, 19/255]).all():  # Trees
                  prob = 0.6
                elif (forest_map[i2,j2] == [0, 1, 0]).all():  # Grass
                  prob = 0.4
                else:  # Water
                  prob = 0.0
                # Determine if the neighbor catches fire based on the probability and a random number
                if random.random() < prob:
                  wildfire_burnedQTemp[i2,j2] = 1
                  wildfire_mapTemp[i2,j2] = [1, 1, 0]

    wildfire_burnedQ=wildfire_burnedQTemp;
    wildfire_map=wildfire_mapTemp;

        # Don't move this, this prints the map at the end of every time step
    plt.subplot(121)
    plt.imshow(forest_map)
    plt.title('Forest Map')
    plt.subplot(122)
    plt.imshow(wildfire_map)
    plt.title('Wildfire Map')
    plt.pause(0.01)
    plt.clf()

        # Check if a new fire starts due to a lightning strike
    for i in range(N):
      for j in range(N):
        if random.random() < lightning_prob:
          print('Lightning struck at', i, j)
          wildfire_burnedQ[i,j] = 1
          wildfire_map[i,j] = [1, 1, 0]
    return (wildfire_map, wildfire_burnedQ)
#def stupid_surveillance(wildfire_map):

def find_closest_fire(aircraft_location, wildfire_map, wildfire_burnedQ):
  closest_fire_loc = (50,50) #Initializing this, we're going to calculate it
  distance = 1000000
  for i in range(N):
    for j in range(N):
      #if (wildfire_map[i,j] == [1, 1, 0]).all(): # is this location is on fire
      if wildfire_burnedQ[i,j] == 1: # is this location on fire
        #print('Inside find_closest_fire and there is a fire at ', i, '', j)
        # if so, find the distance
        distance_test=np.linalg.norm(np.subtract(aircraft_location,[i,j]))
        # print(f'Distance {distance_test}')
        if distance_test < distance:
          distance = distance_test
          closest_fire_loc = [i, j]
  return (distance, closest_fire_loc)

def extinguisher(aircraft_location, wildfire_map, wildfire_burnedQ):

  # Make sure our indices don't extend outside the map
  xlocmin= max(0,aircraft_location[0] - radius)
  xlocmax= min(N,aircraft_location[0] + radius)
  ylocmin= max(0,aircraft_location[1] - radius)
  ylocmax= min(N,aircraft_location[1] + radius)

  for i in range(xlocmin, xlocmax, 1):
    #print('i is ',i)
    for j in range(ylocmin, ylocmax, 1):
      wildfire_burnedQ[i,j] = 0
      wildfire_map[i,j] = [0, 0, 0] #Not on fire anymore
      aircraft_loaded = 0

  print('Just put out a fire between', xlocmin, xlocmax, ylocmin, ylocmax)
  return (aircraft_loaded, wildfire_map, wildfire_burnedQ)


def simulate_aircraft(aircraft_location, base_location, aircraft_loaded, wildfire_map, wildfire_burnedQ):
  # Is there a fire?
  #if np.isin(wildfire_map,[1,1,0]).any():
  #print(wildfire_burnedQ)
  if (wildfire_burnedQ.any()):
    print('Here is a fire')
    #print(wildfire_burnedQ)
    #print(wildfire_map)
    #print(np.isin(wildfire_map,[1,1,0]).any())
    #afire=1

  #if (np.isin(wildfire_map,[1,1,0]).any and aircraft_loaded): # This should figure out whether there is fire AND aircraft has to be loaded
  #if (np.isin(wildfire_burnedQ,1).any and aircraft_loaded): # This should figure out whether there is fire AND aircraft has to be loaded
  if (wildfire_burnedQ.any()):
    if aircraft_loaded:
      print('There is a fire and I am loaded')
      #find the fire first
      distance, closest_fire_loc=find_closest_fire(aircraft_location, wildfire_map, wildfire_burnedQ)
      #fly to fire
      if distance <= maxflydist:
        aircraft_location = closest_fire_loc
        print('Aircraft location is', aircraft_location)
        print('Aircraft x loc ',aircraft_location[0])
        aircraft_loaded, wildfire_map, wildfire_burnedQ = extinguisher (aircraft_location, wildfire_map, wildfire_burnedQ)
      else:
        # Really, we want the aircraft to fly the max distance in the direction of the fire
        aircraft_location = closest_fire_loc # We'll replace this
    else: # fly to home and reload
      aircraft_location = base_location
      aircraft_loaded = 1
      print ('Went home and reloaded')
      #fly to home
  else: # fly to home and reload
    aircraft_location = base_location
    aircraft_loaded = 1
    print ('Went home to wait for the next fire')
    #fly to home
  return (aircraft_location, aircraft_loaded, wildfire_map, wildfire_burnedQ)


# Iterate over time steps
for t in range(1,50):
   # Check each location to see if it has caught fire
   print(f'Time step {t}')
   print('At this time Aircraft location is', aircraft_location)
   wildfire_map, wildfire_burnedQ = simulate_wildfire(forest_map, lightning_prob, wildfire_map, wildfire_burnedQ)
   aircraft_location, aircraft_loaded, wildfire_map, wildfire_burnedQ  = simulate_aircraft(aircraft_location, base_location, aircraft_loaded, wildfire_map, wildfire_burnedQ)
