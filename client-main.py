import os
import sys
import time

import logger.logger as logger

sys.path.insert(1, os.path.abspath("."))

log = logger.Logger(sys.stdout)
log.log("Initialisation...")
