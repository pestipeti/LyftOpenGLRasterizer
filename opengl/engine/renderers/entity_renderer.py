from typing import Generic, List, TypeVar

from OpenGL.GL import (GL_TRIANGLES, GL_UNSIGNED_INT, glBindVertexArray,
                       glDisableVertexAttribArray, glDrawElements,
                       glEnableVertexAttribArray)

from ...entities.agent import Agent
from ...entities.entity import Entity
from ...models.raw_model import RawModel
from ...shaders.static_shader import StaticShader
from ...utils import create_transformation_matrix
from .abstract_renderer import AbstractRenderer

EntityTV = TypeVar('EntityTV', bound=Entity)
AgentTV = TypeVar('AgentTV', bound=Agent)


class EntityRenderer(AbstractRenderer):

    def __init__(self) -> None:
        super().__init__(StaticShader())

    def _do_render(self, **kwargs):

        if 'objects' not in kwargs.keys():
            return

        instances: List[Generic[EntityTV, AgentTV]] = kwargs['objects']

        model: RawModel = instances[0].model

        glBindVertexArray(model.vao_id)
        glEnableVertexAttribArray(0)

        for instance in instances:
            model: RawModel = instance.model

            # transformation_matrix = create_transformation_matrix(
            #     instance.position, instance.rotation, instance.scale)

            self.shader.load_transformation_matrix(instance.transformation_matrix)

            if isinstance(self.shader, StaticShader):
                self.shader.load_vertex_color(instance.color)

            glDrawElements(GL_TRIANGLES, model.vertex_count, GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
