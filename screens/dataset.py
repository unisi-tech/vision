from unisi import *
from crawler import *
from classes import *
from common import *
from blocks.groups import group_list, group_block

name = "Dataset"
icon = 'blur_linear'
order = 0

images = []

def load_images(paths):
    global images
    images = [Image(n, False, header = i + 1, width = 240, height = 120) for i, n in enumerate(paths) if n]
    image_block.scroll_list = images

def mode_changed(_, value):    
    mode.value = value    
    load_images([k for k, v in class_images[group_list.value].items() if v == mode.value]\
                if group_list.value else [])
    if value == sgroup:
         delete.edit = True
         add2group.edit = False
    elif value == snew:
        delete.edit = True
        add2group.edit = True
    else:
        delete.edit = False
        add2group.edit = True
    return image_block

mode = Select('Status', sgroup, mode_changed, options=[sgroup, snew, sdeleted])
how_many_photos = Edit('Photo count', 100, type = 'number')
keywords = Edit('Keywords for searching..', '')

def callback_loading(n, filename):
    user.progress(f" Downloaded {n} from {how_many_photos.value}..")

def scan_photos(_, val):        
    if keywords.value and val == 'Ok':               
        if how_many_photos.value <= 0 or how_many_photos.value > 100:
            return Error(f'How many value has to be in range [1, 100]')
        
        user.progress(f"Downloading images..")                
        vgroup = class_images[group_list.value]     
        new_folder = get_pictures(keywords.value)

        if not new_folder:
            return Error('Download error!')
        paths = os.listdir(new_folder)
                   
        for fn in paths:
            if fn:
                fn = filename2url(f'{new_folder}{divpath}{fn}')
                if (fn.endswith('.jpg') or fn.endswith('.jpeg') or 
                    fn.endswith('.png') or fn.endswith('.webp')):
                    vgroup[fn] = snew 
        mode_changed(mode, snew)        
        return image_block
    
def extend_images(_, __):
    if not group_list.value:
        return Info('Select a group for scanning..')    
    keywords.value = group_list.value
    return Dialog('Scan google images for keywords..', scan_photos, keywords, how_many_photos)

def short_name(fn):
    url = filename2url(fn)
    fn = url.split(divpath)[-1]
    arr = fn.split('.')
    return f"{arr[0]}.{arr[-1]}"
    
def delete_images(_, v):    
    selected = [im for im in images if im.value]        

    if len(selected):
        def delete(_, bname):
            if bname == 'Ok':
                vgroup = class_images[group_list.value]
                for im in selected:
                    vgroup[im.name] = sdeleted            
                mode_changed(mode, mode.value)
                return image_block
        return Dialog(f'Delete from the group {len(selected)} images?', delete)

    return Info('Select images for deleting..')

def add_images(_, v):    
    selected = [im for im in images if im.value]
    
    def add(_, bname):
        if bname == 'Ok':            
            vgroup = class_images[group_list.value]
            for im in selected:
                vgroup[im.name] = sgroup            
            mode_changed(mode, sgroup)
            return image_block

    if len(selected):
        return Dialog(f'Add to the group {len(selected)} images?', add)

    return Info('Select images for adding..')

def invert(_, v):
    for i in images:
        i.value = not i.value
    return image_block        

ext = Button('Extend images', extend_images, icon='collections')
delete = Button('Delete', delete_images, icon='highlight_off')
add2group = Button('Add to group', add_images, icon='add_task')
select = Button('Invert selection', invert, icon = 'published_with_changes')

image_block = Block('Group images', 
    [                        
        mode, 
        select,       
        ext,
        add2group,
        delete
    ],    
    images, icon = 'view_module', scroll = True, scaler = True)

blocks= [group_block, image_block]

def prepare():
    if not group_list.value and group_list.options:
        group_list.value = group_list.options[0]        
    group_list.callback = lambda : mode_changed(mode, mode.value)
    #sync to group_list
    group_list.callback()