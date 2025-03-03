import os
import shutil
import filecmp
import argparse
from tqdm import tqdm
from functions import *

# Function to check if the source and destination directories exist
def check_directories(src_dir, dst_dir):
    # Check if the source directory exists
    if not os.path.exists(src_dir):
        mess = f"\nSource directory '{src_dir}' does not exist."
        print(mess)
        log(mess)
        return False
    # Create the destination directory if it does not exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        mess = f"\nDestination directory '{dst_dir}' created."
        print(mess)
        log(mess)
    return True

# Function to synchronize files between two directories
def sync_directories(src_dir, dst_dir, delete=False):
    # Get a list of all files and directories in the source directory
    files_to_sync = []
    for root, dirs, files in os.walk(src_dir):
        log(f"root-> {root}, dirs-> {dirs}, files-> {files}")
        for directory in dirs:
            files_to_sync.append(os.path.join(root, directory))
        for file in files:
            files_to_sync.append(os.path.join(root, file))

    # Iterate over each file in the source directory with a progress bar
    with tqdm(total=len(files_to_sync), desc="Syncing files", unit="file") as pbar:
        # Iterate over each file in the source directory
        for source_path in files_to_sync:
            # Get the corresponding path in the replica directory
            replica_path = os.path.join(dst_dir, os.path.relpath(source_path, src_dir))

            # Check if path is a directory and create it in the replica directory if it does not exist
            if os.path.isdir(source_path):
                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)
            # Copy all files from the source directory to the replica directory
            else:
                # Check if the file exists in the replica directory and if it is different from the source file
                if not os.path.exists(replica_path) or not filecmp.cmp(source_path, replica_path, shallow=False):
                    # Set the description of the progress bar and print the file being copied
                    pbar.set_description(f"Processing '{source_path}'")
                    mess = f"\nCopying {source_path} to {replica_path}"
                    print(mess)
                    log(mess)

                    try:
                       # Copy the file from the source directory to the replica directory
                       shutil.copy2(source_path, replica_path)
                    except (PermissionError, FileNotFoundError,UnicodeEncodeError) as e:
                        mess = f"{e.strerror} Error copying {source_path} to {replica_path}"
                        log(mess, fn="error_log.log")

            # Update the progress bar
            pbar.update(1)
# Listing directories, subdirectories and files
def list_directories(_dir):
    files_to_copy = []
    for root, dirs, files in os.walk(_dir):
        for directory in dirs:
            files_to_copy.append(os.path.join(root, directory))
        for file in files:
            files_to_copy.append(os.path.join(root, file))
    return files_to_copy


def clean_backup(src_dir, dst_dir):
    pass

if __name__ == "__main__":
    src_pth = "C:\\"

    dst_pth = "F:\\sauvegarde-mike"
    check_directories(src_pth,dst_pth)
    sync_directories(src_pth, dst_pth)

#dr_lst = list_directories("C:\\Users")

#for dr in dr_lst:
#    print(dr)

