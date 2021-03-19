import numpy as np
import matplotlib.pyplot as plt

W = 13154
SREF = 179
CLMAX = 2.1
p = .002377

V_stall = np.sqrt(W/(.5*p*SREF*CLMAX))
V_TO = np.linspace(120 , 180, 100)

POWER = 885
PROP_EFF = .85

T = PROP_EFF*POWER*550/V_TO
T_STATIC = T*1.1

Total_Thrust = T*2
Total_Static_Thrust = T_STATIC*2

a = (Total_Thrust - Total_Static_Thrust)/(-1* V_TO**2)


u = .03
K = .04

CL_g = u/(2*K)

CD_g = .025 + .04 * CL_g**2

g = 31.174

A = g * ((Total_Static_Thrust/W)-u)

B = g/W * (.5 * p * SREF * (CD_g - u*CL_g) + a)

STO = 1/(2*B) * np.log(A/(A-B*V_TO**2))

plt.plot(V_TO, STO+775.72)

d = V_TO**2/(2*32.2*(.05))
plt.plot(V_TO, STO+d)
plt.show()
