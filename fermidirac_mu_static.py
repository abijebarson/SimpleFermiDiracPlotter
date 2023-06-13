# MODIFIED FERMI DIRAC DISTRIBUTION
# WITH CHEMICAL POTENTIAL 
# TO ACCOUNT FOR THE FIXED SMALL NUMBER OF PARTICLES 

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

###### Parameters to change: ######
#=================================#
g = lambda En : (En + 1)*(En + 2)
n = 30 # no. of particles

temp_unit = 'MeV'
Tarr = np.array([0.1, 0.8, 2])

energy_unit = 'MeV'
init_En = 0
fin_En = 10
energy_discreteness = 1

###################################

k = 1 # ignoring Boltzman Constant, since it is included in Temperature

def fd_dist(T, E, Ef):
	return 1/(1 + np.exp((E - Ef)/(k*T)))
	
En = np.arange(init_En, fin_En, energy_discreteness)
Ex = (En+(3/2))*1.5 # h w = 1.5 MeV
garr = g(En)

def temp_func(CP, T):
    '''
    Finding Chemical Potential, such that the number of particles are equal to the given number of particles
    This function acts as the temporary function to solve for CP
    '''
    f = fd_dist(T, Ex, CP)
    Narr = f * garr
    return sum(Narr)-n  

plt.style.use('dark_background') 

fig, ax = plt.subplots()
ax.set_title(f'Fermi-Dirac Distribution for a Nuclear System')
ax.set_xlabel(f'Energy, E [{energy_unit}]')
ax.set_ylabel('f(E)')

for Ti in Tarr:
    mu = scipy.optimize.newton(temp_func, 2, args=(Ti,))
    print("Chemical potential =", mu, 'at T = ', Ti)
    f =  fd_dist(Ti, Ex, mu)

    ax.scatter(Ex, f,label = f'T={Ti} {temp_unit}')
    ax.plot(Ex,f)
    cp = ax.scatter(mu, 0.5, color='#DD1214')

ax.set(xlim=(0, Ex[len(Ex)-1]+1),
       ylim=(0, 1.1))
ax.legend()

plt.show()