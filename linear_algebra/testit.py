#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 10:59:01 2017

@author: mark
"""

from line import Line

l1 = Line([3, -2], 1)
l2 = Line([-6, 4], 0)

print('// = ', l1.is_parallel(l2))

print("not //", Line([1, 2], 3).is_parallel(Line([1, -1], 2)))