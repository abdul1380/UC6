from flask import Flask,jsonify,request,json
from flask_restx import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)


State =  { '1' :{
'e_demand' : 0, # in kWh,
'already_provided': 0, # Amps 
'new_calculated': 0, # Amps 
'type _of_connector': ' ', #AC/DC
'type_of_charger': ' ' ,
'current_time' : ' ',
'current_price' : 0, # euro/ kWh / 5min 
'grid_limit' : 0,# -- in A /5 min or 15 min
}
}
  

class UC6(Resource):
    def post(self):
        data1 = {"success": False}
        #if request.method == 'POST': # ensure an opt:request was properly uploaded to our endpoint
        posted_data = request.get_json()
            #data_global = posted_data['username']
        id = int(max(State.keys())) + 1
        id = '%i' % id
        State[id] = {
                    "e_demand": posted_data["e_demand"],
                    "already_provided": posted_data["already_provided"],
                    'new_calculated': 61,
                    "type _of_connector": posted_data["type _of_connector"],
                    "type _of_charger": posted_data["type_of_charger"],
                     "current_time": posted_data["current_time"],
                     "current_price": posted_data["current_price"],
                     "grid_limit": posted_data["grid_limit"],
                                              
                    }
        
        return State[id], 201 # jsonify(posted_data)
    
    def get(self):
        id = int(max(State.keys()))
        id = '%i' % id
        return jsonify(State[id])
        #return jsonify(id)
    
    
api.add_resource(UC6, '/predict')
if __name__=='__main__':
    app.run(debug=True)

