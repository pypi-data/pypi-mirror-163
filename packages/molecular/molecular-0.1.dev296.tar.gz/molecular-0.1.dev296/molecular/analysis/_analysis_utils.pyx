
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
    # Convert box to right format
    box = box[:, np.newaxis, :]

    # Put a and b in box
    a = a - box * np.round(a / box)
    b = b - box * np.round(b / box)

    # Find minimum distances
    r = np.ones((a.shape[0], a.shape[1], b.shape[1])) * np.inf
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                # Move b
                bm = b + box * [dx, dy, dz]

                # Compute r and update with minimum if necessary
                r = np.amin([r, _distances(a, bm)], axis=0)

    # Return
    return r

