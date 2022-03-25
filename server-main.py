import os
import sys

sys.path.insert(1, os.path.abspath("."))

import server.server as server
import logger.logger as logger

log = logger.Logger(sys.stdout)
log.log("Initialisation...")

server_obj = server.Server("192.168.0.35", 20001, log)

server_obj.start()
