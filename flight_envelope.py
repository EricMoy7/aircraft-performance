import numpy as np
import pickle
from parameters.param import Discipline
import inspect
import matplotlib.pyplot as plt
from multiprocessing import Pool
import math
from cruise import power, speed, coefficients

def f(v):
    alt = 34000
    excess = [1,10]
    while alt > 0:
        p = power(v,alt, weight)
        req = p.fpower_reqhp()
        avail = p.fpower_availhp()
        if req-.5 <= avail <= req+.5  and req-avail >= 0:
            return alt
        else:
            alt += -1
        
        if alt == 1:
            return np.nan

weight = 13000
points = 400
velocity = np.linspace(20,391,points)
print(velocity)



if __name__ == '__main__':
    with Pool(16) as p:
        alt_array= np.array(p.map(f,velocity))
        mach = np.linspace(0.14,.75,400)
        ar = np.concatenate((mach.reshape(-1,1),alt_array.reshape(-1,1)), axis=1)

        ind = np.argwhere(np.isnan(alt_array))

        # altitudes = np.linspace(0,34000, 100)
        # stall_array = []
        # for alt in altitudes:
        #     co = coefficients(100, alt, weight)
        #     vstall = co.fVstall()
        #     spe = speed(100,alt)
        #     stall_array.append(spe.fMach(speed=vstall))

        # print(stall_array)

        plt.plot(ar[0:66,0],ar[0:66,1], linestyle='dashed')
        plt.plot(ar[167:358,0],ar[167:358,1], linestyle='dashed')
        plt.hlines(34000, .220, .459, colors='red')
        plt.legend([r"Stall Speed", r"Top Speed",r"Max Altitude"])
        plt.grid('on', linestyle='--')
        plt.xlabel('Mach')
        plt.ylabel('Altitude (ft)')
        plt.show()