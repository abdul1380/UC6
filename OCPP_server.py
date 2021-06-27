'''
Created on 15 Jul 2020

https://realpython.com/primer-on-python-decorators/

@author: AbdulMannanRauf
'''
import asyncio
from datetime import datetime
import logging
import json
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import * # for all possible imports in enums.py
from ocpp.v16 import call_result,call



try:
    import websockets
except ModuleNotFoundError:
    print("Please install it by running  : ")
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    
    @on(Action.BootNotification) 
    def on_boot_notitication(self, charge_point_vendor, charge_point_model,**kwargs): 
        return call_result.BootNotificationPayload( current_time=datetime.utcnow().isoformat(), 
                                                    interval=10,status=RegistrationStatus.accepted )
    
    @on(Action.FirmwareStatusNotification)
    def on_fimware_notitication(self,status,**kwargs):
        print(status)
        return call_result.FirmwareStatusNotificationPayload()
    
    @on(Action.StatusNotification)
    def on_status_notitication(self,connector_id,error_code,status,**kwargs): # id means RFID
        print(connector_id)
        return call_result.StatusNotificationPayload()
    
    @on(Action.Heartbeat)
    def on_heart_beat(self,**kwargs):
        return call_result.HeartbeatPayload (current_time=datetime.utcnow().isoformat())
    
    
    @on(Action.Authorize)
    def on_authorize_notitication(self,id_tag,**kwargs):
        return call_result.AuthorizePayload (id_tag_info = {"status":"Accepted"})
    
    @on(Action.MeterValues)
    def on_meter_value(self):
        return call_result.MeterValuesPayload()
    
    
    
    async def get_configuration(self):  # https://github.com/mobilityhouse/ocpp/issues/85
        response  = await self.call(call.GetConfigurationPayload())
        # See section 7.29 in https://github.com/mobilityhouse/ocpp/blob/master/docs/v16/ocpp-1.6.pdf
        for setting in response.configuration_key:  # Setting is a dict with 3 keys: key, value and readonly. 
            print(f"{setting['key']}: {setting['value']}")
    
    async def remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(id_tag ='1')
        response = await self.call (request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction started")
    
    async def remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(id_tag ='1')
        response = await self.call (request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction started")
    
    
    async def remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(transaction_id = 1)
        response = await self.call (request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction stopped")
            
    
    
        


connected = set()
clients = dict()
ping_counter = 0
client_counter  = 0


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance"""
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    try:
        await asyncio.gather(cp.start(), cp.get_configuration(),
                             cp.on_remote_start_transaction()
                             )

        connected.add(websocket)
    except:
        connected.remove(websocket)
        print("charger disconnected")
    
        


async def main():
    server = await websockets.serve( on_connect,  '0.0.0.0', 8080, subprotocols=['ocpp1.6'])
    await server.wait_closed()

if __name__ == '__main__':
    try:
        asyncio.run(main()) #with Python 3.7 and higher.
    except AttributeError:
        # For Python 3.6 a bit more code  to run the main() task on an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    

        