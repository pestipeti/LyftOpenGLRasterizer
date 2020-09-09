from typing import Optional

import numpy as np

from ..models import RawModel
from ..utils import create_transformation_matrix
from .base_objects import ScalableBaseObject


class Entity(ScalableBaseObject):

    def __init__(self, model: RawModel, position: np.ndarray, rotation: Optional[np.ndarray] = None,
                 scale: Optional[np.ndarray] = None) -> None:
        super().__init__(position, rotation, scale)

        self.__model: RawModel = model

        # TODO: We should reset this if pos/rot/scale changes.
        self.__transformation_matrix = create_transformation_matrix(self.position, self.rotation, self.scale)

    def move(self, dx: float, dy: float, dz: float):
        self.pos_x += dx
        self.pos_y += dy
        self.pos_z += dz

    def rotate(self, rx: float, ry: float, rz: float):
        self.rot_x += rx
        self.rot_y += ry
        self.rot_z += rz

    @property
    def transformation_matrix(self) -> np.ndarray:
        if self.__transformation_matrix is None:
            self.__transformation_matrix = create_transformation_matrix(self.position, self.rotation, self.scale)

        return self.__transformation_matrix

    @property
    def model(self) -> RawModel:
        return self.__model
    
    @model.setter
    def model(self, model) -> None:
        self.__model = model

    def __str__(self) -> str:
        return f"Entity Position({self.pos_x}, {self.pos_y}, {self.pos_z}) | Rotation({self.rot_x}, {self.rot_y}," \
               f"{self.rot_z}) | Scale({self.scale_x}, {self.scale_y}, {self.scale_z})"
