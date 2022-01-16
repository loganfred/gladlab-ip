import os
import json
import logging
import numpy as np
from skimage.io import imsave
from skimage.draw import polygon2mask

from image import Image
from image import return_channels

log = logging.getLogger(__name__)


def run(args):

    log.info(f'loading data from {args.file}')
    data = json.load(open(args.file))

    lookup = {}

    for index, d in enumerate(data):

        file = d.get('file')
        vertices = np.array(d.get('vert'))
        abspath = d.get('abspath')

        if args.all_channels:
            channels = return_channels(abspath)
        else:
            channels = [d.get('channel')]

        draw_size = d.get('size')
        actual_size = [d.get('meta').get('height'), d.get('meta').get('width')]
        x, y = actual_size

        log.info(f'loading file "{file}"')

        outputs = []

        x_scale, y_scale = map(lambda i: i // draw_size, actual_size)
        log.info(f'Scaling x by {x_scale} ({x} // {draw_size})')
        log.info(f'Scaling y by {y_scale} ({y} // {draw_size})')

        vertices[:, 0] *= x_scale
        vertices[:, 1] *= y_scale

        left = int(np.min(vertices[:, 0]))
        right = int(np.max(vertices[:, 0]))
        top = int(np.min(vertices[:, 1]))
        bottom = int(np.max(vertices[:, 1]))

        for channel in channels:

            with Image(abspath, channel=channel) as zstack:

                # transpose so (x, y) -> (rows, cols)
                mask = polygon2mask(zstack[0].shape, vertices).T
                roi = (left, right, bottom, top)

                hypha = zstack.punchMask(mask, roi, crop=True)
                middle = hypha.shape[0] // 2

                log.info(f'hypha has shape {hypha.shape}'
                         f' and dtype {hypha.dtype}')

                name = f'hypha_{index}_c{channel}.tiff'

                log.info(f'saving file as {name}')

                fout = os.path.join(args.dest, name)

                outputs.append(name)
                imsave(fout, hypha)

        lookup[file] = outputs

    mpath = os.path.join(args.dest, 'manifest.json')
    log.info(f'saving manifest as {mpath}')

    with open(mpath, 'w+') as j:
        json.dump(lookup, j)
