import math
import numpy as np
#from DataModules import *
from AnalysisModules import *

# Main program of RSSC
while True:
    finished = main()
    if finished:
        command = input("Signal strength file generated. Press enter to continue or press E to exit.")
        if command == 'e' or command == 'E':
            exit()
