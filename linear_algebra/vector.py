from math import acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in 2 or 3 dimensions'
    
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __getitem__(self, i):
        return self.coordinates[i]
    
    def __iter__(self):
        return self.coordinates.__iter__()
    
    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        r = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(r)
    
    def minus(self, v):
        r = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(r)
    
    def times_scalar(self, c):
        r = [Decimal(c)*x for x in self.coordinates]
        return Vector(r)

    def magnatude(self):
        s = [x**Decimal('2.0') for x in self.coordinates]
        return sum(s).sqrt()
    
    def normalized(self):
        try:
            return self.times_scalar(Decimal('1.0')/self.magnatude())
        
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zeor vector')
            
    def dot(self, s):
        dp = [x*y for x, y in zip(self.coordinates, s.coordinates)]
        return sum(dp)

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot(u2))
            
            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannont compute an angle with the zero vector')
            else:
                raise e
    
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance
    
    def is_parallel_to(self, v):
        return ( self.is_zero() or
                 v.is_zero() or
                 self.angle_with(v) == 0 or
                 self.angle_with(v) == pi )
        
    def proj(self, v):
        return v.normalize().scalar_mult(self.dot_product(v.normalize()))
    
    def is_zero(self, tolerance=1e-10):
        return self.magnatude() < tolerance
    
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
                
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
        
            return Vector([(y1*z2 - y2*z1),
                           -(x1*z2 - x2*z1),
                            x1*y2 - x2*y1])
    
        except ValueError as e:
            msg = str(e)
            if msg == 'not enough values to unpack (expected 3, got 2)':
                newme = Vector(self.coordinates + (0,))
                return newme.cross_product(Vector(v.coordinates + (0,)))
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
    
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')
    
    def area_of_parallelogram(self, v):
        return self.cross(v).magnitude()


#v1 = Vector(['3', '-2'])
#v2 = Vector(['-6', '4'])
#
#v1.is_orthoginal(v2)
#
#v1.is_parallel_to(v2)