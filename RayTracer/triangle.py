#teoria del codigo obtenido de https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection
from vector import *
from intersect import *

class Triangulo(object): 
    def __init__(self, center, largo, material):
        self.center = center
        self.largo = largo
        self.material = material

    def ray_intersect(self, origin, direction):
        #obtener los vectores de cada posicion
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
        
        #aplicacion de concepto de la pagina que se utilizo para entender
        v0v1 = v2 - v1
        v0v2 = v3 - v1
        pvec = direction * v0v2
        det = v0v1 @ pvec
        
        invDet = 1 / det
        tvec = origin - v1
        u = (tvec @ pvec) * invDet 
        
        if u < 0 or u > 1:
            return False
        
        qvec = tvec * v0v1
        v = (direction @ qvec) * invDet
        
        if v < 0 or (u + v) > 1:
            return False
        
        t = (v0v2 @ qvec) * invDet

        impact = (direction * t) + origin
        normal = (v0v1 * v0v2).norm()
        
        return Intersect(
            distance = t, 
            point = impact, 
            normal = normal,
        )