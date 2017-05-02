# !/usr/bin/python
# -*- coding: utf-8 -*-
import settings
import protocols
import socket
from Station import *
from utils import Logger
from thread import start_new_thread

log = Logger(debug=settings.DEBUG)


def request(connection, data):
        """returns the raw response from the host machine"""
        try:
            connection.send(data)
            # Receive data from the socket (max amount is the buffer size).
            data = connection.recv(protocols.buffer_size)
            log.debug("[TCP] Got back > \"{}\".".format(protocols._remove_new_line(data)[:64]))
        # in case of timeout
        except protocols.timeout, msg:
            log.error("[TCP] Request Timeout. {}".format(msg))
            data = "ERR"
        # in case of error
        except protocols.error, msg:
            log.error("[TCP] Something happen when trying to connect to")
            print "error incoming\n\n"
            print str(protocols.error)
            print "error out\n\n"
            data = "ERR"
        finally:
            # Close socket connection
            connection.close()
        return data		


if __name__ == "__main__":
    print "hi"
    #"QC","StorageAndAssembly","Scorbot","AGV","Belt", "RFID"]
    host = socket.gethostbyaddr(socket.gethostname())
    print host
    tcp1 = protocols.TCP(host[0], port=8881)
    tcp2 = protocols.TCP(host[0], port=8882)
    tcp3 = protocols.TCP(host[0], port=8883)
    tcp4 = protocols.TCP(host[0], port=8884)
    tcp5 = protocols.TCP(host[0], port=8885)
    tcp6 = protocols.TCP(host[0], port=8886)

    tcp_cons = [tcp1, tcp2, tcp3, tcp4, tcp5, tcp6]

    Station = {}

    log.info("Waiting connection from the stations!")
    for tcp in tcp_cons:
        details = tcp.run()
        log.info("{} - Connected".format(details[1]))
        Station.update( { details[1] : details[0] } )
    
    log.info("Cool, now that we're all connected let's get to work!")
	
    stage = 0
    
    result = request(Station["Belt"], "[SUP]GOTO STORAGE")
    if result[:-2] == "OK":
        stage = 1
        log.info("hurray")
	
    #etcetcetc

	#tcp_Belt.request("Start")

