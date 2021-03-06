import math

from random import random, uniform, seed

import pyglet

from pyglet.gl import *

from entity.square import square
from util.vector2 import rotate_vector

class scene(object):
    def __init__(self, world, **kwargs):
        self.entities = []
        self.world = world

        assert self.world is not None, "Invalid world."

        self.offset_x = kwargs.get('offset_x', 0)
        self.offset_y = kwargs.get('offset_y', 0)
        self.width = kwargs.get('width', 300)
        self.height = kwargs.get('height', 300)

        self.top_left = dict(x = self.offset_x, y = self.offset_y)
        self.top_right = dict(x = self.offset_x + self.width, y = self.offset_y)
        self.bottom_left = dict(x = self.offset_x, y = self.offset_y + self.height)
        self.bottom_right = dict(x = self.offset_x + self.width, y = self.offset_y + self.height)

        # generating background
        self.background = []
        self.seed = 1337

        max_depth = .2

        for i in xrange(0, 500):
            seed(self.seed + i * 10293)

            # # determine i-th star's position
            basePosition = (random() * self.world.width, random() * self.world.height);
            depth = uniform(.001, max_depth)
            color = [random(), random(), random(), depth/max_depth]

            self.background.append((basePosition, depth, color))

    # find another way, using raw opengl- still showing signs of inefficency but better. need to figure out how to color the dots 
    def draw_background(self):
        varray = []
        carray = []
        x = self.top_left['x']
        y = self.top_left['y']
        
        for _ in self.background:
            basePosition = _[0]
            depth = _[1]
            color = _[2]

            #parallax scrolling and wrapping
            realPosition = (basePosition[0] + x * depth, basePosition[1] + y * depth)
            wrappedPosition = ( realPosition[0] % self.world.width, realPosition[1] % self.world.height)
            varray += [wrappedPosition[0], wrappedPosition[1], 0]
            carray += color

        # # needs to be commented and understood..
        # glEnable(GL_BLEND)
        # glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        # point_size = GLfloat(10.0)
        # glGetFloatv(GL_POINT_SIZE_MAX_ARB, point_size)
        # glPointSize(point_size)
        # glPointParameterfvARB(GL_POINT_DISTANCE_ATTENUATION_ARB, (GLfloat * 3)(0, 0, 5))
        # glPointParameterfARB(GL_POINT_SIZE_MIN_ARB, 5)
                
        varray = (GLfloat * len(varray))(*varray)
        carray = (GLfloat * len(carray))(*carray)

        glVertexPointer(3, GL_FLOAT, 0, varray)
        glColorPointer(4, GL_FLOAT, 0, carray)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        glDrawArrays(GL_POINTS, 0, len(varray)//3)
        glDisableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);

    def update(self):
        # ask the world for the objects we should render
        self.entities = self.world.get_entities_in(self.top_left, self.top_right, self.bottom_left, self.bottom_right)

    def render(self):
        # get all the entities and draw them
        entities = sorted(self.entities, key = lambda e: e.z_index)
        
        for e in entities:
            e.draw(self.top_left['x'], self.top_left['y'], self.height)

    def translateX(self, x):
        if self.top_left['x'] + x < 0 or self.top_right['x'] + x > self.world.width:
            x = 0

        self.top_left['x'] += x
        self.top_right['x'] += x
        self.bottom_left['x'] += x
        self.bottom_right['x'] += x

    def translateY(self, y):
        if self.top_left['y'] + y < 0 or self.bottom_left['y'] + y > self.world.height:
            y = 0

        self.top_left['y'] += y
        self.top_right['y'] += y
        self.bottom_left['y'] += y
        self.bottom_right['y'] += y

    # does not work correctly, interesting though
    def rotate(self, angle):
        self.top_left = rotate_vector(self.top_left, angle)
        self.top_right = rotate_vector(self.top_right, angle)
        self.bottom_left = rotate_vector(self.bottom_left, angle)
        self.bottom_right = rotate_vector(self.bottom_right, angle)

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)