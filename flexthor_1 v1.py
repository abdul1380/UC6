from time import sleep
from math import pi
import math
import datetime as  dt
from bokeh.io import output_file
from bokeh.plotting import show
from bokeh.models import LogColorMapper, Label, HoverTool, ColorBar, LinearColorMapper,LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import row, column , widgetbox
from bokeh.models.sources import ColumnDataSource
from bokeh.sampledata.unemployment1948 import data
from bokeh.transform import transform
from bokeh.palettes import Spectral11
import os
import numpy as np
import pandas as pd
import Emarket2
import csv
import sys
from random import randint
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models.widgets import TextInput,Toggle
from bokeh.models import Span
import time
from gpiozero import LED
from time import sleep
led = LED(17)

import warnings
# from docutils.nodes import legend

if not sys.warnoptions:
    warnings.simplefilter("ignore")

mypalette=Spectral11[0:10]
# define constants
RED   = '#e6550d'
GREEN = '#31a354'
GREY  = "#e2e2e2"
hover = HoverTool(tooltips=[("index", "$index"),("(x,y)", "($x, $y)"),("desc", "@desc"),])
tools = 'pan,wheel_zoom,xbox_select,reset,hover'


dir1= '/home/pi/Desktop/solar/' 

#dir1= "c:\\eclipse_work\\Businesscase_Winston\\solar_elia\\"



begin_day = time.mktime(dt.datetime(2018, 7, 15, 7, 45, 0).timetuple())*1000
end_day = time.mktime(dt.datetime(2018, 7, 15, 23, 45, 0).timetuple())*1000


sunrise = Span(location=begin_day, dimension='height', line_color='green', line_dash='dashed', line_width=1)
sunset = Span(location=end_day, dimension='height', line_color='red', line_dash='dashed', line_width=1)


curtail_time = time.mktime(dt.datetime(2018, 7, 15, 14, 30, 0).timetuple())*1000
curtail = Span(location=curtail_time, dimension='height', line_color='#2F4F4F', line_dash='dashed', line_width=5)


#d1 = dt.datetime.now()
d1 = dt.datetime(2018,7,15)
step_actual_time = 4*d1.hour + math.floor (d1.minute/15)
df_1 = pd.DataFrame(data =pd.date_range(dt.datetime(2018, d1.month, d1.day, 
                    hour=0, minute=0), periods=96, freq='15min0S'),columns =['time'])

df_1['k'] = [x for x in range(len(df_1))]



source = ColumnDataSource(data=dict(
                                    time = [], nomination = [], PV= [], pv_bart= [],pv_bart1= [],  voltage= [],  
                                    SOC_ch =[], SOC_dis =[]
                                    )       
                        )

data1 = dict( dates=[dt.date(2018, 7, i+1) for i in range(15)], APC_hours = [4,1,1,0,0,1.5,0,3,0,0,0.5,0,2.5,1.8] ,
              APC_saved = [1.5,1,1,0,0,1.5,0,1.5,0,0,0.5,0,1.5,1.5] ,
               eq_eur= [i*0.35 for i in [1.5,1,1,0,0,1.5,0,1.5,0,0,0.5,0,1.5,1.5]],
            )
source1 = ColumnDataSource(data=data1)
source2 = ColumnDataSource(          data=dict( m1=[],m2soc=[] )       )
source4 = ColumnDataSource(          data=dict( m1=[],m2volt=[] )       )


x_min = df_1['time'].min() 
x_max = df_1['time'].max()





#Elia_handle = Emarket2.Elia()  # loads the most recent file
#sleep(10)
df_elia = pd.DataFrame()
for file in os.listdir(dir1):
    df_elia = pd.ExcelFile(dir1+file)
    df_elia = df_elia.parse('SolarForecasts', skiprows=3, index_col=None, na_values=['NA'])
df_elia['time'] = pd.to_datetime(df_elia['DateTime'], format='%d/%m/%Y %H:%M').dt.time
PV_peak = 6
battery_peak = PV_peak 
df_elia['forecast_kW'] = df_elia['Most recent forecast [MW]']/481*PV_peak   # rescasled to 21 kW peak
df_elia['Actual_kW'] = df_elia['Real-time Upscaled Measurement [MW]']/481*PV_peak  # same as above
df_elia['pv_bart'] = df_elia['Real-time-bart-pv']/481*PV_peak  # same as above



df = pd.DataFrame(data= df_elia['forecast_kW'].tolist(), index= df_1['time'], columns=['Nominations']) 
df['k'] =df_1['k'].values
df['time'] =df_1['time'].values
df['Nominations'] = df_elia['forecast_kW'].values
df['PV'] = df_elia['Actual_kW'].values

