import numpy as np
import pickle
from parameters.param import Discipline
import inspect

load = Discipline('rb')
new = load.get()
load.close()

aero, mass, prop, cond = new

class conditions:
    def __init__(self, altitude):
        self.altitude = altitude

    def fTheta(self):
        self.Theta = 1-6.87535*10**(-6) * self.altitude
        return self.Theta
    
    def fDelta(self):
        self.Delta = self.fTheta()**5.2561
        return self.Delta

    def fSigma(self):
        self.Sigma = self.fTheta()/self.fDelta()
        return self.Sigma

    def fTemp(self):
        self.Temp = self.fTheta() * cond["T0"]
        return self.Temp
    
    def fPressure(self):
        self.Pressure = self.fDelta() * cond["P0"]
        return self.Pressure
    
    def fDensity(self):
        self.Density = self.fSigma() * cond["p0"]
        return self.Density

    def run_all(self):
        self.fDelta()
        self.fSigma()
        self.fTemp()
        self.fPressure()
        self.fDensity()

print(vars(conditions(0)))

class speed():
    def __init__(self, KCAS, altitude):
        self.KCAS = KCAS
        self.CON = conditions(altitude)

    def fKTAS(self):
        self.KTAS = cond["p0"] / self.CON.fDensity() * self.KCAS
        return self.KTAS
    
    def fVTAS(self):
        self.VTAS = 1.687809857 * self.fKTAS()
        return self.VTAS

    def fMach(self):
        self.Mach = self.fVTAS()/np.sqrt(1716*cond["y"]* self.CON.fTemp())
        return self.Mach

class coefficients():
    def __init__(self, KCAS, altitude, weight):
        self.KCAS = KCAS
        self.CON = conditions(altitude)
        self.SPE = speed(KCAS, altitude)
        self.weight = weight

    def fqinf(self):
        self.qinf = .5 * cond["y"] * cond["P0"] * self.CON.fDelta() * self.SPE.fMach() ** 2
        return self.qinf

    def fvis(self):
        temp = self.CON.fTemp()
        self.vis = cond["u0"] * (temp/cond["T0"])**1.5*((cond["T0"] + 198.72)/(temp + 198.72))
        return self.vis

    def fRE(self):
        self.RE = aero["MAC"] * self.CON.fDensity() * self.SPE.fVTAS() / self.fvis()
        return self.RE
    
    #Reynolds Per Ft

    def fcf(self):
        self.cf = 0.455/((np.log10(self.fRE())**2.58*(1+0.144*self.SPE.fMach()**2)**0.65))
        return self.cf
    
    def fcdo(self):
        rat = aero["S_wet"]/aero["S_ref"]
        self.cdo = rat*self.fcf()
        return self.cdo

    #Steady level cruise no gamma

    def fCL(self):
        self.CL = self.weight/(self.fqinf() * aero["S_ref"])
        return self.CL

    def fCD(self):
        self.CD = self.fcdo() + self.fCL()**2/(np.pi*aero["AR"]*aero["e"])
        return self.CD
    
    def fLD(self):
        self.LD = self.fCL()/self.fCD()
        return self.LD
    
    def fD(self):
        self.D = self.fqinf() * aero['S_ref'] * self.fCD()
        return self.D



x = coefficients(130,0, 12117)
public_method_names = [method for method in dir(x) if callable(getattr(x, method)) if not method.startswith('_')] 
for method in public_method_names:
    getattr(x, method)()  # call
print(vars(x))
