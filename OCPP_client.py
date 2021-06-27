'''
Created on 15 Jul 2020

@author: AbdulMannanRauf
'''
import asyncio
from datetime import datetime
import logging
from binstar_client.utils.config import CONFIGURATION_KEYS

try:
    import websockets
except ModuleNotFoundError:
    print("Please install it by running  : ")
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on
from ocpp.v16.enums import * # for all imports possible from enumps.py
from ocpp.v16 import call
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    # The very first time a charging station  connects to a Central System, it MUST first send a  BootNotification
    async def send_boot_notification(self): 
        request = call.BootNotificationPayload( charge_point_model="test_hL", charge_point_vendor="Heliox",
                                              )
        response = await self.call(request)
        if response.status ==  RegistrationStatus.accepted:
            print("Connected to central Higher level Charging Managment System (HL-CMS).")
            print(response)
  
    async def send_firmware_notification(self): 
        request = call.FirmwareStatusNotificationPayload(status=FirmwareStatus.downloaded )
        response = await self.call(request)
    
   
    async def send_status_notification(self): 
        request = call.StatusNotificationPayload( connector_id = 1, 
                                                  error_code = ChargePointErrorCode.noError, 
                                                  status = ChargePointStatus.available )
        response = await self.call(request)        
   
    async  def send_heart_beat(self):
        request = call.HeartbeatPayload()
        response =  await self.call(request)
    
    async def send_authorize(self):
        request = call.AuthorizePayload(id_tag = '12345678')
        response = await self.call(request)
        print(response)
        print(response.id_tag_info)
        if response.id_tag_info['status'] ==  AuthorizationStatus.accepted:
            print("Authorization done")
    async def send_meter_values(self):
        meter_values = [
            2,
            "985",
            "MeterValues",
            {
                "connectorId": 1,
                "transactionId": 4866398,
                "meterValue": [
                    {
                        "timestamp": "2020-01-10T09:53:46Z",
                        "sampledValue": [
                            {
                                "value": "3677.200",
                                "context": "Sample.Periodic",
                                "measurand": "Power.Active.Import",
                                "location": "Outlet",
                                "unit": "W"
                            },
                            {
                                "value": "111853.000",
                                "context": "Sample.Periodic",
                                "measurand": "Energy.Active.Import.Register",
                                "location": "Outlet",
                                "unit": "Wh"
                            },
                            {
                                "value": "0.000",
                                "context": "Sample.Periodic",
                                "measurand": "Current.Import",
                                "location": "Outlet",
                                "unit": "A",
                                "phase": "L1"
                            },
                            {
                                "value": "0.000",
                                "context": "Sample.Periodic",
                                "measurand": "Current.Import",
                                "location": "Outlet",
                                "unit": "A",
                                "phase": "L2"
                            },
                            {
                                "value": "16.054",
                                "context": "Sample.Periodic",
                                "measurand": "Current.Import",
                                "location": "Outlet",
                                "unit": "A",
                                "phase": "L3"
                            }
                                    ] # end of sampledValue list 
                    } # end of meter value dictionary
                              ] # end of meter value list. same as above 
        }  # End of "MeterValues dictionary
] # end of meter value list
    
    
    
    
    @on(Action.ClearCache)
    def on_clear_cache(self,**kwargs): 
        return call_result.ClearCachePayload(status=ClearCacheStatus.accepted)
    
    @on(Action.RemoteStartTransaction)
    def on_remote_start_transaction(self,id_tag,**kwargs):        
        return call_result.RemoteStartTransactionPayload(status = RemoteStartStopStatus.accepted)
    
    @on(Action.RemoteStopTransaction)
    def on_remote_stop_transaction(self,transaction_id, **kwargs): 
        return call_result.RemoteStopTransactionPayload(status = RemoteStartStopStatus.accepted)
    
    @on(Action.GetConfiguration)
    def on_get_configuration(self):
        return call_result.GetConfigurationPayload(configuration_key = 
                                                   [{"key":"123","readonly":True,"value":"456"}])
    
        
async def main():  
    Nexxtmove = 'ws://test.nexxtmove.me/b2bevocpp/ocpp-j/heliox_1'
    NexxtGEM = 'ws://10.50.50.237:8080/heliox_1'
    local_server = 'ws://localhost:8080/heliox_1'
    
    # 
    async with websockets.connect(local_server, subprotocols=['ocpp1.6']) as ws:
        cp = ChargePoint('heliox_1', ws) 
        await asyncio.gather(cp.start()    #cp.send_status_notification(), # cp.send_boot_notification(), 
                              #cp.send_firmware_notification()  # 
                              ,cp.send_heart_beat()  
                             #cp.send_authorize()
                             ) 
        # cp.start() refers to a method defined in original ChargePoint class (which is overloaded here)

if __name__ == '__main__':
    try:
        # asyncio.run() is used when running  with Python 3.7 andhigher.
        asyncio.run(main())
        
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()