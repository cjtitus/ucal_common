
from bluesky.utils import PersistentDict
from bluesky.plan_stubs import mv, mvr, abs_set
# startup sequence for beamline
import ucal_common.motors as ucal_motors
import ucal_common.mirrors as ucal_mirrors
import ucal_common.shutters as ucal_shutters
import ucal_common.valves as ucal_valves

# convenience imports
from ucal_common.shutters import psh10, psh7
from ucal_common.mirrors import mir1, mir3, mir4
from ucal_common.detectors import (ucal_i400, dm7_i400, tes, i0, sc,
                                   ref, basic_dets, det_devices)
from ucal_common.motors import (manipx, manipy, manipz, manipr, tesz,
                                manipulator, eslit)
from ucal_hw.energy import en
from ucal_common.sampleholder import sampleholder
from ucal_common.plans.find_edges import find_z_offset, find_x_offset, find_x, find_z
from ucal_common.plans.multimesh import set_multimesh
from ucal_common.plans.plan_stubs import set_exposure
from ucal_common.plans.samples import (load_samples, set_side, set_sample,
                                       set_sample_center, set_sample_edge,
                                       sample_move, load_standard_two_sided_bar,
                                       load_standard_four_sided_bar,
                                       load_sample_dict)
from ucal_common.plans.scans import *
from ucal_common.plans.scan_base import tes_calibrate, tes_take_noise, tes_gscan, tes_count, tes_scan
from ucal_common.run_engine import RE
from ucal_common.configuration import print_config_info, beamline_config

# Motor aliases
energy = en.energy

print_config_info()
RE(set_exposure(1.0))
