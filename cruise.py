import numpy as np
import pickle
from parameters.param import Discipline
import inspect
import matplotlib.pyplot as plt
from multiprocessing import Pool
import math

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
        self.Sigma = self.fDelta()/self.fTheta()
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

class speed():
    def __init__(self, KCAS, altitude):
        self.KCAS = KCAS
        self.CON = conditions(altitude)

    def fKTAS(self):
        self.KTAS = np.sqrt(cond["p0"] / self.CON.fDensity()) * self.KCAS
        return self.KTAS
    
    def fVTAS(self):
        self.VTAS = 1.687809857 * self.fKTAS()
        return self.VTAS

    def fMach(self, speed = None):
        if speed == None:
            self.Mach = self.fVTAS()/np.sqrt(1716*cond["y"]* self.CON.fTemp())
        else:
            self.Mach = speed/np.sqrt(1716*cond["y"]* self.CON.fTemp())
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
        self.cf = 0.455/((np.log10(self.fRE())**2.58*(1+0.144*self.SPE.fMach()**2)**0.65))*aero["Excr"]
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
        self.CD = self.fcdo() + self.fCL()**2/(np.pi*aero["AR"]*aero["e"]) + aero["Ord_Drag"]
        return self.CD
    
    def fLD(self):
        self.LD = self.fCL()/self.fCD()
        return self.LD
    
    def fD(self):
        self.D = self.fqinf() * aero['S_ref'] * self.fCD()
        return self.D

    #Something CL for MAX L/D

    def fLD_Max(self):
        self.LD_Max = 0.5*np.sqrt((np.pi*aero["e"]*aero["AR"])/self.fcdo())
        return self.LD_Max

    def fVstall(self):
        self.VStall = np.sqrt(self.weight/(self.CON.fDensity()*aero["S_ref"]*2.1))
        return self.VStall

class power():
    def __init__(self, KCAS, altitude, weight):
        self.KCAS = KCAS
        self.CON = conditions(altitude)
        self.SPE = speed(KCAS, altitude)
        self.weight = weight
        self.COEF = coefficients(KCAS, altitude, weight)
        self.altitude = altitude
    
    def fpower_req(self, drag = None):
        if (drag == None):
            self.power_req = self.COEF.fD() * self.SPE.fVTAS()
        else:
            self.power_req = drag * self.SPE.fVTAS()
        return self.power_req
    
    def fpower_reqhp(self, drag = None):
        if (drag == None):
            self.power_reqhp = self.fpower_req() / 550
        else:
            self.power_reqhp = self.fpower_req(drag) / 550
        return self.power_reqhp
    
    def fpower_availhp(self):
        self.power_availhp = prop["ESHP_FL000"] - (prop["ESHP_FL000"]-prop["ESHP_FL300"])/30000*self.altitude + ((self.SPE.fKTAS()-50)*1.4)
        if self.power_availhp > prop["ESHP_FL000"]:
            return prop["ESHP_FL000"]
        return self.power_availhp

    def fpower_avail(self):
        self.power_avail = self.fpower_availhp()*550
        return self.power_avail


# x = speed(110,15000)
# public_method_names = [method for method in dir(x) if callable(getattr(x, method)) if not method.startswith('_')] 
# for method in public_method_names:
#     getattr(x, method)()  # call
# print(vars(x))

# x = conditions(15000)
# public_method_names = [method for method in dir(x) if callable(getattr(x, method)) if not method.startswith('_')] 
# for method in public_method_names:
#     getattr(x, method)()  # call
# print(vars(x))



# coef = coefficients(150,0, 12117)
# for i in range(10):
#     coef = coefficients(150,0+i*1000,coef.weight)
#     print(coef.weight)


#======Endurance/Range Diagrams=============================================================


#================================================================================================
# coef = coefficients(150 , 15000, 12117)
# vstall = coef.fVstall()
# vs_array = []
# altitude = np.linspace(0,29000,500)
# for alt in altitude:
#     sp = speed(vstall*.592484,alt)
#     vs_array.append(sp.fMach())

# #max alt line
# max_altx = [vs_array[-1:][0],vs_array[-1:][0]+.2]
# max_alty = [altitude[-1:][0],altitude[-1:][0]]

# plt.plot(max_altx,max_alty)
# plt.plot(vs_array, altitude)
# plt.show()
#================================================================================================
    
