import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import scipy.optimize

###### Parameters to change: ######
#=================================#
g = lambda En : (En + 1)*(En + 2)
n = 30

temp_unit = 'MeV'
init_T = 0.1 # in MeV
fin_T = 1

energy_unit = 'MeV'
init_En = 0
fin_En = 10
energy_discreteness = 1

###################################

k = 1 # ignoring Boltzman Constant, since it is included in Temperature

def fd_dist(T, E, Ef):
	return 1/(1 + np.exp((E - Ef)/(k*T)))
	
En = np.arange(init_En, fin_En, energy_discreteness)
Ex = (En+1.5)*1.5
garr = g(En)

def temp_func(Ef, T):
	f = fd_dist(T, Ex, Ef)
	Narr = f * garr
	return sum(Narr)-n

mu = scipy.optimize.newton(temp_func, 2, args=(init_T,))

print("Chemical potential =", mu, 'at T = ', init_T)

f =  fd_dist(init_T, Ex, mu)

plt.style.use('dark_background') 

fig, ax = plt.subplots()
ax.set_title(f'Fermi-Dirac Distribution for a Nuclear System')
ax.set_xlabel(f'Energy, E [{energy_unit}]')
ax.set_ylabel('f(E)')
fig.subplots_adjust(bottom=0.25)

points  = ax.scatter(Ex, f, color='#DD1214')
cp = ax.scatter(mu, 0.5)

axT = fig.add_axes([0.25, 0.1, 0.65, 0.03])
T_Slider = Slider(
    ax=axT,
    label=f"Temperature [{temp_unit}]",
    valmin=0.0000001,
    valmax=fin_T,
    valinit=init_T,
    orientation="horizontal"
)

def update_T(val):
	T = T_Slider.val
	try:
		mu = scipy.optimize.newton(temp_func, 2, args=(T,))
	except:
		print(f"Can't solve at T = {T}")
		return
	print("mu =", mu, 'at T = ', T	)
	xx = np.vstack((Ex, fd_dist(T, Ex, mu)))
	points.set_offsets(xx.T)
	cp.set_offsets((mu,0.5))
	fig.canvas.draw_idle()

T_Slider.on_changed(update_T)

ax.set(xlim=(0, Ex[len(Ex)-1]+1),
       ylim=(0, 1))

plt.show()