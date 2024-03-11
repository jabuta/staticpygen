import os
import shutil

def init_public():
    try:
        shutil.rmtree("../public")
    except:
        pass
    
    os.mkdir("../public")
    
    