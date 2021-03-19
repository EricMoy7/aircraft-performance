import numpy as np
import matplotlib.pyplot as plt

def range_eq(W_f):
    R = 550*n_p*LD / .585*(np.log(1 + W_f/(W_p+W)))
    return R

n_p = .85
LD = 13.4
V = 314
SFC = .585

W_f = np.linspace(1600,2200, 5)
W_p = np.linspace(0,3000, 100)
W = 8320


for value in W_f:
    R = range_eq(value)
    plt.plot(W_p, R)

plt.xlabel("Payload Weight (LB)")
plt.ylabel("Distance (nmi)")
plt.legend([str(thing)[0:4] + "lbs" for thing in W_f], title="Initial Fuel")
plt.show()
