#https://inmensia.com/articulos/raytracing/planotrianguloycubo.html
#teoria obtenido de esta pagina

from vector import *
from intersect import *

class Cubo(object): 
    def __init__(self, center, largo, material):
        self.center = center
        self.largo = largo
        self.material = material

    def ray_intersect(self, origin, direction):
        tnear = float('-inf')
        tfar = float('inf')

        ml = self.largo / 2

        # interseccion en x
        t1 = ((self.center.x - ml) - origin.x) / direction.x
        t2 = ((self.center.x + ml) - origin.x) / direction.x

        if t1 > t2:
            t1, t2 = t2, t1

        if t1 > tnear:
            tnear = t1

        if t2 < tfar:
            tfar = t2

        if tnear > tfar:
            return False

        # interseccion en y
        t1 = ((self.center.y - ml) - origin.y) / direction.y
        t2 = ((self.center.y + ml) - origin.y) / direction.y

        if t1 > t2:
            t1, t2 = t2, t1

        if t1 > tnear:
            tnear = t1

        if t2 < tfar:
            tfar = t2

        if tnear > tfar:
            return False

        # interseccion en z
        t1 = ((self.center.z - ml) - origin.z) / direction.z
        t2 = ((self.center.z + ml) - origin.z) / direction.z

        if t1 > t2:
            t1, t2 = t2, t1

        if t1 > tnear:
            tnear = t1

        if t2 < tfar:
            tfar = t2

        if tnear > tfar:
            return False

        #en caso que este sea menor es porque el que esta alejado es el que choca
        # de lo contrario tnear corresponde a la interseccion
        if tnear < 0:
            tnear = tfar
            #en caso que aun cambiado sea cero regresar falso
            if tnear < 0:
                return False

        impact = (direction * tnear) - origin
        normal = (impact - self.center).norm()

        return Intersect(
            distance = tnear, 
            point = impact, 
            normal = normal,
        )