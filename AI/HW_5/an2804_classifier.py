import sys
import string
import math

class NbClassifier(object):

    """
    A Naive Bayes classifier object has three parameters, all of which are populated during initialization:
    - a set of all possible attribute types
    - a dictionary of the probabilities P(Y), labels as keys and probabilities as values
    - a dictionary of the probabilities P(F|Y), with (feature, label) pairs as keys and probabilities as values
    """
    def __init__(self, training_filename, stopword_file):
        self.attribute_types = set()
        self.label_prior = {}
        self.word_given_label = {}

        self.collect_attribute_types(training_filename)
        if stopword_file is not None:
            self.remove_stopwords(stopword_file)
        self.train(training_filename)


    """
    A helper function to transform a string into a list of word strings.
    You should not need to modify this unless you want to improve your classifier in the extra credit portion.
    """
    def extract_words(self, text):
        no_punct_text = "".join([x for x in text.lower() if not x in string.punctuation])
        return [word for word in no_punct_text.split()]


    """
    Given a stopword_file, read in all stop words and remove them from self.attribute_types
    Implement this for extra credit.
    """
    def remove_stopwords(self, stopword_file):
        self.attribute_types.difference(set())

    """
    Given a training datafile, add all features that appear at least m times to self.attribute_types
    """
    def collect_attribute_types(self, training_filename, m=1):

        counts = {}
        result = []
        with open(training_filename) as training_file:
            for line in training_file:
                words = line.split()
                #for each word excluding the training labe
                for word in words[1:]:
                    if word not in counts:
                        counts[word] = 1
                    else:
                        counts[word] += 1
        for word in counts:
            if counts[word] > m:
                result.append(word)


        self.attribute_types = set(result)


    """
    Given a training datafile, estimate the model probability parameters P(Y) and P(F|Y).
    Estimates should be smoothed using the smoothing parameter k.
    """
    def train(self, training_filename, k=1):
        self.label_prior = {}
        self.word_given_label = {}

        count_prior = {'ham': 0, 'spam': 0}
        count_words_spam = {}
        count_words_ham = {}
        all_words = set()
        with open(training_filename) as training_file:
            for line in training_file:
                splt = line.split('\t')
                label = splt[0]
                words = self.extract_words(splt[1])

                if label in count_prior:
                    count_prior[label] += 1
                else:
                    count_prior[label] = 1

                for word in words:
                    if word not in all_words:
                        all_words.add(word)
                    if label == 'spam':
                        if word in count_words_spam:
                            count_words_spam[word] += 1
                        else:
                            count_words_spam[word] = 1
                    if label == 'ham':
                        if word in count_words_ham:
                            count_words_ham[word] += 1
                        else:
                            count_words_ham[word] = 1

        # turn counts into probabilities
        count_prior_sum = sum(count_prior.values())
        for label in count_prior:
            self.label_prior[label] = count_prior[label]/count_prior_sum

        for word in count_words_spam:
            word_spam = (word, 'spam')
            numerator = count_words_spam[word] + k
            denominator = count_prior_sum + k*len(all_words)
            self.word_given_label[word_spam] = numerator/denominator

        for word in count_words_ham:
            word_ham = (word, 'ham')
            numerator = count_words_ham[word] + k
            denominator = count_prior_sum + k*len(all_words)
            self.word_given_label[word_ham] = numerator/denominator


    """
    Given a piece of text, return a relative belief distribution over all possible labels.
    The return value should be a dictionary with labels as keys and relative beliefs as values.
    The probabilities need not be normalized and may be expressed as log probabilities.
    """
    def predict(self, text):

        result = {}
        for label in self.label_prior:
            prob = math.log(self.label_prior[label])
            for word in text:
                try:
                    prob += self.word_given_label[(word, label)]
                except KeyError:
                    pass
            result[label] = prob

        return result


    """
    Given a datafile, classify all lines using predict() and return the accuracy as the fraction classified correctly.
    """
    def evaluate(self, test_filename):
        total = 0
        total_correct = 0
        with open(test_filename) as tf:
            for line in tf:
                splt = line.split('\t')

                correct_label = splt[0]
                text = splt[1]
                predict_probs = self.predict(text)

                # Get prediction from predict probs
                max_predict_prob = -100000
                prediction = ""
                for label in predict_probs:
                    if predict_probs[label] > max_predict_prob:
                        max_predict_prob = predict_probs[label]
                        prediction = label

                if prediction == correct_label:
                    total_correct += 1
                total += 1

        return float(total_correct/total)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("\nusage: ./hmm.py [training data file] [test or dev data file] [(optional) stopword file]")
        exit(0)
    elif len(sys.argv) == 3:
        classifier = NbClassifier(sys.argv[1], None)
    else:
        classifier = NbClassifier(sys.argv[1], sys.argv[3])
    print(classifier.evaluate(sys.argv[2]))
