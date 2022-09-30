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
        self.light = Light(V3(0,0,0),1, Color(255,255,255))
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

        #diffuse component
        diffuse_intensity = light_dir @ intersect.normal
        diffuse = material.diffuse * diffuse_intensity * material.albedo[0]

        #specular component
        light_reflection = reflect(light_dir, intersect.normal)
        reflection_intensity = max(0, light_reflection @ direction)
        specular_intensity = reflection_intensity ** material.spec
        specular = self.light.c * specular_intensity * material.albedo[1]

        return diffuse + specular

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

# RED = Material(Color(255,0,0))
# ORANGE = Material(Color(243, 156, 18))
rubber = Material(diffuse=Color(80,0,0), albedo = [0.9,0.1], spec = 10)
ivory = Material(diffuse=Color(100,100,50), albedo = [0.6,0.3], spec = 50)

r = Raytracer(800,800)
r.light = Light(V3(-20,20,20),1, Color(255,255,255))
r.scene = [
    Sphere(V3(-3,0, -16),2,rubber),
    Sphere(V3(2.8,0, -20),2,ivory),    
]
#r.probability(0.1)
r.render()

r.write('r.bmp')