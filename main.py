#!/bin/python3

import os
import sys
import shutil
import hashlib
from datetime import datetime
import time

def calculate_sha256(file_path):
    # returns unique string from argument so can check if file identity matches 
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk:= file.read(8192):
            sha256.update(chunk)
        return sha256.hexdigest()

def log_changes(log_file, action, file_path):
    # Updates logfile acording to action
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_entry = f"[{timestamp}] {action}: {file_path}\n"
    with open(log_file, 'a') as log:
        log.write(log_entry)
    return log_entry

def check_log_existense(log_file):
    # checks if logfile already exists
    if not os.path.exists(log_file):
        open(log_file, 'w')


def update_backup(source_dir, dest_dir, log_file):
    # Performs checkup and backup on source and dest dirs.


    for root, dirs, files in os.walk(source_dir):
        # Walks trough all source dirs/subdirs/files
        dest_root = os.path.join(dest_dir, os.path.relpath(root, source_dir))

        for d in dirs: # compare source dirs to dest dirs
            dest_subdir = os.path.join(dest_root, d)
            if not os.path.exists(dest_subdir):
                os.makedirs(dest_subdir)
        
        for f in files: # compare source files to dest files
            src_file = os.path.join(root, f)
            dest_file = os.path.join(dest_root, f)
            
            # check if dest's file identity matches source 
            if not os.path.exists(dest_file) or calculate_sha256(src_file) != calculate_sha256(dest_file):
                # sets action accordingly and calls log update fuction to document changes
                action = "Updated" if os.path.exists(dest_file) else "Created"
                shutil.copy2(src_file, dest_file)
                print(log_changes(log_file, action, dest_file))

    for root, dirs, files in os.walk(dest_dir):
        # Walks trough all dest dirs/subdirs/files
        src_root = os.path.join(source_dir, os.path.relpath(root, dest_dir))

        for f in files:
            src_file = os.path.join(src_root, f)
            dest_file = os.path.join(root, f)
            
            # if file no longer in dest, delete file
            if not os.path.exists(src_file):
                os.remove(dest_file)
                print(log_changes(log_file, "Deleted", dest_file))

    # informs console that a checkup has just occured
    print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] Checkup Completed:')

def get_arguments():
    source_dir = str(sys.argv[1])
    dest_dir = str(sys.argv[2])
    log_file = str(sys.argv[3])
    sync_interval = int(sys.argv[4])

    return source_dir, dest_dir, log_file, sync_interval

def timing(log_file):
    # returns how long since last backup
    try:
        with open(log_file, 'r') as log:
            lines = log.readlines()
        if lines:
            last_line = lines[-1]
            timestamp_str = last_line.split(']')[0][1:]
            return datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M:%S')
    except FileNotFoundError:
        pass
    return datetime.min

def run_backup_periodically(source_dir, dest_dir, log_file, seconds):
    # executes synchronization with a timer.

    while True:
        # Check the timestamp of the last log entry
        last_log_timestamp = timing(log_file)
        # Calculate time elapsed since the last execution
        elapsed_time = (datetime.now() - last_log_timestamp).total_seconds()
        # If enough time has passed, run the backup immediately
        if elapsed_time >= (seconds * 60):
            update_backup(source_dir, dest_dir, log_file)
            time_until_next_backup = (seconds * 60)
            time.sleep(time_until_next_backup)
        else:
            # Calculate the time until the next scheduled backup
            time_until_next_backup = (seconds * 60) - elapsed_time
            print(f"Next backup scheduled in {time_until_next_backup} seconds.")
            time.sleep(time_until_next_backup)
    
def relpath(path):
    return os.path.join(os.getcwd(), path)

def main():
    try:
        source_dir, dest_dir, log_file, sync_interval = get_arguments()
        check_log_existense(log_file)

        source_dir, dest_dir, log_file = relpath(source_dir), relpath(dest_dir), relpath(log_file)
        run_backup_periodically(source_dir, dest_dir, log_file, sync_interval)

    except IndexError:
        print('''Error, you should be passing the following arguments:
                 Source Dir Path :str
                 Backup Destination Path :str
                 Log File Path :str
                 AutoBackup Timing (minutes) :int ''')

    return

if __name__ == '__main__':
    
    main()
    
    #source_dir = "/home/valente/Desktop/DirBacker/source/"
    #dest_dir = "/home/valente/Desktop/DirBacker/backup/"
    #log_file = "/home/valente/Desktop/DirBacker/log.txt"
    #sync_interval = 0.5

