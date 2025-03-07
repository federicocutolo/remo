import shutil
import os

def cleanup(sample_folder):
    
    # Copy input files (hegel, plato)
    input_hegel = sample_folder + 'exec/input_hegel'
    input_plato = sample_folder + 'database/kinetics/air11_park01'
    input_files = [input_hegel, input_plato]

    for input_file in input_files:
        try:
            shutil.copy2(input_file, sample_folder)
            print(f'Copied {input_file} to {sample_folder}')
        except FileNotFoundError:
            print(f'Error: {input_file} not found. Copy operation skipped.')

    # Remove everything but input files and outputs
    folders_list = ['database/', 'exec/', 'input/']
    files_list = ['CFL_history.dat', 'flowfield_NS_NLTE.cgns', 'flux.log', 'hegel.log', 'mach_endian.dat']

    for folder in folders_list:
        folder_path = sample_folder + folder
        try:
            shutil.rmtree(folder_path)
            print(f'Removed folder: {folder_path}')
        except FileNotFoundError:
            print(f'Error: {folder_path} not found. Removal operation skipped.')
        except OSError as e:
            print(f'Error: {e.strerror}. Failed to remove {folder_path}.')

    for file in files_list:
        file_path = sample_folder + 'output/' + file
        try:
            os.remove(file_path)
            print(f'Removed file: {file_path}')
        except FileNotFoundError:
            print(f'Error: {file_path} not found. Removal operation skipped.')

    print('Cleanup completed.')

# Perform cleanup in the current sample folder
# cleanup(os.getcwd() + '/')