import math
import numpy as np
from DataModules import *
from CustomErrors import *

#------------------ Data structure of Input Parameters ------------------#
class Param:
# The EquationFinder finds the linear equation of a line in a 2-D space.
    c_list = []
    d_list = []
    t_list = []
    r_list = []
    length_c, length_d, length_t, length_r = 0, 0, 0, 0
    sp_list = []
    frequency = 2480*10**6
    power = 0
    tsm = Point(-2, 2)
    
    def __init__(self):#tsmFile, spFile, wallFile):
    # Given two points, find the linear expression of the line passing
    # through those points.
        0 == 0

    def load_params(self, tsm_name, sp_name, wall_name):
        # Process transmitter info
        tsmFile = open(tsm_name, "r")
        tsm_list = tsmFile.readlines()
        # update position
        point_info = tsm_list[0].rstrip("\n").split('#')[0].split(',')
        x = float(point_info[0])
        y = float(point_info[1])
        try:
            if(
                x < SpecParam.x_min or
                x > SpecParam.x_max or
                y < SpecParam.y_min or
                y > SpecParam.y_max
            ):
                raise BadPosition
        except BadPosition:
            print("The transmitter falls outside of the target area!")
            exit()
        self.tsm = Point(x, y)
        # update frequency
        freq_info = tsm_list[2].rstrip("\n").split('#')[0].split(',')
        frequency = float(freq_info[0])
        try:
            if(
                frequency < SpecParam.f_min or
                frequency > SpecParam.f_max 
            ):
                raise BadSignalFrequency
        except BadSignalFrequency:
            print("Invalid signal frequency!")
            exit()
        self.frequency = frequency
        # update transmission power
        power_info = tsm_list[1].rstrip("\n").split('#')[0].split(',')
        power = float(power_info[0])
        try:
            if(
                power < SpecParam.power_min or
                power > SpecParam.power_max 
            ):
                raise BadTransmissionPower
        except BadTransmissionPower:
            print("Invalid transmission power level!")
            exit()
        self.power = power
        tsmFile.close()

        # Process sampling point info
        spFile = open(sp_name, "r")
        sp_info = spFile.readlines()
        sp_list = []
        # update positions
        for line in sp_info:
            xy = line.rstrip("\n").split(',')
            x = float(xy[0])
            y = float(xy[1])
            try:
                if(
                    x < SpecParam.x_min or
                    x > SpecParam.x_max or
                    y < SpecParam.y_min or
                    y > SpecParam.y_max
                ):
                    raise BadPosition
            except BadPosition:
                print("A sampling point falls outside of the target area!")
                exit()
            sp_list.append(Point(x, y))
        self.sp_list = sp_list
        spFile.close()
        
        # Process wall info
        wallFile = open(wall_name, "r")
        wall_info = wallFile.readlines()
        c = []
        d = []
        t = []
        r = []
        # get wall parameters
        for line in wall_info:
            wall_param = line.rstrip("\n").split(',')
            x_c = float(wall_param[0])
            y_c = float(wall_param[1])
            x_d = float(wall_param[2])
            y_d = float(wall_param[3])
            try:
                if(
                    (x_c or x_d) < SpecParam.x_min or
                    (x_c or x_d) > SpecParam.x_max or
                    (y_c or y_d) < SpecParam.y_min or
                    (y_c or y_d) > SpecParam.y_max
                ):
                    raise BadPosition
            except BadPosition:
                print("A wall exceeds the target area!")
                exit()
            c.append(Point(x_c, y_c))
            d.append(Point(x_d, y_d))
            transmittance = float(wall_param[4])
            try:
                if(
                    transmittance < SpecParam.t_min or
                    transmittance > SpecParam.t_max
                ):
                    raise BadTransmittance
            except BadTransmittance:
                print("Invalid transmittance!")
                exit()
            t.append(transmittance)
            reflectance = float(wall_param[5])
            try:
                if(
                    reflectance < SpecParam.r_min or
                    reflectance > SpecParam.r_max
                ):
                    raise BadReflectance
            except BadReflectance:
                print("Invalid reflectance!")
                exit()
            r.append(reflectance)
        # update and check wall parameter lists
        self.length_c = len(c)
        self.length_d = len(d)
        self.length_t = len(t)
        self.length_r = len(r)
        try:
            if not(
                self.length_c == self.length_d and
                self.length_c == self.length_t and
                self.length_c == self.length_r
            ):
                raise InconsistentWallParams
        except InconsistentWallParams:
            print("The numbers of wall parameters are not consistent!")
            exit()
        # update wall parameters
        self.c_list = c
        self.d_list = d
        self.t_list = t
        self.r_list = r
        wallFile.close()

    def updateMap(self, Map):
        self.floor_map = Map
        

#--------------------- Data structure of Floor Map ----------------------#
class FloorMap:
# FloorMap stors the wall map of the floor.
    wall_list = []
    length = 0

    def __init__(self, walls):
    # Create wall map from user inputs.
        self.quick_init(walls)
        
    def create(self, Param):
    # Create wall map from user inputs.
        c = Param.c_list
        d = Param.d_list
        t = Param.t_list
        r = Param.r_list
        walls = []
        for i in range(Param.length_c):
            walls.append(Wall(c[i], d[i], t[i], r[i]))
        self.wall_list = walls
        self.length = len(walls)

    def get_wall(self, index):
    # return the n-th wall in the map given the user input n
        try:
            if(
                index < 0 or
                index > (self.length - 1)
            ):
                raise InvalidIndex
            else:
                return self.wall_list[index]
        except InvalidIndex:
            print("The input index exceeds the size of the map!")
            print()

    def get_map(self):
    # return self
        return self

    def quick_init(self, walls):
    # Create wall map for testings
        self.wall_list = []
        for i in range(len(walls)):
            self.wall_list.append(walls[i])
        self.length = len(walls)

