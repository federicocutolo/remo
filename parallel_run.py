from multiprocessing import Pool
import subprocess
import pandas as pd
import os
import time
import shutil
from extract_qoi import extract_qoi
from copy_replace import copy_replace
from check_termination import check_log_for_termination, check_log_for_errors
from cleanup import cleanup
from restart_solution import activate_restart

def parallel_run(sample):

    sample_folder = cwd + f"../samples/sample_{sample:04d}/"
    successful_samples = cwd + "/../samples/successful_samples"
    failed_samples = cwd + "/../samples/failed_samples"
    exe = sample_folder + 'exec/'

    # Check if sample folder exists
    if os.path.exists(sample_folder):
        $fluid_solver_log_file = exe + '../output/$fluid_solver.log'
        
        if os.path.isfile($fluid_solver_log_file):
            # $fluid_solver.log found, activate restart and run the sample
            print("Sample folder exists and $fluid_solver.log found. Activating restart and running the sample.")
            activate_restart(sample_folder)
            # 
            # Remove specified directories and files
            directories_to_remove = ["ParaView", "precice-run"]
            files_to_remove = ["species", "components", "elements"]

            for directory in directories_to_remove:
                dir_path = os.path.join(exe, directory)
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")

            for file in files_to_remove:
                file_path = os.path.join(exe, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")

        else:
            # $fluid_solver.log not found, sample is considered converged
            print("Sample folder exists but $fluid_solver.log not found. Assuming sample is converged.")
            return
    else:
        # Sample folder does not exist, create it and proceed
        print(f"Sample folder does not exist. Creating folder and running the sample.")
        # Create the folder and directories
        os.makedirs(cwd + "/../samples/successful_samples", exist_ok=True)
        os.makedirs(cwd + "/../samples/failed_samples", exist_ok=True)
        
        sample_dict = df.iloc[sample]
        copy_replace(sample_folder, sample_dict)

    # Define commands for $electromagnetic_solver and $fluid_solver.
    row = df.iloc[sample]
    $fluid_solver_command = '$fluid_solver input_$fluid_solver 2>&1 | tee ../output/$fluid_solver.log'
    $electromagnetic_solver_command = f'$electromagnetic_solver2D -m ../../../mesh/$electromagnetic_solver_farfield.mesh -p precice-config_efield.xml 2>&1 | tee ../output/$electromagnetic_solver.log'

    try:
        # Run $electromagnetic_solver + $fluid_solver
        process_$fluid_solver = subprocess.Popen($fluid_solver_command, cwd=exe, shell=True)
        process_$electromagnetic_solver  = subprocess.Popen($electromagnetic_solver_command, cwd=exe, shell=True)

        while True:
            time.sleep(5)  # Check success/failure every 5 seconds
            
            if check_log_for_termination($fluid_solver_log_file):
                print("Termination term found in $fluid_solver log.")
                if check_log_for_errors($fluid_solver_log_file):
                    print("Errors found in $fluid_solver log. Terminating processes...")
                    process_$fluid_solver.terminate()
                    process_$electromagnetic_solver.terminate()
                    with open(failed_samples, 'a') as file:
                        file.write(f'{sample}\n')
                else:
                    print("No errors found. Marking as successful and terminating processes...")
                    process_$fluid_solver.terminate()
                    process_$electromagnetic_solver.terminate()
                    with open(successful_samples, 'a') as file:
                        file.write(f'{sample}\n')

                break  # Exit the while loop after handling termination

        return_code_$fluid_solver = process_$fluid_solver.wait()
        return_code_$electromagnetic_solver = process_$electromagnetic_solver.wait()
    
        print(f'$fluid_solver finished with return code {return_code_$fluid_solver}')
        print(f'$electromagnetic_solver finished with return code {return_code_$electromagnetic_solver}')

    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
    
    # Extract QoI and save output in a new file 'solution'
    print("Extracting QoI from flowfield.cgns")
    extract_qoi(sample_folder)

    # Perform cleanup
    print("Performing cleanup of sample folder")
    cleanup(sample_folder)

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    cwd = os.getcwd() + '/'
    df = pd.read_csv(cwd + "../samples/samples.csv")

    # Retrieve the SLURM_ARRAY_TASK_ID and use it to select the sample
    task_id = int(os.getenv('SLURM_ARRAY_TASK_ID'))
    parallel_run(task_id)
