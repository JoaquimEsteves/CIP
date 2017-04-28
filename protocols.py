#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import settings
from socket import *
from utils import Logger
log = Logger(debug=settings.DEBUG)

class Protocol(object):

    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE, max_connections=1):
        self.host = host
        self.port = int(port)
        self.buffer_size = buffer_size
        self.max_connections = max_connections

    def _remove_new_line(self, message):
        """if exists, removes \n from the end of the message"""
        if message.endswith('\n'):
            return message[:-1]
        return message

class TCP(Protocol):
    """Class to wrap all TCP interactions between client and server"""
    def __init__(self, host, port=settings.DEFAULT_PORT, m_connections=1):
        super(TCP, self).__init__(host, port, buffer_size=settings.BUFFERSIZE, max_connections = m_connections)
        self.connections = []

    def requestStation(self, station , data):
        """makes tcp socket connection to host and port machine
        returns the raw response from the host machine"""
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_STREAM)
        # Set the value of the given socket option (see the Unix manual page setsockopt(2)).
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        try:
            # Connect to a remote socket at address of the station.
            sock.connect((station.host, station.port))
            # define timout to settings.TIMEOUT_DELAY
            sock.settimeout(settings.TIMEOUT_DELAY)
            log.debug("[TCP] Sending request to {}:{} > \"{}\".".format(self.host, self.port, self._remove_new_line(data)[:64]))
            # Send data to the socket.
            sock.sendall(data)
            # Receive data from the socket (max amount is the buffer size).
            data = sock.recv(self.buffer_size)
            log.debug("[TCP] Got back > \"{}\".".format(self._remove_new_line(data)[:64]))
        # in case of timeout
        except timeout, msg:
            log.error("[TCP] Request Timeout. {}".format(msg))
            data = "ERR"
        # in case of error
        except error, msg:
            log.error("[TCP] Something happen when trying to connect to {}:{}. Error: {}".format(self.host, self.port, msg))
            data = "ERR"
        finally:
            # Close socket connection
            sock.close()
        data = self._remove_new_line(data)
        return data

    def request(self, connection, data):
        """makes tcp socket connection to host and port machine
        returns the raw response from the host machine"""
        try:
            
            #log.debug("[TCP] Sending request to {}:{} > \"{}\".".format(ip, port, self._remove_new_line(data)[:64]))
            # Send data to the socket.
            #print "hi?"
            connection.send(data)
            # Receive data from the socket (max amount is the buffer size).
            data = connection.recv(self.buffer_size)
            print 1
            log.debug("[TCP] Got back > \"{}\".".format(self._remove_new_line(data)[:64]))
        # in case of timeout
        except timeout, msg:
            log.error("[TCP] Request Timeout. {}".format(msg))
            data = "ERR"
        # in case of error
        except error, msg:
            log.error("[TCP] Something happen when trying to connect to {}:{}. Error: {}".format(ip, port, msg))
            print "error incoming\n\n"
            print str(error)
            print "error out\n\n"
            data = "ERR"
        finally:
            # Close socket connection
            connection.close()
        data = self._remove_new_line(data)
        return data		

    def run(self, handler=None):
        """TCP server. TRS runs this server"""
        try:
            # Create a new socket using the given address family, socket type and protocol number
            sock = socket(AF_INET, SOCK_STREAM)
        except error, msg:
            log.error(msg)
            sock.close()
            raise error
        try:
            # Bind socket to local host and port
            sock.bind((self.host, self.port))
            # Listen for connections made to the socket.
            sock.listen(self.max_connections)
        except error , msg:
            log.error(msg)
            sock.close()
            raise error

        log.info("TCP Server is ready for connection on [{}:{}].".format(self.host, self.port))
		
        while True:
            # Accept a connection.
            print "please"
            connection, client_address = sock.accept()
            # Get connection HostIP and HostPORT
            print "pretty please"
            addr_ip, addr_port = client_address
            try:
                #a = self.request(connection,"hi_please receive this!")
                #print a
                #MONSTERS
                data = "WhoAreYou"
                connection.send(data)
            # Receive data from the socket (max amount is the buffer size).
                data = ""
                data_connection = connection.recv(self.buffer_size)
                #Keep receiving until I find a \n!
                while data_connection[-1] != "\n":
                    data += data_connection
                    log.debug("Received {} bytes".format(len(data)))
                    data_connection = connection.recv(self.buffer_size)
                data += data_connection
                log.debug("[TCP] Got back > \"{}\".".format(data[:-2]))
                if data[:-2] not in settings.acceptable_IDs:
                    connection.send("I DON'T KNOW YOU!\n")
                    connection.close()
                else:
                    connection.send("Welcome to the fam, fam!\n")
                    station_name = data
					#WE GUCCI
					#handler.DOSHIT(connection,station_name)
                
           # in case of timeout
            except timeout, msg:
                log.error("[TCP] Request Timeout. {}".format(msg))
                data = "ERR"
                # in case of error
            except error, msg:
                log.error("[TCP] Something happen when trying to connect to {}:{}. Error: {}".format(addr_ip, addr_port, msg))
                print "error incoming\n\n"
                print str(error)
                print "error out\n\n"
                data = "ERR"

		
