import random
from math import *
from sphere import *
from lib import *
from vector import *
from material import *
from light import *
from plane import *
from envmap import *
from texture import *
from cube import *
from triangle import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.clear_color = Color(255,255,255)
        self.current_color = Color(255,255,255)
        self.clear()
        self.scene = []
        self.active_texture = None
        self.envmap = None
        self.light = Light(V3(20,-20,-20),2, Color(255,255,255))
        self.prob = None

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
    def paint_backgound(self,direction):
        return self.envmap.get_color(direction) if (self.envmap is not None) else self.clear_color

    def cast_ray(self,origin,direction, recursion = 0):
        if recursion >= MAX_RECURSION_DEPTH:
            return self.paint_backgound(direction)

        material, intersect = self.scene_intersect(origin,direction)

        if material is None:
            return self.paint_backgound(direction)

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
            reflect_direction = reflect(direction,intersect.normal)
            reflect_bias = -0.5 if reflect_direction @ intersect.normal < 0 else 0.5
            reflect_origin = intersect.point + (intersect.normal * reflect_bias) 
            reflect_color = self.cast_ray(reflect_origin,reflect_direction, recursion + 1)
        else:
            reflect_color = Color(0,0,0)
        reflection = reflect_color * material.albedo[2]

        if (material.albedo[3] > 0):
            refraction_direction = refract(direction, intersect.normal, material.refractive_index)
            refraction_bias = -0.5 if ((refraction_direction @ intersect.normal) < 0) else 0.5
            refraction_origin = (intersect.point + (intersect.normal * refraction_bias))
            refract_color = self.cast_ray(refraction_origin, refraction_direction, (recursion + 1))
        else:
            refract_color = Color(0, 0, 0)
        refraction = refract_color * material.albedo[3]

        return diffuse + specular + reflection + refraction

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
rubber = Material(diffuse=Color(130,0,0), albedo = [0.9,0.1,0,0], spec = 10)
ivory = Material(diffuse=Color(255,255,255), albedo = [0.6,0.3,0.1,0], spec = 50)
red_clay = Material(diffuse=Color(255,0,0), albedo = [0.9,0.1], spec = 50)
black = Material(diffuse=Color(255,0,0), albedo = [0.04,0.96], spec = 50)
grass = Material(diffuse=Color(0,255,0), albedo = [0.03
                                                   
                                                   ,0.97], spec = 50)

#materiales a utilizar
ocean = Material(diffuse=Color(43,101,236), albedo = [0.9,0.10,0,0], spec = 0)
mirror = Material(diffuse=Color(255,255,255), albedo = [0,1,0.8, 0], spec = 1425)
glass = Material(diffuse = Color(150, 180, 200), albedo = [0, 0.5, 0, 0.8], spec = 125, refractive_index = 1.5)
Darkwood = Material(diffuse=Color(109,65,48), albedo = [0.9,0.1,0,0], spec = 0)
leaves = Material(diffuse=Color(125,255,50), albedo = [0.8,0.2,0,0], spec = 0)
red = Material(diffuse=Color(255,0,0), albedo = [0.8,0.2,0,0], spec = 1)
cement = Material(diffuse=Color(162,162,162), albedo = [0.5,0.5,0,0], spec = 0)
piel = Material(diffuse=Color(247, 220, 199), albedo = [0.7,0.2,0,0], spec = 0)
white = Material(diffuse=Color(255, 255, 255), albedo = [0,1,0,0], spec = 0)
sun = Material(diffuse=Color(255, 255, 0), albedo = [0.9,0.1,0,0], spec = 1)

r = Raytracer(1800,1000)
r.envmap = Envmap('./RayTracer/bg.bmp')
r.light = Light(V3(-20,20,20),2, Color(255,255,255))
r.scene = [
    #arbol que esta en la izquierda
    Cubo(V3(-11,2,-15),1,Darkwood),
    Cubo(V3(-11,1,-15),1,Darkwood),
    Cubo(V3(-11,0,-15),1,Darkwood),
    Cubo(V3(-11,-1,-15),1,Darkwood),
    Cubo(V3(-11,-2,-15),1,Darkwood),
    Cubo(V3(-11,-3,-15),1,leaves),
    Cubo(V3(-10,-3,-15),1,leaves),
    Cubo(V3(-9,-3,-15),1,leaves),
    Cubo(V3(-10,-3,-14),1,leaves),
    Cubo(V3(-10,-3,-16),1,leaves),
    Cubo(V3(-12,-3,-15),1,leaves),
    Cubo(V3(-13,-3,-15),1,leaves),
    Cubo(V3(-12,-3,-14),1,leaves),
    Cubo(V3(-12,-3,-16),1,leaves),
    Cubo(V3(-11,-3,-14),1,leaves),
    Cubo(V3(-11,-3,-13),1,leaves),
    Cubo(V3(-11,-3,-16),1,leaves),
    Cubo(V3(-11,-3,-17),1,leaves),
    Cubo(V3(-11,-4,-15),1,leaves),
    Cubo(V3(-10,-4,-15),1,leaves),
    Cubo(V3(-12,-4,-15),1,leaves),
    Cubo(V3(-11,-4,-14),1,leaves),
    Cubo(V3(-11,-4,-16),1,leaves),
    Cubo(V3(-11,-5,-15),1,leaves),
    #manzana del arbol de la izquierda
    Sphere(V3(-10, -2.3, -16), 0.25, red),
    
    #piscina
    Cubo(V3(5, 2,-13),1, cement), Cubo(V3(6, 2,-13),1, cement), Cubo(V3(7, 2,-13),1, cement), Cubo(V3(8, 2,-13),1, cement),
    Cubo(V3(5, 2,-12),1, cement), Cubo(V3(6, 2,-12),1, ocean), Cubo(V3(7, 2,-12),1, ocean), Cubo(V3(8, 2,-12),1, cement),
    Cubo(V3(5, 2,-11),1, cement),Cubo(V3(6, 2,-11),1, ocean), Cubo(V3(7, 2,-11),1, ocean), Cubo(V3(8, 2,-11),1, cement),
    Cubo(V3(5, 2,-10),1, cement), Cubo(V3(6, 2,-10),1, cement), Cubo(V3(7, 2,-10),1, cement), Cubo(V3(8, 2,-10),1, cement),
    
    #persona
    Triangulo(V3(1.75,1,-10),0.25,rubber),
    Cubo(V3(2, 0,-12),1, piel),
    Cubo(V3(2.2, 0,-11),0.1, white),
    Cubo(V3(2.2, -0.1,-11),0.1, white),
    Cubo(V3(2, -0.05,-10),0.05, leaves),
    
    Cubo(V3(1.8, 0,-11),0.1, white),
    Cubo(V3(1.8, -0.1,-11),0.1, white),
    Cubo(V3(1.65, -0.05,-10),0.05, leaves),
    
    Cubo(V3(2, 1,-12),1, Darkwood),
    Cubo(V3(2, 2,-12),1, Darkwood),
    
    #sol
    Sphere(V3(7,-6,-20),1,sun),
    
    #bola de espejo
    Sphere(V3(1.7,0.5,-10),0.2,mirror),
    

    
]
r.render()

r.write('Proyecto2.bmp')

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