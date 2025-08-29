# This file implements a Naive Bayes Classifier
from math import log10

class BayesClassifier():
    """
    Naive Bayes Classifier
    file length: file length of training file
    sections: sections for incremental training
    """
    def __init__(self):
        self.postive_word_counts = {}
        self.negative_word_counts = {}
        self.percent_positive_scentences = 0
        self.percent_negative_scentences = 0
        self.file_length = 499
        self.file_sections = [self.file_length // 4, self.file_length // 3, self.file_length // 2]


    def train(self, train_data, train_labels, vocab):
        """
        This function builds the word counts and sentence percentages used for classify_text
        train_data: vectorized text
        train_labels: vectorized labels
        vocab: vocab from build_vocab
        """
        self.positive_word_counts = dict.fromkeys(vocab, 0)
        self.negative_word_counts = dict.fromkeys(vocab, 0)

        self.percent_positive_scentences = float(sum(train_labels)) / len(train_labels)
        self.percent_negative_scentences = 1 - self.percent_positive_scentences
        for i, sentence in enumerate(train_data):
            if train_labels[i]:
                for word in sentence:
                    self.positive_word_counts[word] += 1
            else:
                for word in sentence:
                    self.negative_word_counts[word] += 1
        return 1


    def classify_text(self, vectors, vocab):
        """
        vectors: [vector1, vector2, ...]
        predictions: [0, 1, ...]
        """
        predictions = []

        for vector in vectors:
            positive_score = self.percent_positive_scentences
            negative_score = self.percent_negative_scentences
            for word in vector:
                temp = (self.positive_word_counts.get(word, 0) + 1) / (float(sum(self.positive_word_counts.values())) + len(vocab))
                positive_score += log10(temp)
                temp = (self.negative_word_counts.get(word, 0) + 1) / (float(sum(self.negative_word_counts.values())) + len(vocab))
                negative_score += log10(temp)
            predictions.append(int(positive_score > negative_score))
        
        return predictions
    