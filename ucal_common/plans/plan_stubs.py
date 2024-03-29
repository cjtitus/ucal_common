from bluesky import Msg
from ucal_common.motors import manipulator
from ucal_common.shutters import psh7
from ucal_common.detectors import det_devices, tes
import warnings


def call_obj(obj, method, *args, **kwargs):
    yield Msg("call_obj", obj, *args, method=method, **kwargs)


def update_manipulator_side(side, *args):
    """
    Sides are numbered starting at 1
    """
    yield from call_obj(manipulator.holder, "update_side", side - 1, *args)


def set_exposure(time, extra_dets=[]):
    dets = det_devices + [tes] + extra_dets
    for d in dets:
        try:
            yield from call_obj(d, "set_exposure", time)
        except RuntimeError as ex:
            warnings.warn(repr(ex), RuntimeWarning)


def open_shutter():
    yield from psh7.open()


def close_shutter():
    yield from psh7.close()
