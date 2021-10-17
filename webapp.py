#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

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

    with Image(f, channel=c, size=s) as zstack:

        # copy so that changes can be made for non-serializable objects
        metadata = dict(zstack.metadata)

        if metadata.get('date'):
            metadata['date'] = metadata['date'].strftime('%m%d%Y, %H:%M:%S')

        metadata.pop('z_levels')
        metadata.update({'sizes': zstack.sizes})

        img = PImage.fromarray(zstack.maxprojection()).convert('L')
        width, height = img.size
        res = f'{width}x{height}'

        with BytesIO() as buffer:
            img.save(buffer, format='png')

            enc = base64.b64encode(buffer.getvalue())
            res = { 'file': os.path.basename(f),
                    'abspath': f,
                    'resolution': res,
                    'channel': c,
                    'size': s,
                    'meta': metadata,
                    'image': enc.decode('utf-8')}
            return web.json_response(res)
