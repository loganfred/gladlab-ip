import os
import glob
import jinja2
import logging
import base64
from io import BytesIO
from PIL import Image as PImage
from aiohttp import web
import aiohttp_jinja2 as aj
import pprint

import qr
import cache
from image import Image

logging.getLogger(__name__)

routes = web.RouteTableDef()
routes.static('/static', 'static')

@routes.get('/')
@aj.template('start.jinja2')
async def start(request):

    listing = request.app['listing']
    return {'listing': listing, 'qrcode': request.app['qrcode']}

@routes.post('/api/img')
async def image(request):
    data = await request.post()

    f = data.get('file')
    c = int(data.get('channel', 0))
    s = int(data.get('size'))  # check None case here

    return web.json_response(cache.get(f, c, s))

def run(args, listing):

    app = web.Application()
    app['listing'] = listing
    app['qrcode'] = qr.create_url(args.port, scale=10)
    app.add_routes(routes)
    aj.setup(app, loader=jinja2.FileSystemLoader('templates'))
    web.run_app(app,
                path='0.0.0.0' if args.lan else 'localhost',
                port=args.port)
