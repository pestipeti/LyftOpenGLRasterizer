from typing import Optional

import numpy as np
from OpenGL.GL import GL_TRIANGLES

from .layer_model import MapLayerModel


class CrosswalkModel(MapLayerModel):

    def __init__(self, vertices: np.ndarray, vertex_count: int, colors: Optional[np.ndarray] = None) -> None:
        super().__init__(vertices, vertex_count, colors)

    def get_draw_mode(self) -> int:
        return GL_TRIANGLES
