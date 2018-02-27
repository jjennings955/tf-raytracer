import numpy as np

class Ray(object):
    def __init__(self, origin, direction):
        self.origin = np.array([origin]).T
        self.direction = np.array([direction]).T

    def __repr__(self):
        return "Ray(origin={}^T, direction={}^T)".format(repr(self.origin.T), repr(self.direction.T))

    def intersect_box(self, box):
        tmin = -np.inf
        tmax = +np.inf
        box = box.box
        for i in range(self.origin.shape[0]):
            print(self.direction[i, 0])
            if self.direction[i, 0] != 0:
                t1 = (box[0, i] - self.origin[i, 0])/(self.direction[i, 0])
                t2 = (box[1, i] - self.origin[i, 0]) / (self.direction[i, 0])
                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))
                print(t1, t2)
                print(tmin, tmax)
            elif self.origin[i, 0] <= box[0, i] or self.origin[i, 0] >= box[1, i]:
                print("case 2")
                return False
        return tmax > tmin and tmax >= 0

    def intersect_box_np(self, box):
        box = box.box
        t = (box.T - self.origin)/self.direction
        tmin = max(np.min(t, axis=1, keepdims=True))
        tmax = min(np.max(t, axis=1, keepdims=True))
        return tmax > tmin and tmax >= 0

class Box(object):
    def __init__(self, p1, p2):
        self.box = np.array([p1, p2])

    def __repr__(self):
        return repr(self.box)

    def point_in_box(self, point):
        return point[0] >= self.box[0, 0] and point[1] >= self.box[1, 1] and point[0] >= self.box[1, 0] and point[0] <= self.box[1, 1]

if __name__ == "__main__":
    box = Box([2, 2, 0], [4, 4, 0])
    box2 = Box([0, 5, -1], [2, 6, 1])
    ray = Ray([0, 0, 0], [-1.2, 2.4, -0.6])
    print(box)
    print(ray)
    -1.280502
    2.482687 - 0.666211
    print(ray.intersect_box(box))
    print(ray.intersect_box(box2))
    print(ray.intersect_box_np(box))
    print(ray.intersect_box_np(box2))
