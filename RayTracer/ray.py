import random
from math import *
from sphere import *
from lib import *
from vector import *
from material import *
from light import *

class Raytracer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.clear_color = Color(0,0,0)
        self.current_color = Color(255,255,255)
        self.framebuffer = []
        self.scene = []
        self.light = Light(V3(0,0,0),1)
        self.prob = None
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def point(self,x,y, c=None):
        if y>=0 and y<self.height and x>=0 and x<self.width:
            self.framebuffer[y][x] = c or self.current_color

    def write(self,filename):
        writebmp(filename,self.width,self.height, self.framebuffer)

    def probability(self, prob):
        self.prob = prob
    
    def render(self):
        fov = int(pi/2)
        ar = self.width / self.height
        tana = tan(fov/2)
        
        for y in range(self.height):
            for x in range(self.width):
                ram = random.random()
                if self.prob:
                    if ram <= self.prob:
                        i = (((2*(x+0.5)/self.width)-1) * (ar * tana))
                        j = ((1-(2*(y+0.5)/self.height)) * tana)
                        
                        direction = V3(i,j,-1).norm()
                        origin = V3(0,0,0)
                        c = self.cast_ray(origin,direction)

                        self.point(x,y,c)
                else:
                    i = (((2*(x+0.5)/self.width)-1) * (ar * tana))
                    j = ((1-(2*(y+0.5)/self.height)) * tana)
                        
                    direction = V3(i,j,-1).norm()
                    origin = V3(0,0,0)
                    c = self.cast_ray(origin,direction)

                    self.point(x,y,c)

    def cast_ray(self,origin,direction):
        material, intersect = self.scene_intersect(origin,direction)

        if material is None:
            return self.clear_color

        light_dir = (self.light.position - intersect.point).norm()
        intensity = light_dir @ intersect.normal

        actual_diffuse = Color(
            round(material.diffuse.r) * intensity,
            round(material.diffuse.g) * intensity,
            round(material.diffuse.b) * intensity,
            )

        return actual_diffuse

    def scene_intersect(self,origin,direction):
        zbuffer = 999999
        material = None
        intersect = None

        for o in self.scene:
            object_intersect = o.ray_intersect(origin,direction)
            if object_intersect:
                if object_intersect.distance < zbuffer:
                    zbuffer = object_intersect.distance
                    material =  o.material
                    intersect = object_intersect
        return material,intersect

RED = Material(Color(255,0,0))
ORANGE = Material(Color(243, 156, 18))

r = Raytracer(800,800)
r.light = Light(V3(-1,5,0),1)
r.scene = [
    Sphere(V3(-3,0, -16),2,RED),
    Sphere(V3(2.8,0, -20),2,ORANGE),
    #ojos
    # Sphere(V3(-3,0, -60),2,RED),
    # Sphere(V3(-2,-15, -60),2,ORANGE),
    # #nariz
    # Sphere(V3(0,-17, -80),1),
    # #boca
    # Sphere(V3(3,-15, -80),1),
    # Sphere(V3(1,-13, -80),1),
    # Sphere(V3(-1,-13, -80),1),
    # Sphere(V3(-3,-15, -80),1),
    # #botones
    # Sphere(V3(0,-4, -60),1),
    # Sphere(V3(0,0, -60),1),
    # Sphere(V3(0,4, -60),1),
    # #cuerpo
    # Sphere(V3(0, -4, -20), 2),
    # Sphere(V3(0, 0, -20), 3),
    
]
#r.probability(0.1)
r.render()

r.write('r.bmp')