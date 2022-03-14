import time
import os
import sys
import logging
from iotprojects.sql_handler import sql_handler 
from flask import Flask, jsonify, request, Response
import datetime

# init Flask app
app = Flask(__name__)
sqlclient = sql_handler.DatabaseMangment()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(422)
def json_not_found(e):
    return "<h1>422 </h1><p>The resource missing json in body.</p>", 422 

@app.route('/', methods=['GET'])
def home():
    return '''<h1>App is Online</h1>'''


# Table: profile
@app.route('/addprofile', methods=['POST'])
def api_addprofile():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
        
    if "profilename" in data:
        profilename = data["profilename"]
    else:
        return page_not_found(404)
    
    threshold=0
    if "threshold" in data:
        threshold=data["threshold"]

    call = sqlclient.addprofile(profilename=profilename, threshold=threshold)
    return jsonify(success=call)

@app.route('/updateprofile', methods=['PATCH'])
def api_updateprofile():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    profileid = None
    profilename = None
    threshold = None
    
    if "profileid" in data:
        profileid = data["profileid"]
    if "profilename" in data:
        profilename = data["profilename"]
    if "threshold" in data:
        threshold = data["threshold"]
    
    if not profileid and not profilename:
        return page_not_found(404)
    
    call = sqlclient.updateprofile(profileid=profileid, profilename=profilename, threshold=threshold)
    return jsonify(success=call)

@app.route('/getprofile', methods=['GET'])
def api_getprofile():
    data = None
    if(request.args):
        data = request.args
    
    profileid = None
    profilename = None
    if data and "profileid" in data:
        profileid = data["profileid"]
    elif data and "profilename" in data:
        profilename = data["profilename"]

    call, _ = sqlclient.getprofile(profileid=profileid,profilename=profilename)
    return Response(response=call, status=200, mimetype="application/json")
    
@app.route('/removeprofile', methods=['DELETE'])
def api_removeprofile():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    profileid = None
    profilename = None
    
    if "profileid" in data:
        profileid = data["profileid"]
    if "profilename" in data:
        profilename = data["profilename"]
    
    if not profileid and not profilename:
        return page_not_found(404)
        
    call = sqlclient.removeprofile(profileid=profileid, profilename=profilename)
    return jsonify(success=call)


# Table: plant
@app.route('/addplant', methods=['POST'])
def api_addplant():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    if "profileid" in data:
        profileid = data["profileid"]
    if "profilename" in data:
        profilename = data["profilename"]
    
    if not profileid and not profilename: 
        return page_not_found(404)
    
    call = sqlclient.addplant(profileid=profileid, plantname=plantname)
    return jsonify(success=call)

@app.route('/updateplant', methods=['PATCH'])
def api_updateplant():
    
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    plantid = None
    profilename = None
    profileid = None
    
    if "plantid" in data:
        plantid = data["plantid"]
    if "profilename" in data:
        profilename = data["profilename"]
    if "profileid" in data:
        profileid = data["profileid"]
    
    if not plantid and not profilename:
        return page_not_found(404)
    
    call = sqlclient.updateplant(plantid=plantid, profilename=profilename, profileid=profileid)
    return jsonify(success=call)

@app.route('/getplant', methods=['GET'])
def api_getplant():
    data = None
    if(request.args):
        data = request.args
    
    plantid=None 
    plantname=None
    if data and "plantid" in data:
        plantid = data["plantid"]
    if data and "plantname" in data:
        plantname = data["plantname"]

    call, _ = sqlclient.getplant(plantid=plantid, plantname=plantname)
    return Response(response=call, status=200, mimetype="application/json")
  
@app.route('/removeplant', methods=['DELETE'])
def api_removeplant():    
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    plantid = None
    plantname = None
    
    if "plantid" in data:
        plantid = data["plantid"]
    if "plantname" in data:
        plantname = data["plantname"]
    
    if not plantid and not plantname:
        return page_not_found(404)
    
    call = sqlclient.removeplant(plantid=plantid, plantname=plantname)
    return jsonify(success=call)


# Table: sensordata
@app.route('/addsensordata', methods=['POST'])
def api_addsensordata():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    print(data)
    
    plantid=None
    plantname=None
    soilmoisture=0
    temperature=0
    humidity=0
    datetimestamp=datetime.datetime.now()
    
    if "plantid" in data:
        plantid = data["plantid"]
    if "plantname" in data:
        plantname = data["plantname"]
    if "soilmoisture" in data:
        soilmoisture = data["soilmoisture"]
    if "temperature" in data:
        temperature = data["temperature"]
    if "humidity" in data:
        humidity = data["humidity"]
    if "datetimestamp" in data:
        datetimestamp = datetime.datetime.strptime(data["datetimestamp"], '%Y-%m-%d %H:%M:%S.%f')
    
    if not plantid and not plantname: 
        return page_not_found(404)
    
    call = sqlclient.addsensordata(plantid=plantid, plantname=plantname, soilmoisture=soilmoisture, temperature=temperature, humidity=humidity, datetimestamp=datetime.datetime.now())
    return jsonify(success=call)

@app.route('/getsensordata', methods=['GET'])
def api_getsensordata():
    data = None
    if(request.args):
        data = request.args
    
    sensordataid=None 
    plantid=None
    plantname=None
    onlylastrecord=None
    if data and "sensordataid" in data:
        sensordataid = data["sensordataid"]
        call, _ = sqlclient.getprofile(sensordataid=sensordataid)
    if data and "plantid" in data:
        plantid = data["plantid"]
    if data and "plantname" in data:
        plantname = data["plantname"]
    if data and "onlylastrecord" in data:
        onlylastrecord = data["onlylastrecord"]

    call, _  = sqlclient.getsensordata(sensordataid=sensordataid, plantid=plantid, plantname=plantname, onlylastrecord=onlylastrecord)
    return Response(response=call, status=200, mimetype="application/json")

@app.route('/removesensordata', methods=['DELETE'])
def api_removesensordata():
    data = None
    if(request.data):
        data = request.get_json()
    else:
        return json_not_found(422)
    
    sensordataid = None
    plantid = None
    plantname = None
    
    if "sensordataid" in data:
        sensordataid = data["sensordataid"]
    if "plantid" in data:
        plantid = data["plantid"]
    if "plantname" in data:
        plantname = data["plantname"]
    
    if not sensordataid and not plantid and not plantname:
        return page_not_found(404)
    
    call = sqlclient.removesensordata(sensordataid=sensordataid, plantid=plantid, plantname=plantname)
    return jsonify(success=call)


def flask_api_to_db_main(debug=False, expose=False):
    app.config["DEBUG"] = debug
    if expose:
        app.run(host="0.0.0.0")
    else:
        app.run()
    
if __name__ == "__main__":
    try:
        flask_api_to_db_main(debug=False)
    except Exception as e:
        logging.error(str(e))