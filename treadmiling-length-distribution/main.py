import numpy as np
import matplotlib.pyplot as plt
import rcparams

from modules.monomer import monomer
from modules.filament import filament

n_initial = 10

n_iters = 2_000
n_sims = 1

record_after = 1_000

#------------------------------------------------------

# Reaction rates
k_T_plus_on = 1.0
k_D_plus_on = 1E-5
k_T_minus_on = 0.01
k_D_minus_on = 2E-5
k_T_plus_off = 0.5
k_D_plus_off = 0.5
k_T_minus_off = 0.005
k_D_minus_off = 1

w_re = 0.05
w_de = 1E-6

#------------------------------------------------------

record_every = int(n_iters * 5 / w_de)

#------------------------------------------------------

def P(k):
    return 1 - np.exp(-k)

#-------------------------------------------------------

for sim_i in range(n_sims):
    # Initialize the filament with n_initial monomers in T state
    f = filament()
    for n in range(n_initial):
        f.add_monomer_minus_end(monomer("T"))
    for t_i in range(n_iters):
        if t_i < record_after and t_i % 1000 == 0:
            print("Steps {} / {} of equilibration".format(t_i, n_iters - record_after))
        if t_i == record_after:
            print("Equilibration complete.")
            print("Starting simulation.")
        # Scan through the filament and switch state
        for m_i in range(f.length):
            P_T_to_D = P(w_de)
            P_D_to_T = P(w_re)
            if f.monomers[m_i].state == "T":
                if np.random.rand() < P_T_to_D:
                    f.swap_state(m_i)
            elif f.monomers[m_i].state == "D":
                if np.random.rand() < P_D_to_T:
                    f.swap_state(m_i)
        
        # Add monomers to the left end
        P_T_plus = P(k_T_plus_on)
        if np.random.rand() < P_T_plus:
            f.add_monomer_plus_end(monomer("T"))
        
        P_D_plus = P(k_D_plus_on)
        if np.random.rand() < P_D_plus:
            f.add_monomer_plus_end(monomer("D"))
            
        # Add monomers to the right end
        P_T_minus = P(k_T_minus_on)
        if np.random.rand() < P_T_minus:
            f.add_monomer_minus_end(monomer("T"))
            
        P_D_minus = P(k_D_minus_on)
        if np.random.rand() < P_D_minus:
            f.add_monomer_minus_end(monomer("D"))
            
        # Remove monomers from the left end
        P_T_plus_off = P(k_T_plus_off)
        if np.random.rand() < P_T_plus_off and f.monomers[0].state == "T":
            f.remove_monomer_plus_end()
            
        P_D_plus_off = P(k_D_plus_off)
        if np.random.rand() < P_D_plus_off and f.monomers[0].state == "D":
            f.remove_monomer_plus_end()
            
        # Remove monomers from the right end
        P_T_minus_off = P(k_T_minus_off)
        if np.random.rand() < P_T_minus_off and f.monomers[-1].state == "T":
            f.remove_monomer_minus_end()
            
        P_D_minus_off = P(k_D_minus_off)
        if np.random.rand() < P_D_minus_off and f.monomers[-1].state == "D":
            f.remove_monomer_minus_end()
            
        # Record the state of the filament
        if t_i > record_after:
            print(t_i, f.length, f.num_T, f.num_D,)
    
    