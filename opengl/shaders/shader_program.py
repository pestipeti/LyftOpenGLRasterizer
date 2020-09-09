from abc import ABC, abstractmethod

import numpy as np
from OpenGL.GL import (GL_COMPILE_STATUS, GL_FALSE, GL_FRAGMENT_SHADER,
                       GL_VERTEX_SHADER, glAttachShader, glBindAttribLocation,
                       glCompileShader, glCreateProgram, glCreateShader,
                       glDeleteProgram, glDeleteShader, glDetachShader,
                       glGetShaderiv, glGetUniformLocation, glLinkProgram,
                       glShaderSource, glUniform1f, glUniform2f, glUniform3f,
                       glUniform4f, glUniformMatrix4fv, glUseProgram,
                       glValidateProgram)

from ..entities.camera import Camera
from ..utils.math import create_view_matrix


class ShaderProgram(ABC):
    """
    Base class
    """

    def __init__(self, vertex_shader_code: str, fragment_shader_code: str) -> None:

        self.__vertex_shader_id: int = self._load_shader(vertex_shader_code, GL_VERTEX_SHADER)
        self.__fragment_shader_id: int = self._load_shader(fragment_shader_code, GL_FRAGMENT_SHADER)
        self.__program_id: int = glCreateProgram()

        self.__location_transformation_matrix: int = -1
        self.__location_view_matrix: int = -1
        self.__location_projection_matrix: int = -1

        glAttachShader(self.__program_id, self.__vertex_shader_id)
        glAttachShader(self.__program_id, self.__fragment_shader_id)
        self._bind_attributes()
        glLinkProgram(self.__program_id)
        glValidateProgram(self.__program_id)
        self._get_uniform_locations()

    def load_projection_matrix(self, matrix: np.ndarray) -> None:
        ShaderProgram._load_matrix(self.__location_projection_matrix, matrix)

    def load_view_matrix(self, camera: Camera) -> None:
        ShaderProgram._load_matrix(self.__location_view_matrix, create_view_matrix(camera))

    def load_transformation_matrix(self, matrix: np.ndarray) -> None:
        ShaderProgram._load_matrix(self.__location_transformation_matrix, matrix)

    def start(self) -> None:
        glUseProgram(self.__program_id)

    # noinspection PyMethodMayBeStatic
    def stop(self) -> None:
        glUseProgram(0)

    def destroy(self) -> None:
        self.stop()

        glDetachShader(self.__program_id, self.__vertex_shader_id)
        glDetachShader(self.__program_id, self.__fragment_shader_id)
        glDeleteShader(self.__vertex_shader_id)
        glDeleteShader(self.__fragment_shader_id)
        glDeleteProgram(self.__program_id)

    @abstractmethod
    def _bind_attributes(self) -> None:
        pass

    def _bind_attribute(self, attribute: int, variable_name: str) -> None:
        glBindAttribLocation(self.__program_id, attribute, variable_name)

    @abstractmethod
    def _get_uniform_locations(self) -> None:
        self.__location_transformation_matrix = self._get_uniform_location("transformationMatrix")
        self.__location_view_matrix = self._get_uniform_location("viewMatrix")
        self.__location_projection_matrix = self._get_uniform_location("projectionMatrix")

    def _get_uniform_location(self, uniform_name: str) -> int:
        return glGetUniformLocation(self.__program_id, uniform_name)

    @staticmethod
    def _load_shader(shader_code: str, shader_type: int) -> int:

        shader_id: int = glCreateShader(shader_type)
        glShaderSource(shader_id, shader_code)
        glCompileShader(shader_id)

        if glGetShaderiv(shader_id, GL_COMPILE_STATUS) == GL_FALSE:
            raise RuntimeError("Could not complie shader!")

        return shader_id

    @staticmethod
    def _load_float(location: int, value: float) -> None:
        glUniform1f(location, value)

    @staticmethod
    def _load_boolean(location: int, value: bool) -> None:
        glUniform1f(location, 1. if value else 0.)

    @staticmethod
    def _load_vector(location: int, vector: np.ndarray) -> None:
        if len(vector) == 2:
            glUniform2f(location, *vector)
        elif len(vector) == 3:
            glUniform3f(location, *vector)
        else:
            glUniform4f(location, *vector)

    @staticmethod
    def _load_matrix(location: int, matrix: np.ndarray) -> None:
        glUniformMatrix4fv(location, 1, True, matrix)
