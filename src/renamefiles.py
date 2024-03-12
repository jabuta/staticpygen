import os
import shutil


    
def repl_directory(origin: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)

    files = os.listdir(origin)
    for file in files:
        file_path = os.path.join(origin,file)
        dest_path = os.path.join(dest,file)
        if os.path.isfile(file_path):
            shutil.copy(file_path,dest_path)
            continue
        repl_directory(file_path,dest_path)