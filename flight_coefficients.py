import numpy as np
import pickle
from parameters.param import Discipline
import inspect
import matplotlib.pyplot as plt
from multiprocessing import Pool
import math
from cruise import speed, power, coefficients

velocity = np.linspace(1,300,100)
spe = speed(velocity, 12000)
mach = np.array(spe.fMach())
ld1_array = []
ld2_array = []
for v in velocity:
    coef = coefficients(v,13000, 12000)
    cl = coef.fCL() 
    cd = coef.fCD()
    ld1 = cl/cd
    ld2 = cl**(1/2)/cd

    ld1_array.append(ld1)
    ld2_array.append(ld2)

ld1_max_ind = np.argmax(ld1_array)
ld2_max_ind = np.argmax(ld2_array)



plt.plot(mach, ld1_array)
plt.plot(mach, ld2_array)
plt.scatter([mach[ld1_max_ind],mach[ld2_max_ind]],[ld1_array[ld1_max_ind],ld2_array[ld2_max_ind]], color="Black", zorder=3)
plt.text(mach[ld1_max_ind],ld1_array[ld1_max_ind]+.5, s=np.round(ld1_array[ld1_max_ind],2))
plt.text(mach[ld2_max_ind],ld2_array[ld2_max_ind]+.5, s=np.round(ld2_array[ld2_max_ind],2))
plt.legend([r"$\frac{cl}{cd}$", r"$\frac{cl^\frac{1}{2}}{cd}$"])
plt.xlabel("Mach")
plt.ylabel("Coefficient Values")
plt.grid('on', linestyle='--')
plt.ylim((0,25))
print(mach[ld1_max_ind])
print(mach[ld2_max_ind])
plt.show()

