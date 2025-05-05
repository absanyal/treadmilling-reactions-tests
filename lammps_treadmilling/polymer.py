import numpy as np
import matplotlib.pyplot as plt
import rcparams

import numpy as np

###################################

T = 1
sigma0 = 1.0

##################################

data_file_name = "polymer.data"
input_file_name = 'input.lammps'
dump_file_name = 'dump.lammpstrj'
position_file_name = 'positions.dat'

##################################

xlo, xhi = 0.0, 200
ylo, yhi = 0.0, 200
zlo, zhi = 0.0, 200

x_width = xhi - xlo
y_width = yhi - ylo
z_width = zhi - zlo

x_mid = (xhi + xlo) / 2
y_mid = (yhi + ylo) / 2
z_mid = (zhi + zlo) / 2

Rcyl_outer = x_width / 2
Rcyl_inner = Rcyl_outer - 2

#######################################

num_monomers = 10
print("Number of monomers: ", num_monomers)

num_free_monomers = 2000

# ----------------

num_mm_bonds = num_monomers - 1
num_mm_angles = num_mm_bonds - 1
num_mm_dihedrals = num_mm_angles - 1
#####################################

num_atoms = num_monomers
num_bonds = num_mm_bonds
num_angles = num_mm_angles
num_dihedrals = num_mm_dihedrals

################################

time_step = 0.0001

autoseed = 1
fixed_seed = 12345

langevin_damp = 10

dump_freq = 1000
measure_freq = 1000

run_thermo_freq = 100000
run_steps = 3000000

# --------------------------------------

if autoseed:
    langevin_seed = np.random.randint(0, 2**16 - 1)
else:
    langevin_seed = fixed_seed

################################
# Monomer-monomer bond length
r0 = 1.0 * sigma0

# Monomer-linker bond length
rl0 = 1.0 * sigma0

# Bond spring constant
k_s = 100 * 0.5

# Bending stiffness
k_theta = 20 * 0.5
# k_theta = 80 * 0.5

# Intrinsic curvature angle at rest
theta0 = 180 - 7.6
# theta0 = 180
# theta0 = 180 - 2.5

# Torsional stiffness
k_phi = k_theta / 2.915

# Intrinsic torsional angle at rest
# phi0 = 20
phi0 = 0

# Lennard Jones epsilon (kB T)
epsilon = 0.0

# Lennard Jones sigma
sigma = sigma0

# Lennard Jones cutoff
rcut = 2.5 * sigma
# rcut = (2**(1/6)) * sigma0

# Initial monomer position
x_i, y_i, z_i = x_width / 2, y_width / 2, z_width / 2

##############################################################################

with open(data_file_name, 'w') as data_f:
    data_f.write("Single coarse grain polymer\n")
    data_f.write(f"\n")

    data_f.write("{} atoms\n".format(num_atoms))
    data_f.write("{} bonds\n".format(num_bonds))
    data_f.write("{} angles\n".format(num_angles))
    data_f.write("{} dihedrals\n".format(num_dihedrals))
    data_f.write("\n")

    # data_f.write("1 atom types\n")
    data_f.write("4 atom types\n")
    data_f.write("1 bond types\n")
    data_f.write("1 angle types\n")
    data_f.write("1 dihedral types\n")
    data_f.write("\n")

    data_f.write("{} {} xlo xhi\n".format(xlo, xhi))
    data_f.write("{} {} ylo yhi\n".format(ylo, yhi))
    data_f.write("{} {} zlo zhi\n".format(zlo, zhi))
    data_f.write("\n")

    data_f.write("Masses\n")
    data_f.write("\n")

    data_f.write("1 1.0\n")
    data_f.write("2 1.0\n")
    data_f.write("3 1.0\n")
    data_f.write("4 1.0\n")
    data_f.write("\n")

    data_f.write("Bond Coeffs\n")
    data_f.write("\n")
    data_f.write("1 {} {}\n".format(k_s, r0))

    data_f.write("\n")

    data_f.write("Angle Coeffs\n")
    data_f.write("\n")
    data_f.write("1 {} {}\n".format(k_theta, theta0))
    data_f.write("\n")

    data_f.write("Dihedral Coeffs\n")
    data_f.write("\n")
    data_f.write("1 {} {}\n".format(k_phi, phi0))
    data_f.write("\n")

    data_f.write("Atoms\n")
    data_f.write("\n")

    atom_x, atom_y, atom_z = x_i, y_i, z_i

    molecule_id = 1
    # atom_type = 1
    for atom_i in range(num_monomers):
        atom_id = atom_i + 1
        if atom_id == 1:
            atom_type = 3
        elif atom_id == num_atoms:
            atom_type = 4
        else:
            atom_type = 1
        data_f.write("{} {} {} {} {} {}\n".format(
            atom_id, molecule_id, atom_type, atom_x, atom_y, atom_z))

        atom_x += r0

    data_f.write("\n")

    data_f.write("Bonds\n")
    data_f.write("\n")

    bond_type = 1
    for bond_i in range(num_mm_bonds):
        bond_id = bond_i + 1
        atom1_id = bond_i + 1
        atom2_id = bond_i + 2
        data_f.write("{} {} {} {}\n".format(
            bond_id, bond_type, atom1_id, atom2_id))

    data_f.write("\n")

    data_f.write("Angles\n")
    data_f.write("\n")

    angle_type = 1
    for angle_i in range(num_mm_angles):
        angle_id = angle_i + 1
        atom1_id = angle_i + 1
        atom2_id = angle_i + 2
        atom3_id = angle_i + 3
        data_f.write("{} {} {} {} {}\n".format(
            angle_id, angle_type, atom1_id, atom2_id, atom3_id))

    data_f.write("\n")

    data_f.write("Dihedrals\n")
    data_f.write("\n")

    dihedral_type = 1
    for dihedral_i in range(num_mm_dihedrals):
        dihedral_id = dihedral_i + 1
        atom1_id = dihedral_i + 1
        atom2_id = dihedral_i + 2
        atom3_id = dihedral_i + 3
        atom4_id = dihedral_i + 4
        data_f.write("{} {} {} {} {} {}\n".format(
            dihedral_id, dihedral_type, atom1_id, atom2_id, atom3_id, atom4_id))

    data_f.write("\n")

