import matplotlib.pyplot as plt
import numpy as np
import my_ga_1
import datetime as dt 
import pandas as pd 
import matplotlib.dates as mdates
from matplotlib.pyplot import grid
from matplotlib.ticker import AutoMinorLocator


final_current_6 =  np.array([32.41125946, 34.61013761, 30.58773186, 28.56292964, 30.12231385, 40.8055005,
 51.61275824, 75.95896465, 33.62291529, 65.34592046, 80.01226714, 70.15005758,
 43.98419406 ,55.8972883,  18.47306499, 22.93805272, 33.2786817 , 65.23734915,
 78.74424822, 67.7273251,  60.82271378, 54.7171954,  63.13220668, 63.23620169])


# for i in range(len(final_current)-1):
#     #print(final_current[i+1])
#     #print(final_current[i])
#     if abs(final_current[i+1] - final_current[i]) < 20:
#         final_current[i] = (final_current[i+1] + final_current[i])*0.5 
#         final_current[i+1] = final_current[i]



final_current_5 =  np.array ([ 4.83201068 ,67.38872027, 86.16222809, 47, 47, 47,
 75, 85.7900483,  75,  80, 80, 80,
 75, 80, 80, 60,60,60, 30,0,0, 0,0,0])

grid_limit_5= [100,85,90,85, 80,77,85, 100,85,90, 85, 80,77,85, 100,85,90,85, 80,77,85, 100,85,90]
grid_limit_1 = [100 for i in range(24)]

final_current =final_current_5
grid_limits =grid_limit_5    




tariffs1 = [0.35, 0.35,0.35,0.35,0.35, 0.35,0.35,0.35,0.35, 0.35,0.35,0.35,   0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1] # eur/5 min
tariffs2 = [0.47, 0.47,0.47,0.46,0.46, 0.46,0.4,0.4,0.4, 0.35,0.35,0.35,   0.38,0.38,0.38,0.33,0.33,0.33,0.38,0.38,0.38,0.48,0.48,0.48] # eur/5 min
tariffs3 = [0.47, 0.47,0.47,0.46,0.46, 0.46,0.35,0.35,0.35, 0.2,0.2,0.2,   0.2,0.2,0.2,0.3,0.3,0.3,0.38,0.38,0.38,0.44,0.44,0.44] # eur/5 min



tariffs=tariffs3




arrival_time = dt.datetime(2020, 7, 11,13,30)   # 2020-07-11 13:30:00
print("arrival time = ",arrival_time)  
SOC_init= 0.2
E_demand = 40e3 # 40kWh 
parking_duration = 2 # hrs 
parking_end_time = arrival_time + dt.timedelta(hours=parking_duration)   # charing time  = 2hr by default
print("parking end time=  ",parking_end_time)
num_slots = parking_duration*12 # each slot is 5 min so 12 /hr

x_time = pd.date_range(arrival_time, periods=24, freq='5min')
voltage = 400

E_final = voltage * final_current /12000
P_final = voltage * final_current /1000


print("Final energy = " ,sum(E_final),"kWh")
cost_final = E_final*tariffs
print("Charging cost = ",sum(cost_final)," eur")
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
