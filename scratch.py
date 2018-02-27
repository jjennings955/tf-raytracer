import numpy as np

z = np.loadtxt('teapot.obj', skiprows=0, converters={0 : lambda f : 'fv'.index(chr(ord(f)))})
vertices = 0.1*np.float32(z[np.where(z[:, 0] == 1)][:, 1:])
faces = np.int32(z[np.where(z[:, 0] == 0)][:, 1:] - 1)
print(vertices)
print(faces)