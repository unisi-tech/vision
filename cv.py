from transformers import AutoModelForImageClassification, AutoImageProcessor
import torch , common, datasets, faiss, numpy as np 
from torch.nn import functional as F
from PIL import Image

from classes import class_images
import config, torch
from config import *
from common import *

from torchvision.transforms import (
    Compose,
    Normalize,
    RandomHorizontalFlip,
    RandomResizedCrop,
    ToTensor,
    Resize,
    CenterCrop
)

class CustomToTensor(ToTensor):
    def __call__(self, pic):
        if pic.mode != 'RGB':        
            pic = pic.convert('RGB')        
        return super(CustomToTensor, self).__call__(pic)

model = None 
image_processor = None
vector_index = None
vector_dataset = None

device = "cuda" if torch.cuda.is_available() else "cpu"

public_dirs = getattr(config, 'public_dirs', [])
config.public_dirs = public_dirs + [config.dataset_dir.replace('\\', '/')]

if not hasattr(config, 'test_size'):
    config.test_size = 0.2

def load_model():    
    if exists(config.fneuronet):
        global model, image_processor
        model = AutoModelForImageClassification.from_pretrained(config.fneuronet)         
        model.to(device)
        image_processor = AutoImageProcessor.from_pretrained(config.fneuronet)
        
load_model()

def transform_learn(imageProcessor):
    normalize = Normalize(mean=imageProcessor.image_mean, std=imageProcessor.image_std)
    size = (
        imageProcessor.size["shortest_edge"]
        if "shortest_edge" in imageProcessor.size
        else (imageProcessor.size["height"], imageProcessor.size["width"])
    )
    transform = Compose(
        [
            RandomResizedCrop(size),
            RandomHorizontalFlip(),
            CustomToTensor(),
            normalize
        ]
    )
    return transform    

def transform_test(imageProcessor):
    normalize = Normalize(mean=imageProcessor.image_mean, std=imageProcessor.image_std)
    
    return Compose(
    [
        # We first resize the input image to 256x256 and then we take center crop.
        Resize(int((256 / 224) * imageProcessor.size["shortest_edge"])),
        CenterCrop(imageProcessor.size["shortest_edge"]),
        CustomToTensor(),
        normalize
    ]
)

def image_dataset(split = True):
    """make dataset for user images"""
    images = []
    labels = []
    for cl, files in class_images.items():
        files = [file for file, status in files.items() if status == sgroup]
        if files:
            count = len(files)
            images.extend(files)
            labels.extend([cl] * count)
    
    dataset = datasets.Dataset.from_dict({"image": images, 'label' : labels}).cast_column("image", datasets.Image())
    dataset = dataset.class_encode_column("label")    
    if split:
        dataset = dataset.train_test_split(config.test_size)
    return dataset

def classify_image(path):
    if model:
        image = Image.open(path)
        inputs = image_processor(image, return_tensors="pt").to(device)    
        with torch.no_grad():
            logits = model(**inputs).logits            
            predicted = F.softmax(logits[0], dim=0).cpu().numpy()
            arr = []
            id2label = model.config.id2label
            for i, val in enumerate(predicted):
                arr.append([id2label[i], val.item()])
            arr.sort(key = lambda _: _[1], reverse=True)
        return arr

def extract_embeddings(model: torch.nn.Module):
    """Utility to compute embeddings."""
    device = model.device
    transform = transform_test(image_processor)

    def raw(batch):
        images = batch["image"]
        image_batch_transformed = torch.stack(
            [transform(image) for image in images]
        )
        new_batch = {"pixel_values": image_batch_transformed.to(device)}
        with torch.no_grad():            
            logits = model(**new_batch).logits
            embeddings = logits.cpu() 
        return {"embeddings": embeddings}
    
    return raw

