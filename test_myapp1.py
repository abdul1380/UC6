''' Imp weblinks
https://pynative.com/python-post-json-using-requests-library/
'''

#import pycurl
from io import BytesIO 
from urllib.parse import urlencode
import time
from urllib.request import Request, urlopen
import requests
import json


optimization_request = {
'e_demand' : 40, # in kWh,
'already_provided': 0, # initially 0, in kWh ? in A?
'type _of_connector': 'type 2',
'type_of_charger': 'DC' ,
'current_time' : '15:30',
'current_price' : [ 0.2, 0.1, 0.2, 0.3, ], # euro/ kWh, 1 value each 5min 
'grid_limit' : [ 50, 50, 45, 30, 45,],# -- in A, same number of values
}


#First POST operation and then GET to see the same data
my_url = 'http://127.0.0.1:5000/predict'
response = requests.post(my_url, json=optimization_request)
print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response)
print(response.json())





