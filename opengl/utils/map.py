import numpy as np

from l5kit.data.map_api import MapAPI
from tqdm import tqdm

from .helpers import obj_exists, obj_load, obj_save
from .tripy import earclip
from ..models import LaneSurfaceModel, LaneLinesModel, CrosswalkModel


def create_lane_surface_model(map_api: MapAPI) -> LaneSurfaceModel:
    vertices = []
    vertexType = []

    if obj_exists("lane_surface_vertices", './cache'):
        vertices = obj_load("lane_surface_vertices", './cache')
        vertexType = obj_load("lane_surface_vertex_types", "./cache")
        return LaneSurfaceModel(vertices, len(vertices) // 3, colors=vertexType)

    print("Generating triangles from lanes' polygon dataponts...")
    for element in tqdm(map_api):
        element_id = MapAPI.id_as_str(element.id)

        if map_api.is_lane(element):
            lane = map_api.get_lane_coords(element_id)
            left = lane["xyz_left"]
            right = lane["xyz_right"]

            coords = np.vstack((left, np.flip(right, 0)))
            coords = earclip(coords)

            for triangle in coords:

                for vertex in triangle:
                    vertices.append(vertex[0])
                    vertices.append(vertex[1])
                    # z-axis (0 in 2d)
                    vertices.append(0.0001)
                    vertexType.append(1000)

    vertices = np.array(vertices, dtype=np.float32)
    vertexType = np.array(vertexType, dtype=np.float32)

    obj_save(vertices, "lane_surface_vertices", "./cache")
    obj_save(vertexType, "lane_surface_vertex_types", "./cache")

    return LaneSurfaceModel(vertices, len(vertices) // 3, colors=vertexType)


def create_crosswalks_model(map_api: MapAPI) -> CrosswalkModel:
    vertices = []
    vertexType = []

    for element in map_api:
        element_id = MapAPI.id_as_str(element.id)

        if map_api.is_crosswalk(element):
            crosswalk = map_api.get_crosswalk_coords(element_id)
            coords = earclip(crosswalk["xyz"])

            for triangle in coords:

                for vertex in triangle:
                    vertices.append(vertex[0])
                    vertices.append(vertex[1])
                    # z-axis (0 in 2d)
                    vertices.append(0.001)
                    # White
                    vertexType.append(1)

    vertices = np.array(vertices, dtype=np.float32)
    vertexType = np.array(vertexType, dtype=np.float32)

    return CrosswalkModel(vertices, len(vertices) // 3, colors=vertexType)


def create_lane_line_model(map_api: MapAPI) -> LaneLinesModel:
    vertices = []
    vertexType = []

    for element in map_api:
        element_id = MapAPI.id_as_str(element.id)

        if map_api.is_lane(element):
            lane = map_api.get_lane_coords(element_id)
            lane_coords = lane["xyz_left"]

            for idx in range(len(lane_coords) - 1):
                vertices.append(lane_coords[idx][0])
                vertices.append(lane_coords[idx][1])
                vertices.append(1.)
                vertexType.append(3)

                vertices.append(lane_coords[idx + 1][0])
                vertices.append(lane_coords[idx + 1][1])
                vertices.append(1.)
                vertexType.append(3)

            lane_coords = lane["xyz_right"]

            for idx in range(len(lane_coords) - 1):
                vertices.append(lane_coords[idx][0])
                vertices.append(lane_coords[idx][1])
                vertices.append(1.)
                vertexType.append(3)

                vertices.append(lane_coords[idx + 1][0])
                vertices.append(lane_coords[idx + 1][1])
                vertices.append(1.)
                vertexType.append(3)

    vertices = np.array(vertices, dtype=np.float32)
    vertexType = np.array(vertexType, dtype=np.float32)

    return LaneLinesModel(vertices, len(vertices) // 3, vertexType)
