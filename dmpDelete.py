import os

def delete_dmp_files(directory):
    #Recursively delete any file with a .dmp filename in /home/satops/EXPORT and subdirectories.
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dmp"):
                os.remove(os.path.join(root, file))
                print(f"Deleted {os.path.join(root, file)}")
        for dir in dirs:
            delete_dmp_files(os.path.join(root, dir))

delete_dmp_files('/home/gorilla/fileCopy/folderEnd')