from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from OpenGL.GL import glBindVertexArray

from ...engine.loader import Loader
from ..raw_model import RawModel


class MapLayerModel(RawModel, ABC):

    def __init__(self, vertices: np.ndarray, vertex_count: int, colors: Optional[np.ndarray] = None) -> None:
        super().__init__(vertices, vertex_count)

        self.__colors = colors

    @abstractmethod
    def get_draw_mode(self) -> int:
        pass

    def load_to_vao(self, loader: Loader) -> None:
        super().load_to_vao(loader)

        vao_id = self.vao_id
        glBindVertexArray(vao_id)

        loader.store_data_in_attribute_list(1, self.__colors, dim=1)

        # Unbind VAO
        glBindVertexArray(0)
