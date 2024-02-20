import torch
from torch import nn 
from torch.utils.data import Dataset, DataLoader
from torchinfo import summary

import numpy as np 
import matplotlib.pyplot as plt
import random 
import json 

from nltk_utils import bag_of_words, tokenize, stem
from model import IntentModelClassifier

with open('intents.json', 'r') as f:
    print(f'Loaded `intents.json` file')
    intents = json.load(f)

# print(intents)

all_words = []
tags = []
pair = []

# Loop through each sentence in intent patterns
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)        # Add to tag list
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to list
        all_words.extend(w)
        pair.append((w, tag))

# Stem and Lowercase each word
ignore_words = ['?','.','!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# Remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(f"\nPatterns Found: {len(pair)}\nTags Found: {len(tags)}\nUnique stemmed words Found: {len(all_words)}")
print(f"\nTags:\n{tags}\n\nUnique stemmed words:\n{all_words}\n")
# Create training dataloader
X_train = []
y_train = []
for (pattern_sentence, tag) in pair:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(tags.index(tag))

X_train = np.array(X_train)
y_train = np.array(y_train)


# Setting up device-agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Loaded on {device} device')

# Custom DataLoader
class ChatDataLoader(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

dataset = ChatDataLoader()

BATCH_SIZE = 8

train_dataLoader = DataLoader(dataset = dataset,
                        batch_size = BATCH_SIZE,
                        shuffle = True,
                        num_workers = 0     # no of CPU-core dataloaders
                    )

model = IntentModelClassifier(input_size = len(X_train[0]),
                        hidden_size = 8,
                        output_size = len(tags)).to(device)

# Generate Model Summary
summary(model)

# Setting up loss_fn and optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 1000

# Tracking
epoch_count = []
loss_values = []

# Train Loop
for epoch in range(epochs):
    for (words, labels) in train_dataLoader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        label_preds = model(words)
        loss = loss_fn(label_preds, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if epoch%100 == 0 or epoch == epochs-1:
        epoch_count.append(epoch)
        loss_values.append(loss)
        print(f'Epoch:{epoch} --- Train loss: {loss:.4f}')


data = {
    "model_state": model.state_dict(),
    "input_size": len(X_train[0]),
    "hidden_size": 8,
    "output_size": len(tags),
    "all_words": all_words,
    "tags": tags
}

# Saving Model
model_save_path = "model/intent.pth"
torch.save(data, model_save_path)
print(f'Saved trained model to directory {model_save_path}')

# Plot loss curves
plt.figure(figsize=(8,3))
plt.plot(epoch_count, np.array(torch.tensor(loss_values).numpy()), label="Train Loss")
# plt.plot(epoch_count, np.array(torch.tensor(test_loss_values).numpy()), label="Test Loss")
plt.title("Train loss curve")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend()
plt.show()