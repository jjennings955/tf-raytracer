import numpy as np

def expand_bits(v):
    v = (v * 0x00010001) & 0xFF0000FF
    v = (v * 0x00000101) & 0x0F00F00F
    v = (v * 0x00000011) & 0xC30C30C3
    v = (v * 0x00000005) & 0x49249249
    return v

def morton3D(x, y, z):
    x = np.clip(x * 1024.0, 0.0, 1023.0).astype(np.uint32)
    y = np.clip(y * 1024.0, 0.0, 1023.0).astype(np.uint32)
    z = np.clip(z * 1024.0, 0.0, 1023.0).astype(np.uint32)

    xx = expand_bits(x)
    yy = expand_bits(y)
    zz = expand_bits(z)
    return xx * 4 + yy * 2 + zz

def centroids(vertices):
    return np.mean(vertices, axis=1)

def extent(vertices):
    mins = np.min(vertices.reshape(-1,3), axis=0)
    maxes = np.max(vertices.reshape(-1, 3), axis=0)
    #maxes = np.max(vertices, axis=1)
    return mins, maxes

class BVH(object):
    def __init__(self, vertices):
        # Compute centroid of each triangle
        # Compute morton codes of centroids
        # Sort triangles by morton codes
        cents = centroids(vertices)
        #mortons = morton3D(vertices[:, 0], vertices[:, 1], vertices[:, 2])
        mortons = morton3D(cents[:, 0], cents[:, 1], cents[:, 2])
        indices = np.argsort(mortons)
        self.sorted_mortons = mortons[indices]
        self.vertices = vertices[indices]
        self.root_node = BVHNode(self.vertices)


    def raycast(self, origin, direction):
        return self.root_node.ray_cast(origin, direction)

    def split(self):
        self.root_node.split()


class BVHNode(object):
    def __init__(self, vertices, leaf_threshold=4):
        self.leaf_threshold = leaf_threshold
        self.vertices = vertices
        self.children = []
        self.compute_bounds()

    def is_leaf(self):
        return len(self.children) == 0

    def ray_cast(self, origin, direction):
        results = []

        if self.is_leaf():
            intersects, t = ray_intersect_aabb(origin, direction, np.array(self.bounds))
            if intersects:
                print("HEY", self.vertices.shape)
                return self.vertices
            else:
                return []
        else:
            for child in self.children:
                intersects, t = ray_intersect_aabb(origin, direction, np.array(self.bounds))
                if intersects:
                    print("It does! ", self.bounds)
                    results.extend(child.ray_cast(origin, direction))
            return results


    def compute_bounds(self):
        self.bounds = extent(self.vertices)

    def split(self):
        num_vertices = self.vertices.shape[0]
        if num_vertices > self.leaf_threshold:
            print("Splitting")
            left = self.vertices[:num_vertices//2]
            right = self.vertices[num_vertices//2:]
            splits = [left, right]
            for split in splits:
                child_node = BVHNode(split)
                self.children.append(child_node)
                child_node.split()

def ray_intersect_aabb(origin, direction, box):
    print(origin, direction, box)
    t = (box.T - origin)/direction
    tmin = max(np.min(t, axis=1, keepdims=True))
    tmax = min(np.max(t, axis=1, keepdims=True))
    print(tmin, tmax)
    return (tmax > tmin and tmax >= 0), tmin

from util import load_model
if __name__ == "__main__":
    vertices, faces = load_model('teapot.obj', normalize=True)
    triangles = vertices[faces]
    mybvh = BVH(triangles)
    import time
    start = time.time()

    mybvh.root_node.split()
    print(len(mybvh.raycast(np.array([[0, 0, 0]]).T, np.array([[0.5, 0.5, 0.5]]).T)))
    end = time.time()
    print(end - start)