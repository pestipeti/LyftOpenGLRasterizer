from typing import Optional

import numpy as np

from ..engine.loader import Loader


class RawModel:

    def __init__(self, vertices: np.ndarray, vertex_count: int, indices: Optional[np.ndarray] = None) -> None:
        super().__init__()

        self.__vertices: np.ndarray = vertices
        self.__indices: Optional[np.ndarray] = indices

        self.__vao_id: int = -1
        self.__vertex_count: int = vertex_count

    @property
    def vao_id(self) -> int:
        return self.__vao_id

    def is_loaded_to_vao(self) -> bool:
        return self.__vao_id >= 0

    @property
    def vertex_count(self) -> int:
        return self.__vertex_count

    @property
    def vertices(self) -> np.ndarray:
        return self.__vertices

    def load_to_vao(self, loader: Loader) -> None:
        self.__vao_id = loader.load_to_vao(self.__vertices, self.__indices)

    def remove_from_vao(self, loader: Loader) -> None:
        loader.remove_from_vao(self.__vao_id)
        self.__vao_id = -1

    def destroy(self, loader: Loader) -> None:
        self.remove_from_vao(loader)
