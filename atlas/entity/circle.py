import pyglet
import math

from pyglet.gl import *

from entity import entity
class circle(entity):
    def __init__(self, **kwargs):
        super(circle, self).__init__(**kwargs)
        self.radius = kwargs.get('radius', 50)
        self.num_vertices = kwargs.get('num_vertices', 20)
        for i in xrange(0, self.num_vertices):
            theta = 2.0 * math.pi * (float(i)/self.num_vertices); #get the current angle 
            x = self.radius * math.cos(theta) #calculate the x component 
            y = self.radius * math.sin(theta) #calculate the y component 
            self.vertices += [dict(x=x,y=y)];