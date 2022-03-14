import paho.mqtt.client as mqtt
from random import randint
import time
import json
import unittest
from iotprojects.sql_handler import sql_handler
from iotprojects.mqtt_to_db_client import mqtt_to_db_client
import threading

DEFAULT_MQTT_SERVER = "127.0.0.1"
DEFAULT_MQTT_PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)

def clientCode(data = dict(), server=DEFAULT_MQTT_SERVER, port=DEFAULT_MQTT_PORT):
    time.sleep(3)
    client = mqtt.Client("project_test_user_client")
    client.on_connect=on_connect
    client.username_pw_set(username="testmqtttodbclient", password="passwordtestmqtttodbclient")
    client.connect(server,port)
    client.loop_start()

    randNumber = randint(1,3)
    data["plantid"] = randNumber
    data["soilmoisture"] = randint(0,100)
    data["temperature"] = randint(0,100)
    data["humidity"] = randint(0,100)
    
    jsondata = json.dumps(data, default=str)

    client.publish(str(randNumber), jsondata, qos=0)
    # print("Just published: topic:" + str(randNumber)+ " Message:" + jsondata)
    client.loop_stop()
    client.disconnect()
    return data

class Testsql_handler(unittest.TestCase):
    
    def test_init(self):
        sqlclient = sql_handler.DatabaseMangment(testing=True)
        self.assertNotEqual(sqlclient, None)
    
    def test_one(self):
        data = dict()
        server = DEFAULT_MQTT_SERVER
        t = threading.Thread(target=clientCode, args=(data, server), daemon=True)
        t.start()
        mqtt_to_db_client.mqtt_to_db_client_main(server=server, keepalive=5, resetDB=True, loglevel=50)
        t.join()

        sqlclient = sql_handler.DatabaseMangment()
        tempresult, tempresultlist = sqlclient.getsensordata(onlylastrecord=True)
        tempjsonresult = json.loads(tempresult)
        
        self.assertEqual(tempjsonresult[0]["plantid"], data.get("plantid"))
        self.assertEqual(tempjsonresult[0]["soilmoisture"], data.get("soilmoisture"))
        self.assertEqual(tempjsonresult[0]["temperature"], data.get("temperature"))
        self.assertEqual(tempjsonresult[0]["humidity"], data.get("humidity"))

if __name__ == "__main__":
    unittest.main()