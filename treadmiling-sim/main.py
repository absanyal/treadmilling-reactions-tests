import numpy as np
import matplotlib.pyplot as plt
import rcparams
from modules.filaments import filament

n_trials = 100
n_iters = 30000

r_on = 0.5
tau_det = 10
r_nuc = 0.2

dt_react = 0.1

n_filaments_init = 1
initial_length = 2
num_free_monomers_init = 1000

time_list = np.arange(0, n_iters * dt_react, dt_react)

avg_lengths = np.zeros((n_trials, n_iters))
num_filaments_list = np.zeros((n_trials, n_iters))

with open('lengths.txt', 'w') as f_lengths:
    f_lengths.write('#Trial\ttime_index\ttime\tavg_length\n')

with open('num_filaments.txt', 'w') as f_num_filaments:
    f_num_filaments.write('#Trial\ttime_index\ttime\tnum_filaments\n')

with open('lengths.txt', 'a') as f_lengths, open('num_filaments.txt', 'a') as f_num_filaments:
    for trial_i in range(n_trials):
        num_free_monomers = num_free_monomers_init
        print('Trial {} of {}'.format(trial_i + 1, n_trials))
        filament_list = [filament(initial_length, dt_react) for _ in range(n_filaments_init)]
        for iter_i in range(n_iters):
            for f in filament_list:
                if num_free_monomers > 0:
                    f.grow(r_on)
                    if f.is_polymerized:
                        num_free_monomers -= 1
                        f.is_polymerized = False
                f.age_up_tail()
                if f.length > 2:
                    f.shrink(tau_det)
                    if f.is_depolymerized:
                        num_free_monomers += 1
                        f.is_depolymerized = False
                if f.length == 2:
                    f.depolymerize(tau_det)
                    if f.is_depolymerized:
                        filament_list.remove(f)
                    else:
                        f.is_depolymerized = False
                        filament_list.remove(f)
                        num_free_monomers += 2
                    
            
            p_nuc = r_nuc * dt_react
            r = np.random.uniform()
            if r < p_nuc:
                filament_list.append(filament(2, dt_react))
                num_free_monomers -= 2
            
            t = iter_i * dt_react
            num_filaments = len(filament_list)
            if num_filaments == 0:
                avg_lengths[trial_i, iter_i:] = 0
            else:
                avg_length = sum([f.length for f in filament_list]) / num_filaments
                avg_lengths[trial_i, iter_i] = avg_length
            
            num_filaments_list[trial_i, iter_i] = num_filaments
            
            avg_length = avg_lengths[trial_i, iter_i]
            
            f_lengths.write('{}\t{}\t{:.2f}\t{:.4f}\n'.format(trial_i, iter_i, t, avg_length))
            
            f_num_filaments.write('{}\t{}\t{:.2f}\t{}\n'.format(trial_i, iter_i, t, num_filaments))
        
        f_lengths.flush()
        f_num_filaments.flush()
        
        with open('siminfo.txt', 'w') as f:
            f.write('#n_trials n_iters dt_react\n')
            f.write('{} {} {}\n'.format(trial_i + 1, n_iters, dt_react))

# Critical length calculation
p_on = r_on * dt_react
L_c = - r_on * tau_det * np.log(1 - p_on)

with open('Lc.txt', 'w') as f_Lc:
    f_Lc.write('#Critical length\n')
    f_Lc.write('{}\n'.format(L_c))

print('Critical length: {:.4f}'.format(L_c))