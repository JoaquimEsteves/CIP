import settings
import protocols
from utils import Logger
log = Logger(debug=settings.DEBUG)
from socket import *

if __name__ == "main":
    log.info("Starting server")
    protocols.run()
    for i in