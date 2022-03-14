import time
import os
import sys
import sqlite3
from contextlib import closing
import json
import datetime

#------------------------------------------
# SQLite DB
#------------------------------------------
class DatabaseMangment():
    def __init__(self, testing=False, resetDB=False):
        # json dumps
        self.__resultJsonDumps = json.dumps(list(dict()), default=str)
        # list of tuple
        self.__resultListOfTuple = list(tuple())

        if testing:
            self.db_loc = ":memory:"
        else:
            self.db_loc = str(os.path.dirname(os.path.realpath(__file__))) + "/db/mqttlog.db"
            if not os.path.exists(self.db_loc):
                resetDB=True
        if not self.db_loc:
            print("failed to open db")
        self.__connection = None
        self.__establishConnection(resetDB)
        if not testing and resetDB:
            self.__add_default_entries()
         
    def __del__(self):
        self.__connection.commit()
        self.__connection.close()
             
    def __establishConnection(self, resetDB=False):
        if self.__connection:
            self.__connection.commit()
            self.__connection.close()
        self.__connection = None
        try:
            self.__connection = sqlite3.connect(self.db_loc, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread=False)
            # Auto Commit
            # self.__connection.isolation_level = None
            # Log excuted statements by printing it
            # self.__connection.set_trace_callback(print)
            if resetDB:
                self.__resetDB()
            self.__buildDB()
        except sqlite3.Error as e:
            print(e)
            return False
        return True
    
    def resetDBandbuildit(self, resetDB=True, add_default_entries=True):
        return self.__establishConnection(resetDB=resetDB)
        if add_default_entries:
            self.__add_default_entries()
    

    def __resetDB(self):
        for table in ["sensordata", "plant", "profile"]:
            self.__query_executor("DROP TABLE IF EXISTS " + table)

    def __buildDB(self):
        sql_create_profile_table = """ CREATE TABLE IF NOT EXISTS profile (
                                    profileid integer NOT NULL PRIMARY KEY,
                                    profilename text NOT NULL UNIQUE,
                                    threshold interger NOT NULL
                                    )
                                    """
        
        sql_create_plant_table = """ CREATE TABLE IF NOT EXISTS plant (
                                    plantid integer NOT NULL PRIMARY KEY,
                                    plantname text NOT NULL UNIQUE,
                                    profileid interger,
                                    FOREIGN KEY(profileid) REFERENCES profile(profileid) ON DELETE SET NULL
                                    )
                                    """

        sql_create_sensordata_table = """ CREATE TABLE IF NOT EXISTS sensordata (
                                    sensordataid integer NOT NULL PRIMARY KEY,
                                    plantid interger NOT NULL,
                                    soilmoisture interger NOT NULL DEFAULT 0,
                                    temperature interger NOT NULL DEFAULT 0,
                                    humidity interger NOT NULL DEFAULT 0,
                                    datetimestamp timestamp NOT NULL DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW', 'localtime')),
                                    FOREIGN KEY(plantid) REFERENCES plant(plantid) ON DELETE CASCADE
                                    )
                                    """
        if self.__connection:
            self.__query_executor("PRAGMA foreign_keys=1")
            self.__query_executor(sql_create_profile_table)
            self.__query_executor(sql_create_plant_table)
            self.__query_executor(sql_create_sensordata_table)
        else:
            print("Error! cannot create the database without connection.")
            return False
        return True
    
    def __query_executor(self, query, data_tuple=None, get_result=False):
        try:
            with closing(self.__connection.cursor()) as cursor:
                if data_tuple is not None:
                    cursor.execute(query, data_tuple)
                else:
                    cursor.execute(query)
                if get_result:
                    self.__convert_result_to_json(cursor)
        except Exception as e:
            print(e)
            return False
        self.__connection.commit()                 
        return True

    def __convert_result_to_json(self, cursor):
        col_names = [i[0] for i in cursor.description]
        result_set = cursor.fetchall()
        rows_affected = len(result_set)
        if rows_affected < 1:
            self.__resultJsonDumps = json.dumps(list(dict()), default=str)
            self.__resultListOfTuple = list(tuple())
            return True
        jsonDB = []
        jsonDBList = []
        for result in result_set:
            jsonDB.append(dict(zip(col_names, result)))
            jsonDBList.append(result)
        self.__resultJsonDumps = json.dumps(jsonDB, default=str)
        self.__resultListOfTuple = result_set
        return True

    def __add_default_entries(self):
        self.addprofile(profilename="low", threshold=20)
        self.addprofile(profilename="medium", threshold=40)
        self.addprofile(profilename="high", threshold=60)
        self.addplant(profileid=1, plantname="plantone")
        self.addplant(profileid=2, plantname="planttwo")
        self.addplant(profileid=3, plantname="plantthree")
        
    # Table: profile
    #     profileid integer NOT NULL PRIMARY KEY
    #     profilename text NOT NULL UNIQUE
    #     threshold interger NOT NULL DEFAULT 0
    def addprofile(self, profilename, threshold=0):
        sql_query = "INSERT INTO profile (profilename, threshold) values (?,?)"
        data_tuple = (profilename, threshold)
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def updateprofile(self, profileid=None, profilename=None, threshold=None):
        sql_query = None
        data_tuple = None

        if profileid and profilename and threshold:
            sql_query = "UPDATE profile SET threshold=?, profilename=? WHERE profileid=?"
            data_tuple = (threshold, profilename, profileid)
        elif profileid and profilename:
            sql_query = "UPDATE profile SET profilename=? WHERE profileid=?"
            data_tuple = (profilename, profileid)
        elif profileid and threshold:     
            sql_query = "UPDATE profile SET threshold=? WHERE profileid=?"
            data_tuple = (threshold, profileid)
        elif profilename and threshold:
            sql_query = "UPDATE profile SET threshold=? WHERE profilename=?"
            data_tuple = (threshold, profilename)
        else:
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def getprofile(self, profileid=None, profilename=None):
        sql_query = None
        data_tuple = None
        if profileid:     
            sql_query = "SELECT * FROM profile WHERE profileid=?"
            data_tuple = (profileid, )
        elif profilename:
            sql_query = "SELECT * FROM profile WHERE profilename=?"
            data_tuple = (profilename, )
        else:
            sql_query = "SELECT * FROM profile"
        self.__query_executor(sql_query, data_tuple=data_tuple, get_result=True)
        return self.__resultJsonDumps, self.__resultListOfTuple

    def removeprofile(self, profileid=None, profilename=None):
        sql_query = None
        data_tuple = None
        if profileid:     
            sql_query = "DELETE FROM profile WHERE profileid=?"
            data_tuple = (profileid,)
        elif profilename:
            sql_query = "DELETE FROM profile WHERE profilename=?"
            data_tuple = (profilename,)
        else:
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)


    # Table: plant
    #     plantid integer NOT NULL PRIMARY KEY,
    #     plantname text NOT NULL UNIQUE,
    #     profileid interger NOT NULL,
    #     FOREIGN KEY(profileid) REFERENCES profile(profileid) ON DELETE SET NULL
    def addplant(self, profileid, plantname):
        sql_query = "INSERT INTO plant (profileid, plantname) values (?,?)"
        data_tuple = (profileid, plantname)
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def updateplant(self, plantid=None, plantname=None, profileid=None):
        sql_query = None
        data_tuple = None

        if plantid and profileid and plantname:
            sql_query = "UPDATE plant SET profileid=?, plantname=? WHERE plantid=?"
            data_tuple = (profileid, plantname, plantid)
        elif plantid and plantname:
            sql_query = "UPDATE plant SET plantname=? WHERE plantid=?"
            data_tuple = (plantname, plantid)
        elif plantid and profileid:     
            sql_query = "UPDATE plant SET profileid=? WHERE plantid=?"
            data_tuple = (profileid, plantid)
        elif plantname and profileid:
            sql_query = "UPDATE plant SET profileid=? WHERE plantname=?"
            data_tuple = (profileid, plantname)
        else:
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def getplant(self, plantid=None, plantname=None):
        sql_query = None
        data_tuple = None
        if plantid:     
            sql_query = "SELECT * FROM plant WHERE plantid=?"
            data_tuple = (plantid, )
        elif plantname:
            sql_query = "SELECT * FROM plant WHERE plantname=?"
            data_tuple = (plantname, )
        else:
            sql_query = "SELECT * FROM plant"
        self.__query_executor(sql_query, data_tuple=data_tuple, get_result=True)
        return self.__resultJsonDumps, self.__resultListOfTuple

    def removeplant(self, plantid=None, plantname=None):
        sql_query = None
        data_tuple = None
        if plantid:     
            sql_query = "DELETE FROM plant WHERE plantid=?"
            data_tuple = (plantid,)
        elif plantname:
            sql_query = "DELETE FROM plant WHERE plantname=?"
            data_tuple = (plantname,)
        else:
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)


    # Table: sensordata
    #     sensordataid integer NOT NULL PRIMARY KEY,
    #     plantid interger NOT NULL,
    #     soilmoisture interger NOT NULL DEFAULT 0,
    #     temperature interger NOT NULL DEFAULT 0,
    #     humidity interger NOT NULL DEFAULT 0,
    #     datetimestamp timestamp NOT NULL DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW', 'localtime')),
    #     FOREIGN KEY(plantid) REFERENCES plant(plantid) ON DELETE CASCADE
    def addsensordata(self, plantid=None, plantname=None, soilmoisture=0, temperature=0, humidity=0, datetimestamp=datetime.datetime.now()):
        sql_query = None
        data_tuple = None
        if plantid:
            sql_query = "INSERT INTO sensordata (plantid, soilmoisture, temperature, humidity, datetimestamp) values (?,?,?,?,?)"
            data_tuple = (plantid, soilmoisture, temperature, humidity, datetimestamp)
        elif plantname:
            sql_query = "INSERT INTO sensordata (plantid, soilmoisture, temperature, humidity, datetimestamp) SELECT plant.plantid,?,?,?,? FROM plant WHERE plantname=?"
            data_tuple = (soilmoisture, temperature, humidity, datetimestamp, plantname)
        else:
            print("need one of plantid or plantname")
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def getsensordata(self, sensordataid=None, plantid=None, plantname=None, onlylastrecord=False):
        sql_query = None
        data_tuple = None
        if sensordataid:     
            sql_query = "SELECT * FROM sensordata WHERE sensordataid=?"
            data_tuple = (sensordataid, )
        elif plantid:
            sql_query = "SELECT * FROM sensordata WHERE plantid=?"
            data_tuple = (plantid, )
        elif plantname:
            sql_query = "SELECT * FROM sensordata WHERE plantid= (SELECT plant.plantid FROM plant WHERE plantname=?)"
            data_tuple = (plantname, )
        else:
            sql_query = "SELECT * FROM sensordata"
    
        if onlylastrecord:
            sql_query += " ORDER BY sensordataid desc LIMIT 1"

        self.__query_executor(sql_query, data_tuple=data_tuple, get_result=True)
        return self.__resultJsonDumps, self.__resultListOfTuple

    def removesensordata(self, sensordataid=None, plantid=None, plantname=None):
        sql_query = None
        data_tuple = None
        if sensordataid:     
            sql_query = "DELETE FROM sensordata WHERE sensordataid=?"
            data_tuple = (sensordataid,)
        elif plantid:
            sql_query = "DELETE FROM sensordata WHERE plantid=?"
            data_tuple = (plantid,)
        elif plantname:
            sql_query = "DELETE FROM sensordata WHERE plantid= (SELECT plant.plantid FROM plant WHERE plantname=?)"
            data_tuple = (plantname,)
        else:
            return False
        return self.__query_executor(sql_query, data_tuple=data_tuple)

    def logdecodejson(self, topic, jsonpayload):
        jsonData = json.loads(jsonpayload)
        plantid = int(jsonData["plantid"])
        soilmoisture = int(jsonData["soilmoisture"])
        temperature = int(jsonData["temperature"])
        humidity = int(jsonData["humidity"])
        sql_query = "insert into sensordata (plantid, soilmoisture, temperature, humidity) values (?,?,?,?)"
        data_tuple = (plantid, soilmoisture, temperature, humidity)
        return self.__query_executor(sql_query, data_tuple=data_tuple)
