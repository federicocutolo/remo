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
        hegel_log_file = exe + '../output/hegel.log'
        
        if os.path.isfile(hegel_log_file):
            # hegel.log found, activate restart and run the sample
            print("Sample folder exists and hegel.log found. Activating restart and running the sample.")
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
            # hegel.log not found, sample is considered converged
            print("Sample folder exists but hegel.log not found. Assuming sample is converged.")
            return
    else:
        # Sample folder does not exist, create it and proceed
        print(f"Sample folder does not exist. Creating folder and running the sample.")
        # Create the folder and directories
        os.makedirs(cwd + "/../samples/successful_samples", exist_ok=True)
        os.makedirs(cwd + "/../samples/failed_samples", exist_ok=True)
        
        sample_dict = df.iloc[sample]
        copy_replace(sample_folder, sample_dict)

    # Define commands for flux and hegel.
    row = df.iloc[sample]
    hegel_command = 'hegel input_hegel 2>&1 | tee ../output/hegel.log'
    flux_command = f'flux2D -m ../../../mesh/flux_farfield.mesh -p precice-config_efield.xml -cr 0.05 -cls 0.08382 -cle 0.367063 -o 1 -f 2.1e6 -pdt 0.00000001 -pr 100 -power {row["par_pow"]} -nc 3 -co_r 59.42e-3 -co_loc \'132.435e-3 166.435e-3 200.435e-3\'' #2>&1 | tee ../output/flux.log

    try:
        # Run flux + hegel
        process_hegel = subprocess.Popen(hegel_command, cwd=exe, shell=True)
        process_flux  = subprocess.Popen(flux_command, cwd=exe, shell=True)

        while True:
            time.sleep(5)  # Check success/failure every 5 seconds
            
            if check_log_for_termination(hegel_log_file):
                print("Termination term found in hegel log.")
                if check_log_for_errors(hegel_log_file):
                    print("Errors found in hegel log. Terminating processes...")
                    process_hegel.terminate()
                    process_flux.terminate()
                    with open(failed_samples, 'a') as file:
                        file.write(f'{sample}\n')
                else:
                    print("No errors found. Marking as successful and terminating processes...")
                    process_hegel.terminate()
                    process_flux.terminate()
                    with open(successful_samples, 'a') as file:
                        file.write(f'{sample}\n')

                break  # Exit the while loop after handling termination

        return_code_hegel = process_hegel.wait()
        return_code_flux = process_flux.wait()
    
        print(f'hegel finished with return code {return_code_hegel}')
        print(f'flux finished with return code {return_code_flux}')

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
