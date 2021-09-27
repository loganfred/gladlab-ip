import logging
import numpy as np
from pims import pipeline
from nd2reader import ND2Reader
from skimage.measure import block_reduce

log = logging.getLogger(__name__)

@pipeline
def resample(frame, factor, **kwargs):
    log.info('using pipeline resample')
    return block_reduce(frame, (factor, factor), **kwargs)

class Image(ND2Reader):

    def __init__(self, file, axis='z', channel=0, scale=1):

        super().__init__(file)

        log.info('initializing image class')
        log.info(f'channel is {channel}')
        log.info(f'axis is {axis}')
        log.info(f'using scale = {scale}')

        self.iter_axes = axis
        self.default_coords['c'] = channel

        # note that pipelines don't modify the image metadata themselves
        self.thumbnails = self.compress(scale) if scale > 1 else None


    def compress(self, scale, func=np.max):
        log.info(f'compressing to thumbnails at 1/{scale} for speed')
        return resample(self, scale, func=func)

    def mean(self):

        def get_mean(img):
            for frame in img:
                yield frame.mean()

        m = np.array([avg for avg in get_mean(self)]).mean()

        log.info(f'mean is {m}')
        return m


    def maxprojection(self):
        log.info(f'making max projection of shape {self[0].shape}')

        data = self.thumbnails if self.thumbnails else self
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
