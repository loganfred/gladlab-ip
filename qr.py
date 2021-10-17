import logging
import pyqrcode
import socket

log = logging.getLogger(__name__)

def create_url(port, scale=10):

    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    ipaddr =  socket.gethostbyname(socket.gethostname())

    log.info(f'making QR code for ip addr "{ipaddr}:{port}"')
    qrcode = pyqrcode.create(f'http://{ipaddr}:{port}')
    return f'data:image/png;base64, ' + qrcode.png_as_base64_str(scale=scale)
