import settings
import protocols
from utils import Logger
log = Logger(debug=settings.DEBUG)
from socket import *

if __name__ == "main":
    log.info("Starting server")
    tcp_socket = socket.socket(AF_INET, socket.SOCK_STREAM)
    try:
        client_address = tcp_socket.accept()
        addresses = protocols.request(client_address[0], client_address[1]))