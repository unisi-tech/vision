from unisi import *
from common import *
from classes import *

edit_group = Edit('Group name', '', focus = True)

def add_group(_, value):
    new_group = edit_group.value.strip()
    if value == 'Ok' and new_group:                
        if new_group in class_images:
            return Error(f'Group "{new_group}" already exists!')        
        class_images[new_group] = {}
        group_list.value = new_group                
        group_list.options = sorted(class_images.keys())                
        group_list.callback()
        return True

def add_group_dialog(_, __):
    if not group_list.value:
        return Info('Select a root group for adding..')    
    edit_group.value = ''    
    return Dialog(f'Adding a group..', add_group , edit_group)    

def rename_group(_, value):
    new_name = edit_group.value.strip()
    if value == 'Ok' and new_name:
        if new_name in class_images:
            return Error(f'Group {new_name} already exists!')
        old = group_list.value        
        class_images[new_name] = class_images[old]
        del class_images[old]
        group_list.options = sorted(class_images.keys())
        group_list.value = new_name                
        group_list.callback()
        return True

def rename_group_dialog(_, __):
    if not group_list.value:
        return Info('Select a group for renaming..')
    edit_group.value = group_list.value
    return Dialog(f'Edit name of the group {group_list.value}..', rename_group, edit_group)    

def delete_group(_, value):
    if value == 'Ok':                
        old = group_list.value                
        if old in class_images:
            del class_images[old]
        group_list.options = sorted(class_images.keys())
        group_list.value = None        
        group_list.callback()
        return True

def delete_group_dialog(_, __):
    if not group_list.value:
        return Info('Select a root group for deleting..')    
    return Dialog(f'Delete {group_list.value} group?', delete_group)    

def load_group(_, value):
    group_list.value = value
    return group_list.callback()

group_list = Select('_Vision groups', None, load_group, type = 'list', 
        options = sorted(class_images.keys()), callback = empty_func)    

add_group_button = Button('_Add', add_group_dialog, icon='add')
rename_group_button = Button('Rename', rename_group_dialog)
delete_group_button = Button('_Delete', delete_group_dialog, icon='highlight_off')

group_block = Block('Groups',
[           
    add_group_button, rename_group_button, delete_group_button        
], group_list, icon = 'api')

