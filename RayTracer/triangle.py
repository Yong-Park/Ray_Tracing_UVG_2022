from vector import *
from intersect import *

class Triangulo(object): 
    def __init__(self, center, largo, material):
        self.center = center
        self.largo = largo
        self.material = material

    def ray_intersect(self, origin, direction):

        v1x = (self.center.x - (self.largo / 2)) + origin.x / direction.x
        v1y = (self.center.y - (self.largo / 2)) + origin.y / direction.y
        v1z = (self.center.z) + origin.z / direction.z

        v1 = V3(v1x,v1y,v1z)

        v2x = (self.center.x + (self.largo / 2)) + origin.x / direction.x
        v2y = (self.center.y - (self.largo / 2)) + origin.y / direction.y
        v2z = (self.center.z) + origin.z / direction.z

        v2 = V3(v2x,v2y,v2z)

        v3x = (self.center.x) + origin.x / direction.x
        v3y = (self.center.y + (self.largo / 2)) + origin.y / direction.y
        v3z = (self.center.z) + origin.z / direction.z

        v3 = V3(v3x,v3y,v3z)
        
        edge1 = v2 - v1
        edge2 = v3 - v1

        normal = (edge1 * edge2).norm()
        
        area2 = normal.__length__()
        # check if ray and plane are parallel.
        NdotRayDirection = normal @ direction
        
        if NdotRayDirection < 0:
            return False
        
        d = -(normal @ v1)
        t = -(normal @ origin + d) / NdotRayDirection
        
        if t < 0:
            return False
        
        impact = (direction * t) + origin
        
        
        return Intersect(
            distance = t, 
            point = impact, 
            normal = normal,
        )