import os, pickle
from common import *
from config import *
from unigui import Info, divpath

def scan_dataset():
    classes = {}

    for root, _, files in os.walk(dataset_dir):
        name = root[len(dataset_dir):]
        if name:
            if name.startswith(divpath):
                name = name[1:]
            root += divpath
            classes[name] = {root + file: sgroup for file in files}
    return classes
            
class_images = scan_dataset() if not exists(fclasses_images)\
    else pickle.load(open(fclasses_images, "rb"))

#check are fclasses_images compatible with dataset_dir
if exists(fclasses_images) and class_images:
    val = next(iter(class_images.values()))
    if val and not next(iter(val)).startswith(dataset_dir): 
        class_images = scan_dataset()        

def save_dataset_config():
    save_obj(class_images, fclasses_images)
    return Info('The dataset config is saved')


            

    

    

    

    



