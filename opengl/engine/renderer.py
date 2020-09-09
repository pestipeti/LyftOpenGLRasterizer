import math
from typing import Dict, List, Tuple, Union

import numpy as np
from OpenGL.GL import (GL_BACK, GL_BLEND, GL_COLOR_BUFFER_BIT, GL_CULL_FACE,
                       GL_DEPTH_BUFFER_BIT, GL_NEVER, glClear, glClearColor,
                       glCullFace, glDepthFunc, glDisable, glEnable)

from ..engine.renderers import AbstractRenderer
from ..entities import Camera, Entity
from ..models.map.layer_model import MapLayerModel

FOV = 100
NEAR_PLANE = -10
FAR_PLANE = 10


# noinspection PyMethodMayBeStatic
class Renderer:
    """
    Handles model rendering to the screen.
    """

    def __init__(self, display_width: int, display_height: int, camera: Camera,
                 pixel_size: float = 0.5, projection: str = '3d') -> None:
        super().__init__()

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        # I haven't implemented yet
        self.__projection: str = projection
        self.__camera: Camera = camera

        self.__renderers: Dict[str, AbstractRenderer] = {}
        self.__projection_matrix = self.__create_orthographic_projection_matrix(
            display_width, display_height, pixel_size)
        # self.__projection_matrix = self.__create_perspective_projection_matrix(display_width, display_height)

    def add_renderer(self, renderer_name: str, renderer: AbstractRenderer):
        renderer.shader.start()
        renderer.shader.load_projection_matrix(self.__projection_matrix)
        renderer.shader.stop()
        self.__renderers[renderer_name] = renderer

    def prepare(self) -> None:
        """
        Clears the screen before rendering the next frame.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_BLEND)
        # glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_NEVER)
        # glEnable(GL_POLYGON_OFFSET_FILL)
        # glDepthMask(GL_TRUE)

    def render(self, renderers: List[Tuple[str, List[Union[Entity, MapLayerModel]]]]) -> None:
        """
        Execute the registered renderer classes' render method.

        Args:
            (List[Tuple[str, List[Union[Entity, MapLayerModel]]]]) renderers:
        """
        self.prepare()

        for (renderer_name, render_elements) in renderers:
            renderer = self.__renderers[renderer_name]
            renderer.render(objects=render_elements, camera=self.__camera)

    def destroy(self) -> None:
        pass

    def __create_orthographic_projection_matrix(self, display_width: int, display_height: int,
                                                pixel_size: float = 0.5):

        projection_matrix = np.eye(4, dtype=np.float32)
        projection_matrix[0, 0] = 2 / (pixel_size * display_width)
        projection_matrix[1, 1] = 2 / (pixel_size * display_height)
        projection_matrix[2, 2] = 1.0

        # TODO: Move this hardcoded EGO center_x to config
        projection_matrix[0, 3] = -2 * 0.25

        return projection_matrix

    def __create_perspective_projection_matrix(self, display_width: int, display_height: int) -> np.ndarray:

        aspect_ratio = display_width / display_height
        frustum_len = FAR_PLANE - NEAR_PLANE
        scale = math.tan(math.radians(FOV / 2.0))

        projection_matrix = np.zeros((4, 4), dtype=np.float32)
        projection_matrix[0, 0] = 1.0 / (scale * aspect_ratio)
        projection_matrix[1, 1] = 1.0 / scale
        projection_matrix[2, 2] = -(FAR_PLANE + NEAR_PLANE) / frustum_len
        projection_matrix[3, 2] = -2.0 * NEAR_PLANE * FAR_PLANE / frustum_len
        projection_matrix[2, 3] = -1.0

        return projection_matrix
