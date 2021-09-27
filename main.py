#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

import os
import glob
import jinja2
import logging
from io import BytesIO
from PIL import Image as PImage
from aiohttp import web
import aiohttp_jinja2 as aj

from image import Image
from logs import log

log.setLevel(logging.INFO)

routes = web.RouteTableDef()
folder = '/Users/loganf/source/gladfelter/FISH_wil'

files = glob.glob(f'{folder}/*.nd2')
files.sort()
names = [os.path.basename(f) for f in files]

@routes.get('/')
@aj.template('start.jinja2')
async def start(request):

    listing = zip(names, files)
    return {'text': 'hello world',
            'listing': listing}

@routes.get('/page')
@aj.template('page.jinja2')
async def page(request):

    listing = zip(names, files)
    return {'text': 'hello world',
            'listing': listing}

@routes.post('/img')
async def image(request):
    data = await request.post()

    f = data.get('file')
    c = int(data.get('channel', 0))
    s = int(data.get('scale', 1))

    with Image(f, channel=c, scale=s) as zstack:

        img = PImage.fromarray(zstack.maxprojection()).convert('L')

        with BytesIO() as buffer:
            img.save(buffer, format='png')

            return web.Response(body=buffer.getvalue(),
                                content_type='image/png')


app = web.Application()
app.add_routes(routes)
aj.setup(app, loader=jinja2.FileSystemLoader('templates'))
web.run_app(app)


'''
import numpy as np
from matplotlib import pyplot as plt
from skimage.draw import polygon2mask
from skimage.io import imsave

from image import Image
import events
from args import parser
from logs import log


@app.route('/')
def start():

    with Image(file) as zstack:

        return render_template('start.html', zstack)

def main(args):

    fig, ax = plt.subplots(1)

    with Image(args.FILE) as zstack:

        proj = zstack.maxprojection()

        img = ax.imshow(proj, cmap='gray')

        lasso = events.LassoManager(ax)

        plt.show()

        for index, vertices in enumerate(lasso.vertices):

            left = int(np.min(vertices[:, 0]))
            right = int(np.max(vertices[:, 0]))
            top = int(np.min(vertices[:, 1]))
            bottom = int(np.max(vertices[:, 1]))

            # transpose so (x, y) -> (rows, cols)
            mask = polygon2mask(proj.shape, vertices).T
            roi = (left, right, bottom, top)

            hypha = zstack.punchMask(mask, roi, crop=True)
            middle = hypha.shape[0] // 2

            log.info(f'hypha {index} has shape {hypha.shape}'
                     f' and dtype {hypha.dtype}')

            log.info(f'saving as hypha_{index}.tiff')

            imsave(f'hypha_{index}.tiff', hypha)


if __name__ == '__main__':

    args = parser.parse_args()
    log.setLevel(args.loglevel)
    main(args)
'''
