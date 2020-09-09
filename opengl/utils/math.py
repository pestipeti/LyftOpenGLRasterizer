import math

import numpy as np

from ..entities.camera import Camera

EYE_3 = np.eye(3)
EYE_4 = np.eye(4)


def create_rotation_matrix(rot_x: float, rot_y: float, rot_z: float) -> np.ndarray:
    """
    Creates rotation matrix fromEuler angles.

    Args:
        (float) rot_x: Rotation angle for x-axis
        (float) rot_y: Rotation angle for y-axis
        (float) rot_z: Rotation angle for z-axis

    Returns:
         (np.ndarray): Rotation matrix
    """
    sx, sy, sz = math.sin(rot_x), math.sin(rot_y), math.sin(rot_z)
    cx, cy, cz = math.cos(rot_x), math.cos(rot_y), math.cos(rot_z)

    cc, cs = cx * cz, cx * sz
    sc, ss = sx * cz, sx * sz

    # matrix = np.eye(3)
    matrix = EYE_3.copy()

    matrix[0, 0] = cy * cz
    matrix[0, 1] = sy * sc - cs
    matrix[0, 2] = sy * cc + ss

    matrix[1, 0] = cy * sz
    matrix[1, 1] = sy * ss + cc
    matrix[1, 2] = sy * cs - sc

    matrix[2, 0] = -sy
    matrix[2, 1] = cy * sx
    matrix[2, 2] = cy * cx

    return matrix


def create_transformation_matrix(position: np.ndarray, rotation: np.ndarray, scale: np.ndarray) -> np.ndarray:
    """
    Compose transformation matrix (translation, rotation, scale)

    Args:
        (np.ndarray) position: numpy array of shape (N, ). Order: x, y, z
        (np.ndarray) rotation: numpy array of shape (N, ). Euler angles in degrees, order: x, y, z
        (np.ndarray) scale: numpy array of shape (N, )

    Returns:
        (np.ndarray) transformation matrix, shape (n+1, n+1) where n is the number of axis (usually 3 - 3D case)
    """
    n = len(position)

    # matrix = np.eye(n + 1)
    matrix = EYE_4.copy()

    rotation_matrix = create_rotation_matrix(rotation[0], rotation[1], rotation[2])

    scale_diag = EYE_3.copy()
    scale_diag[0, 0] = scale[0]
    scale_diag[1, 1] = scale[1]
    scale_diag[2, 2] = scale[2]

    matrix[:n, :n] = np.dot(rotation_matrix, scale_diag)
    matrix[:n, n] = position[:]

    return matrix


def create_view_matrix(camera: Camera):
    n = 3
    matrix = np.eye(n + 1)

    rotation_matrix = create_rotation_matrix(-1 * camera.rot_x, -1 * camera.rot_y, -1 * camera.rot_z)

    matrix[:n, :n] = rotation_matrix
    matrix[:n, n] = np.dot(rotation_matrix, -1 * camera.position)

    return matrix
