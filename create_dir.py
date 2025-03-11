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
