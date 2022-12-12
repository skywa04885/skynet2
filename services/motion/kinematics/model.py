from dataclasses import dataclass
import numpy as np
import math


def r_x(theta: float) -> np.array:
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, math.cos(theta), - math.sin(theta), 0.0],
        [0.0, math.sin(theta), math.cos(theta), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])


def r_y(theta: float) -> np.array:
    return np.array([
        [math.cos(theta), 0.0, - math.sin(theta), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [- math.sin(theta), 0.0, math.cos(theta), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])


def r_z(theta: float) -> np.array:
    return np.array([
        [math.cos(theta), - math.sin(theta), 0.0, 0.0],
        [math.sin(theta), math.cos(theta), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])


def t(x: float, y: float, z: float) -> np.array:
    return np.array([
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, z],
        [0.0, 0.0, 0.0, 1.0]
    ])


@dataclass
class TorsoParameters:
    origin: np.array
    width: float  # The width of the torso.
    height: float  # The height of the torso.
    pitch: float  # Rotation around the Y axis
    roll: float  # Rotation around the X axis.
    yaw: float  # Rotation around the Z axis.


@dataclass
class LegParameters:
    theta_1: float  # Rotation around the (local) X axis.
    theta_2: float  # Rotation around the (local) Y axis.
    theta_3: float  # Rotation around the (local) Y axis.


class Model:
    def __init__(self, torso_parameters: TorsoParameters) -> None:
        self.torso_parameters = torso_parameters

        self._cached_torso_transformation_matrix = None

        pass

    @property
    def torso_transformation_matrix(self) -> np.array:
        if not self._cached_torso_transformation_matrix:
            m = t(self.torso_parameters.origin[0], self.torso_parameters.origin[1], self.torso_parameters.origin[2])
            m = np.matmul(m, r_z(self.torso_parameters.roll))
            m = np.matmul(m, r_y(self.torso_parameters.pitch))
            m = np.matmul(m, r_x(self.torso_parameters.yaw))
            self._cached_torso_transformation_matrix = m

        return self._cached_torso_transformation_matrix

    @property
    def leg_origin_back_left(self) -> np.array:
        return np.matmul(self.torso_transformation_matrix, np.array([
            self.torso_parameters.height / 2.0,
            - self.torso_parameters.width / 2.0,
            0.0,
            0.0
        ]))

    @property
    def leg_origin_back_right(self) -> np.array:
        return np.matmul(self.torso_transformation_matrix, np.array([
            self.torso_parameters.height / 2.0,
            self.torso_parameters.width / 2.0,
            0.0,
            0.0
        ]))

    @property
    def leg_origin_front_left(self) -> np.array:
        return np.matmul(self.torso_transformation_matrix, np.array([
            - self.torso_parameters.height / 2.0,
            - self.torso_parameters.width / 2.0,
            0.0,
            0.0
        ]))

    @property
    def leg_origin_front_right(self) -> np.array:
        return np.matmul(self.torso_transformation_matrix, np.array([
            - self.torso_parameters.height / 2.0,
            self.torso_parameters.width / 2.0,
            0.0,
            0.0
        ]))


model = Model(torso_parameters=TorsoParameters(
    origin=np.array([0.0, 10.0, 0.0, 0.0]),
    width=20.0,
    height=40.0,
    pitch=math.radians(0.0),
    roll=math.radians(0.0),
    yaw=math.radians(0.0)
))

print(np.around(model.leg_origin_front_right, decimals=2))
