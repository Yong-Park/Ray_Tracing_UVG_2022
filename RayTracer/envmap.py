import struct
from math import *
from lib import *

class Envmap(object):

  # Método constructor de la clase Envmap.
  def __init__(self, path):
    self.path = path
    self.__read()

  # Método para leer el archivo que se pase a la instancia.
  def __read(self):

    # Lectura del archivo con la función open().
    with open(self.path, "rb") as image:

      # Salto del header y obtención del width y height de la imagen.
      image.seek(2 + 4 + 2 + 2)
      header_size = struct.unpack("=l", image.read(4))[0]
      image.seek(2 + 4 + 2 + 2 + 4 + 4)
      self.width = struct.unpack("=l", image.read(4))[0]
      self.height = struct.unpack("=l", image.read(4))[0]
      image.seek(header_size)
      self.pixels = []

      # Definición de los pixeles de la imagen de Envmap.
      for y in range(self.height):
        self.pixels.append([])
        for x in range(self.width):
          b = ord(image.read(1))
          g = ord(image.read(1))
          r = ord(image.read(1))
          self.pixels[y].append(Color(r, g, b))

  # Método para obtener el color de un pixel del Envmap.
  def get_color(self, direction):

    # Obtención de los valores de x e y para pintar.
    normalized_direction = direction.norm()
    x = round(((atan2(normalized_direction.z, normalized_direction.x) / (2 * pi)) + 0.5) * self.width)
    y = (-1 * round((acos((-1 * normalized_direction.y)) / pi) * self.height))

    # Arreglo de problemas con índices.
    x -= 1 if (x > 0) else 0
    y -= 1 if (y > 0) else 0

    # Retorno del color encontrado.
    return self.pixels[y][x]
        


        