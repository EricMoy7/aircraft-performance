import numpy as np

bhp = 750
rho = .0024
rho_sl = .0024
N_e = 2
D_prop = 7.5
gam_climb = 10.3 * np.pi/180
gam_min = .024 #two engine
weight = 13008
s_ref = 250
g = 32.2
Cl = 2
Cl_max = 2.1



T_AV = 5.75*bhp * ((rho/rho_sl*N_e*D_prop**2)/bhp)**(1/3)
print(T_AV)

G = gam_climb - gam_min
U = .01 * Cl_max + 0.02
BFL = ((.863)/(1+2.3*G)) * ((weight/s_ref)/(rho*g*Cl) + 50) * (1/(T_AV/weight - U) + 2.7) + (655/np.sqrt(rho/rho_sl))
print(BFL)