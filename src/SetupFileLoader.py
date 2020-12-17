"""
---------------------------
Setup File - OLS
---------------------------

This class loads the setupFile.json and creates a dictionary.
Below an example of setupFile.json (REMOUVE comments "#..." on real JSON file)

{
    "setupName" : "Gp2Dummy",
    "mcar"		: 728,        #[Kg]; total car mass
    "clt"		: 3.1,        #[100 pt.]; Lift coeffitien (-)
    "cx"		: 1.0,        #[100 pt.]; Drag coeffitien
    "afrcar"	: 1.0,        #[m2]; Frontal Area
    "mbrk"		: 7000,       #[Nm]; Max Braking Torque
    "gripx"		: 1.15,       #tyre friction coeff long
    "gripy"		: 1.40,       #tyre friction coeff lat
    "loadEff"   : 0.10,       #grip Load Effect % / 1KN of Fz
    "rtyre"		: 0.32,       #[m]; tyre radius
    "rGearRat"	: [10.0,7.8,6.1,7.8,5.2,4.5,4.0],  #Final Gear Ratio
    "reff"		: 0.95,       # drive line efficiency
    "EngNm"     : [200,300,430,380], # [Nm]; Engine Torque
    "EngRpm"    : [0,3000,7000,10000],  # [rpm]Engine rmp
    "rho"		: 1.22        #[Kg/m3]; air density
}

---------------------------
@autor: Davide Strassera
@first release: 2019-12-21
by Python 3.7
---------------------------

"""
# Import Packages
import json


class SetupFileLoader:

    def __init__(self, setupFileName):
        self.setupFileName = setupFileName
        self.setupDict = {}

    def loadJSON(self):
        # load json
        with open(self.setupFileName) as f:
            data = json.load(f)
        # set setupDict
        self.setupDict = data
