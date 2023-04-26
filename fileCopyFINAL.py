# This script is to copy the last two days of folderStart to a subfolder called folderEnd with a root folder of last date capture.
# i.e now is 20230420 and this script will copy over from 20230418 00:00 (HH:MM) to 20230419 23:59 (HH:MM) into a folder of called 20230419
#
# Script also excludes any folders called 'test' or 'folder2' - modify this to reflect unwanted folder duplication
# Script should be set to a cron job for every two days to avoid duplicate files  
#
# Example folder Start
# folderStart
# ├── DUMP
# │   ├── HFS_timestamp_SAT_nnn.csv
# │   ├── HFS_timestamp_SAT_nnn.dmp
# │   ├── HFS_timestamp_SAT_nnn.fss
# │   ├── HFS_timestamp_SAT_nnn.jpg
# │   ├── HFS_timestamp_SAT_nnn.lfe
# │   └── HFS_timestamp_SAT_nnn.png
# ├── GIF
# │   ├── IR1
# │   │   └── timestampSAT.gif
# │   ├── IR2
# │   │   └── timestampSAT.gif
# │   ├── IR3
# │   │   └── timestampSAT.gif
# │   ├── VIS1
# │   │   └── timestampSAT.gif
# │   ├── VIS2
# │   │   └── timestampSAT.gif
# │   └── VIS3
# ├── JPG
# │   ├── 1ovf
# │   │   └── timestampSAT.JPG
# │   ├── 4ovf
# │   │   └── timestampSAT.JPG
# │   └── IR2
# │       └── timestampSAT.JPG
# ├── file1.txt
# ├── file2.txt
# ├── file3.txt
# ├── file4.txt
# ├── file5.txt
# ├── test
# │   └── test1.txt
# └── test.txt
#
# Will end up with:
# folderEnd
# └── 20230418
#     ├── DUMP
#     │   ├── HFS_timestamp_SAT_nnn.csvll 
#     │   ├── HFS_timestamp_SAT_nnn.dmp
#     │   ├── HFS_timestamp_SAT_nnn.fss
#     │   ├── HFS_timestamp_SAT_nnn.jpg
#     │   ├── HFS_timestamp_SAT_nnn.lfe
#     │   └── HFS_timestamp_SAT_nnn.png
#     ├── GIF
#     │   ├── IR1
#     │   │   └── timestampSAT.gif
#     │   ├── IR2
#     │   │   └── timestampSAT.gif
#     │   ├── IR3
#     │   │   └── timestampSAT.gif
#     │   ├── VIS1
#     │   │   └── timestampSAT.gif
#     │   └── VIS2
#     │       └── timestampSAT.gif
#     └── JPG
#         ├── 1ovf
#         │   └── timestampSAT.JPG
#         ├── 4ovf
#         │   └── timestampSAT.JPG
#         └── IR2
#            └── timestampSAT.JPG

import os
import shutil
import datetime
import time

t0 = time.perf_counter()

# Get the date of yesterday
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# Source and exclude folders
source_folder = "/home/gorilla/fileCopy/folderStart"
exclude_folders = ["test", "folder2"]

# Creates a destination folder with yesterday's date
destination_folder = os.path.join("/home/gorilla/fileCopy/folderEnd", yesterday.strftime("%Y%m%d"))
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Defines a function to exclude folders
def exclude_folders_func(folder, files):
    return [f for f in files if any(exclude_folder in os.path.join(folder, f) for exclude_folder in exclude_folders)]

def delete_dmp_files(directory):
    #Recursively delete any file with a .dmp filename in /home/satops/EXPORT and subdirectories.
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dmp"):
                os.remove(os.path.join(root, file))
                print(f"Deleted {os.path.join(root, file)}")
        for dir in dirs:
            delete_dmp_files(os.path.join(root, dir))

# Iterates recursively through all source_folder directories and files and returns three values: 
#   current foldername, list of subfolders and list if files all in the current folder  
#   The code then creates a new list of subfolders that excludes the exclude_folders using list comprehension 
for foldername, subfolders, filenames in os.walk(source_folder):
    subfolders[:] = [subfolder for subfolder in subfolders if subfolder not in exclude_folders]

    # Loops through files in each folder and reads mtime
    for filename in filenames:
        source_file = os.path.join(foldername, filename)
        mtime = os.path.getmtime(source_file)
        mtime_date = datetime.datetime.fromtimestamp(mtime).date()
        # Then copies if mtime is (1) between yesterday               and (2) also between yesterday 00:00:00 and yesterday 23:59:59
        if mtime_date == yesterday and datetime.time(0, 0, 0) <= datetime.datetime.fromtimestamp(mtime).time() <= datetime.time(23, 59, 59):
            destination_file = os.path.join(destination_folder, os.path.relpath(source_file, source_folder))
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copy2(source_file, destination_file)
            os.utime(destination_file, (mtime, mtime))

        # Example tests to run to validte mtime comparisons if current date is 20230426
        # Earlier today - No Copy
        # find /home/gorilla/fileCopy/folderStart -exec touch -t 202304260000 {} \;
        # One days ago - Copy
        # find /home/gorilla/fileCopy/folderStart -exec touch -t 202304252359 {} \;
        # Two days ago - Copy
        # find /home/gorilla/fileCopy/folderStart -exec touch -t 202304240000 {} \;
        # Three days ago - No Copy
        # find /home/gorilla/fileCopy/folderStart -exec touch -t 202304232359 {} \; 

# Then renames the files copied
for dirpath, dirnames, filenames in os.walk(destination_folder):
    for filename in filenames:
        # DUMP folder satid to sat_name (Can probably be modifed with an or in each if statement to reflect DUMP vs JPG/GIF - if "noaj" or "noa1"...)
        if "noaj" in filename:
            new_filename = filename.replace("noaj", "NOAA-19") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noai" in filename:
            new_filename = filename.replace("noai", "NOAA-18") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noaf" in filename:
            new_filename = filename.replace("noaf", "NOAA-15") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noa1" in filename:
            new_filename = filename.replace("noa1", "METOP-1") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noa3" in filename:
            new_filename = filename.replace("noa3", "METOP-3") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noa9" in filename:
            new_filename = filename.replace("noa9", "METOP-SIM") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "noaz" in filename:
            new_filename = filename.replace("noaz", "NOAA-SIM") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "srl1" in filename:
            new_filename = filename.replace("srl1", "SERAL-1")   
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "gaz1" in filename:
            new_filename = filename.replace("gaz1", "GAZELLE-1") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "o3l1" in filename:
            new_filename = filename.replace("o3l1", "OCEANSAT") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        # JPG/GIF Folders satid to sat_name
        if "no1" in filename:
            new_filename = filename.replace("no1", "_NOAA-19") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        if "no2" in filename:
            new_filename = filename.replace("no2", "_NOAA-18") 
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
        # try:
        #     if "dmp" in filename:
        #         os.unlink(os.path.join(dirpath, filename))
        # except FileNotFoundError:  
        #     pass

delete_dmp_files(destination_folder)

t1 = time.perf_counter()
deltaT = round(t1-t0, 3)
print(f'Exectution took {deltaT} seconds')

