import os
import shutil

def init_public():
    try:
        shutil.rmtree("public/")
    except:
        pass
    repl_static("static/")
    
def repl_static(curr_path: str):
    if not os.path.exists(curr_path.replace("static","public",1)):
        os.mkdir(curr_path.replace("static","public",1))

    curr_files = os.listdir(curr_path)
    print(curr_files)
    for file in curr_files:
        file_path = os.path.join(curr_path,file)
        if os.path.isfile(file_path):
            shutil.copy(file_path,file_path.replace("static","public",1))
            continue
        repl_static(file_path)