# -*- coding: utf-8 -*-

"""
Created on Tue May 23 16:53:22 2017

@author: rsr708
"""
from math import acos, sqrt, degrees, pi

# Implement Vector module
class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
            
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
            
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
            
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    
    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def plus(self, v):
        r = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(r)
    
    def minus(self, v):
        r = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(r)
    
    def scalar_mult(self, s):
        r = [s*x for x in self.coordinates]
        return Vector(r)

    def magnatude(self):
        s = [x**2 for x in self.coordinates]
        return sqrt(sum(s))
    
    def normalize(self):
        try:
            return self.scalar_mult(1.0/self.magnatude())
        
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zeor vector')
            
    def dot_product(self, s):
        dp = [x*y for x, y in zip(self.coordinates, s.coordinates)]
        return sum(dp)

    def theta(self, s, t='rad'):
        r = acos(self.dot_product(s) / (self.magnatude() * s.magnatude()))
        if t == 'degrees':
            r = degrees(r)
        return r
    
    def is_orthoginal(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) 
    
    def is_parallel_to(self, s):
        return ( self.is_zero() or
                 s.is_zero() or
                 self.theta(v) == 0 or
                 self.theta(v) == pi )
        
    def proj(self, v):
        return v.normalize().scalar_mult(self.dot_product(v.normalize()))
    
    def perp(self, v):
        return self.plus(self.proj(v).scalar_mult(-1))

    def cross_product(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
        
            return Vector([(y1*z2 - y2*z1),
                           -(x1*z2 - x2*z1),
                            x1*y2 - x2*y1])
    
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                newme = Vector(self.coordinates + (0,))
                return newme.cross_product(Vector(v.coordinates + (0,)))
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
    
    def cp_area(self, v):
        return sqrt(sum([x**2 for x in self.cross_product(v).coordinates]))
    
    def cp_triangle_area(self, v):
        return self.cp_area(v) / 2
    
v0 = Vector([5,3])
w0 = Vector([-1, 0])

print(v0.cross_product(w0))
print(v0.cp_area(w0))

v1 = Vector([8.462, 7.893, -8.187])
w1 = Vector([6.984, -5.975, 4.778])

print("v1 x w1 = ", v1.cross_product(w1))

v2 = Vector([-8.987, -9.838, 5.031])
w2 = Vector([-4.268, -1.861, -8.866])

print("Area of parallelogram", v2.cp_area(w2))

v3 = Vector([1.5, 9.547, 3.691])
w3 = Vector([-6.007, 0.124, 5.772])

print("Area of triangle = ", v3.cp_area(w3) / 2)
print("Area of triangle = ", v3.cp_triangle_area(w3))

#v1 = Vector([3.039, 1.879])
#b1 = Vector([0.825, 2.036])
#
#print("proj_b(v) = ", v1.proj(b1))
#
#v2 = Vector([-9.88, -3.264, -8.159])
#b2 = Vector([-2.155, -9.353, -9.473])
#
#print("v_perp = ", v2.perp(b2))
#
#v3 = Vector([3.009, -6.172, 3.692, -2.51])
#b3 = Vector([6.404, -9.144, 2.759, 8.718])
#
#print("v = ", v3.proj(b3), " + ", v3.perp(b3))

#v1 = Vector([-7.579, -7.88])
#w1 = Vector([22.737, 23.64])
#
#print(v1.dot_product(w1))
#
#v2 = Vector([-2.029, 9.97, 4.172])
#w2 = Vector([-9.231, -6.639, -7.245])
#print(v2.dot_product(w2))
#print([y/x for x, y in zip(v2.coordinates, w2.coordinates)])
#
#v3 = Vector([-2.328, -7.284, -1.214])
#w3 = Vector([-1.821, 1.072, -2.94])
#print(v3.dot_product(w3))
#print([y/x for x, y in zip(v3.coordinates, w3.coordinates)])

#v1 = Vector([7.887, 4.138])
#w1 = Vector([-8.802, 6.776])
#print("v1 * v2 = ", v1.dot_product(w1))
#
#v2 = Vector([-5.955, -4.904, -1.874])
#w2 = Vector([-4.496, -8.755, 7.103])
#print("v2 * w2 = ", v2.dot_product(w2))
#
#v3 = Vector([3.183, -7.627])
#w3 = Vector([-2.668, 5.319])
#print("Theta(v3, w3) = ", v3.theta(w3))
#
#v4 = Vector([7.35, 0.221, 5.188])
#w4 = Vector([2.751, 8.259, 3.985])
#print("Theta(v4, w4) = ", v4.theta(w4, 'degrees'))

#v1 = Vector([1,2,-1])
#v2 = Vector([3,1,0])
#
#print(v1.dot_product(v2))
#print(v1.theta(v2))

#v1 = Vector([-0.221, 7.437])
#print(v1.magnatude())
#v2 = Vector([8.813, -1.331, -6.247])
#print(v2.magnatude())
#v3 = Vector([5.581, -2.136])
#print(v3.normalize())
#v4 = Vector([1.996, 3.108, -4.554])
#print(v4.normalize())

#print(Vector([8.218, -9.341]).plus(Vector([-1.129, 2.111])))
#print(Vector([7.119, 8.215]).minus(Vector([-8.223, 0.878])))
#print(Vector([1.671, -1.012, -0.318]).scalar_mult(7.41))