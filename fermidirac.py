import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Enter the element name to evaluate
element = 'Rb'

# Source of fermi energy values: http://hyperphysics.phy-astr.gsu.edu/hbase/Tables/fermi.html
# Originally refered at: Ashcroft, N. W. and Mermin, N. D., Solid State Physics, Saunders, 1976.
fermi_energy = {
	'Li':4.74,
	'Na':3.24,
	'K': 2.12,
	'Rb': 1.85,
	'Cs':1.59
}

# Fixed Parameters
Ef = fermi_energy[element] # in eV
init_T  = 250 # in K
k = 8.617333262e-5 # in eV K^-1

# Parameters to change:
g = 1 # Degeneracy
n = 20 # total no of energy levels to evaluate

def fd_dist(T, E):
	return g/(1 + np.exp((E - Ef)/(k*T)))

Ex = np.linspace(0, 2*Ef, n)
f = (fd_dist(init_T, Ex))

print(Ex, f)

## Plotting part starts 
plt.style.use('dark_background') #comment this out for light mode

fig, ax = plt.subplots()
ax.set_title(f'Fermi-Dirac Distribution for {element}')
ax.set_xlabel('Energy, E [eV]')
ax.set_ylabel('population, f(E)')
fig.subplots_adjust(bottom=0.25)

# curve, = ax.plot(Ex, f, linewidth=2.0) #for curve
points  = ax.scatter(Ex, f, color='#DD1214')

axT = fig.add_axes([0.25, 0.1, 0.65, 0.03])
T_Slider = Slider(
    ax=axT,
    label="Temperature [K]",
    valmin=0,
    valmax=10000,
    valinit=init_T,
    orientation="horizontal"
)

def update_T(val):
	xx = np.vstack((Ex, fd_dist(T_Slider.val, Ex)))
	points.set_offsets(xx.T)
	# curve.set_ydata(fd_dist(T_Slider.val, Ex)) #for curve
	fig.canvas.draw_idle()

T_Slider.on_changed(update_T)

ax.set(xlim=(0, Ex[len(Ex)-1]),
       ylim=(0, f[len(f)-1])[0])

plt.show()	