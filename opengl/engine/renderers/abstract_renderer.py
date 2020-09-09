from abc import ABC, abstractmethod
from typing import TypeVar

from ...shaders import ShaderProgram

ShaderTV = TypeVar('ShaderTV', bound=ShaderProgram)


class AbstractRenderer(ABC):

    def __init__(self, shader: ShaderTV) -> None:
        super().__init__()

        self.__shader: ShaderTV = shader

    @property
    def shader(self) -> ShaderTV:
        return self.__shader

    def init(self) -> None:
        pass

    def _before_render(self, **kwargs) -> None:
        self.shader.start()

        if 'camera' in kwargs.keys():
            self.shader.load_view_matrix(kwargs["camera"])

    def render(self, **kwargs):
        self._before_render(**kwargs)
        self._do_render(**kwargs)
        self._after_render(**kwargs)

    @abstractmethod
    def _do_render(self, **kwargs):
        pass

    def _after_render(self, **kwargs) -> None:
        self.shader.stop()

    def destroy(self) -> None:
        pass
