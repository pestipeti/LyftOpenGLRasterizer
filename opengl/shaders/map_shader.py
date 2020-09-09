from .shader_program import ShaderProgram

MAP_VERTEX_SHADER = """
#version 400 core

in vec3 position;
in float vertexType;

out vec3 color;

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

void main(void) {
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);
    
    if (vertexType == 0) {
        // black
        color = vec3(0.0f, 0.0f, 0.0f);
    } else if (vertexType == 1) {
        // white
        color = vec3(0.98f, 0.98f, 0.98f);
    } else if (vertexType == 1000) {
        color = vec3(0.5f, 0.5f, 0.5f);
    } else {
        // default color
        color = vec3(1.0f, 0.85f, 0.32f);
    }

}
"""

MAP_FRAGMENT_SHADER = """
#version 400 core

in vec3 color;

out vec4 out_Color;

void main(void) {
    out_Color = vec4(color, 1.0f);
}
"""


class MapShader(ShaderProgram):

    def __init__(self) -> None:
        self.__location_projection_matrix: int = -1
        self.__location_view_matrix: int = -1

        super().__init__(MAP_VERTEX_SHADER, MAP_FRAGMENT_SHADER)

    def _bind_attributes(self) -> None:
        self._bind_attribute(0, "position")
        self._bind_attribute(1, "vertexType")

    def _get_uniform_locations(self) -> None:
        super()._get_uniform_locations()
