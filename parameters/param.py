import pickle
import os

class Discipline:
    def __init__(self, crud):
        self.load(crud)

    def load(self, crud):
        print("Loading file...")
        here = os.path.dirname(os.path.abspath(__file__))
        self.outfile = open(os.path.join(here, "params"), crud)

    def get(self):
        a, b, c, d = pickle.load(self.outfile)
        return a, b, c, d
    
    def dump(self, dis):
        print("Dumping data to file...")
        pickle.dump(dis, self.outfile)

    def close(self):
        print("Closing file...")
        return self.outfile.close()
        

aero = {
    'S_ref': 250,
    'Span': 45,
    'Taper': 0.66,
    'Avg_Chord': 6.25,
    'Root_Chord': 7.5,
    'MAC': 6.33,
    'AR': 8.1,
    'e': 0.8,
    'S_wet': 1360,
    'cdo': 0,
    "K": .06,
    'Excr': 1.1,
    'Ord_Drag': .003,
    }

mass = {
    'Wfuel': 2200,
    'Wpayload': 3000,
    'Wempty': 8000,
    'MTOW': 13000,
}

prop = {
    'ESHP_FL000': 1600,
    'ESHP_FL300': 400,
    'n': 0.9,
    'ESFC_FL000': .585,
}

cond = {
    "p0": 0.0023769,
    "T0": 518.67,
    "P0": 2116.22,
    "a0": 661.477,
    "y": 1.4,
    "u0": 3.62E-07
}

dis = (aero, mass, prop, cond)

run = Discipline('wb')
run.dump(dis)
run.close()
