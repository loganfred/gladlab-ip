#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

import os
import glob
import jinja2
import logging
import argparse
import aiohttp
import aiohttp_jinja2 as aj

from logs import log
import postprocess
import webapp
import cache

log.setLevel(logging.INFO)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    cache_parser = subparsers.add_parser('thumbs')
    web_parser = subparsers.add_parser('draw')
    compute_parser = subparsers.add_parser('postprocess')

    cache_parser.add_argument('folder', help='Folder with nd2 files')
    cache_parser.add_argument('-s', '--size', default=512)
    cache_parser.add_argument('-c', '--channel', default=0)

    web_parser.add_argument('folder', help='Folder with nd2 files')
    web_parser.add_argument('-p', '--port', action='store', default=8080)
    web_parser.add_argument('-t', '--tablet', action='store_true', dest='lan')

    compute_parser.add_argument('folder', help='Folder with nd2 files')

    args = parser.parse_args()

    # go ahead and get the list of files and file names
    files = glob.glob(os.path.join(args.folder, '*.nd2'))
    files.sort()
    names = [os.path.basename(f) for f in files]
    listing = zip(names, files)

    if args.command == 'thumbs':
        cache.run(args, listing)
    elif args.command == 'draw':
        webapp.run(args, listing)
    elif args.command == 'postprocess':
        postprocess.run(args, listing)
    else:
        parser.print_usage()




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
