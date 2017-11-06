"""Author: (c)copyright Earl Martin Momongan"""
"""email: techwiz@csu.fullerton.edu"""
"""phone: (714)510-7497"""

import time
import math

class MyPRNG: #MyPRNG class
    
    def __init__(self):                             #class initialize function
        self.sec = int(round(time.time()))          #program uses the current time in seconds as seed
        self.prn = 16807 * self.sec % 2147483647    #function to generate prn using seconds as seed
        
    def next_prn(self):
        self.prn = 16807 * self.prn % 2147483647    #function to return next prn
        return self.prn      
    
    def seed(self, rseed):                          #function to prompt user to enter a number as a seed
        self.prn = 16807 * rseed % 2147483647
        
        
    
    