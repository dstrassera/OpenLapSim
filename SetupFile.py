"""
---------------------------
Setup File - OLS
---------------------------
"""
# Import Packages
import numpy as np

class SetupFile:
    
    def __init__(self):
        
        self.setupDict = {
        # Vehicle Parameters - GP2
            "mcar"    : 688+40,     #[Kg]
            "clt"     : 3.1,        #[100 pt.]
            "cx"      : 1.0,        #[100 pt.]
            "afrcar"  : 1.0,        #[m2]
            "mbrk"    : 7000,       #[Nm]
            "gripx"   : 1.0,        #tyre friction coeff long
            "gripy"   : 1.25,       #tyre friction coeff lat
            "rtyre"   : 0.32,       #[m]; tyre radius
            "rGearRat" : [10.0,7.8,6.1,7.8,5.2,4.5,4.0], #Final Gear Ratio
            "reff"    : 0.95,       # drive line efficiency
            "EngMap"  : np.array([[200,300,430,380],[0,3000,7000,10000]]), #[Nm,rmp]
            "rho"     : 1.22,       #[Kg/m3]; air density
        }

