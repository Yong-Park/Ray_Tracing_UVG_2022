from vector import *
from intersect import *

class Cubo(object):
    def __init__(self,center,vmin,vmax,material):
        self.center = center
        self.vmin = vmin 
        self.vmax= vmax
        self.material = material   

    def ray_intersect(self,origin,direction):
        # invdir = 1 / direction

        tmin = (self.vmin.x - origin.x) / direction.x
        tmax = (self.vmax.x - origin.x) / direction.x
        tymin = (self.vmin.y - origin.y) / direction.y
        tymax = (self.vmax.y - origin.y) / direction.y

        if ((tmin > tymax) or (tymin > tmax)):
            return None

        if (tymin > tmin):
            tmin = tymin
        if (tymax < tmax):
            tmax = tymax

        tzmin = (self.vmin.z - origin.z) / direction.z
        tzmax = (self.vmax.z - origin.z) / direction.z

        if ((tmin > tzmax) or (tzmin > tmax)):
            return None

        if (tzmin > tmin):
            tmin = tzmin
        if(tzmax < tmax):
            tmax = tzmax

        normal = V3(1,1,0)
        impact = (direction * tmax) + origin

        # print('tmin ', tmin)
        # print('tmax ', tmax)

        return Intersect(
            distance = tmax,
            point = impact,
            normal = normal,
        )
        