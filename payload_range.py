import numpy as np
import matplotlib.pyplot as plt
import math

def range_eq(W_f,W_p):
    R = 550*n_p*LD / .585*(np.log(1 + W_f/(W_p+W)))
    return R

n_p = .8
LD = 11
SFC = .585

W_f = 1600
W_p = 3000
W = 8933
f = 1.2

p2x = [range_eq(W_f,W_p),range_eq(W_f,W_p*.6)*f]
p2y = [W_p,W_p*.6]
p3x = [range_eq(W_f,W_p*.6)*f,range_eq(W_f,0)*1.1]
p3y = [W_p*.6,0]

plt.hlines(W_p,0,range_eq(W_f,W_p), color='Blue')
plt.plot(p2x,p2y, color='Orange')
plt.plot(p3x,p3y, color='Red')
plt.vlines(range_eq(W_f,W_p),0,W_p, linestyle='--', color='Blue')
plt.vlines(range_eq(W_f,W_p*.6)*f,0,W_p*.6, linestyle='--', color='Orange')


plt.text(10,W_p+40,'Max Payload Weight')
plt.text(p2x[0]+20, p2y[0]+20, 'Ferry Mission (60%)', rotation=np.degrees(np.arctan((p2y[0]-p2y[1])/(p2x[0]-p2x[1]))), rotation_mode='anchor',transform_rotates_text=True)
plt.text(p3x[0]+20, p3y[0]+20, 'Zero Payload', rotation=np.degrees(np.arctan((p3y[0]-p3y[1])/(p3x[0]-p3x[1]))), rotation_mode='anchor',transform_rotates_text=True)

plt.ylim((0,3200))
plt.grid('on', linestyle='--')
plt.xlabel('Range (nmi)')
plt.ylabel('Payload Weight (lbs)')

plt.show()

print('==================================')
print(f'Max Payload Range: {p2x[0]}nmi')
print(f'Ferry Payload Range: {p2x[1]}nmi')
print(f'No Payload Range: {p3x[1]}nmi')
print('==================================')