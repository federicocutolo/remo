import os

def activate_restart(sample_folder):
    log_file_path = os.path.join(sample_folder, 'output', '$fluid_solver.log')
    input_file_path = os.path.join(sample_folder, 'exec', 'input_$fluid_solver')

    # If the $fluid_solver.log file exists the simulation did't converge, so activate restart flags
    if os.path.exists(log_file_path):
        # Read the content of input_$fluid_solver
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
        # Uncomment the specific lines
        with open(input_file_path, 'w') as file:
            for line in lines:
                if line.strip().startswith('#SIMULATION_RESTART_PATH'):
                    file.write('SIMULATION_RESTART_PATH = ../output\n')
                elif line.strip().startswith('#SIMULATION_RESTART_FILE'):
                    file.write('SIMULATION_RESTART_FILE = flowfield_NS_NLTE.cgns\n')
                else:
                    file.write(line)

        print(f"Modified {input_file_path} as {log_file_path} was found.")
    else:
        print(f"{log_file_path} not found. No changes made to {input_file_path}.")
