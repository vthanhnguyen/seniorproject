import paho.mqtt.client as mqtt
import time
import os
import sys
from iotprojects.sql_handler import sql_handler 
import signal
import optparse
import logging


DEFAULT_MQTT_SERVER = "127.0.0.1"
DEFAULT_MQTT_PORT = 1883
DEFAULT_TOPIC = "#"
DEFAULT_USERNAME = "mqtttodbclient"
DEFAULT_PASSWORD = "passwordmqtttodbclient"

class GracefulKiller:
	def __init__(self):
		self.kill_now = False
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
 
	def exit_gracefully(self, signum, frame):
		self.kill_now = True

#------------------------------------------
# MQTT
#------------------------------------------

def on_connect(client, userdata, flags, rc):
    msg = "Connected with result code: %i"    
    if (rc):
        userdata['logger'].error(msg, rc)
    else:
        userdata['logger'].info(msg, rc)
    client.subscribe("#", qos=2)

def on_message(client, userdata, message):
    userdata['logger'].debug("received message: Topic: %s Message: %s", str(message.topic), str(message.payload.decode("utf-8")))
    userdata['sqlclient'].logdecodejson(str(message.topic), str(message.payload.decode("utf-8")))

def mqtt_to_db_client_main(server=DEFAULT_MQTT_SERVER, port=DEFAULT_MQTT_PORT, keepalive=None, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD, getLogger="mqtttodbclientlogger", resetDB=False, verbose=False, loglevel=20):

    # init logging
    if (verbose):
        loglevel = logging.DEBUG
    
    logger = logging.getLogger(getLogger)
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s %(filename)s [%(levelname)s] %(funcName)s: %(message)s')
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # add killer
    killer = GracefulKiller()

    sqlclient = sql_handler.DatabaseMangment(resetDB=resetDB)
    client_userdata={"sqlclient":sqlclient, "logger":logger}
    
    client = mqtt.Client("mqtt_to_db_client",userdata=client_userdata)
    client.on_connect=on_connect
    client.on_message=on_message

    # check username and password
    logger.debug("username: %s" ,username)
    if (len(username) > 0):
        if (len(password) == 0):
            raise ValueError("please do not use username without password")
        client.username_pw_set(username, password)

    logger.debug("server: %s" ,server)
    logger.debug("port: %i", port)
    client.connect(server, port)

    client.loop_start()
    if keepalive:
        logger.info("start program loop for: %s", str(keepalive))
        time.sleep(keepalive)
    else:
        # forever loop
        try:
            logger.info("start program Forever loop")

            while (1):
                time.sleep(0.1)
            
                if (killer.kill_now):
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            logger.info("exit program loop")
    
    client.loop_stop()
    client.disconnect()
    del sqlclient 


def main():
    parser = optparse.OptionParser(
        usage = "%prog [options]",
        description = "MQTT to DB client Application",
        version="%prog 0.1a"
    )

    group = optparse.OptionGroup(parser, "MQTT settings")
    group.add_option("-s", "--server",
        dest = "server",
        action = "store",
        type = "string",
        help = "mqtt server, default %default",
        default = DEFAULT_MQTT_SERVER
    )
    group.add_option("--port",
        dest = "port",
        action = "store",
        type = "int",
        help = "mqtt server port, default %default",
        default = DEFAULT_MQTT_PORT
    )
    group.add_option("-k", "--keepalive",
        dest = "keepalive",
        action = "store",
        type = "int",
        help = "keepalive option for mqtt server, default %default",
        default = None
    )
    group.add_option("-u", "--username",
        dest = "username",
        action = "store",
        type = "string",
        help = "connection username",
        default = DEFAULT_USERNAME
    )
    group.add_option("-p", "--password",
        dest = "password",
        action = "store",
        type = "string",
        help = "connection password",
        default = DEFAULT_PASSWORD
    )
    group.add_option("-r", "--resetdb",
        dest = "resetdb",
        action = "store_true",
        help = "Reset sqlite DB",
        default = False
    )
    parser.add_option_group(group)

    group = optparse.OptionGroup(parser, "Basic settings")
    group.add_option("-l", "--loglevel",
        dest = "loglevel",
        action = "store",
        type = 'int',
        help = str(logging.CRITICAL) + ": critical  " + str(logging.ERROR) + ": error  " + str(logging.WARNING) + ": warning  " + str(logging.INFO) + ":info  " + str(logging.DEBUG) + ":debug",
        default = logging.INFO
    )
    group.add_option("-v", "--verbose",
        dest = "verbose",
        action = "store_true",
        help = "show debug messages (overrites loglevel to debug)",
        default = False
    )
    parser.add_option_group(group)

    # parse options
    (options, _) = parser.parse_args()

    mqtt_to_db_client_main(server=options.server, port=options.port, keepalive=options.keepalive, username=options.username, password=options.password, resetDB=options.resetdb, verbose=options.verbose, loglevel = int(options.loglevel))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(str(e))