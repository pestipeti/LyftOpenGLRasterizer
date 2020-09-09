from typing import List, Optional

import numpy as np
from OpenGL.GL import (GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_FALSE,
                       GL_FLOAT, GL_STATIC_DRAW, glBindBuffer,
                       glBindVertexArray, glBufferData, glDeleteBuffers,
                       glDeleteVertexArrays, glGenBuffers, glGenVertexArrays,
                       glVertexAttribPointer)


class Loader:
    """
    Handles the geometry-data loading into Vertex Array Objects. It keeps track
    all of the created VAOs and VBOs, so that they can be destroyed when the
    applciation exits.
    """

    def __init__(self) -> None:
        """
        Initializes the loader.
        """
        super().__init__()

        self.__vaos: List[int] = []
        self.__vbos: List[int] = []

    def load_to_vao(self, vertices: np.ndarray, indices: Optional[np.ndarray] = None) -> int:
        """
        Creates a new Vertex Array Object and stores the position information of the vertices into
        attribute 0 of the VAO

        Args:
            vertices (np.ndarray): position data of the vertices
            indices (Optional[np.ndarray]): indices of the datapoints

        Returns:
            (int): The new vao_id
        """
        vao_id: int = self.__create_vao()

        if indices is not None:
            self.__bind_indices_buffer(indices)

        self.store_data_in_attribute_list(0, vertices, 3)

        # Unbind VAO
        glBindVertexArray(0)

        return vao_id

    # noinspection PyMethodMayBeStatic
    def remove_from_vao(self, vao_id: int) -> None:
        glDeleteVertexArrays(1, vao_id)

    def destroy(self) -> None:
        """
        Deletes all the VAOs and VBOs from the video-memory when the application is closed.
        """
        for vao in self.__vaos:
            glDeleteVertexArrays(1, vao)

        self.__vaos = []

        for vbo in self.__vbos:
            glDeleteBuffers(1, vbo)

        self.__vbos = []

    def __create_vao(self) -> int:
        """
        Creates a new Vertex Array Object, activates (bind) it and returns its ID.

        A VAO holds data (geometric coordinates, colors, etc) and it is stored in the GPU's
        memory, so that it can be accessed fast during rendering.

        Returns:
            (int): The new Vertex Array Object's ID
        """
        vao_id: int = glGenVertexArrays(1)
        self.__vaos.append(vao_id)
        glBindVertexArray(vao_id)

        return vao_id

    def __bind_indices_buffer(self, indices: np.ndarray) -> None:
        vbo_id = glGenBuffers(1)
        self.__vbos.append(vbo_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, size=indices.nbytes, data=indices, usage=GL_STATIC_DRAW)

    # noinspection PyMethodMayBeStatic
    def store_data_in_attribute_list(self, attribute_number: int, data: np.ndarray, dim: int = 3,
                                     datatype: int = GL_FLOAT) -> None:
        """
        Stores the position information of the vertices at attribute 0 of the Vertex Array Object.

        It handles the necessary VBO

        Args:
            (int) attribute_number: The attribute number of the VAO where we want the data to be stored
            (np.ndarray) data: Data to be stored
            (int) dim: The dimension number of the individual data point. E.g 3 for (x, y, z) coordinates
        """
        vbo_id = glGenBuffers(1)
        self.__vbos.append(vbo_id)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glVertexAttribPointer(attribute_number, dim, datatype, GL_FALSE, 0, None)

        # Unbind VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
