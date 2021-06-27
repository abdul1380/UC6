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
x_time = pd.date_range(arrival_time, periods=24, freq='5min')

for generation in range(num_generations):
    
    fitness_cost = my_ga_1.cal_pop_fitness(tariffs, i_ga, grid_limits) # ( 2400 values)
    run_min_fitness_cost_idx = np.where(fitness_cost == np.min(fitness_cost))
    run_best_current =  i_ga[run_min_fitness_cost_idx, :][0][0]  # to acess (([x]))
    #print( run_best_current)
    #plt.step(x_time, run_best_current,label='Current')
    #plt.pause(0.05)

    # Selecting the best  (1920)  parents out of 2400 in the population for crossover.
    best_parents = my_ga_1.select_mating_pool(i_ga, fitness_cost, nc)
    # parents will be of shape (1920,24) i.e (num_parents_mating,slots)

    # Generating next generation using crossover.
    offspring_size = (pop_size[0]-best_parents.shape[0],num_slots) # pop_size[0] = 2400 and best_parents.shape[0] = 1920
    offspring_crossover = my_ga_1.crossover(best_parents,offspring_size)  # ( 480,24)
    

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = my_ga_1.mutation(offspring_crossover) # ( 480,24)

    # Creating the new population based on the parents and offspring.
    i_ga[0:best_parents.shape[0], :] = best_parents  # first 40 rows will be form healthy parents
    i_ga[best_parents.shape[0]:, :] = offspring_mutation # next 60 rows will be from mutation
    
    
    
    
    

    # The best result in the current iteration.
    #print("Best result : ", new_current)

# Getting the best solution after iterating finishing all generations.
fitness_cost = my_ga_1.cal_pop_fitness(tariffs, i_ga,grid_limits)
# Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness_cost == np.min(fitness_cost))

print("Best solution : ", i_ga[best_match_idx, :])
final_current =  i_ga[best_match_idx, :][0][0]
print("final_current = " ,final_current)

E_final = voltage * final_current /12000
P_final = voltage * final_current /1000


print("Final energy = " ,sum(E_final),"kWh")
cost_final = E_final*tariffs
print(sum(cost_final))
#p.plot(final_current)

SOC = [0 for i in range(len(final_current))]
SOC[0] = 0.2

for i in range(len(final_current)-1):
    e = final_current[i]*400/12000
    SOC[i+1] = SOC[i] + e/60
    
SOC= np.array(SOC)*100   

''' plotting '''

x_time = pd.date_range(arrival_time, periods=24, freq='5min')
#print(x_time)
#ticks_to_use = x_time[::2] # every 2nd values will be considered
#plt.style.use('ggplot')
fig, (ax1, ax2,ax3,ax4) = plt.subplots(4,1)
#fig.suptitle('(Constant electricity tariff / No grid limitation)')

ax=ax1
ax.step(x_time, tariffs,label='Tariffs',linewidth=2.0, color='gold')
ax.set(ylabel="eur/kwh", title="Tariffs")
#ax.legend(loc='upper right');
ax.set_xlim(arrival_time, parking_end_time)
ax.set_ylim(0.15, 0.5)
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d.%m'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
ax.grid(which='both')
ax.grid(which='minor', alpha=0.4)
ax.grid(which='major', alpha=0.8)
for label in ax.get_xmajorticklabels() + ax.get_xminorticklabels():
    label.set_rotation(20)
    label.set_horizontalalignment("right")

ax=ax2
ax.step(x_time, final_current,label='Current')
ax.step(x_time,grid_limits,label='Grid limit')
ax.set(ylabel="Current (A)", title="Current HL CMS")
ax.legend(loc='upper right');
ax.set_xlim(arrival_time, parking_end_time)
ax.set_ylim(0, 110)
ax.yaxis.set_minor_locator(AutoMinorLocator())

ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d.%m'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
ax.grid(which='both')
ax.grid(which='minor', alpha=0.4)
ax.grid(which='major', alpha=0.8)
for label in ax.get_xmajorticklabels() + ax.get_xminorticklabels():
    label.set_rotation(20)
    label.set_horizontalalignment("right")



ax=ax3
ax.plot(x_time, SOC,label='SOC')
ax.set(ylabel="SOC %")
ax.set_xlim(arrival_time, parking_end_time)
ax.set_ylim(0, 105)
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d.%m'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
ax.grid(which='both')
ax.grid(which='minor', alpha=0.4)
ax.grid(which='major', alpha=0.8)
for label in ax.get_xmajorticklabels() + ax.get_xminorticklabels():
    label.set_rotation(20)
    label.set_horizontalalignment("right")


ax=ax4
ax.step(x_time, P_final,label='Power(kW)')
ax.set(ylabel="Power(kW)")
ax.set_xlim(arrival_time, parking_end_time)
ax.set_ylim(0, 45)
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d.%m'))
ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
ax.grid(which='both')
ax.grid(which='minor', alpha=0.4)
ax.grid(which='major', alpha=0.8)
for label in ax.get_xmajorticklabels() + ax.get_xminorticklabels():
    label.set_rotation(20)
    label.set_horizontalalignment("right")


plt.show()