
#optional:  add unigui path if unigui is installed near (for deep testing or developing)
import os,sys
wd = os.getcwd()
pos = wd.rfind('/')
if pos >= 0:
    sys.path.insert(0,wd[:pos] + '/unigui')

from aiohttp import web
from classes import save_dataset_config
from unigui import *
import cv

async def handle_cv(request):    
    fs_count = request.query_string.split(':')                
    fs = fs_count[0]    
    if fs.startswith('http'):
        fs += ':' + fs_count[1]
        fs_count.pop(0)
        fs = cache_url(fs)
    
    result = cv.classify_image(fs)
    count = 0 if len(fs_count) < 2 else int(fs_count[1])

    if count and len(result) >= count:
        result = result[:count]
    
    return web.json_response(result)                        

User.toolbar = [Button('_Save ds_config', lambda _, __ : save_dataset_config(), 
                    icon = 'save', tooltip = 'Save dataset configuration')]

start(http_handlers = [web.get('/cv', handle_cv)])