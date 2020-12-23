import math
import numpy as np
from DataModules import *
#from Point import *

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidWall(Error):
    """Raised when the input value is too large"""
    pass

class InvalidIndex(Error):
    """Raised when the input index exceeds the number of walls"""
    pass

class InvalidReceivedStrength(Error):
    """Raised when the received strength is greater than the transmission power level"""
    pass

class BadPosition(Error):
    """Raised when the point falls outside of the target area"""
    pass

class BadSignalFrequency(Error):
    """Raised when the input frequency is invalid"""
    pass

class BadTransmissionPower(Error):
    """Raised when the transmission power level is invalid"""
    pass

class BadTransmittance(Error):
    """Raised when the transmissance value is invalid"""
    pass

class BadReflectance(Error):
    """Raised when the reflectance value is invalid"""
    pass

class InconsistentWallParams(Error):
    """Raised when the numbers of wall parameters are not consistent"""
    pass
