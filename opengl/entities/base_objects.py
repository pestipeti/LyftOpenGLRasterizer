from abc import ABC
from typing import Optional

import numpy as np

AXIS_X = 0
AXIS_Y = 1
AXIS_Z = 2


class BaseObject(ABC):

    def __init__(self, position: Optional[np.ndarray] = None, rotation: Optional[np.ndarray] = None) -> None:
        super().__init__()

        self.__position: np.ndarray = position if position is not None else np.zeros((3, ), dtype=np.float32)
        self.__rotation: np.ndarray = rotation if rotation is not None else np.zeros((3, ), dtype=np.float32)

    @property
    def position(self) -> np.ndarray:
        return self.__position

    @position.setter
    def position(self, position: np.ndarray) -> None:
        self.__position = position

    @property
    def rotation(self) -> np.ndarray:
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation: np.ndarray) -> None:
        self.__rotation = rotation

    @property
    def pos_x(self) -> float:
        return self.__position[AXIS_X]

    @pos_x.setter
    def pos_x(self, x: float) -> None:
        self.__position[AXIS_X] = x

    @property
    def pos_y(self) -> float:
        return self.__position[AXIS_Y]

    @pos_y.setter
    def pos_y(self, y: float) -> None:
        self.__position[AXIS_Y] = y

    @property
    def pos_z(self) -> float:
        return self.__position[AXIS_Z]

    @pos_z.setter
    def pos_z(self, z: float) -> None:
        self.__position[AXIS_Z] = z

    @property
    def rot_x(self) -> float:
        return self.__rotation[AXIS_X]

    @rot_x.setter
    def rot_x(self, rot_x: float) -> None:
        self.__rotation[AXIS_X] = rot_x

    @property
    def rot_y(self) -> float:
        return self.__rotation[AXIS_Y]

    @rot_y.setter
    def rot_y(self, rot_y: float) -> None:
        self.__rotation[AXIS_Y] = rot_y

    @property
    def rot_z(self) -> float:
        return self.__rotation[AXIS_Z]

    @rot_z.setter
    def rot_z(self, rot_z: float) -> None:
        self.__rotation[AXIS_Z] = rot_z


class ScalableBaseObject(BaseObject, ABC):

    def __init__(self, position: Optional[np.ndarray] = None, rotation: Optional[np.ndarray] = None,
                 scale: Optional[np.ndarray] = None) -> None:
        super().__init__(position, rotation)

        self.__scale: np.ndarray = scale if scale is not None else np.ones((3,), dtype=np.float32)

    @property
    def scale(self) -> np.ndarray:
        return self.__scale

    @scale.setter
    def scale(self, scale: np.ndarray) -> None:
        self.__scale = scale

    @property
    def scale_x(self) -> float:
        return self.__scale[AXIS_X]
    
    @scale_x.setter
    def scale_x(self, scale: float) -> None:
        self.__scale[AXIS_X] = scale

    @property
    def scale_y(self) -> float:
        return self.__scale[AXIS_Y]

    @scale_y.setter
    def scale_y(self, scale: float) -> None:
        self.__scale[AXIS_Y] = scale

    @property
    def scale_z(self) -> float:
        return self.__scale[AXIS_Z]

    @scale_z.setter
    def scale_z(self, scale: float) -> None:
        self.__scale[AXIS_Z] = scale
