import numpy as np

W = 12100
SREF = 179
CLMAX = 1.8
p = .002377

V_stall = np.sqrt(W/(.5*p*SREF*CLMAX))
V_TO = V_stall*1.2

print(V_TO)

POWER = 885
PROP_EFF = .85

T = PROP_EFF*POWER*550/V_TO
T_STATIC = T*1.1

Total_Thrust = T*2
Total_Static_Thrust = T_STATIC*2

a = (Total_Thrust - Total_Static_Thrust)/(-1* V_TO**2)


u = .025
K = .04

CL_g = u/(2*K)

CD_g = .025 + .04 * CL_g**2

g = 31.174

A = g * ((Total_Static_Thrust/W)-u)

B = g/W * (.5 * p * SREF * (CD_g - u*CL_g) + a)

STO = 1/(2*B) * np.log(A/(A-B*V_TO**2))
print(STO)