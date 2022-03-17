import os
import sys
import time

sys.path.insert(1, os.path.abspath("."))

import logger.logger as logger

import client.client as client

log = logger.Logger(sys.stdout)
log.log("Initialisation...")

client_obj = client.Client(("192.168.0.35", 20001), log)
