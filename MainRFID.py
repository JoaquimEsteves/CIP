# !/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import protocols
import socket
import traceback
import logging
import time
#from Station import *
from utils import Logger
from thread import start_new_thread

log = Logger(debug=settings.DEBUG)


def request(connection, data):
        """returns the raw response from the host machine"""
        try:
            connection.send(data)
            log.info("Sent: {}".format(data))
            # Receive data from the socket (max amount is the buffer size).
            data = connection.recv(settings.BUFFERSIZE)
            log.debug("[TCP] Got back > \"{}\".".format(data))
        # in case of timeout
        #except timeout, msg:
        #    log.error("[TCP] Request Timeout. {}".format(msg))
        #    data = "ERR"
        # in case of error
        except Exception as e:
            log.error("[TCP] Something happen when trying to connect to")
            print "error incoming\n\n"
            print e
            print "error out\n\n"
            data = "ERR"
        finally:
            # Close socket connection
            #connection.close()
            return data
        return data		


if __name__ == "__main__":
    print "hi"
    #"QC","StorageAndAssembly","Scorbot","AGV","Belt", "RFID"]
    #host = socket.gethostbyaddr(socket.gethostname())
    #print host
    host = [socket.gethostname()]
    # tcp5 = protocols.TCP(host[0], port=8885)
    tcp1 = protocols.TCP(host[0], port=8881)
    tcp2 = protocols.TCP(host[0], port=8884)
    
    tcp_cons = [tcp1,tcp2]

    Station = {}

    log.info("Waiting connection from the stations!")
    for tcp in tcp_cons:
        details = tcp.run()
        log.info("{} - Connected".format(details[1]))
        Station.update( { details[1] : details[0] } )
    
    log.info("Cool, now that we're all connected let's get to work!")
	
    # stage = 0
    try:
        result1 = request(Station["QC"],"QC3")
        log.debug("OKHERE")
        result = request(Station["Belt"], "GoToQuaCont")
        log.info( "{} and {}".format(result1,result))
        data = Station["QC"].recv(settings.BUFFERSIZE)
        log.error("data: {}".format(data))
    finally:
        log.error("result {}".format(result))
        result = request(Station["Belt"], "GoToTrash!!")
        try:
            if result == "OK":
                log.info("closing sucessfully, kindoff")
                for sta in Station:
                    Station[sta].close()
            else:
                log.error("bad close")
                for sta in Station:
                    Station[sta].close()
        finally:
            log.error("Complete failure, couldn't even close connections!")