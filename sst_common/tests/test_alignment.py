# from sst_common.api import *
import pytest
import sst_common
import numpy as np
sst_common.STATION_NAME = "sst_sim"
from sst_common.motors import (samplex, sampley, samplez, sampler,
                               sample_holder, manipulator)
from sst_common.plans.find_edges import (scan_z_medium, find_x_offset,
                                         find_r_offset,
                                         scan_r_medium, scan_r_fine,
                                         scan_r_coarse)
from sst_common.plans.alignment import find_corner_x_r, find_corner_coordinates
from bluesky.plan_stubs import mvr


# need to directly set hardware in fixtures
def test_scan_z_finds_edge(RE, fresh_manipulator):
    z_offset = RE(scan_z_medium()).plan_result
    assert np.isclose(z_offset, 0, 0.05)
    samplez.set(-1)
    z_offset2 = RE(scan_z_medium()).plan_result
    assert np.isclose(z_offset2, 0, 0.05)


def test_find_x_offset(RE, fresh_manipulator):
    samplex.set(3)
    x_offset = RE(find_x_offset()).plan_result
    assert np.isclose(x_offset, 5, 0.05)
    sampler.set(45)
    x_offset = RE(find_x_offset()).plan_result
    # Find diagonal with tolerance of 0.05
    assert np.isclose(x_offset, np.sqrt(50), 0.05)


def test_find_r_offset(RE, fresh_manipulator):
    samplex.set(3)
    sampler.set(1)
    RE(find_x_offset())
    theta = RE(find_r_offset()).plan_result
    assert np.isclose(theta, 0, 0.1)
    sampler.set(10)
    theta = RE(find_r_offset()).plan_result
    assert np.isclose(theta, 0, 0.1)


@pytest.mark.parametrize('n', range(5))
def test_random_offset(RE, random_angle_manipulator, n):
    _, angle = random_angle_manipulator
    samplex.set(3)
    RE(find_x_offset())
    angle2 = RE(find_r_offset()).plan_result
    assert np.isclose(angle, -1*angle2, 0.1)


@pytest.mark.parametrize('angle', [1, 2, 4, 6, 8])
def test_find_corner_x_r(RE, fresh_manipulator, angle):
    sampler.set(angle)
    x, theta = RE(find_corner_x_r()).plan_result
    assert np.isclose(x, 5, 0.1)
    assert np.isclose(theta, 0, 0.1)
    # print(f"theta: {theta}")


def test_corner_coordinates(RE, fresh_manipulator):
    samplex.set(3)
    sampler.set(4)
    x1, y1, r1, r2 = RE(find_corner_coordinates()).plan_result

    assert np.isclose(r1, 0, 0.1)
    assert np.isclose(r2, 90, 0.1)
    assert np.isclose(x1, 5, 0.1)
    assert np.isclose(y1, 5, 0.1)

    sampler.set(87)
    samplex.set(3)
    x1, y1, r1, r2 = RE(find_corner_coordinates()).plan_result

    assert np.isclose(r1, 90, 0.1)
    assert np.isclose(r2, 180, 0.1)
    assert np.isclose(x1, 5, 0.1)
    assert np.isclose(y1, 5, 0.1)


def test_random_corner_coordinates(RE, random_angle_manipulator):
    _, angle = random_angle_manipulator
    samplex.set(3)
    x1, y1, r1, r2 = RE(find_corner_coordinates()).plan_result

    assert np.isclose(r1, -1*angle, 0.1)
    assert np.isclose(r2, 90 - angle, 0.1)
    assert np.isclose(x1, 5, 0.1)
    assert np.isclose(y1, 5, 0.1)

    sampler.set(90)
    samplex.set(3)
    x1, y1, r1, r2 = RE(find_corner_coordinates()).plan_result

    assert np.isclose(r1, 90 - angle, 0.1)
    assert np.isclose(r2, 180 - angle, 0.1)
    assert np.isclose(x1, 5, 0.1)
    assert np.isclose(y1, 5, 0.1)

# Better random tests
# Test actual alignment
# Test/estimate time taken?
