import hashlib
from pathlib import Path
from src import processing, lumping, auts, gaut2gap
from src.visualization import viz_layout

BASE_PATH = Path(__file__).resolve().parents[1]

HASH_FILE = "last_hash.txt"
DATA_DIR = BASE_PATH / 'data' / 'external' / '5_user_data'

def calculate_hash(directory):
    """Calculate a hash for all files and directories in the given directory."""
    hash_md5 = hashlib.md5()

    for filepath in sorted(Path(directory).rglob('*')):  # Sorting for consistency
        if filepath.is_file():
            with open(filepath, 'rb') as f:
                while chunk := f.read(4096):
                    hash_md5.update(chunk)
        elif filepath.is_dir():
            # Include directory names in the hash, normalized as string paths
            hash_md5.update(str(filepath).encode('utf-8'))

    return hash_md5.hexdigest()

def load_previous_hash(hash_file):
    """Load the previous hash from the hash file."""
    hash_file_path = Path(hash_file)
    if hash_file_path.exists():
        with open(hash_file_path, 'r') as f:
            return f.read().strip()
    return None

def save_current_hash(hash_file, current_hash):
    """Save the current hash to the hash file."""
    with open(hash_file, 'w') as f:
        f.write(current_hash)

def main():
    # Calculate the current hash for the user data directory
    current_hash = calculate_hash(DATA_DIR)
    previous_hash = load_previous_hash(HASH_FILE)

    if current_hash != previous_hash:
        print("Data has changed. Running necessary processes...")

        print("Running processing...")
        processing.main()

        print("Running Saucy...")
        auts.main()

        print("Processing data for GAP")
        gaut2gap.main()

        print("Running lumping...")
        lumping.main()

        # Save the new hash after the processes have been run
        save_current_hash(HASH_FILE, current_hash)
    else:
        print("No changes in user data. Skipping processes.")

    print("Running visualisation...")
    viz_layout.main()

if __name__ == "__main__":
    main()
