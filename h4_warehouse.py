"""
11/18/2019
Homework #4
"""

"""
An inventory system that simulates >= 1 Warehouses with >= 1 Home Depots (HD) and schedule them
for when it runs. Each HD's inventory will be decremented until it reaches below the RP.

DES t.u = 1 hour
"""

import simpy        # simpy runtime
import random       # for internal randomness calculations
import numpy as np  # abbreviate numpy to np
import pdb          # Python debugger
import math         # Math function for flooring values to int

env=simpy.Environment()

seedNumber = 314607         # Assign a 5-6 unsigned number for seeding
np.random.seed(seedNumber)  # Generate the seeding using seedNumber

"""
Warehouse class
"""

class Warehouse:
    """ Constructor for Warehouse operations """
    def __init__ (self,env,warehouseName, numberOfHD):
        self.env = env
        self.warehouseName = warehouseName    # Name of warehouse
        self.numberOfHD = numberOfHD          # Number of HD stores to be supplied
        self.pfList = []                      # Initialize a list of scheduled HDs
        
        print("Running class Warehouse __init__ fcn for", warehouseName,    # See the Warehouse created along with seedNumber used for seeding
              " at time", env.now, "//NumPy seed is" , seedNumber)

    """ Create 'numberOfHD' instances of Home Depots and schedule them """
    def createHDInstance(self):
        print("Creating", self.numberOfHD, "stores for", self.warehouseName)    # See # of HD stores created for Warehouse
        
        #for loop HD 1 to numberOfHD
        for k in range(1, (self.numberOfHD+1), 1):  
            self.pfList.append(HomeDepot(self.warehouseName, k))    # Append HD k to pfList
            env.process(self.pfList[k-1].doOrders(self.env))        # Schedule doOrders() for HD in pfList[k-1]

"""
Home Depot class
"""

class HomeDepot:
    """ Constructor for Home Depot operations """
    def __init__ (self,  warehouseName, homeDepotNum): 
        self.homeDepotNum = homeDepotNum                    # Home Depot number
        self.order = math.floor(np.random.uniform(10,46))   # Initial random uniform distr between 10 and 45 inclusive floored to int
        self.inventory = 200                                # Inventory max at 200
        self.RP = 50                                        # RP at 50
        self.pfTime = math.floor(np.random.uniform(1,3))    # Initial random pfTime between 1 and 2 inclusive floored to int
        self.warehouseName = warehouseName                  # Warehouse name for Home Depot instance
 
        print(self.warehouseName, 'HD', self.homeDepotNum, 'created. Inventory:', self.inventory, 'RP:', self.RP)

    """ Do the orders for Home Depot"""
    def doOrders(self, env):
        print('Starting doOrders() for', self.warehouseName, # Start orders for HDs
              'HD', self.homeDepotNum, 'at time', env.now)   #
        
        # Iterate until the inventory reaches below RP
        while self.inventory >= self.RP:                     
            yield env.timeout(self.pfTime)                   # Delay by pfTime (1 or 2 t.u)
            self.inventory = self.inventory - self.order     # Decrease the inventory by the order

            print(self.warehouseName, 'HD', self.homeDepotNum, 'inventory level is', self.inventory, 'at time', env.now)
            
            self.order = math.floor(np.random.uniform(10,46))    # New order with random uniform distr betweeen 10 and 45 inclusive floored to int
            self.pfTime = math.floor(np.random.uniform(1,3))     # New random pfTime between 1 and 2 inclusive floored to int
        
        print('Finished', self.warehouseName, 'HD', self.homeDepotNum,          # Print remaining inventory and time finished
              'doOrders() at time', env.now, 'with inventory', self.inventory)

    
w = Warehouse(env, "WH1", 3)    # Create Warehouse named WH1 with 3 Home Depots   
w.createHDInstance()            # Call createHDInstance() to create and schedule Home Depots

env.run()  # Run until no more events scheduled

print('Finish run at model time', env.now)  # Display the time after finishing all runs
