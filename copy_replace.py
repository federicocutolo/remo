import os
import shutil

def replace(dict_values, filename_template, filename_out, symbolleft="(", symbolright=")"):
    # Extract the directory from the filename
    directory = os.path.dirname(filename_out)
    lines = []
    with open(filename_template, "r") as fileread:
        for line in fileread:
            line_new = line
            for param, value in dict_values.items():
                 line_new = line_new.replace(f"{symbolleft}{param}{symbolright}",f"{value}")
            line = line_new
            lines.append(line)
        with open(filename_out, "w+") as filewrite:
            for line in lines:
                filewrite.write(line)

def copy_replace(sample_folder, sample_dict):
    # Copy template folder for each sample
    shutil.copytree('../folder.template', sample_folder)
    # Substitute parameter values inside sample[i] everytime "{par_xx}" is found in the folder.template.
    for root, dirs, files in os.walk(sample_folder):
        if root in(sample_folder + "/input", "/output"):
            continue # skip input and output folders from param replacement
        for name in files:
            if name in("flux2D"):
                continue # skip non txt files
            path_file = os.path.join(root, name)
            replace(sample_dict, path_file, path_file, symbolleft="{", symbolright="}")