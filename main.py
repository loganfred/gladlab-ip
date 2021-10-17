#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

import os
import glob
import jinja2
import logging
import argparse
import aiohttp
import aiohttp_jinja2 as aj

from logs import log
import webapp
import qr

log.setLevel(logging.INFO)


def collectND2Files(folder):
    files = glob.glob(os.path.join(folder, '*.nd2'))
    files.sort()
    names = [os.path.basename(f) for f in files]
    return zip(names, files)


def generateQRCode(port):
    return qr.create_url(port, scale=10)


def main(args):

    QR = generateQRCode(args.port)
    LISTING = collectND2Files(args.folder)
    HOST = '0.0.0.0' if args.lan else 'localhost'
    PORT = args.port

    app = aiohttp.web.Application()
    app['listing'] = LISTING
    app['qrcode'] = QR
    app.add_routes(webapp.routes)
    aj.setup(app, loader=jinja2.FileSystemLoader('templates'))
    aiohttp.web.run_app(app, path=HOST, port=PORT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", help="Folder with nd2 files")
    parser.add_argument("-p", "--port", action="store", default=8080)
    parser.add_argument("-t", "--tablet", action="store_true", dest="lan")

    args = parser.parse_args()
    main(args)



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
