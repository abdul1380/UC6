import string
import random
# from  deap  import base,  creator, tools
#from scipy.optimize import minimize
from flask import Flask,jsonify,request,json
from flask_restx import Resource, Api, reqparse
from io import BytesIO 
from urllib.parse import urlencode
import time
#from urllib.request import Request, urlopen
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import my_ga_1
import datetime as dt 
import pandas as pd 
import matplotlib.dates as mdates
from matplotlib.pyplot import grid
from matplotlib.ticker import AutoMinorLocator
from turtledemo import round_dance
#from spyder.widgets.findinfiles import ON



arrival_time = dt.datetime(2020, 7, 11,13,30)   # 2020-07-11 13:30:00
print("arrival time = ",arrival_time)  
SOC_init= 0.2
E_demand = 40e3 # 40kWh 
parking_duration = 2 # hrs 
parking_end_time = arrival_time + dt.timedelta(hours=parking_duration)   # charing time  = 2hr by default
print("parking end time=  ",parking_end_time)
tariffs1 = [0.35, 0.35,0.35,0.35,0.35, 0.35,0.35,0.35,0.35, 0.35,0.35,0.35,   0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] # eur/5 min
grid_limit_1 = [100 for i in range(24)]

tariffs2 = [0.47, 0.47,0.47,0.46,0.46, 0.46,0.4,0.4,0.4, 0.35,0.35,0.35,   0.38,0.38,0.38,0.33,0.33,0.33,0.38,0.38,0.38,0.48,0.48,0.48] # eur/5 min

tariffs3 = [0.47, 0.47,0.47,0.46,0.46, 0.46,0.35,0.35,0.35, 0.2,0.2,0.2,   0.2,0.2,0.2,0.3,0.3,0.3,0.38,0.38,0.38,0.44,0.44,0.44] # eur/5 min
grid_limit_3= [100,85,90,85, 80,77,85, 100,85,90, 85, 80,77,85, 100,85,90,85, 80,77,85, 100,85,90]


tariffs=tariffs3
grid_limits =grid_limit_3
i_max = 150
i_min = 0
num_slots = parking_duration*12 # each slot is 5 min so 12 /hr
i_init = np.random.uniform(low=0,high=1,size =num_slots)*grid_limit_1 + i_min
print(i_init)

voltage = 400
E_init = voltage * i_init /12000
print("iniital random energy = " ,sum(E_init),"kWh")
cost_init = E_init*tariffs
print(sum(cost_init))


pop_rows = 2400 # chromosomes in population. or no: of rows in the population matrix  
pc = 0.8 # crossover percentage
nc = 2*round(pc*pop_rows/2) # no: of cross over b/w parents = 1920
pm = 0.2    #  Mutation Percentage
nm = round(pm*pop_rows);   # no: of mutations


pop_size = (pop_rows,num_slots) # The population have pop_rows and each row has num_slots values
i_ga_init = np.random.uniform(low= 0, high=1, size=pop_size) 
i_ga_init = i_ga_init*grid_limit_1 + i_min
i_ga = i_ga_init

num_generations = 200

import numpy.matlib

class empty_individual:
    def __init__(self): 
        self.Position =[]
        self.Cost = []
        
    
     
    
obj = empty_individual()






