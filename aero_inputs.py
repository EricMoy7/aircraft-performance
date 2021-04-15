from cruise import conditions, speed, coefficients, power
import numpy as np
import pickle
from parameters.param import Discipline
import inspect
import matplotlib.pyplot as plt

load = Discipline('rb')
new = load.get()
load.close()

aero, mass, prop, cond = new

def perm(self):
    self.fCD = 0.036
    return self.fCD

drag_red = 300
max_pow = 2400
pow_a = []
pow_b = []
v = np.linspace(50,350,150)
KTAS = []
for vel in v:
    POW = power(vel, 10000, 13000)
    coefficients.fCD = perm
    COEF = coefficients(vel, 10000, 13000)
    pow_a.append(POW.fpower_reqhp(COEF.fD())- 100)

    print(COEF.fCL(), vel, POW.fpower_reqhp())
    SP = speed(vel, 10000)
    KTAS.append(SP.fKTAS())


plt.plot(KTAS, pow_a)
plt.hlines(max_pow,50,400,color='red')
plt.text(75,2300, "Max Engine Power (2400 hp) @ 12,000ft")

idx1 = np.argwhere(np.diff(np.sign(pow_a[20:] - np.ones_like(pow_a[20:])*max_pow))).flatten()
idx1 = idx1+20

plt.vlines(KTAS[idx1[0]], 0 ,max_pow, linestyles='dashed')

#Vert line text
plt.text(KTAS[idx1[0]]-10, max_pow*.1, f'Current', rotation=90)
plt.text(KTAS[idx1[0]]+2, max_pow*.1, f'{str(KTAS[idx1[0]])[:6]}kn', rotation=90)

plt.legend(["Current",f"Minimum Required (-{drag_red}LB Drag)"])
plt.ylim(0,3000)
plt.ylabel("Power (hp)")

plt.show()