df['voltage'] = df_elia['voltage'].values
df['batt_ch'] = df_elia['battery_ch'].values
df['batt_dis'] = df_elia['battery_dis'].values
df['pv_bart'] = df_elia['pv_bart'].values
df['pv_bart1'] = df['pv_bart'].values + 0.2

def display():
    p = figure(plot_width=1400, plot_height=200,x_range=(0,152), y_range=(0,200))
    p.image_url( url=[ "https://www.golder.com/wp-content/uploads/2017/07/Projects_Italian-Embassy-PV-Project.jpg"],
             x=1, y=1, w=100, h=200, anchor="bottom_left")
    p.image_url( url=[ "https://ik.imagekit.io/tayna/prod-images/1200/exide/er660.png"],
             x=101, y=1, w=50, h=200, anchor="bottom_left")
    #p.border_fill_color = "black"
    #p.background_fill_color = "black"
    p.axis.visible=False
    p.yaxis.major_label_text_color = "white"
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label 
    p.xgrid.grid_line_color = None 
    p.ygrid.grid_line_color = None
    return p




def bar_plot_2():
    p = figure(plot_width=100, plot_height=300, title = 'SOC',y_range=[0, 100])
    p.title.text_font_size = '14pt'
    p.title.text_color ='blue'
    p.vbar(x='m1', width=0.1, top='m2soc',source = source2,color="blue")
    xaxis = None
    yaxis = None
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks    
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label 
    p.xgrid.grid_line_color = None 
    p.ygrid.grid_line_color = None
    return p

def bar_plot_3():
    p = figure(plot_width=100, plot_height=300, title = 'Voltage:', y_range=[220, 260] )
    p.title.text_font_size = '14pt'
    p.title.text_color ='red'
    p.vbar(x='m1', width=0.1, top='m2volt',source = source4,color="red")
    
    #p.xaxis = None
    #p.yaxis = None
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks    
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label 
    p.xgrid.grid_line_color = None 
    p.ygrid.grid_line_color = None
    return p

def bar_plot_4():
    p = figure(plot_width=100, plot_height=300, title = 'COMP:', y_range=[0, 100] )
    p.title.text_font_size = '11pt'
    p.vbar(x='m1', width=0.1, top='m2soc',source = source2,color="green")
    xaxis = None
    yaxis = None
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks    
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label 
    p.xgrid.grid_line_color = None 
    p.ygrid.grid_line_color = None
    return p

    
    
def Actual():
    global x_min, x_max
    p = figure(plot_width=1500, plot_height=200, title = 'GENK PV ', y_range=[0, 5],
               x_range = (x_min.timestamp()*1000, x_max.timestamp()*1000), x_axis_type='datetime')
    p.title.text_font_size = '11pt'
    p.step(x='time', y = 'nomination', source = source , line_width= 3, color='orange', legend=" Flexthor forecast")
    p.line(x='time', y = 'PV',source = source, line_width=3, color='deepskyblue' , legend=" Actual PV  ")
    p.legend.location = "top_left"
    p.legend.background_fill_color = "whitesmoke"
    p.legend.click_policy="hide"
    p.yaxis[0].axis_label =  ' kW'
    p.xaxis.ticker = [df.index[x].timestamp()*1000 for x in range(96)]
    p.xaxis.major_label_orientation = pi/2
    
    p.add_layout(sunrise)
    p.add_layout(sunset)
    p.xaxis.major_label_text_color = "black"
    p.xaxis.major_label_text_font_size = "8pt"  
    p.yaxis.major_label_text_color = "black"
    p.yaxis.major_label_text_font_size = "11pt"
    p.background_fill_color = "lightgray"
    #p.border_fill_color = "darkgrey"
    p.min_border_left = 10
    p.min_border_top = 10
    return p


