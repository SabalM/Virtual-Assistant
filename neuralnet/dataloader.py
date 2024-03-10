import numpy as np
from torch.utils.data import Dataset
from nltk_utils import bag_of_words, tokenize, stem

class IntentDataset(Dataset):
    def __init__(self, pair, all_words, tags):
        self.n_samples = len(pair)
        self.x_data = []
        self.y_data = []

        for (pattern_sentence, tag) in pair:
            bag = bag_of_words(pattern_sentence, all_words)
            self.x_data.append(bag)
            label = tags.index(tag)
            self.y_data.append(label)

        self.x_data = np.array(self.x_data)
        self.y_data = np.array(self.y_data)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples
