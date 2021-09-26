import sys
import logging

log = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handler.setFormatter(logging.Formatter(fmt))
log.addHandler(handler)

logging.getLogger('matplotlib').setLevel(logging.WARNING)
