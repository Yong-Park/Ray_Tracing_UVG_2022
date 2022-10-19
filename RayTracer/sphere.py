from vector import *
from intersect import *

class Sphere(object):
    def __init__(self,center,radius,material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self,origin,direction):
        L = self.center - origin
        tca = L @ direction
        l = L.__length__()

        d2 = l**2 - tca**2 

        if d2 > self.radius**2:
            return None

        thc = (self.radius**2-d2)**0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False

        impact = (direction * t0) + origin 
        normal = (impact - self.center).norm()
        print(t0)

        return Intersect(
            distance = t0,
            point = impact,
            normal = normal,
        )
        