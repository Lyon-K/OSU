# CS331 Sentiment Analysis Assignment 3
# This file contains the processing functions
import re
from classifier import BayesClassifier
# import matplotlib.pyplot as plt

def process_text(text):
    """
    Preprocesses the text: Remove apostrophes, punctuation marks, etc.
    Returns a list of text
    """
    preprocessed_text = re.sub(r'[^a-z ]+', '', text.lower()).split()
    return preprocessed_text


def build_vocab(preprocessed_text):
    """
    Builds the vocab from the preprocessed text
    preprocessed_text: output from process_text
    Returns unique text tokens
    """
    vocab = set()
    for sentence in preprocessed_text:
        vocab.update(set(sentence))
    vocab = sorted(vocab)
    return vocab


def vectorize_text(text, vocab):
    """
    Converts the text into vectors
    text: preprocess_text from process_text
    vocab: vocab from build_vocab
    Returns the vectorized text and the labels
    """
    vector = dict.fromkeys(vocab, 0)
    for word in text:
        vector[word] += 1
    vectorized_text = vector.values()
    labels = vector.keys()
    return vectorized_text, labels


def accuracy(predicted_labels, true_labels):
    """
    predicted_labels: list of 0/1s predicted by classifier
    true_labels: list of 0/1s from text file
    return the accuracy of the predictions
    """
    correct_prediction = 0
    total_predictions = len(predicted_labels)
    for i in range(total_predictions):
        correct_prediction += int(predicted_labels[i] == true_labels[i])
    accuracy_score = (float(correct_prediction) / total_predictions)*100
    return accuracy_score

def preprocess_dataset(filename):
    lines = []
    texts = []
    class_labels = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        sentence, class_label = line.strip().split('\t')
        texts.append(process_text(sentence))
        class_labels.append(int(class_label))

    return texts, class_labels

def main():
    # Take in text files and outputs sentiment scores
    training_data, training_labels = preprocess_dataset('trainingSet.txt')
    test_data, test_labels = preprocess_dataset('testSet.txt')

    part_size = -(len(training_data)//-4)
    training_accuracies = []
    test_accuracies = []
    part_range = range(0, len(training_data), part_size)
    for part_start in part_range:
        # partial datasets
        part_training_data = training_data[0 : part_start + part_size]
        part_training_labels = training_labels[0 : part_start + part_size]
        part_test_data = test_data[0 : part_start + part_size]
        part_test_labels = test_labels[0 : part_start + part_size]

        bayes_classfier = BayesClassifier()
        training_vocab = build_vocab(part_training_data)
        bayes_classfier.train(part_training_data, part_training_labels, training_vocab)
        training_predicted_labels = bayes_classfier.classify_text(part_training_data, training_vocab)
        test_predicted_labels = bayes_classfier.classify_text(part_test_data, training_data)


        training_accuracy = accuracy(training_predicted_labels, part_training_labels)
        test_accuracy = accuracy(test_predicted_labels, part_test_labels)
        part_percentage = (float(part_start + part_size)/part_size)/4
        part_percentage_string = str(part_percentage).rjust(4)
        print("[{part}]\ttraining accuracy: {accuracy}".format(part=part_percentage_string, accuracy=training_accuracy))
        print("[{part}]\ttest accuracy: {accuracy}\n".format(part=part_percentage_string, accuracy=test_accuracy))
        training_accuracies.append(training_accuracy)
        test_accuracies.append(test_accuracy)
    
    percentages = [25, 50, 75, 100]
    with open('results.txt', 'w') as f:
        for i in range(4):
            num_examples = min(part_range[i] + part_size, len(training_data))
            f.write("accuracy: {accuracy:.2f}%;\t#examples:{examples};\ttrainingSet.txt\n".format(accuracy=training_accuracies[i],examples=num_examples))
            num_examples = min(part_range[i] + part_size, len(test_data))
            f.write("accuracy: {accuracy:.2f}%;\t#examples:{examples};\ttestSet.txt\n\n".format(accuracy=test_accuracies[i],examples=num_examples))

    # plots
    # _, axis = plt.subplots(1,2)
    # axis[0].set_title('training dataset')
    # axis[0].plot(percentages, training_accuracies, color='red', label='training dataset')
    # # axis[0].set_ylim(60, 100)
    # axis[0].set_xlabel('Training set size(%)')
    # axis[0].set_xticks(percentages, percentages)
    # axis[0].set_ylabel('Accuracy(%)')

    # axis[1].set_title('testing dataset')
    # axis[1].plot(percentages, test_accuracies, color='green', label='testing dataset')
    # # axis[1].set_ylim(60, 100)
    # axis[1].set_xlabel('Training set size(%)')
    # axis[1].set_xticks(percentages, percentages)
    # axis[1].set_ylabel('Accuracy(%)')
    # plt.show()
    return 1


if __name__ == "__main__":
    main()