import hashlib
from pathlib import Path
import json
import shutil

from src import processing, lumping, auts, gaut2gap
from src.visualization import viz_layout

BASE_PATH = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_PATH / 'data' / 'external' / '5_user_data'
HASH_FILE = BASE_PATH / 'data_hash.json'  # File to store the hash value


def calculate_dir_hash(directory: Path) -> str:
    """
    Calculate a combined hash for all files in the specified directory based solely on their contents.
    Args:
        directory (Path): The directory path whose contents will be hashed.
    Returns:
        str: A hexadecimal string representing the combined hash of the directory contents.
    """
    hash_obj = hashlib.sha256()

    # Walk through each file in the directory (recursively) and sort for stable order
    for file_path in sorted(directory.rglob('*')):
        if file_path.is_file() and file_path.name != '.DS_Store':
            # Open and read the file in binary mode
            with open(file_path, 'rb') as file:
                while chunk := file.read(8192):  # Read file in chunks
                    hash_obj.update(chunk)
    
    # Return the resulting hash as a hexadecimal string
    return hash_obj.hexdigest()

def read_stored_hash() -> str:
    """
    Reads the stored hash from the HASH_FILE if it exists (HASH_FILE is stored at the start of this script).
    Handles cases where the file is empty or corrupted.
    
    Returns:
        str: The stored hash string if it exists and is valid, otherwise an empty string.
    """
    if HASH_FILE.exists():
        try:
            with open(HASH_FILE, 'r') as f:
                data = json.load(f)
                return data.get('dir_hash', '')
        except (json.JSONDecodeError, KeyError):
            # If the file is empty or corrupt, return an empty string
            print("Hash file is empty or corrupted. Returning an empty stored hash.")
            return ''
    return ''


def store_hash(new_hash: str):
    """
    Stores the calculated hash in HASH_FILE which is set at the start of this script.

    Args:
        new_hash (str): The new hash string to be stored.
    """

    with open(HASH_FILE, 'w') as f:
        json.dump({'dir_hash': new_hash}, f)
    return

def clear_folders(folders):
    """
    Clear all files and subdirectories within the specified folders.

    Args:
        folders (list[Path]): A list of folder paths to be cleared.
    """

    for folder in folders:
        if folder.exists() and folder.is_dir():
            print(f"Clearing folder: {folder}")
            # Remove all files and subdirectories within the folder
            for item in folder.iterdir():
                if item.is_file():
                    item.unlink()  # Delete the file
                elif item.is_dir():
                    shutil.rmtree(item)  # Delete the directory and its contents
    return

def main():
    """
    Main function to check for changes in user data and run necessary processing steps.

    It calculates the current hash of the user data directory and compares it with the stored hash.
    If there are changes, it clears specific folders, runs the data processing steps, and updates the stored hash.
    Finally, it runs the visualization process.
    """
    current_hash = calculate_dir_hash(DATA_DIR)
    stored_hash = read_stored_hash()
    
    if current_hash == stored_hash:
        print("Files are unchanged, skipping processes.")
    else:
        print("Files have changed, running processes...")

        CLEAR_FOLDERS=[
            BASE_PATH / 'data' / 'processed' / 'gap_output',
            BASE_PATH / 'data' / 'processed' / 'lumping_output',
            BASE_PATH / 'data' / 'processed' / 'processing_output',
            BASE_PATH / 'data' / 'processed' / 'saucy_output',
            BASE_PATH / 'data' / 'processed' / 'viz_files'
        ]

        print("Clearing old files to visualise new user data...")
        clear_folders(CLEAR_FOLDERS)

        print("Running processing...")
        processing.main()

        print("Running Saucy...")
        auts.main()

        print("Processing data for GAP")
        gaut2gap.main()

        print("Running lumping...")
        lumping.main()

        # Store the new hash after running the processes
        store_hash(current_hash)

    print("Running visualisation...")
    viz_layout.main()

if __name__ == "__main__":
    main()
