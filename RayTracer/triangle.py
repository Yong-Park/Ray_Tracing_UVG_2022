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

        v1x = (self.center.x + self.v1.x) + origin.x / direction.x
        v1y = (self.center.y + self.v1.y) + origin.y / direction.y
        v1z = (self.center.z + self.v1.z) + origin.z / direction.z

        v1 = V3(v1x,v1y,v1z)

        v2x = (self.center.x + self.v2.x) + origin.x / direction.x
        v2y = (self.center.y + self.v2.y) + origin.y / direction.y
        v2z = (self.center.z + self.v2.z) + origin.z / direction.z

        v2 = V3(v2x,v2y,v2z)

        v3x = (self.center.x + self.v3.x) + origin.x / direction.x
        v3y = (self.center.y + self.v3.y) + origin.y / direction.y
        v3z = (self.center.z + self.v3.z) + origin.z / direction.z

        v3 = V3(v3x,v3y,v3z)

        normal = ((v2 - v1) * (v3 - v1) / (v2-v1) * (v3 - v1))

        d1 = -(normal.x * v1.x + normal.y * v1.y + normal.z * v1.z)
        d2 = -(normal.x * v2.x + normal.y * v2.y + normal.z * v2.z)
        d3 = -(normal.x * v3.x + normal.y * v3.y + normal.z * v3.z)

        if d1 > d2:
            d1 = d1
        else:
            d1 = d2
        if d1 > d3:
            d1 = d1
        else:
            d1 = d3
        if d2 > d3:
            d1 = d2
        else:
            d1 = d3

        impact = (direction * d1) - origin
        #calculo para ver si tiene impacto
        s1 = ((v2 - v1) * (impact - v1)) @ normal
        s2 = ((v3 - v2) * (impact - v2)) @ normal
        s3 = ((v1 - v3) * (impact - v3)) @ normal

        if (s1 > 0 and s2 > 0 and s3 > 0) \
            or (s1 < 0 and s2 <0 and s3 < 0):
            pass
        else:
            return False

        return Intersect(
            distance = d1, 
            point = impact, 
            normal = normal,
        )