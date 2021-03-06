import os
import sys

sys.path.insert(1, os.path.abspath("."))

import utils.logger as logger

import client.client as client

log = logger.Logger(sys.stdout)
log.log("Initialisation...")

client_obj = client.Client(("localhost", 20001), log)
client_obj.start()
