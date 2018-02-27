import numpy as np


def load_model(fname='teapot.obj', normalize=True):
    z = np.loadtxt('teapot.obj', skiprows=0, converters={0: lambda f: 'fv'.index(chr(ord(f)))})
    vertices = np.float32(z[np.where(z[:, 0] == 1)][:, 1:])
    if normalize:
        vertices -= np.min(vertices)
        vertices = vertices/np.max(vertices)
    faces = np.int32(z[np.where(z[:, 0] == 0)][:, 1:] - 1)
    return vertices, faces