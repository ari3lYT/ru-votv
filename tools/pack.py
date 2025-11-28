import os
import subprocess
import argparse
import sys

def pack_pak(input_path, output_pak_path, mount_point=None):
    """
    Packs files into a .pak file using u4pak.py.
    """
    u4pak_path = os.path.join(os.path.dirname(__file__), 'u4pak', 'u4pak.py')
    if not os.path.exists(u4pak_path):
        print(f"Error: u4pak.py not found at {u4pak_path}")
        return

    if not os.path.exists(input_path):
        print(f"Error: Input directory not found at {input_path}")
        return

    output_dir = os.path.dirname(output_pak_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # u4pak.py pack <archive> <files>
    # We need to list all files in the input directory.
    files_to_pack = []
    for root, _, files in os.walk(input_path):
        for file in files:
            files_to_pack.append(os.path.join(root, file))

    # The paths for u4pak need to be relative to the input directory
    # and need to be in the format expected by the game.
    # For now, we will assume the structure in input_path is correct.
    # u4pak expects file paths relative to the current working directory.
    # Let's run it from the input_path directory.

    relative_files = [os.path.relpath(p, input_path) for p in files_to_pack]

    command = [
        sys.executable,
        os.path.abspath(u4pak_path),
        'pack',
    ]
    if mount_point:
        command += ['--mount-point', mount_point]
    command.append(os.path.abspath(output_pak_path))
    command += relative_files

    print(f"Running command: {' '.join(command)}")
    try:
        # We change the cwd to the input path to handle relative paths correctly.
        subprocess.run(command, check=True, cwd=input_path)
        print("Packing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during packing: {e}")
    except FileNotFoundError:
        print("Error: 'python' command not found. Make sure Python is installed and in your PATH.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pack files into an Unreal Engine 4 .pak file.')
    parser.add_argument('input_path', help='Directory containing the files to pack.')
    parser.add_argument('output_pak_path', help='Path to the output .pak file.')
    parser.add_argument('--mount-point', dest='mount_point', default=None, help='Optional mount point to pass to u4pak.')
    args = parser.parse_args()

    pack_pak(args.input_path, args.output_pak_path, args.mount_point)
