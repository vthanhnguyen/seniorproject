import unittest
import datetime
from iotprojects.sql_handler.sql_handler import *
from iotprojects.flask_api_to_db.flask_api_to_db import app
import os
import json

class BaseCase(unittest.TestCase):

    def setUp(self):
        self.sqlclient = DatabaseMangment()
        self.sqlclient.resetDBandbuildit(add_default_entries=False)
        self.setDB()
        self.app = app.test_client()
    
    def setDB(self):
        self.sqlclient.addprofile(profilename="one")
        self.sqlclient.addprofile(profilename="two", threshold=40)
        self.sqlclient.addplant(profileid=2, plantname="plantone")
        self.sqlclient.addplant(profileid=2, plantname="planttwo")
        self.sqlclient.addplant(profileid=1, plantname="plantthree")
        self.sqlclient.addsensordata(plantid=1, datetimestamp=datetime.datetime.strptime("2022-02-11 02:51:47.134000", '%Y-%m-%d %H:%M:%S.%f'))
        self.sqlclient.addsensordata(plantid=1, soilmoisture=6, temperature=9, humidity=69, datetimestamp=datetime.datetime.strptime("2022-02-11 02:51:49.134000", '%Y-%m-%d %H:%M:%S.%f'))
        self.sqlclient.addsensordata(plantname="planttwo", soilmoisture=4, temperature=6, humidity=46, datetimestamp=datetime.datetime.strptime("2022-02-11 02:52:52.134000", '%Y-%m-%d %H:%M:%S.%f'))
    
    def tearDown(self):
        self.sqlclient.resetDBandbuildit()

