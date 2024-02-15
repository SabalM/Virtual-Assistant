import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence):
    """Splits sentence into array of tokens/words"""
    return nltk.word_tokenize(sentence)


def stem(word):
    """
    Stemming = Contracts the root form of word
    Example:
        words = ["running", "runs", "runner", "easily"]
        stem_words = [stem(w) for w in words]
            -> ["run", "ran", "run", "easili"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    Returns Bag of Words that exists in the sentence, otherwise 0
    Example:
        sentence = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
        words = ["the", "cat", "jumps", "over", "the", "moon", "lazy", "dog", "quick", "brown"]
            -> Bag of Words representation:
                bag = [1, 0, 1, 1, 1, 0, 1, 1, 1, 1]  
    """
    sentence_words = [stem(word) for word in tokenized_sentence]
    # Initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, word in enumerate(words):
        if word in sentence_words:
            bag[idx] = 1

    return bag
