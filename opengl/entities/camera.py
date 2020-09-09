import numpy as np

from .base_objects import BaseObject


class Camera(BaseObject):

    def __init__(self, position: np.ndarray = None, rotation: np.ndarray = None) -> None:
        super().__init__(position, rotation)

    def __str__(self) -> str:
        return f"Camera Position({self.pos_x}, {self.pos_y}, {self.pos_z}) |" \
               f"Rotation({self.rot_x}, {self.rot_y}, {self.rot_z})"
