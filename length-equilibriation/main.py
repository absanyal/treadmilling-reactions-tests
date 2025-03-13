import numpy as np
import matplotlib.pyplot as plt
import rcparams

# r_on_list = np.linspace(0.01, 10, 100)
# tau_det_list = np.linspace(0.01, 20, 100)

r_on = 0.7
# tau_det = 1
dt = 0.1

L0 = 20
N_wanted = 20

num_filaments = 100

tau_det = - N_wanted / (r_on * np.log(r_on * dt))

print("r_on: {:.2f}".format(r_on))
print("tau_det: {:.2f}".format(tau_det))
print("L0: {:.0f}".format(L0))
print("N_c = {:.0f}".format(N_wanted))

# n_points_total = len(r_on_list) * len(tau_det_list)
# print("Total number of points: {}".format(n_points_total))

# avg_length_grid = np.zeros((len(r_on_list), len(tau_det_list)))


t_steps = 10000

t_list = np.arange(0, t_steps*dt, dt)

length_list = np.zeros((num_filaments, t_steps))
average_trace = np.zeros(t_steps)

plt.figure(figsize=(5, 5))
        
t_tail = np.zeros(num_filaments)
length = np.ones(num_filaments) * L0
for t_i, t in enumerate(t_list):
    for f_i in range(num_filaments):
        p_on = r_on * dt
        p_off = 1 - np.exp(-t_tail[f_i]/tau_det)
        
        t_tail[f_i] += dt
        
        dice = np.random.rand()
        if dice < p_on:
            length[f_i] += 1
        
        dice = np.random.rand()
        if dice < p_off:
            if length[f_i] > 0:
                length[f_i] -= 1
                t_tail[f_i] = 0
            
        length_list[f_i, t_i] = length[f_i]
    
    average_trace[t_i] = np.mean(length)
    
    if (t_i+1) % 1000 == 0 or t_i == len(t_list) - 1:
        for f_i in range(num_filaments):
            fi_skip = 20
            if f_i % fi_skip == 0:  
                plt.plot(t_list[:t_i], length_list[f_i, :t_i], color='black', alpha=0.5, lw=0.5)
            else:
                plt.plot(t_list[:t_i], length_list[f_i, :t_i], color='black', alpha=0.1, lw=0.1)
        plt.xlim(0, t_steps*dt)
        
        # plt.yscale('log')
        
        plt.plot(t_list[:t_i], average_trace[:t_i], color='blue', label='Average length (running)')
        
        avg_length = np.mean(length_list[:, :t_i+1])
        
        plt.axhline(avg_length, color='b', label='Average length: {:.2f}'.format(avg_length), ls='--')
        plt.axhline(N_wanted, color='r', label=r'$N_c$ = {:.0f}'.format(N_wanted), ls='--')
        
        plt.xlabel("Time (s)")
        plt.ylabel("Length")
        plt.legend()
        
        plt.savefig("test.pdf")
        
        plt.clf()