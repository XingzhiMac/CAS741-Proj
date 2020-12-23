import math
import numpy as np
import CustomErrors

#-------------------- Data structure of type Point ---------------------#
class Point:
# The Point module stores the 2-D Cartesian coordinates of a point.
# It contains a getter and a setter function to read and return the
# 2-D coordinates in addition to the create() function.
    x = 0 # x-coordinate of the Point
    y = 0 # y-coordinate of the Point

    def __init__(self, x_coordinate, y_coordinate):
    # Given x- and y- coordinates, create a new Point.
        self.x = x_coordinate
        self.y = y_coordinate

    def set_coordinates(self, x_coordinate, y_coordinate):
    # Change or update the x- and y- coordinates of the Point.
        self.x = x_coordinate
        self.y = y_coordinate

    def get_coordinates(self):
    # Get the x- and y- coordinates of the Point.
        return self.x, self.y


#--------------------- Data structure of type Wall ----------------------#
class Wall:
# The Wall module stors the vertices, transmittance, reflectance, and
# parameters of the linear equation as well as the unit normal vector
# of the wall.
    start = 0 # Starting vertex of the wall
    end = 0 # End vertex of the wall
    transmittance = 0 # As is.
    reflectance = 0 # As is.
    m1 = 0 # Parameter of the linear equation
    m2 = 0 # Parameter of the linear equation
    k = 0 # Parameter of the linear equation
    n1 = 0 # Parameter of the wall's unit normal vector 
    n2 = 0 # Parameter of the wall's unit normal vector
    
    def __init__(self, start, end, transmittance, reflectance):
    # Given parameters required in MIS, create a new Wall.
        try:
            if (start.get_coordinates() == end.get_coordinates()):
                raise CustomErrors.InvalidWall
        except CustomErrors.InvalidWall:
            print("The wall cannot have zero length!")
            print()
            exit("Error: InvalidWall")
        self.start = start
        self.end = end
        self.transmittance = transmittance
        self.reflectance = reflectance
        self.m1, self.m2, self.k = EquationFinder.find_equation(self.start, self.end)
        self.n1, self.n2 = self.find_unit_normal(self.start, self.end)

    def set_start_point(self, start):
    # Change or update the starting vertex of the wall
        try:
            if (start.get_coordinates() == self.end.get_coordinates()):
                raise InvalidWall
        except InvalidWall:
            print("The wall cannot have zero length!")
            print()
            exit("Error: InvalidWall")
        self.start = start
        self.m1, self.m2, self.k = EquationFinder.find_equation(self.start, self.end)
        self.n1, self.n2 = self.find_unit_normal(self.start, self.end)

    def set_start_point(self, end):
    # Change or update the end vertex of the wall
        try:
            if (self.start.get_coordinates() == end.get_coordinates()):
                raise InvalidWall
        except InvalidWall:
            print("The wall cannot have zero length!")
            print()
            exit("Error: InvalidWall")
        self.end = end
        self.m1, self.m2, self.k = EquationFinder.find_equation(self.start, self.end)
        self.n1, self.n2 = self.find_unit_normal(self.start, self.end)

    def get_start_point(self):
    # Return the starting point
        return self.start

    def get_end_point(self):
    # Return the end point
        return self.end

    def set_transmittance(self, transmittance):
    # Change or update the transmittance of the wall
        self.transmittance = transmittance

    def set_reflectance(self, reflectance):
    # Change or update the reflectance of the wall
        self.reflectance = reflectance

    def get_transmittance(self):
    # Return the transmittance of the wall
        return self.transmittance

    def get_reflectance(self):
    # Return the reflectance of the wall
        return self.reflectance

    def get_unit_normal(self):
    # Return the parameters of the wall's unit normal vector
        return self.n1, self.n2

    def get_line_equation(self):
    # Return the parameters of the wall's linear equation
        return self.m1, self.m2, self.k
        
    # Local functions
    def find_unit_normal(self, C, D):
    # Find parameters of the wall's unit normal vector 
        x_C, y_C = C.get_coordinates()
        x_D, y_D = D.get_coordinates()
        denom = 1/math.sqrt(float(y_D-y_C)**2+float(x_D-x_C)**2)
        n1 = (y_D-y_C)*denom
        n2 = (x_C-x_D)*denom
        return n1,n2
    # Local functions end


