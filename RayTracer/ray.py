import random
from math import *
from sphere import *
from lib import *
from vector import *
from material import *
from light import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.clear_color = Color(0,0,100)
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

    def cast_ray(self,origin,direction, recursion = 0):
        if recursion >= MAX_RECURSION_DEPTH:
            return self.clear_color

        material, intersect = self.scene_intersect(origin,direction)

        if material is None:
            return self.clear_color

        light_dir = (self.light.position - intersect.point).norm()

        #sombra
        shadow_bias = 1.1
        shador_origin = intersect.point + (intersect.normal * shadow_bias)
        shadow_material = self.scene_intersect(shador_origin, light_dir)

        shadow_intensity = 0
        if shadow_material:
            # estamos en la sombra
            shadow_intensity = 0.7

        #diffuse component
        diffuse_intensity = light_dir @ intersect.normal
        diffuse = material.diffuse * diffuse_intensity * material.albedo[0] * (1-shadow_intensity)

        #specular component
        light_reflection = reflect(light_dir, intersect.normal)
        reflection_intensity = max(0, light_reflection @ direction)
        specular_intensity = reflection_intensity ** material.spec
        specular = self.light.c * specular_intensity * material.albedo[1]

        #reflection
        if material.albedo[2] > 0:
            reverse_direction = direction * -1
            reflect_direction = reflect(reverse_direction,intersect.normal)
            reflect_bias = -0.5 if reflect_direction @ intersect.normal < 0 else 0.5
            reflect_origin = intersect.point + (intersect.normal * reflect_bias) 
            reflect_color = self.cast_ray(reflect_origin,reflect_direction, recursion + 1)
        else:
            reflect_color = Color(0,0,0)
        reflection = reflect_color * material.albedo[2]

        return diffuse + specular + reflection

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
rubber = Material(diffuse=Color(80,0,0), albedo = [0.9,0.1,0], spec = 10)
ivory = Material(diffuse=Color(255,255,255), albedo = [0.6,0.3,0], spec = 50)
red_clay = Material(diffuse=Color(255,0,0), albedo = [0.9,0.1], spec = 50)
black = Material(diffuse=Color(255,0,0), albedo = [0.04,0.96], spec = 50)
grass = Material(diffuse=Color(0,255,0), albedo = [0.03,0.97], spec = 50)
mirror = Material(diffuse=Color(255,255,255), albedo = [0,1,0.8], spec = 1425)


r = Raytracer(800,800)
r.light = Light(V3(-20,20,20),2, Color(255,255,255))
r.scene = [
    Sphere(V3(0, -1.5, -10), 1.5, ivory),
    # Sphere(V3(-2, -1, -12), 0.5, mirror),
    Sphere(V3(1, 1, -8), 1.7, rubber),
    Sphere(V3(-3, 3, -10), 2, mirror),
]
# r.scene = [
#     #izquierda
#     Sphere(V3(-7,0, -20),1,red_clay),
#     Sphere(V3(-6,3, -20),1,red_clay),
#     #derecha
#     Sphere(V3(-3,0, -20),1,red_clay),
#     Sphere(V3(-4,3, -20),1,red_clay),
#     #cabeza
#     Sphere(V3(-5,-2, -20),1.5,red_clay),
#     #eyes
#     Sphere(V3(-5,-2.5, -18),0.2,black),
#     Sphere(V3(-4,-2.5, -18),0.2,black),
#     #body
#     Sphere(V3(-5,1, -20),2,rubber),
#     #parte de nariz
#     Sphere(V3(-4.65,-1.5, -18.5),0.5,red_clay),
#     #nariz
#     Sphere(V3(-4.5,-1.5, -18),0.2,black),
#     #ears
#     Sphere(V3(-6,-3.5, -20),0.5,red_clay),
#     Sphere(V3(-4,-3.5, -20),0.5,red_clay),
    
#     #izquierda
#     Sphere(V3(7,0, -20),1,grass),
#     Sphere(V3(6,3, -20),1,grass),
#     #derecha
#     Sphere(V3(3,0, -20),1,grass),
#     Sphere(V3(4,3, -20),1,grass),
#     #cabeza
#     Sphere(V3(5,-2, -20),1.5,grass),
#     #eyes
#     Sphere(V3(5,-2.5, -18),0.2,black),
#     Sphere(V3(4,-2.5, -18),0.2,black),
#     #body
#     Sphere(V3(5,1, -20),2,ivory),
#     #parte de nariz
#     Sphere(V3(4.65,-1.5, -18.5),0.5,grass),
#     #nariz
#     Sphere(V3(4.5,-1.5, -18),0.2,black),
#     #ears
#     Sphere(V3(6,-3.5, -20),0.5,grass),
#     Sphere(V3(4,-3.5, -20),0.5,grass),    
# ]
#r.probability(0.1)
r.render()

r.write('prueba.bmp')