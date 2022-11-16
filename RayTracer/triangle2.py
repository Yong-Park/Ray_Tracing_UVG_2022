from vector import *
from intersect import *

class Triangulo(object): 
    def __init__(self, center, v1,v2,v3, material):
        self.center = center
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.material = material

    def ray_intersect(self, origin, direction):

        d = self.center + origin / direction



        impact = (direction * tnear) - origin
        normal = (impact - self.center).norm()
        return Intersect(
            distance = d1, 
            point = impact, 
            normal = normal,
        )