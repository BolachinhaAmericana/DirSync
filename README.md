# DirSync

Small project that synchronizes two directories from a one-sided perspective, performing a regular backup of the source directory.

## How it Works

DirSync performs a contents scan for every directory and sub-directory and checks the integrity of all files using sha256. 
The checkup is periodic as per an interval taken as argument. Every checkup verifies if the source and destination directories' content align.
If the latter don't perfectly match, synchronization takes place, adjuring every difference in the destination to reflect the source.

## Usage
1. Clone this Git Repository\
2. run ```$python3 main.py [source_dir] [backup_dir] [logfile] [time] ```
\
where:
- source_dir - directory you wish to backup
- backup_dir - path where the backup will be stored
- logfile - file to store the logs
- time: int- interval (in minutes) to periodically perform the checkup and backup

### Notes and possible issues
The path must me relative to current directory.
