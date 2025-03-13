import numpy as np
import matplotlib.pyplot as plt
import rcparams
from scipy.optimize import curve_fit


def linear(x, a, b):
    return a*x + b


L0 = 100

filament = np.arange(1, L0+1, 1)
filament = list(filament)

r_on = 3
r_off = 3

dt = 0.01

p_on = r_on * dt
p_off = r_off * dt

if p_on >= 1:
    raise ValueError('P_on is too high')
if p_off >= 1:
    raise ValueError('P_off is too high')


t_steps = 5000
t_list = np.arange(0, t_steps*dt, dt)

L_list = []
com_list = []

plt.figure()

for t_i, t in enumerate(t_list):
    dice_on = np.random.rand()
    if dice_on < p_on:
        filament.append(filament[-1] + 1)

    dice_off = np.random.rand()
    if dice_off < p_off:
        if len(filament) > 1:
            filament.pop(0)

    bottom = filament[0]
    top = filament[-1]

    L_list.append(len(filament))

    plt.scatter([t, t], [bottom, top], c='b', s=5)

    com = np.mean(filament)
    plt.scatter(t, com, c='r', s=10, alpha=0.5)
    com_list.append(com)

    plt.xlim(0, t_steps*dt)

    plt.xlabel('Time (s)')
    plt.ylabel('Position')

    if t_i % 1000 == 0 or t_i == len(t_list)-1:
        plt.savefig('treadmilling.png')


plt.clf()
plt.cla()

plt.plot(t_list, L_list)

plt.ylim(bottom=0)

plt.xlabel('Time (s)')
plt.ylabel('Length')

plt.savefig('length.png')

p_opt, p_cov = curve_fit(linear, t_list, com_list)

treadmilling_velocity = p_opt[0]

y_fit = linear(t_list, *p_opt)

plt.clf()
plt.cla()

plt.plot(t_list, com_list, label='Simulation')
plt.plot(t_list, y_fit, label=r'Fit: $v_{{\mathrm{{treadmilling}}}} = {:.2f}$'.format(
    treadmilling_velocity))
plt.legend()

plt.xlabel('Time (s)')
plt.ylabel('Center of mass')

plt.savefig('center_of_mass.png')

print('Treadmilling velocity: {:.2f} monomer/s'.format(treadmilling_velocity))
