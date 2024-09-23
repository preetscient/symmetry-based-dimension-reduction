# src/main.py
import os
import hashlib
import glob
import time

from . import batch_lumping, batch_gaut2gap, batch_auts
from . import vizprocessing

def compute_file_hash(filepath):
    """
    Computes the MD5 hash of the specified file.

    Parameters:
    filepath (str): The path to the file for which the MD5 hash will be calculated.

    Returns:
    str: The MD5 hash of the file as a hexadecimal string.
    """
    hash_md5 = hashlib.md5() # Create a new MD5 hash object
    with open(filepath, "rb") as f: # Open the file in binary mode
        for chunk in iter(lambda: f.read(4096), b""): # Read file in chunks of 4096 bytes
            hash_md5.update(chunk) # Update the hash with each chunk
    return hash_md5.hexdigest() # Return the computed hash as a hex string

def has_data_changed(DATA_FILES,HASH_FILES):
    """
    Checks if any data files have changed by comparing stored hashes with current hashes.

    Parameters:
    DATA_FILES (list): A list of paths to the data files to be checked.
    HASH_FILES (dict): A dictionary mapping each data file path to its corresponding hash file path.

    Returns:
    bool: True if any data file has changed or if any hash file is missing; otherwise, False.
    """
    for data_file in DATA_FILES: # Iterate through each data file
        hash_file = HASH_FILES[data_file] # Get corresponding hash file
        if not os.path.exists(hash_file):
            return True  # No hash file means data has not been processed
        
        # Compute the current hash of the data file
        with open(hash_file, 'r') as file:
            stored_hash = file.read().strip()
        current_hash = compute_file_hash(data_file)
        if current_hash != stored_hash:
            return True # If the current hash doesn't match the stored hash, the data has changed
    
    return False # If all hashes match, data has not changed

def store_data_hashes(DATA_FILES,HASH_FILES):
    """
    Stores the current hashes of the data files in their corresponding hash files.

    Parameters:
    DATA_FILES (list): A list of paths to the data files.
    HASH_FILES (dict): A dictionary mapping each data file path to its corresponding hash file path.

    Returns:
    None
    """
    for data_file in DATA_FILES:
        current_hash = compute_file_hash(data_file)
        with open(HASH_FILES[data_file], 'w') as file:
            file.write(current_hash)
    return

def main():
    """
    Main function to process network data files.

    This function performs the following steps:
    1. Sets up paths and identifies data files to process.
    2. Checks if any data files have changed by comparing file hashes.
    3. If no changes are detected, processing is skipped.
    4. If changes are detected:
       - Runs various processing scripts (`batch_auts`, `batch_gaut2gap`, `batch_lumping`).
       - Updates visualizations with `vizprocessing`.
       - Stores new file hashes to track processed data.
    
    Returns:
    None
    """
    current_file_path   = os.path.abspath(__file__)
    base_path = os.path.join(current_file_path, '..')
    base_path = os.path.normpath(base_path)

    # Define the path to the .scy files
    data_path = os.path.join(base_path,'data','external','1_network_data','networkrepository','*.scy')
    
    # Get a list of all data files matching the pattern in the data path
    DATA_FILES = glob.glob(data_path)
    
    # Create a dictionary mapping each data file to its corresponding hash file
    HASH_FILES = {file: f"{file}_hash.txt" for file in DATA_FILES}

    
    if not has_data_changed(DATA_FILES,HASH_FILES): # Check if any data files have changed
        print("Processing has already been completed for all data files.")
    
    else:

        print("Running saucy")
        batch_auts.main()

        print("Running gaut2gap...")
        batch_gaut2gap.main()
        
        print("Running lumping...")
        batch_lumping.main()

        print("Processing pre-loaded networks...")
        vizprocessing.main()
        
        #Store the new hashes after successful processing
        store_data_hashes(DATA_FILES,HASH_FILES)
        print("Processing complete. Data hashes updated.")
    
    return

if __name__ == '__main__':
    main()
