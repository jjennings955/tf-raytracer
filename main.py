import numpy as np
from pyglet.gl import *

from util import load_model

window = pyglet.window.Window()
angle = 0

@window.event
def on_show():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    # Set up projection matrix.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(100.0, float(window.width)/window.height, 0.1, 360)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()

def box(p1=None, p2=None):
    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_LINES, [0, 1, 1, 2, 2, 3, 3, 0,  # front square
                                                         4, 5, 5, 6, 6, 7, 7, 4,  # back square
                                                         0, 4, 1, 5, 2, 6, 3, 7],  # connectors

                                 ('v3f', (p1[0], p1[1], p1[2],
                                          p1[0], p2[1], p1[2],
                                          p2[0], p2[1], p1[2],
                                          p2[0], p1[1], p1[2],

                                          p1[0], p1[1], p2[2],
                                          p1[0], p2[1], p2[2],
                                          p2[0], p2[1], p2[2],
                                          p2[0], p1[1], p2[2])))

def draw_bvh(root_node):
    draw_bvh_helper(root_node)

def draw_bvh_helper(node, depth=0, max_depth=6):
    box(*node.bounds)
    if depth < max_depth:
        for child in node.children:
            draw_bvh_helper(child, depth+1)

def model(fname='teapot.obj'):
    from bvh import BVH
    vertices, faces = load_model(fname='teapot.obj')
    triangles = vertices[faces]
    mybvh = BVH(triangles)
    mybvh.split()
    glScalef(3.0, 3.0, 3.0)
    glColor3f(1.0, 0, 0)
    pyglet.graphics.draw_indexed(vertices.shape[0], pyglet.gl.GL_LINES, faces.ravel().tolist(),# connectors
                           ('v3f', vertices.ravel().tolist()))
    glColor3f(0.0, 1.0, 0)
    draw_bvh(mybvh.root_node)

@window.event
def on_draw():
    global angle
    #glClear(GL_COLOR_BUFFER_BIT)
    window.clear()
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()

    pyglet.gl.gluLookAt(5.5, 5.5, -2, 1., 1., 3., 0., 1., 0.)

    glColor3f(1.0, 0, 0)
    glScalef(2.0, 2.0, 2.0)
    pyglet.gl.glRotated(angle, 0, 1, 0)
    model()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(105.0, float(window.width)/window.height, 0.1, 360)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()

def update(dt):
    global angle
    angle += 5
    angle = angle % 360

pyglet.clock.schedule_interval(update, 0.1)

pyglet.app.run()