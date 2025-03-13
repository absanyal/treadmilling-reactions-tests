import numpy as np
import matplotlib.pyplot as plt
import rcparams

r_on_list = np.linspace(0.01, 10, 100)
tau_det_list = np.linspace(0.01, 20, 100)

n_points_total = len(r_on_list) * len(tau_det_list)
print("Total number of points: {}".format(n_points_total))

avg_length_grid = np.zeros((len(r_on_list), len(tau_det_list)))

L0 = 20

dt = 0.1
t_steps = 1000

t_list = np.arange(0, t_steps*dt, dt)

length_list = np.zeros(t_steps)

counter = 0
for r_on_i, r_on in enumerate(r_on_list):
    for tau_det_i, tau_det in enumerate(tau_det_list):
        
        t_tail = 0
        length = L0
        for t_i, t in enumerate(t_list):
            p_on = r_on * dt
            p_off = 1 - np.exp(-t_tail/tau_det)
            
            t_tail += dt
            
            dice = np.random.rand()
            if dice < p_on:
                length += 1
            
            dice = np.random.rand()
            if dice < p_off:
                if length > 0:
                    length -= 1
                t_tail = 0
                
            length_list[t_i] = length
            
        mid_pt = int(t_steps/2)
        avg_length = np.mean(length_list[mid_pt:])
        
        avg_length_grid[r_on_i, tau_det_i] = avg_length
        # avg_length_grid[r_on_i, tau_det_i] = np.log(avg_length + 1)
        
        counter += 1
        percent_done = 100 * counter / n_points_total
        
        if (counter) % 1000 == 0:
            print("{} / {} | {:.2f} % done".format(counter, n_points_total, percent_done))

plt.figure(figsize=(6, 5))

plt.imshow(avg_length_grid, origin='lower', extent=[tau_det_list[0], tau_det_list[-1], r_on_list[0], r_on_list[-1]], aspect='auto')

plt.xlabel(r'$\tau_{{\mathrm{{det}}}}$')
plt.ylabel(r'$r_{\mathrm{on}}$')
plt.colorbar()

plt.savefig('avg_length_grid.png', bbox_inches='tight')