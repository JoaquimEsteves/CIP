import socket
import sys
import errno

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
tcp_socket.listen(16)
while(True):
    connection, client_address = tcp_socket.accept()
    print "Successfully connected with %s : %d fam" %(client_address[0], client_address[1])

tcp_socket.close()

#it must be possible to wait for incomming messages from the clients




