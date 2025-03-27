import os
import sys
import time
import argparse

def list_files_and_dirs_recursive(root):
    files_dict = {}
    dirs_set = set()
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).lower()
        dirs_set.add(rel_dir)
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            relative_path = os.path.relpath(full_path, root).lower()
            size = os.path.getsize(full_path)
            files_dict[relative_path] = size
    return files_dict, dirs_set

def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"

def print_progress_bar(copied, total_size, start_time, bar_length=30):
    percent = copied / total_size
    filled_length = int(bar_length * percent)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    elapsed = time.time() - start_time
    speed = copied / elapsed if elapsed > 0 else 0
    remaining = (total_size - copied) / speed if speed > 0 else 0
    sys.stdout.write(
        f"\r|{bar}| {percent*100:5.1f}% "
        f"({human_readable_size(copied)}/{human_readable_size(total_size)}) "
        f"ETA: {int(remaining)}s"
    )
    sys.stdout.flush()

def copy_with_progress(src, dst):
    total_size = os.path.getsize(src)
    copied = 0
    buffer_size = 1024 * 1024  # 1MB
    start_time = time.time()

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            buf = fsrc.read(buffer_size)
            if not buf:
                break
            fdst.write(buf)
            copied += len(buf)
            print_progress_bar(copied, total_size, start_time)
    print(f"\n✓ Copied: {os.path.basename(src)}")

def sync_directories(origin, destination, log_file):
    print("Reading source...")
    origin_files, origin_dirs = list_files_and_dirs_recursive(origin)
    print(f"{len(origin_files)} files and {len(origin_dirs)} folders in source.")

    print("Reading destination...")
    dest_files, dest_dirs = list_files_and_dirs_recursive(destination)
    print(f"{len(dest_files)} files and {len(dest_dirs)} folders in destination.")

    errors = []

    # Create missing folders
    for rel_dir in origin_dirs:
        if rel_dir not in dest_dirs:
            dest_dir_full = os.path.join(destination, rel_dir)
            try:
                os.makedirs(dest_dir_full, exist_ok=True)
                print(f"✓ Folder created: {dest_dir_full}")
            except Exception as e:
                print(f"✗ Error creating folder: {dest_dir_full} -> {e}")
                errors.append(f"Folder: {dest_dir_full} | Error: {e}")

    # Copy missing or different files
    for rel_path, size in origin_files.items():
        dest_size = dest_files.get(rel_path)
        origin_full = os.path.join(origin, rel_path)
        dest_full = os.path.join(destination, rel_path)
        if dest_size is None or dest_size != size:
            try:
                os.makedirs(os.path.dirname(dest_full), exist_ok=True)
                print(f"Starting copy: {rel_path}")
                copy_with_progress(origin_full, dest_full)
            except Exception as e:
                print(f"\n✗ Error copying {rel_path}: {e}")
                errors.append(f"File: {origin_full} | Error: {e}")

    # Final report
    print("\nProcess completed!")

    if errors:
        print("\n⚠️ Some files/folders could not be copied. Generating log...")
        try:
            with open(log_file, 'w') as log:
                for item in errors:
                    log.write(item + "\n")
            print(f"\nLog saved at: {os.path.abspath(log_file)}")
        except Exception as e:
            print(f"Error saving log: {e}")
    else:
        print("\nAll missing files and folders were successfully copied!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync missing or changed files from one directory to another.")
    parser.add_argument("origin", help="Source directory to copy files from")
    parser.add_argument("destination", help="Destination directory to copy files to")
    parser.add_argument("--log", default="transfer_errors.txt", help="Optional path for error log file")

    args = parser.parse_args()

    if not os.path.exists(args.origin):
        print(f"❌ Source path does not exist: {args.origin}")
        sys.exit(1)

    if not os.path.exists(args.destination):
        print(f"❌ Destination path does not exist: {args.destination}")
        sys.exit(1)

    sync_directories(args.origin, args.destination, args.log)
