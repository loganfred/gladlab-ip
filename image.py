import os
import logging
import numpy as np
from pims import pipeline
from nd2reader import ND2Reader
from skimage.measure import block_reduce

log = logging.getLogger(__name__)

@pipeline
def resample(frame, factor, **kwargs):
    log.info('pipeline'
             f' frame: {frame.shape}'
             f' factor: {factor}')
    return block_reduce(frame, (factor, factor), **kwargs)

def return_channels(file):

    with ND2Reader(file) as img:

        channels = img.sizes['c']

        return range(channels)

class Image(ND2Reader):

    def __init__(self, file, axis='z', framespec='yx', channel=0, size=None):

        super().__init__(file)

        assert self.sizes['x'] == self.sizes['y'], 'image breaks assumption of 1:1 aspect ratio'

        # specify which subset of the data we're iterating with (pims)
        self.iter_axes = axis
        self.bundle_axes = framespec
        self.default_coords['c'] = channel

        # add a separate thumbs attribute (note: lazy eval)
        if size is not None:
            self.thumbnails = self.compress(size)
        else:
            self.thumbnails = None

    def compress(self, size, func=np.max):

        scale = self.sizes['x'] // size
        log.info(f'compress size: {size} scale: 1/{scale}')
        return resample(self, scale, func=func)

    def mean(self):

        def get_mean(img):
            for frame in img:
                yield frame.mean()

        m = np.array([avg for avg in get_mean(self)]).mean()

        log.info(f'mean is {m}')
        return m


    def maxprojection(self):


        data = self.thumbnails if self.thumbnails else self
        if self.thumbnails:
            log.info(f'Using thumbnails for the max projection')
        else:
            log.info(f'Using full nd2 images for the max projection')

        log.info(f'making max projection of shape {data[0].shape}')

        maxProj = np.zeros(data[0].shape)
        for frame in data:
            maxProj = np.maximum(maxProj, frame, out=maxProj)
        return maxProj

    def punchMask(self, mask, bbox, crop=False, fill=0):
        log.info('clipping images using mask')
        log.info(f'crop is {crop}')
        log.info(f'bbox is {bbox}')

        result = np.where(mask, self, self.mean())

        if crop:
            l, r, t, b = bbox
            return result[:, b:t, l:r]

        else:
            return result
