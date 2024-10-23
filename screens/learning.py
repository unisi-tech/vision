from unisi import *
from common import *
from config import *
from classes import *
from transformers import TrainerCallback
import train, cv, asyncio

name = "Learning"
icon = 'face_retouching_natural'
order = 1

trainer = None

class StatCallback(TrainerCallback):    
    def on_epoch_end(self, _, state, __, **___):
        state.log_history.reverse()
        for info in state.log_history:
            if 'eval_accuracy' in info:
                epoch = len(epochtable.rows) + 1
                epochtable.rows.append([epoch, info['eval_accuracy'], info['eval_loss']])
                #user.progress(f'Running {epoch + 1} epoch..', epochtable)
                break

epochtable = Table('Epochs', None, headers = ['Epoch', 'Accuracy', 'Loss'], tools = False)

pblock = ParamBlock('Learning parameters', learning_rate=3e-4 if 'convnext' in neuronet else 5e-5,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=16,
    num_train_epochs=10,
    warmup_ratio=0.1,
    logging_steps=10)

async def runlearn(_, val):
    global trainer
    epochtable.rows = []
    await user.progress('Learning..', epochtable)    
    trainer = await train.get_trainer(user, pblock.params)
    trainer.add_callback(StatCallback)
    trainer.train()
    return Info('Learing is finished. You can save the network if the result is satisfied.', epochtable)

create_index_switch = Switch('Create image index', True, type = 'check')

def set_main(_, val):        
    if not trainer:
        return Error("You haven't trained the net!")
    question = 'Do you want replace the system net by the trained one?' if exists(neuronet)\
        else 'Do you want set the trainned net as the system one?'
    return Dialog(question, set_main_responce, create_index_switch)
    
async def set_main_responce(_, bname):
    if bname == 'Ok':
        await user.progress('Set neuronet..')
        trainer.save_model(fneuronet)
        save_dataset_config()
        cv.load_model()
        if create_index_switch.value:
            await user.progress('Create index..')
            cv.create_index()
        else:
            cv.remove_index()
        return Info('Successfully done.')
    
async def create_index(_, bname):
    if bname == 'Ok':        
        await user.progress('Create index..')
        cv.create_index()
        return calc_anomalies(0,0)
    
err_list = []

def selecting_changed(image, select): 
    image.value = select
    if atype.value == 'Duplicates':          
        for im in image_block.scroll_list:
            if im.name == image.name:
                im.value = select         
        return image_block
    
async def calc_anomalies(_, __):
    global err_list
    if not cv.model:
        return Warning('You have to learn the system first!')
    if atype.value == 'Duplicates':
        if not exists(fvector_index):
            return Dialog('A search index does not exist! Create?', create_index)
    await user.progress('Calculating anomalies..')
    err_list = cv.anomalies(atype.value == 'Duplicates')
    images = [Image(file, False, selecting_changed, label = f'{dg}:{dp}\n {rg}:{rp}', width = 380, height = 240) 
            for dg, dp, rg, rp, file, _ in err_list]
    image_block.scroll_list = images    
        
startbut = Button('Start leaning', runlearn, icon = 'cast_for_education')

setasmain_but = Button('Set the trained as main', set_main)

tblock = Block('Training', [startbut, setasmain_but], epochtable, icon = 'settings_suggest')

atype = Select('Type', 'Errors', options = ['Errors', 'Duplicates'])

def sel_images():
    images = image_block.scroll_list
    return [im for im in images if im.value]

async def delete_images(_, __):
    allimages = image_block.value[1] if len(image_block.value) > 1 else []
    images = [im for im in allimages if im.value]
    
    async def delete(_, bname):
        if bname == 'Ok':
            for im in images:
                for files in class_images.values():            
                    if im.name in files:
                        files[im.name] = sdeleted                        
                        break
            await user.progress('Creating index..')
            cv.create_index()
            return calc_anomalies(0,0)

    return Dialog(f'Delete {len(images)} image(s) from the dataset?', delete)\
        if images else Warning('Images are not selected!')    

detected = 'detected'

def move_images(_, __):
    images = sel_images()
    group = Select('Group', detected, options = [detected, *class_images.keys()])
    def move(_, bname):
        if bname == 'Ok':
            nonlocal group
            move_group = group.value if group.value != detected else None
            for im in images:
                for group, files in class_images.items():            
                    if im.name in files:
                        files[im.name] = sdeleted
                        mgr = move_group if move_group else im.label.split(':')[0]
                        class_images[mgr][im.name] = sgroup    
                        break

    return Dialog(f'Move {len(images)} image(s) to the group?', move, group)\
        if images else Warning('Images are not selected!')    

image_block = Block('Anomalies', [atype,  Button('Calculate', calc_anomalies), 
    Button('Move selected', move_images), Button('Delete selected', delete_images)], 
        scroll = True, scaler = True)

blocks = [[pblock, tblock], image_block]
