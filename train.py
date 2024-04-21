
from transformers import *
import evaluate, numpy as np
import cv
from config import neuronet

async def get_trainer(user, params):    
    imageProcessor = AutoImageProcessor.from_pretrained(neuronet)
    await user.progress('Prepare training..')
    
    transform = cv.transform_learn(imageProcessor)
    def transforms(examples):
        examples["pixel_values"] = [transform(img.convert("RGB")) for img in examples["image"]]
        del examples["image"]
        return examples
    
    dataset = cv.image_dataset()
    dataset = dataset.with_transform(transforms)

    data_collator = DefaultDataCollator()
    accuracy = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return accuracy.compute(predictions=predictions, references=labels)

    labels = dataset["train"].features["label"].names
    label2id, id2label = dict(), dict()
    for i, label in enumerate(labels):
        label2id[label] = str(i)
        id2label[str(i)] = label

    await user.progress(f'Loading {neuronet} network..')
    
    model = AutoModelForImageClassification.from_pretrained(neuronet, num_labels=len(labels),
        ignore_mismatched_sizes=True, id2label =id2label, label2id=label2id)
    model.to(cv.device)

    await user.progress(f'Running epochs..')

    training_args = TrainingArguments(
        output_dir="checkpoints",
        remove_unused_columns=False,
        evaluation_strategy="epoch",
        save_strategy="epoch",        
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
        **params
    )

    return Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        tokenizer=imageProcessor,
        compute_metrics=compute_metrics,    
    )