def bart_plot():
    global x_min, x_max
    p = figure(plot_width=1500, plot_height=200, title = 'GENK based customer ', y_range=[0, 5],
               x_range = (x_min.timestamp()*1000, x_max.timestamp()*1000), x_axis_type='datetime', #y_range=[0, 10] 
               )
    p.title.text_font_size = '11pt'
    p.line(x='time', y = 'pv_bart1',source = source, line_width=2, color='deepskyblue')
    p.line(x='time', y = 'pv_bart',source = source, line_width=5, color='lightskyblue',line_alpha =0.3)
    p.vbar(x='time', width=900000 ,top='pv_bart',source = source,line_color='lightskyblue',line_alpha =0.3, fill_color= 'lightskyblue', fill_alpha = 0.3, legend=" Bart PV ")
    p.legend.location = "top_left"
    p.legend.background_fill_color = "whitesmoke"
    p.legend.click_policy="hide"
    p.yaxis[0].axis_label =  ' kW'
    
    
    
    p.xaxis.ticker = [df.index[x].timestamp()*1000 for x in range(96)]
    p.xaxis.major_label_orientation = pi/2
    p.xaxis.major_label_text_color = "black"
    p.xaxis.major_label_text_font_size = "8pt"  
    p.yaxis.major_label_text_color = "black"
    p.yaxis.major_label_text_font_size = "11pt"
    p.background_fill_color = "lightgray"
    #p.border_fill_color = "darkgrey"
    p.min_border_left = 10
    p.min_border_top = 10
    return p





def bar_plot():
    global x_min, x_max
    p = figure(plot_width=1500, plot_height=200, title = 'Battery SOC', 
               x_range = (x_min.timestamp()*1000, x_max.timestamp()*1000), x_axis_type='datetime',
              y_range=[-15, 125] )
    p.title.text_font_size = '11pt'
    p.vbar(x='time', width=900000 ,top='SOC_dis',source = source,line_color='white', fill_color= RED,legend=" Battery SOC_dis ")
    p.vbar(x='time', width=900000 ,top='SOC_ch',source = source,line_color='white', fill_color= GREEN ,legend=" Battery SOC_chg ")
    p.yaxis[0].axis_label = 'SOC'
    p.extra_y_ranges = {"foo": Range1d(start=140, end=260)}
    
    p.add_layout(LinearAxis(y_range_name="foo",axis_label='%'), 'right')
    p.step(x='time' ,y ='voltage',source = source,line_color='mediumslateblue',line_width=3,y_range_name="foo", legend=" grid voltage ")

    
    p.legend.location = "bottom_right"
    p.legend.background_fill_color = "whitesmoke"
    p.legend.click_policy="hide"
    
    p.xaxis.ticker = [df.index[x].timestamp()*1000 for x in range(96)]
    p.xaxis.major_label_orientation = pi/2
    p.xaxis.major_label_text_color = "black"
    p.xaxis.major_label_text_font_size = "8pt"  
    p.yaxis.major_label_text_color = "black"
    p.yaxis.major_label_text_font_size = "11pt"
    p.background_fill_color = "lightgray"
    #p.border_fill_color = "darkgrey"
    p.min_border_left = 10
    p.min_border_top = 10
    return p



step = 0
actual_PV_kW = 0
batt_current_kW_needed = 0
batt_current_kWh_needed = 0
batt_current_kWh = 0
batt_current_kW  = 0
first_time =True
my_flag =True
batt_kW_list =[]

def update_data():
    global step, actual_PV_kW, batt_current_kW_needed, batt_current_kWh_needed
    global batt_current_kWh, batt_current_kW,first_time,SOE_final, bat_val, my_flag
    
    while step < 96:
        
        print(step)
        d = dt.datetime.now()
        print(d.strftime("%Y-%m-%d %I:%M:%S %p"))
        step_actual_time = 4*d.hour + math.floor (d.minute/15)
        data = pd.DataFrame()
        data = data.append(df.iloc[step])
       
        if (step < step_actual_time-1 or my_flag):
            new_data = dict( time = data['time'].tolist() ,  nomination =data['Nominations'].tolist(),
                            PV = data['PV'].tolist()     ,  pv_bart = data['pv_bart'].tolist() ,  
                            pv_bart1 = data['pv_bart1'].tolist() , voltage = data['voltage'].tolist() ,  
                            SOC_ch = data['batt_ch'].tolist() , SOC_dis = data['batt_dis'].tolist()  
                              )
            
            
            source.stream(new_data, 100)
            if(step<1):
                source2.stream(dict(m1=[1], m2soc=data['batt_dis'].tolist()))
                source4.stream(dict(m1=[1], m2volt=data['voltage'].tolist()))
            elif (step<55):
                ind = len(source2.data['m2soc']) - 1 
                source2.patch(   dict(  m2soc=[(ind, df.iloc[step]['batt_dis'])]  )   )
                source4.patch(   dict(  m2volt=[(ind, df.iloc[step]['voltage'])]  )   )
                led.on()

            elif(step < 63):
                ind = len(source2.data['m2soc']) - 1
                source2.patch(   dict(  m2soc=[(ind, df.iloc[step]['batt_dis'])]  )   )
                source4.patch(   dict(  m2volt=[(ind, df.iloc[step]['voltage'])]  )   )
                led.off()
            else:
                ind = len(source2.data['m2soc']) - 1
                source2.patch(   dict(  m2soc=[(ind, df.iloc[step]['batt_ch'])]  )   )
                source4.patch(   dict(  m2volt=[(ind, df.iloc[step]['voltage'])]  )   )
                led.on()

                
                #source4.patch(   dict(  m2imb=[(ind, df.iloc[step]['error_kW_no_battery'])]  )   )
            
            sleep(1)
        else:
            t = d.minute%15
            if(t < 11):
                q = 11-t
                print("waiting for", q," min")
                sleep(q*60)
            else:
                print(" t is  10 or higher and all set")                 
            #elia_unbalance_handle_1 =Emarket2.Elia_unbalance()
            #Elia_handle_1 = Emarket2.Elia()
            #sleep(10)
            #df1 = pd.DataFrame()
            #df1 = df_elia
        
            #for file in os.listdir(dir1):
                #df1 = pd.ExcelFile(dir1+file)
                #df1 = df1.parse('SolarForecasts', skiprows=3, index_col=None, na_values=['NA'])
                
            #actual_PV_kW  = df1.iloc[step]['Real-time Upscaled Measurement [MW]']/481*PV_peak
            #error_val =0
            #bat_val = data['Nominations'].values[0] - actual_PV_kW
            #print("step ",step,"  1 bat_val= ", bat_val)
            #batt_current_kW_needed = bat_val
            #batt_current_kWh_needed = batt_current_kW_needed*0.25
            #if(first_time ==True):
                #SOE_final = df_elia.iloc[step-1]['SOE']- batt_current_kWh_needed # SOE prev - needed kWH
                #print("step ",step,"  2 SOE_final= ", SOE_final)
                #first_time =False

            #new_data = dict( time = data['time'].tolist() ,  nomination =data['Nominations'].tolist(),
             #               PV = [actual_PV_kW],  pv_bart = data['pv_bart'].tolist() , pv_bart1 = data['pv_bart1'].tolist(),
              #              voltage = data['voltage'].tolist() ,
               #              )
            
            #ind = len(source2.data['m2soc']) -1 
            #source2.patch(dict(m2soc=[(ind, SOE_final/SOE_max*100)]))
            #source4.patch(dict(m2soc=[(ind, error_val)]))
            #source.stream(new_data, 100)
            print("wating for 5 more minutes")
            sleep(5*60)                
            
        step +=1
                
p0 =display()
#p01 = wedge_plot()

#p010 =row(p0,p01)
p1 = Actual() 
p2 = bart_plot()
p3 = bar_plot()
p8 =  bar_plot_2()
p9 = bar_plot_3()
p10 = bar_plot_4()

pq = row(p8,p9)

data_column_1 = column(p0,p1,p2,p3)


table_column = [    TableColumn(field="dates", title="Date", formatter=DateFormatter()),
                    TableColumn(field="APC_hours", title="APC hours"),
                    TableColumn(field="APC_saved", title="APC saved"),
                    TableColumn(field="eq_eur", title="Equivalent euros"),
               ]
data_table1 = DataTable(source=source1, columns=table_column, width=400, height=400)

data1 = dict( dates=[dt.date(2018, 11, i+1) for i in range(20)], SOC_set_point=[50 for i in range(20)] ,
              Nominated_volume = [randint(20,50) for i in range(20) ],
              Traded_volume = [randint(20,50) for i in range(20) ],
            )
source1 = ColumnDataSource(data1)
table_column = [    TableColumn(field="dates", title="Date", formatter=DateFormatter()),
                    TableColumn(field="SOC_set_point", title="SOC set point"),
                    TableColumn(field="Nominated_volume", title="Nominated Volume"),
               ]
data_table2 = DataTable(source=source1, columns=table_column, width=400, height=400)

d = dt.datetime.now()
text_input1 = TextInput(value=d.strftime("%Y-%m-%d %I:%M:%S %p"), title="Table:")
text_input2 = TextInput(value="Run time calculation for today", title="Table:")

toggle = Toggle(label="HISORICAL APC DATA FOR TWO WEEKS ", button_type="success")


data2 =column(widgetbox(toggle),widgetbox(data_table1),pq,# widgetbox(text_input2),  widgetbox(data_table2)
              ) 

dashboard = row(data_column_1,data2)
curdoc().add_root(dashboard)
curdoc().add_periodic_callback(update_data, 5e3)
curdoc().title = "WELCOME TO FLEXTHOR"
#update_data()        

