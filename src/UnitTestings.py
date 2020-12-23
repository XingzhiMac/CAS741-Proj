import math
import numpy as np
#from DataModules import *
from AnalysisModules import *


#------------------ Unit Tests for Point module --------------#
print("#------------------ Unit Tests for Point module --------------#")
a = Point(0,0)
print("point a:", a.get_coordinates(), ", should be (0,0)")

b = Point(3,4)
print("point b:", b.get_coordinates(), ", should be (3,4)")

c = Point(1,10)
print("point c:", c.get_coordinates(), ", should be (1,10)")

d = Point(3,0)
print("point d:", d.get_coordinates(), ", should be (3,0)")

print()

#------------------ Unit Tests for Wall module --------------#
print("#------------------ Unit Tests for Wall module --------------#")
w1 = Wall(a,c,0.1,0.5) # normal wall
print("wall a-c:")
print("equation: ", w1.m1, "x + ", w1.m2, "y = ", w1.k, " or")
print(w1.m2, "y = ", -w1.m1, "x + ", w1.k)
print("correct equation: y = 10x")
print("unit normal vector: [", w1.n1, w1.n2, "]")
print("correct unit normal vector: [ .9950    -.0995 ] or [ -.9950    .0995 ]\n")

w2 = Wall(b,c,0.1,0.5) # normal wall
print("wall b-c:")
print("equation: ", w2.m1, "x + ", w2.m2, "y = ", w2.k, " or")
print(w2.m2, "y = ", -w2.m1, "x + ", w2.k)
print("correct equation: y = -3x + 13")
print("unit normal vector: [", w2.n1, w2.n2, "]")
print("correct unit normal vector: [ .9487    .3162 ] or [ -.9487    -.3162 ]\n")

w3 = Wall(a,b,0.1,0.5) # normal wall
print("wall a-b:")
print("equation: ", w3.m1, "x + ", w3.m2, "y = ", w3.k, " or")
print(w3.m2, "y = ", -w3.m1, "x + ", w3.k)
print("correct equation: y = 4x/3")
print("unit normal vector: [", w3.n1, w3.n2, "]")
print("correct unit normal vector: [ .8    -.6 ] or [ -.8    .6 ]\n")

w4 = Wall(b,d,0.1,0.5) # vertical wall
print("wall b-d:")
print("equation: ", w4.m1, "x + ", w4.m2, "y = ", w4.k, " or")
print(w4.m2, "y = ", -w4.m1, "x + ", w4.k)
print("correct equation: x = 3")
print("unit normal vector: [", w4.n1, w4.n2, "]")
print("correct unit normal vector: [ 1    0 ] or [ -1    0 ]\n")

#------------------ Unit Tests for Linear Path module --------------#
print("#------------------ Unit Tests for Linear Path module --------------#")
tsm = Point(-2,2)
sp1 = Point(13,2)
sp2 = Point(4,5)
sp3 = Point(-2,10)

path1 = LinearPath(tsm, sp1) # horizontal path
print("path 1:")
print("equation: ", path1.m1, "x + ", path1.m2, "y = ", path1.k, " or")
print(path1.m2, "y = ", -path1.m1, "x + ", path1.k)
print("correct equation: y = 2")
print("length: ", path1.length)
print("correct length: 15\n")

path2 = LinearPath(tsm, sp2) # normal path
print("path 2:")
print("equation: ", path2.m1, "x + ", path2.m2, "y = ", path2.k, " or")
print(path2.m2, "y = ", -path2.m1, "x + ", path2.k)
print("correct equation: y = 0.5x + 3")
print("length: ", path2.length)
print("correct length: 6.7082\n")

path3 = LinearPath(tsm, sp3) # vertical path
print("path 3:")
print("equation: ", path3.m1, "x + ", path3.m2, "y = ", path3.k, " or")
print(path3.m2, "y = ", -path3.m1, "x + ", path3.k)
print("correct equation: x = -2")
print("length: ", path3.length)
print("correct length: 8\n")

#------------------ Unit Tests for Intersection module --------------#
print("#------------------ Unit Tests for Intersection module --------------#")
wall1 = Wall(a,c,0.1,0.5)
wall2 = Wall(b,c,0.1,0.5)
wall3 = Wall(a,b,0.1,0.5)
wall4 = Wall(b,d,0.1,0.5)

path1 = LinearPath(tsm, sp1)
path2 = LinearPath(tsm, sp2)
path3 = LinearPath(tsm, sp3)

m = Intersection.find_intersection(wall1, path1)
validity = Intersection.is_valid(wall1, path1)
print("wall a-c and path1:\nintersects at: ", m.get_coordinates())
print("supposed to be (0.2, 2)")
print("validity of the intersection: ", validity)
print("supposed to be 1\n")

m = Intersection.find_intersection(wall4, path3)
validity = Intersection.is_valid(wall4, path3)
print("wall b-d and path3:\nintersects at: ", m.get_coordinates())
print("supposed to be: (0, 0)")
print("validity of the intersection: ", validity)
print("supposed to be 0\n")

m = Intersection.find_intersection(wall3, path3)
validity = Intersection.is_valid(wall3, path3)
print("wall a-b and path3:\nintersects at: ", m.get_coordinates())
print("supposed to be: (-2, -2.667)")
print("validity of the intersection: ", validity)
print("supposed to be 0\n")

#------------------ Unit Tests for LinearLoss module --------------#
print("#------------------ Unit Tests for LinearLoss module --------------#")
wall1 = Wall(a,c,0.1,0.5)
wall2 = Wall(b,c,0.1,0.5)
wall3 = Wall(a,b,0.1,0.5)
walls = [wall1,wall2,wall3]
frequency = 2480*10**6
flm = FloorMap(walls)

path1 = LinearPath(tsm, sp1)
path2 = LinearPath(tsm, sp2)
path3 = LinearPath(tsm, sp3)

lpl = LinearLoss.find_linear_path_loss(path1, (2480*10**6), flm)
print("Linear path loss for path1 = ", lpl)
print("supposed to be: 4.1185*10^-09\n")

#------------------ Unit Tests for Specular Reflection module --------------#
print("#------------------ Unit Tests for Specular Reflection module --------------#")
wall1 = Wall(a,c,0.1,0.5)
wall2 = Wall(b,c,0.1,0.5)
wall3 = Wall(a,b,0.1,0.5)
start = Point(-2,2)
end = Point(-1,3)

path1, path2, ind = Specular.get_mirrored_paths(wall1, start, end)
print("test 1:")
print("first half (path1):")
print("starts at: ", path1.start.get_coordinates())
print("supposed to be: (-2, 2)")
print("ends at: ", path1.end.get_coordinates())
print("supposed to be: (0.1782, 1.782)")
print("length: ", path1.length)
print("correct length: 2.189")
print("second half (path2):")
print("starts at: ", path2.start.get_coordinates())
print("supposed to be: (0.1782, 1.782)")
print("ends at: ", path2.end.get_coordinates())
print("supposed to be: (-1, 3)")
print("length: ", path2.length)
print("correct length: 1.694")
print("validity = ", ind, ", supposed to be 1\n")

path1, path2, ind = Specular.get_mirrored_paths(wall2, start, end)
print("test 2:")
print("validity = ", ind, ", supposed to be 0\n")