class Testsql_handler(BaseCase):
    
    def check_response(self, url, data):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        tempresult = json.dumps(response.json, default=str)
        self.assertEqual(tempresult, data)

    def test_init(self):
        self.assertNotEqual(self.sqlclient, None)
        response = self.app.get('/getprofile', headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_addprofile(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        self.check_response('/getprofile', data)

    def test_updateprofile1(self):
        data = '[{"profileid": 1, "profilename": "COOL", "threshold": 20}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        payload = {"profileid":1, "profilename":"COOL", "threshold":20}
        response = self.app.patch('/updateprofile', json=payload)
        self.check_response('/getprofile', data)

    def test_updateprofile2(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "Hello", "threshold": 40}]'
        payload = {"profileid":2, "profilename":"Hello"}
        response = self.app.patch('/updateprofile', json=payload)
        self.check_response('/getprofile', data)

    def test_updateprofile3(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 55}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        payload = {"profileid":1, "threshold":55}
        response = self.app.patch('/updateprofile', json=payload)
        self.check_response('/getprofile', data)

    def test_updateprofile4(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 5}]'
        payload = {"profilename":"two", "threshold":5}
        response = self.app.patch('/updateprofile', json=payload)
        self.check_response('/getprofile', data)

    def test_getprofile1(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        self.check_response('/getprofile', data)

    def test_getprofile2(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        payload = {"profileid":1}
        response = self.app.get('/getprofile', json=payload)
        self.assertEqual(response.status_code, 200)
        tempresult = json.dumps(response.json, default=str)
        self.assertEqual(tempresult, data)
        
    def test_getprofile3(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        payload = {"profilename":"one"}
        response = self.app.get('/getprofile', json=payload)
        self.assertEqual(response.status_code, 200)
        tempresult = json.dumps(response.json, default=str)
        self.assertEqual(tempresult, data)

    def test_removeprofile(self):
        response = self.app.delete('/removeprofile')
        self.assertEqual(response.status_code, 422)

    def test_removeprofile1(self):
        payload = {"profileid":1}
        response = self.app.delete('/removeprofile', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_removeprofile2(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        payload = {"profileid":2}
        response = self.app.delete('/removeprofile', json=payload)
        self.assertEqual(response.status_code, 200)
        self.check_response('/getprofile', data)

    def test_removeprofile3(self):
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        payload = {"profilename":"two"}
        response = self.app.delete('/removeprofile', json=payload)
        self.assertEqual(response.status_code, 200)
        self.check_response('/getprofile', data)


    # ################################################
    # def test_addplant(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)
    
    # def test_updateplant1(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "oneplant", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.updateplant(plantid=1, plantname="oneplant", profileid=1)
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_updateplant2(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "twoplant", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.updateplant(plantid=2, plantname="twoplant")
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_updateplant3(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.updateplant(plantid=1, profileid=1)
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_updateplant4(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.updateplant(plantname="plantone", profileid=1)
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)
    
    # def test_getplant(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     data = '[]'
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)
                
    # def test_getplant1(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_getplant2(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}]'
    #     tempresult, tempresultlist = sqlclient.getplant(plantid=1)
    #     self.assertEqual(tempresult, data)

    # def test_getplant3(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}]'
    #     tempresult, tempresultlist = sqlclient.getplant(plantname="plantone")
    #     self.assertEqual(tempresult, data)

    # def test_removeplant(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     self.assertEqual(sqlclient.removeplant(), False)

    # def test_removeplant1(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     self.assertEqual(sqlclient.removeplant(plantid=1), True)

    # def test_removeplant2(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.removeplant(plantid=2)
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_removeplant3(self):
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.removeplant(plantname="planttwo")
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # ################################################
    # def test_addsensordata(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)
    
    # def test_getsensordata(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     data = '[]'
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)
                
    # def test_getsensordata1(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)

    # def test_getsensordata2(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata(sensordataid=1)
    #     self.assertEqual(tempresult, data)

    # def test_getsensordata3(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata(plantid=1)
    #     self.assertEqual(tempresult, data)

    # def test_getsensordata4(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata(plantname="plantone")
    #     self.assertEqual(tempresult, data)

    # def test_getsensordata5(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata(sensordataid=1, onlylastrecord=True)
    #     self.assertEqual(tempresult, data)

    # def test_removesensordata(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     self.assertEqual(sqlclient.removesensordata(), False)

    # def test_removesensordata1(self):
    #     sqlclient = DatabaseMangment(testing=True)
    #     self.assertEqual(sqlclient.removesensordata(sensordataid=1), True)

    # def test_removesensordata2(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
    #     sqlclient.removesensordata(sensordataid=2)
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)

    # def test_removesensordata3(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
    #     sqlclient.removesensordata(plantid=1)
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)
    
    # def test_removesensordata4(self):
    #     sqlclient = get_client()
    #     data = '[{"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
    #     sqlclient.removesensordata(plantname="plantone")
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)
    
    # def test_logdecodejson(self):
    #     sqlclient = get_client()
    #     jsonpayload = '{"plantid":2,"soilmoisture": 45, "temperature": 23, "humidity": 58}'
    #     sqlclient.logdecodejson(topic="Doesn't matter",jsonpayload=jsonpayload)
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(len(tempresultlist), 4)

    # ################################################
    # def test_edgecase1(self):
    #     """
    #     Case where profileid is deleted from profile table.
    #         As we don't use "NOT NULL" for plant.profileid it means:
    #             1. plant.profileid will be set to "Null" after deleteing profile.profileid
    #             2. profile.profileid can be deleted without Cascading plant entries that contains that profileid.
    #         Therefore it imporant for devloper to verify plant.profileid referce to existing entry in profile.profileid
    #         This test case verifies this behavior
    #     """
    #     sqlclient = DatabaseMangment(testing=True)
    #     sqlclient.addprofile("Cool")
    #     sqlclient.addplant(1, "plantone")
    #     sqlclient.addplant(None, "planttwo")
    #     self.assertEqual(sqlclient.removeprofile(profileid=2), True)
    #     data = '[{"profileid": 1, "profilename": "Cool", "threshold": 0}]'
    #     tempresult, tempresultlist = sqlclient.getprofile()
    #     self.assertEqual(tempresult, data)

    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": null}]'
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    # def test_edgecase2(self):
    #     """
    #     case where plantid is deleted from plant table 
    #         will cascade all entries in sensordata table with that plantid.
    #         This test case verifies this behavior
    #     """
    #     sqlclient = get_client()
    #     data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
    #     sqlclient.removeplant(plantid=2)
    #     tempresult, tempresultlist = sqlclient.getplant()
    #     self.assertEqual(tempresult, data)

    #     data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
    #     tempresult, tempresultlist = sqlclient.getsensordata()
    #     self.assertEqual(tempresult, data)


if __name__ == "__main__":
        unittest.main()
