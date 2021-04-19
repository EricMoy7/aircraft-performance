import numpy as np
import matplotlib.pyplot as plt
from cruise import coefficients, speed

def range_eq(W_f,W_p, LD):
    R = 550*n_p*LD / .585*(np.log(1 + W_f/(W_p+W)))
    return R

n_p = .8
LD = 11
SFC = .585

W_f = 1600
W_p = 3000
W = 8933

alt = 18000

velocity = np.linspace(1,500, 100)
R = []
M = []
for v in velocity:
    co = coefficients(v,alt,W_f+W_p+W)
    vrange = range_eq(W_f, W_p, co.fLD())
    R.append(vrange)
    sp = speed(v,alt)
    M.append(sp.fMach())

print((M[np.argmax(R)],R[np.argmax(R)]))

plt.plot(M, R)
plt.xlabel('Mach')
plt.ylabel('Range (nmi)')
plt.grid('on', linestyle='--')
plt.show()