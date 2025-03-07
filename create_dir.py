import numpy as np
from UQpy.sampling import LatinHypercubeSampling
from UQpy.distributions import Uniform
from UQpy.sampling.stratified_sampling.latin_hypercube_criteria import *
import pandas as pd
import os

# Define number of samples to generate and distribution for each parameter
n =500

# Pressure and power
dist_pre = Uniform(loc=2000, scale=6000)
dist_pow = Uniform(loc=80e3, scale=200e3)

# Chemical rates (Park_2001)
# #1 N2+M=N+N+M:{3.0E+22},-1.6,113200.d0,1 [M = N, O]
# dist_01 = Uniform(loc=np.log(3.0e+21), scale=np.log(100))
#3 O2+M=O+O+M:{1.0E+22},-1.5,59360.d0,1 [M = N, O]
# dist_03 = Uniform(loc=np.log(1.0e+21), scale=np.log(100))
#4 O2+M=O+O+M:{2.0E+21},-1.5,59360.d0,1 [M = N2, O2, NO, N2p, O2p, NOp, Np, Op]
# dist_04 = Uniform(loc=np.log(2.0e+20), scale=np.log(100))
# #6 NO+M=N+O+M:{1.0E+17},0.0,75500.d0,1 [M = NO, N, O, Np, Op]
# dist_06 = Uniform(loc=np.log(1.0e+16), scale=np.log(100))
# #7 N2+em=N+N+em:{3.0E+24},-1.6,113200.d0,4
# dist_07 = Uniform(loc=np.log(3.0e+23), scale=np.log(100))
#9 N+em=Np+em+em:{2.5E+34},-3.82,168600.d0,9
# dist_09 = Uniform(loc=np.log(2.5e+33), scale=np.log(100))
# #13 N2+O=NO+N:{5.69E+12},0.42,42938.d0,6
# dist_13 = Uniform(loc=np.log(5.69e+11), scale=np.log(100))
# #17 NO+Op=Np+O2:{1.4E+05},1.90,15300.d0,6
# dist_17 = Uniform(loc=np.log(1.4e+04), scale=np.log(100))
#22 Op+N2=N2p+O:{9.0E+11},0.36,22800.d0,6
# dist_22 = Uniform(loc=np.log(9.0e+10), scale=np.log(100))

distributions = [dist_pre, dist_pow] #, dist_03, dist_04, dist_09, dist_22]

# Generate samples
criterion = MaxiMin(iterations=100, metric=DistanceMetric.EUCLIDEAN)
lhs = LatinHypercubeSampling(distributions=distributions, nsamples=n, random_state=np.random.RandomState(789), 
                             criterion=criterion)

# Define names of parameters
parameters = ['par_pre', 'par_pow'] #, 'par_03', 'par_04', 'par_09', 'par_22']

# Create dictionary for parameters values to store them in a .csv file
samples = []
folders = []
for i in range(n):
    sample_dict = {}
    for j in range(len(parameters)):
        values = lhs.samples[i]
        if j < 2:
            sample_dict[parameters[j]] = values[j]  # Store the value directly
        else:
            sample_dict[parameters[j]] = np.exp(values[j])  # Apply exponential to the value
    samples.append(sample_dict)


folder_name = 'samples'
if not os.path.exists(os.getcwd() + f'/../{folder_name}'):
        os.makedirs(os.getcwd() + f'/../{folder_name}')
df = pd.DataFrame(samples)
df.to_csv(os.getcwd() + f'/../{folder_name}/samples.csv')