def calc_embeddings(dataset, batch_size, softmax = False):
    model.to(device)
    transform = transform_test(image_processor)

    def process(batch):
        images = batch["image"]
        image_batch_transformed = torch.stack(
            [transform(image) for image in images]
        )
        new_batch = {"pixel_values": image_batch_transformed.to(device)}
        with torch.no_grad():            
            logits = model(**new_batch).logits
            if softmax:
                logits = F.softmax(logits, dim=1)
            embeddings = logits.cpu() 
        return {"embeddings": embeddings}
        
    return dataset.map(process, batched=True, batch_size= batch_size)

def create_index(embeddings = None):
    global vector_index, vector_dataset
    if not embeddings:
        dataset = image_dataset(split=False)
        embeddings = calc_embeddings(dataset, batch_size)["embeddings"]
        
    vector_index = faiss.IndexFlatL2(len(dataset.features['label'].names))
    narr = np.asarray(embeddings, dtype=np.float32)
    faiss.normalize_L2(narr)    
    vector_index.add(narr)    

    faiss.write_index(vector_index,fvector_index)    
    labels = dataset.features["label"].names
    vector_dataset = [[el['image'].filename, labels[el['label']]] for el in dataset]
    common.save_obj(vector_dataset,fvector_dataset)

def remove_index():
    if exists(fvector_dataset):
        os.remove(fvector_dataset)
    if exists(fvector_index):
        os.remove(fvector_index)

def search_image(path, count):    
    if model:
        image = Image.open(path)
        inputs = image_processor(image, return_tensors="pt").to(device)    
        with torch.no_grad():
            embeddings = model(**inputs).logits                
        
        #embeddings = embeddings.mean(dim=1)
        vector = embeddings.detach().cpu().numpy()
        vector = np.float32(vector)
        faiss.normalize_L2(vector)

        global vector_index, vector_dataset
        if not vector_index:
            vector_dataset = common.load_obj(fvector_dataset)
            vector_index = faiss.read_index(fvector_index)
        ds,inds = vector_index.search(vector, count)
        return [[*vector_dataset[ifg], distance] for ifg, distance in zip(inds[0],ds[0])]
    return []

def index_embeddings():
    # Number of docs added to your index
    num_docs = vector_index.ntotal
    # Get the dimension of your embeddings
    embedding_dimension = vector_index.d    
    return faiss.rev_swig_ptr(vector_index.get_xb(), num_docs *
        embedding_dimension).reshape(num_docs, embedding_dimension)

def anomalies(duplicate = False):
    err_list = []
    if duplicate:
        global vector_index, vector_dataset
        if not vector_index:
            vector_dataset = common.load_obj(fvector_dataset)
            vector_index = faiss.read_index(fvector_index)
        embeddings = index_embeddings()
        ds,inds = vector_index.search(embeddings, 2)
        aset = list(set((min(i,j), max(i,j)) for i, j in inds if i != j))
        max_equal_distance = config.max_equal_distance
        aset.sort(key = lambda _: ds[_[0]][1] )
        count = 0
        for i, j in aset:
            distance = ds[i][1]
            if distance <= max_equal_distance:
                err_list.append([count, vector_dataset[i][1], distance,  '', vector_dataset[i][0], ''])
                err_list.append([count, vector_dataset[j][1], distance,  '', vector_dataset[j][0], ''])                            
                count += 1        
    else:
        dataset = image_dataset(split=False)
        embeddings = calc_embeddings(dataset, batch_size, softmax = True)["embeddings"]
        labels = dataset.features["label"].names        
    
        for el, emb in zip(dataset, embeddings):
            detected_label = np.argmax(emb)
            ilabel = el['label']
            if detected_label != ilabel:
                prob2false = emb[detected_label]
                prob2true = emb[ilabel]
                err_list.append([labels[detected_label], prob2false,labels[ilabel], 
                    prob2true, el['image'].filename, prob2false / prob2true])
            
        err_list.sort(key = lambda _: _[5], reverse=True)
    return err_list





