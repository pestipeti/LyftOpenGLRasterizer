from typing import Optional

import numpy as np

from ..models.raw_model import RawModel
from .entity import Entity


class Agent(Entity):

    def __init__(self, model: RawModel, position: np.ndarray, rotation: Optional[np.ndarray] = None,
                 scale: Optional[np.ndarray] = None, color: Optional[np.ndarray] = None) -> None:
        super().__init__(model, position, rotation, scale)

        self.__color: np.ndarray = color if color is not None else (np.ones((3,), dtype=np.float32) * 0.5)

    @property
    def color(self) -> np.ndarray:
        return self.__color

    @color.setter
    def color(self, color: np.ndarray) -> None:
        self.__color = color
