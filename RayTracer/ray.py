from lib import *
import random
from math import *
from sphere import *
from vector import *

class Raytracer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.clear_color = color(0,0,0)
        self.current_color = color(255,255,255)
        self.framebuffer = []
        self.scene = []
        self.colors = []
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
        color_id = 0
        for o in self.scene:
            if o.ray_intersect(origin,direction):
                return r.colors[color_id]
            color_id += 1
        return self.clear_color

RED = color(255,0,0)
ORANGE = color(243, 156, 18)

r = Raytracer(800,800)
r.scene = [
    #ojos
    Sphere(V3(2,-15, -60),1),
    Sphere(V3(-2,-15, -60),1),
    #nariz
    Sphere(V3(0,-17, -80),1),
    #boca
    Sphere(V3(3,-15, -80),1),
    Sphere(V3(1,-13, -80),1),
    Sphere(V3(-1,-13, -80),1),
    Sphere(V3(-3,-15, -80),1),
    #botones
    Sphere(V3(0,-4, -60),1),
    Sphere(V3(0,0, -60),1),
    Sphere(V3(0,4, -60),1),
    #cuerpo
    Sphere(V3(0, -4, -20), 2),
    Sphere(V3(0, 0, -20), 3),
    
]
r.colors = [
    BLACK,
    BLACK,
    ORANGE,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    BLACK,
    WHITE,
    WHITE
    
]
#r.probability(0.1)
r.render()

r.write('r.bmp')