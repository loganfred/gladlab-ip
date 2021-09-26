#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

import numpy as np
from matplotlib import pyplot as plt
from skimage.draw import polygon2mask
from skimage.io import imsave

from image import Image
import events
from args import parser
from logs import log


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
