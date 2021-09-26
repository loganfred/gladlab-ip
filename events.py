import logging
from matplotlib import pyplot as plt
from matplotlib import path as mpath
from matplotlib import patches as mpatches
from matplotlib.widgets import LassoSelector
from matplotlib.widgets import Button
from skimage.draw import polygon2mask
import numpy as np

log = logging.getLogger(__name__)


class LassoManager:
    def __init__(self, ax):

        log.info(f'initializing lasso manager')

        self.axes = ax
        self.canvas = ax.figure.canvas
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)

        self.vertices = []

    def callback(self, verts):

        log.info('lasso callback triggered')

        path = mpath.Path(verts)
        patch = mpatches.PathPatch(path,
                                   fill=False,
                                   edgecolor='xkcd:white',
                                   alpha=1,
                                   hatch='//')

        self.axes.add_patch(patch)
        self.vertices.append(path.vertices)

        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso

    def on_press(self, event):

        log.info(f'lasso event triggered: {event}')

        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        self.lasso = LassoSelector(event.inaxes,
                                   self.callback,
                                   lineprops=dict(color='xkcd:yellow',
                                                  linestyle=':'))
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)


class ColorPicker:

    def __init__(self, ax):

        log.info(f'initializing color picker')

        self.axes = ax
        self.canvas = ax.figure.canvas
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)

        self.values = []

    def on_press(self, event):

        log.info(f'picker event triggered: {event}')

        self.values = event.xdata, event.ydata
