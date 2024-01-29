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
lightning_prob = 0.0001
# Initialize the wildfire map, with all locations being unburned
wildfire_map = np.zeros((N,N,3))
# Randomly select a starting location for the wildfire
i,j = random.randint(0,N-1), random.randint(0,N-1)
wildfire_map[i,j] = [1, 1, 0]  # Fire (Yellow)
#Initialize starting point, start at center of the map
aircraft_location=(50,50)
#Initial a home base for the aircraft, start at center of the map
base_location=(50,50)
#Put a flag for whether or not the aircraft is loaded with retardant
aircraft_loaded=1


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
def simulate_wildfire(forest_map, lightning_prob):
     for i in range(N):
         for j in range(N):
             if (wildfire_map[i,j] == [1, 1, 0]).all():
                 # Check each neighboring location to see if it catches fire
                 for i2 in range(max(0,i-1),min(i+2,N)):
                     for j2 in range(max(0,j-1),min(j+2,N)):
                         if (wildfire_map[i2,j2] == [0, 0, 0]).all():
                             # Compute the probability of the neighbor catching fire based on the neighbor's terrain type
                             if (forest_map[i2,j2] == [139/255, 69/255, 19/255]).all():  # Trees
                                 prob = 0.6
                             elif (forest_map[i2,j2] == [0, 1, 0]).all():  # Grass
                                 prob = 0.4
                             else:  # Water
                                 prob = 0.0
                             # Determine if the neighbor catches fire based on the probability and a random number
                             if random.random() < prob:
                                 wildfire_map[i2,j2] = [1, 1, 0]


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
                    wildfire_map[i,j] = [1, 1, 0]
     return wildfire_map
#def stupid_surveillance(wildfire_map):

def find_closest_fire(aircraft_location, wildfire_map):
  closest_fire_loc = (50,50) #Initializing this, we're going to calculate it
  distance = 1000000
  for i in range(N):
    for j in range(N):
      if (wildfire_map[i,j] == [1, 1, 0]).all(): # is this location is on fire
      # if so, find the distance
        distance_test=np.linalg.norm(np.subtract(aircraft_location,[i,j]))
        print(f'Distance {distance_test}')
        if distance_test < distance:
          distance = distance_test
          closest_fire_loc = wildfire_map[i,j]
    return (distance, closest_fire_loc)




def simulate_aircraft(aircraft_location, base_location, aircraft_loaded, wildfire_map):
  if 1:
  #fly to fire
  #find the fire first
    distance, closest_fire_loc=find_closest_fire(aircraft_location, wildfire_map)
  #fly to home
  return (aircraft_location, aircraft_loaded, wildfire_map)

"""
def distance_to_closest_fire(aircraft_location,wildfire_map):
def extinguisher():
"""

# Iterate over time steps
for t in range(1,50):
   # Check each location to see if it has caught fire
   print(f'Time step {t}')
   wildfire_map = simulate_wildfire(forest_map, lightning_prob)
   simulate_aircraft(aircraft_location, base_location, aircraft_loaded, wildfire_map)