################################################################################

with open(input_file_name, 'w') as f:
    f.write("units lj\n")
    f.write("dimension 3\n")

    f.write("\n")

    f.write("neighbor 1.5 bin\n")
    f.write("neigh_modify every 1 delay 0 check yes\n")

    f.write("\n")

    f.write("boundary p p p\n")

    f.write("\n")

    f.write("atom_style molecular\n")

    f.write("\n")

    f.write("pair_style lj/cut 5.0\n")

    f.write("\n")

    f.write("bond_style harmonic\n")
    f.write("angle_style harmonic\n")
    f.write("dihedral_style quadratic\n")

    f.write("\n")

    f.write("read_data {}\n".format(data_file_name))
    
    f.write("\n")
    
    f.write("pair_coeff * * {} {} {}\n".format(epsilon, sigma, rcut))
    f.write("pair_modify shift yes\n")

    f.write("\n")

    f.write("group monomers type 1\n")
    f.write("group plus_end type 3\n")
    f.write("group minus_end type 4\n")
    f.write("group free type 2\n")
    f.write("group polymer type 1 3 4\n")

    f.write("\n")

    f.write("special_bonds lj 0.0 1.0 1.0\n")

    f.write("\n")

    # f.write("region membrane cylinder z {} {} {} {} {} side in\n".format(
    #     x_mid, y_mid, Rcyl_outer, zlo, zhi))

    # f.write("\n")
    
    if autoseed:
        thisseed = np.random.randint(0, 2**16 - 1)
    else:
        thisseed = fixed_seed
    f.write("create_atoms 2 random {} {} NULL overlap 1.0 maxtry 1000\n".format(
        num_free_monomers, thisseed))

    f.write("timestep {}\n".format(time_step))

    f.write("\n")

    f.write("shell mkdir ./dump/\n")
    f.write("shell mkdir ./data/\n")

    f.write("\n")

    f.write("minimize 0.0 0.0 1000 10000\n")

    f.write("\n")

    # for n_i in range(1, num_monomers + 1):
    #     f.write("variable x{} equal x[{}]\n".format(n_i, n_i))
    #     f.write("variable y{} equal y[{}]\n".format(n_i, n_i))
    #     f.write("variable z{} equal z[{}]\n".format(n_i, n_i))
    #     f.write("\n")

    f.write("thermo_style custom step time temp etotal\n")
    f.write("thermo {}\n".format(int(run_thermo_freq)))

    f.write("\n")

    f.write("reset_timestep 0\n")
    f.write("variable tsteps equal time\n")

    f.write("\n")

    # f.write('fix monomer_pos all print {} "${{tsteps}} '.format(measure_freq))
    # for n_i in range(1, num_monomers + 1):
    #     f.write('${{x{0}}} ${{y{0}}} ${{z{0}}} '.format(n_i))

    # f.write('" file data/{} screen no\n\n'.format(position_file_name))

    f.write("\n")

    f.write("dump dumpall all atom {} dump/{}\n".format(int(dump_freq), dump_file_name))

    f.write("\n")

    f.write("fix 1 all nve\n")
    f.write("fix 2 all langevin 1.0 1.0 {} {}\n".format(
        langevin_damp, langevin_seed))
    
    f.write("fix 1000 all balance 1000 1.05 shift xy 10 1.1\n")

    f.write("\n")

    f.write("thermo {}\n".format(int(run_thermo_freq)))
    f.write("run {}\n".format(int(run_steps)))

    f.write("\n")

    f.write("write_data dump/final.data\n")
