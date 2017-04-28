import settings
import protocols
from utils import Logger
log = Logger(debug=settings.DEBUG)
from socket import *



#create 6 sockets, main handles each
#main handles the procedure (1st roleer,qc etc...)
#main states host and port
#how do we call each station
if __name__ == "main":
    log.info("Starting server")
    protocols.run()
    for i in