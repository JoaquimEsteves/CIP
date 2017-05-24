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

Station = {}

class GotoTrashError(Exception):
    def __init__(self, message="Sending the piece to the trash!"):

        # Call the base class constructor with the parameters it needs
        (GotoTrashError, self).__init__(message)

class AbortError(Exception):
    def __init__(self, message="aborting!"):

        # Call the base class constructor with the parameters it needs
        (AbortError, self).__init__(message)


def request(connection, data,OK_message = "OK"):
        """returns the raw response from the host machine"""
        try:
            log.info("Sending: {}".format(data))
            connection.send(data)
            # Receive data from the socket (max amount is the buffer size).
            data = connection.recv(settings.BUFFERSIZE)
            log.debug("[TCP] Got back > \"{}\".".format(data))
        except Exception as e:
            log.error("[TCP] Something happen when trying to connect to")
            print "error incoming\n\n"
            print e
            print "error out\n\n"
            data = "ERR"
            return data
            
        if data != OK_message:
            log.error("data in is different from expected> \"{}\" was expecting \"{}\".".format(data,OK_message))
            raw = raw_input("Would you like to [T]rash, [R]esend or [A]bort?\n")
            if raw == "T" or "t":
                raise GotoTrashError()
            elif raw == "R" or "r":
                return request(connection,data,OK_message)
            elif raw == "A" or "a":
                raise AbortError()
        else:
            return data
    


if __name__ == "__main__":
    print "hi"
    #"QC","StorageAndAssembly","Scorbot","AGV","Belt", "RFID"]
    #host = socket.gethostbyaddr(socket.gethostname())
    #print host
    host = [socket.gethostname()]
    tcp1 = protocols.TCP(host[0], port=8881) #Belt
    # tcp2 = protocols.TCP(host[0], port=8882) #Storage
    # tcp3 = protocols.TCP(host[0], port=8883) #AGV
    # tcp4 = protocols.TCP(host[0], port=8884) #QC
    # tcp5 = protocols.TCP(host[0], port=8885) #RFID
    # tcp6 = protocols.TCP(host[0], port=8886) #Scorbot

    tcp_cons = [tcp1]

    
    
    log.info("Waiting connection from the stations!")
    for tcp in tcp_cons:
        details = tcp.run()
        log.info("{} - Connected".format(details[1]))
        Station.update( { details[1] : details[0] } )
    
    log.info("Cool, now that we're all connected let's get to work!")
	
    try:

        request(Station["Belt"], "GoToStorage", "Done")
        
        log.debug("SLEEPING 5")
        time.sleep(5)
    
        # request(Station["Belt"], "GoToQuaCont", "Done")
        
        # log.debug("SLEEPING 5")
        # time.sleep(5)
       

       
        # request(Station["Belt"], "GoToScorbot", "Done")
        
        # log.debug("SLEEPING 5")
        # time.sleep(5)
        
        
        # request(Station["Belt"], "GoToTrash!!", "Done")
       
        
       
        
        request(Station["StorageAndAssembly"],"STAGE1")
        welcome = request(Station["QC"], "QC3", "message received")
        request(Station["Belt"],"GoToQuaCont",OK_message = "Done")
        log.debug("Waiting on reply from QC")
        result2 = Station["QC"].recv(settings.BUFFERSIZE)
        if result2 != "OK":
            raise GotoTrashError()
        request(Station["Belt"],"GoToStorage","Done")
        request(Station["StorageAndAssembly"],"STAGE2")
        welcome = request(Station["QC"], "QC1", "message received")
        request(Station["Belt"],"GoToQuaCont",OK_message = "Done")
        log.debug("Waiting on reply from QC")
        result2 = Station["QC"].recv(settings.BUFFERSIZE)
        if result2 != "OK":
            raise GotoTrashError()
        request(Station["Belt"],"GoToScorbot","Done")
        request(Station["StorageAndAssembly"],"STAGE3")
        res = request(Station["AGV"], "GOTO SCORBOT")
        log.info("Waiting on AGV")
        request(Station["Scorbot"], "EXTRACT", "OK")
        #Send belt to initial position.
        Station["Belt"].send("GoToStorage")
        
        request(Station["AGV"], "GOTO STORAGE")
        raise AbortError()
    except AbortError:
        try:
            log.info("closing sucessfully, kindoff")
            for sta in Station:
                Station[sta].close()
        except:
            log.error("Complete failure, couldn't even close connections!")
    
    
    except GotoTrashError:
        try:
            request(Station["Belt"], "GoToTrash!!","Done")
            rfidStatus = Station["RFI"].recv(settings.BUFFERSIZE)
            log.error("RFID STATUS - {}".format(rfidStatus))
            
        finally:
            log.info("closing sucessfully, kindoff")
            for sta in Station:
                Station[sta].close()
    except Exception as e:
        log.error("Unknown error {}".format(str(e)))
        