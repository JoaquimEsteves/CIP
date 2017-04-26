import socket
import sys
import errno
import thread
import argparse
from thread import start_new_thread

PORT = 8888
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "socket creating"
server_address = ('localhost', PORT)
print "Starting up on %d port %s server_address" %(PORT, server_address)

try:
    tcp_socket.bind(server_address)
except socket.error, v:
    errorcode = v[0]
    if errorcode == errno.ECONNREFUSED:
        print "I'm sorry fam, but yo connection was refused"
    sys.exit()

print "Socket binding finished"
tcp_socket.listen(16) #CHECK THIS OUT LATER THIS IS SUSPICIOUS AS FUUUUUUUUUUU

def threaded_connection(connection,IP,PORT):
    connection.send("Welcome, at the end of every command press ENTER")
    while (True):
        data = connection.recv(1024)
        print "IP:" + str(IP) + " Port:" + str(PORT) + "Says:" +data
        print "data stuff"
        #if raw_input('A'):
         #   break
        #connection.sendall(data)
        #print "senddata"
    connection.close()

while(True):
    try:
        connection, client_address = tcp_socket.accept()
        print "Successfully connected with %s : %d fam" % (client_address[0], client_address[1])
        #threading starts here
        start_new_thread(threaded_connection, (connection,client_address[0], client_address[1],))
    except KeyboardInterrupt, e:
        # if CTRL+C is pressed, then go for last step
        print "GETTING THE HELL OUT."
        break

tcp_socket.close()

#it must be possible to wait for incomming messages from the clients




