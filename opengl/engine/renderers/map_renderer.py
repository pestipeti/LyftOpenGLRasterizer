import numpy as np
from OpenGL.GL import (glBindVertexArray, glDisableVertexAttribArray,
                       glDrawArrays, glEnableVertexAttribArray)

from ...shaders.map_shader import MapShader
from ...utils import create_transformation_matrix
from .abstract_renderer import AbstractRenderer


class MapRenderer(AbstractRenderer):

    def __init__(self) -> None:
        super().__init__(MapShader())

        self.transformation_matrix = create_transformation_matrix(
            np.array([0., 0., 0.]), np.array([0., 0., 0.]), np.array([1., 1., 0.]))

        self.shader.start()
        self.shader.load_transformation_matrix(self.transformation_matrix)
        self.shader.stop()

    def _do_render(self, **kwargs):

        if 'objects' not in kwargs.keys():
            return

        instances = kwargs['objects']

        for instance in instances:
            glBindVertexArray(instance.vao_id)
            glEnableVertexAttribArray(0)
            glEnableVertexAttribArray(1)

            glDrawArrays(instance.get_draw_mode(), 0, instance.vertex_count)

            glDisableVertexAttribArray(0)
            glDisableVertexAttribArray(1)
            glBindVertexArray(0)
