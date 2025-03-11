# README

## Parallel Simulation Handler

This script executes multiple simulations in parallel using a thermo-fluid dynamics solver and an electromagnetic solver. It manages simulation folders, handles restarts, monitors progress, and cleans up after execution.

### Requirements
- Python 3
- Required modules: `multiprocessing`, `subprocess`, `pandas`, `os`, `time`, `shutil`
- Additional dependencies: `extract_qoi`, `copy_replace`, `check_termination`, `cleanup`, `restart_solution`

### How It Works
1. **Parallel Execution:** The script runs multiple simulations in parallel using multiprocessing.
2. **Folder Management:** It checks for existing sample folders and either restarts or creates new ones.
3. **Execution:** It runs the thermo-fluid dynamics solver and the electromagnetic solver.
4. **Monitoring:** It checks log files for termination and errors, handling failures accordingly.
5. **Post-Processing:** It extracts QoI (Quantity of Interest) and cleans up simulation folders.

### Usage
To run the script, execute:
```bash
python parallel_run.py
```

### Code Overview
- `parallel_run(sample)`: Handles execution for a single sample.
- `copy_replace(sample_folder, sample_dict)`: Copies necessary files.
- `extract_qoi(sample_folder)`: Extracts QoI from simulation results.
- `check_log_for_termination(hegel_log_file)`: Checks if a simulation has completed.
- `check_log_for_errors(hegel_log_file)`: Identifies errors in the simulation logs.
- `cleanup(sample_folder)`: Cleans up unnecessary files after execution.

### Execution Process
1. **Check if the sample folder exists:**
   - If it exists and contains a log file, the script restarts the sample.
   - If it doesn't exist, the script creates it and prepares the necessary files.

2. **Run the simulations:**
   - The script constructs and executes commands for the thermo-fluid dynamics solver and the electromagnetic solver.
   - The process runs asynchronously while checking for termination and errors.

3. **Handle errors:**
   - If an error is detected, the sample is marked as failed.
   - If no errors occur, it is marked as successful.

4. **Extract QoI and cleanup:**
   - QoI is extracted from the results.
   - Temporary files are deleted to save space.

### Environment Variables
- `SLURM_ARRAY_TASK_ID`: Used to determine which sample to run in a cluster environment.

### Notes
- Ensure all dependencies are correctly installed.
- Adjust solver commands if running on a different system.
- Modify the script to customize logging and error handling.

For further modifications, refer to the function definitions within the script.