#--------------------- Data Structure of Linear Signal Path ----------------------#
class LinearPath:
# The LinearPath Module stores the start point, the end point, the equation of the
# point, and the length of the path

    start = 0 # Starting vertex of the linear path
    end = 0 # End vertex of the linear path
    m1 = 0 # Parameter of the linear equation
    m2 = 0 # Parameter of the linear equation
    k = 0 # Parameter of the linear equation
    length = 0 # Length of the linear path from the starting point to the end point
    
    def __init__(self, start, end):
    # Create a new linear path with the given starting and end points
        self.start = start
        self.end = end
        self.m1, self.m2, self.k = EquationFinder.find_equation(self.start, self.end)
        start_x, start_y = self.start.get_coordinates()
        end_x, end_y = self.end.get_coordinates()
        self.length = math.sqrt(float(end_x-start_x)**2+float(end_y-start_y)**2)

    def get_start_point(self):
    # Return the starting point of the path's linear euqation
        return self.start

    def get_end_point(self):
    # Return the end point of the path's linear euqation
        return self.end

    def get_line_equation(self):
    # Return the parameters of the path's linear equation
        return self.m1, self.m2, self.k

    def get_length(self):
    # Return the parameters of the path's linear equation
        return self.length


#--------------------- Methods of Equation Finder ----------------------#
class EquationFinder:
# The EquationFinder finds the linear equation of a line in a 2-D space.

    def find_equation(C, D):
    # Given two points, find the linear expression of the line passing
    # through those points.
        x_C, y_C = C.get_coordinates()
        x_D, y_D = D.get_coordinates()
        if (x_D-x_C) == 0:
            m1 = 1
            m2 = 0
        else:
            m1 = -1.0*(y_D-y_C)/(x_D-x_C)
            m2 = 1
        k = 1.0*(m1*x_C+m2*y_C)
        k2 = 1.0*(m1*x_D+m2*y_D)
        return m1, m2, k

#------------------------ Methods of Inesecion -------------------------#
class Intersection:

    def find_intersection(wall, path):
    # Given a wall and a linear signal path, find their intersection point
        M11 = wall.m1
        M12 = wall.m2
        M21 = path.m1
        M22 = path.m2
        K1 = wall.k
        K2 = path.k
        M = np.array([[M11, M12], [M21, M22]])
        K = np.array([K1, K2])
        if np.linalg.det(M) == 0:
            intersection = Point(0, 0)
        else:
            t = np.linalg.solve(M, K)
            intersection = Point(t[0], t[1])
        return intersection

    def is_valid(wall, path):
    # Given a wall and a linear signal path, find the validity of their intersection point
        M11 = wall.m1
        M12 = wall.m2
        M21 = path.m1
        M22 = path.m2
        K1 = wall.k
        K2 = path.k
        M = np.array([[M11, M12], [M21, M22]])
        K = np.array([K1, K2])

        wall_Cx = wall.start.x
        wall_Dx = wall.end.x
        wall_Cy = wall.start.y
        wall_Dy = wall.end.y
        path_Cx = path.start.x
        path_Dx = path.end.x
        path_Cy = path.start.y
        path_Dy = path.end.y
        if np.linalg.det(M) == 0:
            validity = 0
        else:
            t = np.linalg.solve(M, K)
            intersection = Point(t[0], t[1])
            if(
                max(min(wall_Cx, wall_Dx), min(path_Cx, path_Dx)) <= t[0] and
                min(max(wall_Cx, wall_Dx), max(path_Cx, path_Dx)) >= t[0] and
                max(min(wall_Cy, wall_Dy), min(path_Cy, path_Dy)) <= t[1] and
                min(max(wall_Cy, wall_Dy), max(path_Cy, path_Dy)) >= t[1]
            ):
                if(
                    (t[0] == wall_Cx and t[1] == wall_Cy) or
                    (t[0] == wall_Dx and t[1] == wall_Dy) or
                    (t[0] == path_Cx and t[1] == path_Cy) or
                    (t[0] == path_Dx and t[1] == path_Dy)
                ):
                    validity = 0
                else:
                    validity = 1
            else:
                validity = 0
        return validity
        
#--------------------- Methods of Specular Reflection Module ----------------------#
class Specular:
# Methods and steps to find the validity and potential paths of signal reflections.

    def get_mirrored_paths(wall, start, end):
    # Find the first and the second half of the reflected path, and the validity of reflection.
        n1 = wall.n1
        n2 = wall.n2
        n = np.array([n1,n2])
        t1 = wall.start.x
        t2 = wall.start.y
        t = np.array([t1, t2])
        p1 = start.x
        p2 = start.y
        p = np.array([p1,p2])
        x1 = p-t        #(p-t)
        x2 = np.dot(n,x1)  # n dot (p-t)
        image = p - n*2*x2     # Find the reflection of the end point with image source model
        p0 = Point(image[0], image[1]) # p0 is the Reflection image of the end point
        mirrored_path = LinearPath(start, p0)
        t0 = Intersection.find_intersection(wall, mirrored_path)
        ind = Intersection.is_valid(wall, mirrored_path)
        path1 = LinearPath(start, t0)
        path2 = LinearPath(t0, end)
        return path1, path2, ind
