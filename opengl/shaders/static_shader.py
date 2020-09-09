import numpy as np

from .shader_program import ShaderProgram

STATIC_VERTEX_SHADER = """
#version 400 core

in vec3 position;

out vec3 color;

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

uniform vec3 vColor;

void main(void) {
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);
    color = vColor;
}
"""

STATIC_FRAGMENT_SHADER = """
#version 400 core

in vec3 color;

out vec4 out_Color;

void main(void) {
    out_Color = vec4(color, 1.0f);
}
"""


class StaticShader(ShaderProgram):

    def __init__(self) -> None:
        self.__location_v_color: int = -1

        super().__init__(STATIC_VERTEX_SHADER, STATIC_FRAGMENT_SHADER)

    def load_vertex_color(self, color: np.ndarray) -> None:
        StaticShader._load_vector(self.__location_v_color, color)

    def _bind_attributes(self) -> None:
        self._bind_attribute(0, "position")

    def _get_uniform_locations(self) -> None:
        super()._get_uniform_locations()

        self.__location_v_color = self._get_uniform_location("vColor")
