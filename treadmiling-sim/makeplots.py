import numpy as np
import matplotlib.pyplot as plt
import rcparams

num_trials, num_iters, dt_react = np.loadtxt('siminfo.txt', skiprows=1, unpack=True)

num_trials = int(num_trials)
num_iters = int(num_iters)

print('Number of trials: {}'.format(num_trials))
print('Number of iterations per trial: {}'.format(num_iters))

t_list = np.arange(0, num_iters * dt_react, dt_react)

avg_len_array = np.loadtxt('lengths.txt', skiprows=1, usecols=(3,))
avg_len_array = avg_len_array.reshape(num_trials, num_iters)

num_filaments_array = np.loadtxt('num_filaments.txt', skiprows=1, usecols=(3,))
num_filaments_array = num_filaments_array.reshape(num_trials, num_iters)

# L_c = np.loadtxt('Lc.txt', skiprows=1)
# print('Critical length: {:.4f}'.format(L_c))

fig, ax = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

for trial_i in range(num_trials):
    ax[0].plot(t_list, avg_len_array[trial_i], color='k', alpha=0.1, lw=0.1)
    ax[1].plot(t_list, num_filaments_array[trial_i], color='k', alpha=0.1, lw=0.1)
    
ax[0].plot(t_list, avg_len_array.mean(axis=0), color='r', lw=2)
ax[1].plot(t_list, num_filaments_array.mean(axis=0), color='r', lw=2)

# ax[0].set_xlabel('Time (s)')
ax[0].set_xlabel('Number of iterations')
ax[0].set_ylabel('Average length')
ax[0].set_ylim(bottom=2)
ax[0].set_xlim(left=t_list[0], right=t_list[-1])
# ax[0].set_xscale('log')

# ax[0].axhline(y=L_c, color='b', linestyle='--', lw=1)

# ax[1].set_xlabel('Time (s)')
ax[1].set_xlabel('Number of iterations')
ax[1].set_ylabel('Number of filaments')
ax[1].set_ylim(bottom = 0)
ax[1].set_xlim(left=t_list[0], right=t_list[-1])
# ax[1].set_xscale('log')

               

plt.savefig('averages.png', bbox_inches='tight')

ax[0].clear()
ax[1].clear()

hm0 = ax[0].imshow(avg_len_array, aspect='auto', cmap='viridis', origin='lower', extent=(0, t_list[-1], 0, num_trials))
hm1 = ax[1].imshow(num_filaments_array, aspect='auto', cmap='viridis', origin='lower', extent=(0, t_list[-1], 0, num_trials))

ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Trial number')
ax[0].set_title('Average length')
ax[0].set_aspect('auto')
plt.colorbar(hm0, ax=ax[0])

ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Trial number')
ax[1].set_title('Number of filaments')
ax[1].set_aspect('auto')
plt.colorbar(hm1, ax=ax[1])

plt.savefig('heatmaps.png', bbox_inches='tight')