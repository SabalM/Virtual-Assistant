import torch
from torch import nn
from torch.utils.data import DataLoader
from torchinfo import summary
import matplotlib.pyplot as plt
import numpy as np
import json
import argparse

from dataloader import IntentDataset
from nltk_utils import bag_of_words, tokenize, stem
from model import IntentModelClassifier

# Argument Parser
parser = argparse.ArgumentParser(description="Intent Model Training Script")
parser.add_argument("--batch_size", "-b", 
                            type=int, 
                            default=8, 
                            help="Batch size for training")
parser.add_argument("--epochs", "-e", 
                            type=int, 
                            default=500, 
                            help="Number of epochs for training")
parser.add_argument("--plot", "-p", 
                            type=int, 
                            default=0, 
                            help="Whether to plot the loss curve (1 for yes, 0 for no)")
args = parser.parse_args()

# Load intents
with open('intents.json', 'r') as f:
    print(f'Loaded `intents.json` file')
    intents = json.load(f)

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

# Create training dataset
dataset = IntentDataset(pair, all_words, tags)

# Training DataLoader
train_dataLoader = DataLoader(dataset=dataset,
                              batch_size=args.batch_size,
                              shuffle=True,
                              num_workers=0)     # no of CPU-core dataloaders

# Initialize Model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Loaded on {device} device')

model = IntentModelClassifier(input_size=len(all_words),
                              hidden_size=8,
                              output_size=len(tags)).to(device)

# Generate Model Summary
summary(model)

# Setting up loss_fn and optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Tracking
epoch_count = []
loss_values = []

# Train Loop
for epoch in range(args.epochs):
    for (words, labels) in train_dataLoader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        label_preds = model(words)
        loss = loss_fn(label_preds, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if epoch % 25 == 0 or epoch == args.epochs - 1:
        epoch_count.append(epoch)
        loss_values.append(loss)
        if epoch % 100 == 0 or epoch == args.epochs - 1:
            print(f'Epoch:{epoch} --- Train loss: {loss:.4f}')

# Save trained model
model_save_path = "model/intent.pth"
torch.save({
    "model_state": model.state_dict(),
    "input_size": len(all_words),
    "hidden_size": 8,
    "output_size": len(tags),
    "all_words": all_words,
    "tags": tags
}, model_save_path)
print(f'Saved trained model to directory {model_save_path}')

# Plot loss curve if specified
if args.plot == 1:
    plt.figure(figsize=(8,3))
    plt.plot(epoch_count, np.array(torch.tensor(loss_values).numpy()), label="Train Loss")
    plt.title("Train loss curve")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.legend()
    plt.show()