#--------------------- Methods of Linear Path Loss ----------------------#
class LinearLoss:
# Methods and steps to calculate propagation loss on a linear path.

    def find_linear_path_loss(path, frequency, Map):
    # Find linear path loss
        fspl = (math.pi*4*path.length*frequency/(3.0*10**8))**2
        T_total = 1
        for i in range(Map.length):
            wall = Map.get_wall(i)
            ind = Intersection.is_valid(wall, path)
            T_total = T_total * (wall.transmittance)**ind
        return T_total/fspl

#---------------- Data Structure of Line-Of-Sight Signal Module -----------------#
class LineOfSight:
# Data structure of line-of-sight signal.
    phi = 0
    
    def __init__(self, sp, Param):
    # given the sampling point, create the LineOfSight object
        self.sp = sp
        self.freq = Param.frequency
        self.tsm = Param.tsm
        self.path = LinearPath(self.tsm, self.sp)
        self.length = self.path.get_length()
        self.tsm_power = 10.0**((Param.power-30)/10.0)
        self.dbm = self.tsm_power*LinearLoss.find_linear_path_loss(
            self.path,
            self.freq,
            Param.floor_map.get_map()
        )

    def get_path_length(self):
        return self.length

    def get_amplitude(self):
        return self.dbm

    def get_phase_angle(self):
        return self.phi

#---------------- Data Structure of First-Order Reflection Signal Module -----------------#
class FirstOrderReflection:
# Data structure of first-order reflection signal.

    def __init__(self, sp, wall, los, Param):
    # given the sampling point, wall, line-of-sight signal, create the First-Order Reflection Signal
        self.sp = sp
        freq = Param.frequency
        self.tsm = Param.tsm
        self.tsm_power = 10.0**((Param.power-30)/10.0)
        self.path1,self.path2,self.ind = Specular.get_mirrored_paths(
            wall,
            self.tsm,
            self.sp
        )
        if self.ind == 1:
            self.length = self.path1.get_length() + self.path2.get_length()
            t1 = LinearLoss.find_linear_path_loss(
                self.path1,
                freq,
                Param.floor_map.get_map()
            )
            t2 = LinearLoss.find_linear_path_loss(
                self.path2,
                freq,
                Param.floor_map.get_map()
            )
            self.dbm = self.tsm_power*t1*t2*wall.get_reflectance()
            self.phi = 2*math.pi*(freq*(self.length - los.get_path_length())/(3*10**8)%1)
        else:
            self.dbm = 0
            self.phi = 0

    def get_amplitude(self):
        return self.dbm

    def get_phase_angle(self):
        return self.phi
    
#---------------- Methods of Received Signal Strength Module -----------------#
class ReceivedSignalStrength:

    def get_received_power(sp, Param):
    # Calculation of the received signal strength at tgiven sampling point.
        Map = Param.floor_map.get_map()
        los = LineOfSight(sp, Param)
        real = los.get_amplitude()*math.cos(los.get_phase_angle())*10**10
        imag = los.get_amplitude()*math.sin(los.get_phase_angle())*10**10
        fors = []
        for i in range(Map.length):
            wall = Map.get_wall(i)
            fors = FirstOrderReflection(sp, wall, los, Param)
            real += fors.get_amplitude()*math.cos(fors.get_phase_angle())*10**10
            imag += fors.get_amplitude()*math.sin(fors.get_phase_angle())*10**10
        amplitude = math.sqrt(real**2 + imag**2)*10**(-10)
        dbm = 30+10*math.log(amplitude,10)
        try:
            if( dbm >= Param.power ):
                raise InvalidReceivedStrength
            else:
                return dbm
        except InvalidReceivedStrength:
            print("Invalid result: something went wrong in the program!")
            print()

#--------------------- Method of Output Module ----------------------#
class Output:
# output results to the file with the name given by the user.
    def output(fileName, sp_list, sp_dbm_list):
        out = open(fileName, "w")
        for i in range(len(sp_list)):
            output_line = str(sp_list[i].get_coordinates())+ ', '+ str(sp_dbm_list[i])+'\n'
            out.write(output_line)
            out.flush()
        out.close()
        return True

#--------------------- Method of Output Module ----------------------#
class SpecParam:
# output results to the file with the name given by the user.
    power_max = 15
    power_min = -30
    f_min = 30
    f_max = 3*10**11
    x_min = -20
    y_min = -20
    x_max = 20
    y_max = 20
    t_min = 0
    t_max = 1
    r_min = 0
    r_max = 1
    
#--------------------- Control Module ----------------------#
def main():
    param = Param()
    tsm_file = 'input/'+input("Please enter the name of your tsm file (e.g. tsm1.txt):")
    sp_file = 'input/'+input("Please enter the name of the sp file (e.g. sp1.txt):")
    wall_file = 'input/'+input("Please enter the name of the wall file (e.g. wall1.txt):")
    output_file = 'output/'+input("Please type a name for the output file (e.g. out.txt):")
    param.load_params(tsm_file, sp_file, wall_file)
##    param.load_params("input/tsm1.txt", "input/sp1.txt", "input/wall1.txt")
    floorMap = FloorMap([])
    floorMap.create(param)
    param.updateMap(floorMap)
    sp_list = param.sp_list
    sp_dbm_list = []
    for sp in sp_list:
        sp_dbm_list.append(ReceivedSignalStrength.get_received_power(sp, param))
##    Output.output("output/out1.txt", sp_list, sp_dbm_list)
    finished = Output.output(output_file, sp_list, sp_dbm_list)
    return finished
