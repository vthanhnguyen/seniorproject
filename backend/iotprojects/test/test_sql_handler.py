import unittest
import datetime
from iotprojects.sql_handler.sql_handler import *

def get_client():
    sqlclient = DatabaseMangment(testing=True)
    sqlclient.addprofile(profilename="one")
    sqlclient.addprofile(profilename="two", threshold=40)
    sqlclient.addplant(profileid=2, plantname="plantone")
    sqlclient.addplant(profileid=2, plantname="planttwo")
    sqlclient.addplant(profileid=1, plantname="plantthree")
    sqlclient.addsensordata(plantid=1, datetimestamp=datetime.datetime.strptime("2022-02-11 02:51:47.134000", '%Y-%m-%d %H:%M:%S.%f'))
    sqlclient.addsensordata(plantid=1, soilmoisture=6, temperature=9, humidity=69, datetimestamp=datetime.datetime.strptime("2022-02-11 02:51:49.134000", '%Y-%m-%d %H:%M:%S.%f'))
    sqlclient.addsensordata(plantname="planttwo", soilmoisture=4, temperature=6, humidity=46, datetimestamp=datetime.datetime.strptime("2022-02-11 02:52:52.134000", '%Y-%m-%d %H:%M:%S.%f'))
    return sqlclient

class Testsql_handler(unittest.TestCase):
    
    def test_init(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertNotEqual(sqlclient, None)

    def test_addprofile(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)
    
    def test_updateprofile1(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "COOL", "threshold": 20}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        sqlclient.updateprofile(profileid=1, profilename="COOL", threshold=20)
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_updateprofile2(self):
        sqlclient = DatabaseMangment(testing=True)
        sqlclient.addprofile("one", 20)
        sqlclient.addprofile("two", threshold=40)
        data = '[{"profileid": 1, "profilename": "one", "threshold": 20}, {"profileid": 2, "profilename": "Hello", "threshold": 40}]'
        sqlclient.updateprofile(profileid=2, profilename="Hello")
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_updateprofile3(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 55}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        sqlclient.updateprofile(profileid=1, threshold=55)
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_updateprofile4(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 5}]'
        sqlclient.updateprofile(profilename="two", threshold=5)
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)
    
    def test_getprofile(self):
        sqlclient = DatabaseMangment(testing=True)
        data = '[]'
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_getprofile1(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}, {"profileid": 2, "profilename": "two", "threshold": 40}]'
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_getprofile2(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        tempresult, tempresultlist = sqlclient.getprofile(profileid=1)
        self.assertEqual(tempresult, data)

    def test_getprofile3(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        tempresult, tempresultlist = sqlclient.getprofile(profilename="one")
        self.assertEqual(tempresult, data)

    def test_removeprofile(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removeprofile(), False)

    def test_removeprofile1(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removeprofile(profileid=1), True)

    def test_removeprofile2(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        sqlclient.removeprofile(profileid=2)
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    def test_removeprofile3(self):
        sqlclient = get_client()
        data = '[{"profileid": 1, "profilename": "one", "threshold": 0}]'
        sqlclient.removeprofile(profilename="two")
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

    ################################################
    def test_addplant(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)
    
    def test_updateplant1(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "oneplant", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.updateplant(plantid=1, plantname="oneplant", profileid=1)
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_updateplant2(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "twoplant", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.updateplant(plantid=2, plantname="twoplant")
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_updateplant3(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.updateplant(plantid=1, profileid=1)
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_updateplant4(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.updateplant(plantname="plantone", profileid=1)
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)
    
    def test_getplant(self):
        sqlclient = DatabaseMangment(testing=True)
        data = '[]'
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)
                
    def test_getplant1(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 2, "plantname": "planttwo", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_getplant2(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}]'
        tempresult, tempresultlist = sqlclient.getplant(plantid=1)
        self.assertEqual(tempresult, data)

    def test_getplant3(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}]'
        tempresult, tempresultlist = sqlclient.getplant(plantname="plantone")
        self.assertEqual(tempresult, data)

    def test_removeplant(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removeplant(), False)

    def test_removeplant1(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removeplant(plantid=1), True)

    def test_removeplant2(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.removeplant(plantid=2)
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_removeplant3(self):
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.removeplant(plantname="planttwo")
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    ################################################
    def test_addsensordata(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)
    
    def test_getsensordata(self):
        sqlclient = DatabaseMangment(testing=True)
        data = '[]'
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)
                
    def test_getsensordata1(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)

    def test_getsensordata2(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata(sensordataid=1)
        self.assertEqual(tempresult, data)

    def test_getsensordata3(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata(plantid=1)
        self.assertEqual(tempresult, data)

    def test_getsensordata4(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata(plantname="plantone")
        self.assertEqual(tempresult, data)

    def test_getsensordata5(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata(sensordataid=1, onlylastrecord=True)
        self.assertEqual(tempresult, data)

    def test_removesensordata(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removesensordata(), False)

    def test_removesensordata1(self):
        sqlclient = DatabaseMangment(testing=True)
        self.assertEqual(sqlclient.removesensordata(sensordataid=1), True)

    def test_removesensordata2(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
        sqlclient.removesensordata(sensordataid=2)
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)

    def test_removesensordata3(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
        sqlclient.removesensordata(plantid=1)
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)
    
    def test_removesensordata4(self):
        sqlclient = get_client()
        data = '[{"sensordataid": 3, "plantid": 2, "soilmoisture": 4, "temperature": 6, "humidity": 46, "datetimestamp": "2022-02-11 02:52:52.134000"}]'
        sqlclient.removesensordata(plantname="plantone")
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)
    
    def test_logdecodejson(self):
        sqlclient = get_client()
        jsonpayload = '{"plantid":2,"soilmoisture": 45, "temperature": 23, "humidity": 58}'
        sqlclient.logdecodejson(topic="Doesn't matter",jsonpayload=jsonpayload)
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(len(tempresultlist), 4)

    ################################################
    def test_edgecase1(self):
        """
        Case where profileid is deleted from profile table.
            As we don't use "NOT NULL" for plant.profileid it means:
                1. plant.profileid will be set to "Null" after deleteing profile.profileid
                2. profile.profileid can be deleted without Cascading plant entries that contains that profileid.
            Therefore it imporant for devloper to verify plant.profileid referce to existing entry in profile.profileid
            This test case verifies this behavior
        """
        sqlclient = DatabaseMangment(testing=True)
        sqlclient.addprofile("Cool")
        sqlclient.addplant(1, "plantone")
        sqlclient.addplant(None, "planttwo")
        self.assertEqual(sqlclient.removeprofile(profileid=2), True)
        data = '[{"profileid": 1, "profilename": "Cool", "threshold": 0}]'
        tempresult, tempresultlist = sqlclient.getprofile()
        self.assertEqual(tempresult, data)

        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 1}, {"plantid": 2, "plantname": "planttwo", "profileid": null}]'
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

    def test_edgecase2(self):
        """
        case where plantid is deleted from plant table 
            will cascade all entries in sensordata table with that plantid.
            This test case verifies this behavior
        """
        sqlclient = get_client()
        data = '[{"plantid": 1, "plantname": "plantone", "profileid": 2}, {"plantid": 3, "plantname": "plantthree", "profileid": 1}]'
        sqlclient.removeplant(plantid=2)
        tempresult, tempresultlist = sqlclient.getplant()
        self.assertEqual(tempresult, data)

        data = '[{"sensordataid": 1, "plantid": 1, "soilmoisture": 0, "temperature": 0, "humidity": 0, "datetimestamp": "2022-02-11 02:51:47.134000"}, {"sensordataid": 2, "plantid": 1, "soilmoisture": 6, "temperature": 9, "humidity": 69, "datetimestamp": "2022-02-11 02:51:49.134000"}]'
        tempresult, tempresultlist = sqlclient.getsensordata()
        self.assertEqual(tempresult, data)


if __name__ == "__main__":
        unittest.main()
