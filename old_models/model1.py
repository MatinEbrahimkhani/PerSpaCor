
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForTokenClassification,
                          AutoConfig, Trainer, TrainingArguments, DataCollatorForTokenClassification)


from utils.corpusprocessor import CorpusType
from utils.corpusprocessor import CorpusLoader
from utils.labeler import Labeler

corpus = CorpusLoader()
data = corpus.load_bijan(CorpusType.sents_raw)

labeler = Labeler()
labeler.set_text(data, corpus_type=CorpusType.sents_raw)
chars, labels = labeler.Labeler()

pretrained_model = "HooshvareLab/bert-base-parsbert-uncased"
model_dir = "./Model1/"
# pretrained_model = "bert-base-multilingual-cased"

# chars = chars[:20]
# labels = labels[:20]

for i, label in enumerate(labels):
    labels[i] = [int(l) for l in label]

tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
config = AutoConfig.from_pretrained(pretrained_model)


config.num_labels = 3

model = AutoModelForTokenClassification.from_config(config)
tokens_all = []
for char in chars:
    tokens = [tokenizer.encode(ch)[1] for ch in char]
    tokens.insert(0, 2)  # Adding CLS token at the beginning of each sequence "2 is the tokenized "[CLS]" "
    tokens.append(4)  # Adding SEP token at the end of each sequence "4 is the tokenized "[SEP]" "
    tokens_all.append(tokens)

labels_all = []
for label in labels:
    lab = label
    lab.insert(0,0) # # Adding CLS token label at the beginning of each sequence 
    lab[-1] = 1 # at the end of a sentence there would be a space obviously
    lab.append(0) # Adding SEP token label at the end of each sequence 
    labels_all.append(lab)

# Creating a Dataset object from the tokenized inputs and labels
dataset = Dataset.from_dict({"input_ids": tokens_all, "labels": labels_all})

# Initializing a data collator for token classification with the pre-trained tokenizer
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

# Setting up training arguments for the Trainer class
training_args = TrainingArguments(
    output_dir=model_dir,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    evaluation_strategy="no",
    save_strategy="no"
)

# Initializing a Trainer instance with the model, training arguments, dataset, tokenizer, and data collator
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=None,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Training the model on the dataset
trainer.train()

# Saving the trained model in the "./Model/model/" directory
trainer.save_model(model_dir + "model/")




