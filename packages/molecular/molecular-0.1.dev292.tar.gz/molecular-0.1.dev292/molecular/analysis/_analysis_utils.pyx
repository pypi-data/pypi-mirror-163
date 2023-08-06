
#cython: language_level=3

from scipy.spatial.distance import cdist
import numpy as np
cimport numpy as np


def _distances(a, b):
    r = np.zeros((a.shape[0], a.shape[1], b.shape[1]))
    for i in range(a.shape[0]):
        r[i, :, :] = cdist(a[i, :, :], b[i, :, :])
    return r


def _minimum_distances(a, b, box):
    # Put a in box
    a = a - box[:, np.newaxis, :] * np.round(a / box[:, np.newaxis, :])

    # Find minimum distances
    min_r = np.ones((a.shape[0], a.shape[1], b.shape[1])) * np.inf
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                # Put b in box
                b = b - box[:, np.newaxis, :] * np.round(b / box[:, np.newaxis, :])

                # Move b
                b = b + (box * [dx, dy, dz])[:, np.newaxis, :]

                # Update min_r?
                r = _distances(a, b)
                mask = r < min_r
                if np.sum(mask) > 0:
                    min_r[mask] = r[mask]

    # Return
    return min_r

