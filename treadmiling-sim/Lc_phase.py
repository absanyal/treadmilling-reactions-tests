import numpy as np
import matplotlib.pyplot as plt
import rcparams

dt_react = 0.1

tau_det_list = np.linspace(0.1, 10, 1000)
r_on_list = np.linspace(0.01, 5, 1000)

Lc_vals = np.zeros((len(tau_det_list), len(r_on_list)))

for tau_i, tau_det in enumerate(tau_det_list):
    for r_i, r_on in enumerate(r_on_list):
        p_on = r_on * dt_react

        Lc = - r_on * tau_det * np.log(1 - p_on)

        Lc_vals[tau_i, r_i] = Lc

plt.figure()

plt.imshow(Lc_vals, aspect='auto', cmap='viridis', origin='lower', extent=(
    r_on_list[0], r_on_list[-1], tau_det_list[0], tau_det_list[-1]))

plt.colorbar()

plt.xlabel(r'$r_{\mathrm{on}}$')
plt.ylabel(r'$\tau_{\mathrm{det}}$')

plt.savefig('Lc_phase.png', bbox_inches='tight')
