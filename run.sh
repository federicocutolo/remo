#!/bin/bash

# FILENAME: datagen_2D_torch

#SBATCH -J datagen_1000_samples              # Job name
#SBATCH --output=/dev/null                   # Suppress stdout (avoid in parallelization)
#SBATCH --error=/dev/null                    # Suppress stderr (avoid in parallelization)
#SBATCH -p shared                            # Name of the queue ("shared" if ntasks<128)
#SBATCH --array=0-499                        # Define the range of the job array (SLURM_ARRAY_TASK_ID)
#SBATCH --ntasks=1                           # Number of tasks (processes) per job
#SBATCH --cpus-per-task=4                    # Number of CPU cores per task (adjust as needed)
#SBATCH --time=30:00:00                      # Walltime

# Load modules
source ~/.bashrc
modules

# Remember to activate conda env with all python libraries required by the code!

# Run script
python3 parallel_run.py
