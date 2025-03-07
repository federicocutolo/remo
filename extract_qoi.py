import numpy as np
import pandas as pd
import os
import h5py

# Define cases list

def extract_qoi(sample_folder):
    sol_dir = sample_folder + "output/"
    
    # Convert .cgns files from ADF to HDF
    folder = os.listdir(sol_dir)
    for i in folder:
        if i.find('flowfield_NS_NLTE') != -1:
            os.system(f"cgnsconvert -hf {i}")

    sol = sol_dir + '/flowfield_NS_NLTE.cgns'
    print(sol_dir)

    # Define quantity of interest subset
    # X_em, X_N, X_O, X_N2, X_NO, X_O2, X_N2p, X_NOp, X_Np, X_O2p, X_Op, Th, Tve, rho, p, H, Mf, u, v, w
    qoi = ['Th', 'Tve', 'X_N', 'X_O', 'X_NO', 'Mf', 'u', 'v', 'H']

    # Define mesh block of interest (for multiblock grid)
    zone = 1

    # Read coordinates and define points grid
    with h5py.File(sol,'r') as f:
        Y = np.array(f[f'/Base_/Zone_000{zone}/GridCoordinates/CoordinateY/ data'])
        X = np.array(f[f'/Base_/Zone_000{zone}/GridCoordinates/CoordinateX/ data'])
    Xc = 0.5 * X[1:,1:] + 0.5 * X[:-1,:-1]
    Yc = 0.5 * Y[1:,1:] + 0.5 * Y[:-1,:-1]

    # Extract flowfield qois at torch exit
    outlet_field = np.empty((Xc.shape[0], len(qoi)))
    with h5py.File(sol,'r') as f:
    	for i, qty in enumerate(qoi):
            outlet_field_ = np.array(f[f'/Base_/Zone_000{zone}/flowfield_NS_NLTE/{qty}/ data'])
            outlet_field[:,i] = outlet_field_[:,-1]

    # Store qois in case.dat file
    y_coord = Yc[:,-1].reshape(-1, 1)
    outlet_field = np.hstack((y_coord, outlet_field))
    print(outlet_field.shape)
    q = ['y', 'Th', 'Tve', 'X_N', 'X_O', 'X_NO', 'Mf', 'u', 'v', 'H']
    df = pd.DataFrame(outlet_field, columns=q)
    df.to_csv(sol_dir + f'solution.dat', index=False)

    return df
