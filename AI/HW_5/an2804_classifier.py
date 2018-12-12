import sys
import string
import math

"""
Report on before and after values  without extra credit stopfile and changes to extract words--

Without tuning:
train --> 0.9751121076233183
test --> 0.9676840215439856
dev(held out) --> 0.9515260323159784

With tuning k=.02:
train --> 0.9968609865470852
test --> 0.9802513464991023
dev --> 0.9802513464991023
----------------------------------------------------------------------------
Changes to extract words allowing for some punctuation, stopfile_mini.txt and k=.02
train --> 0.997085201793722 (slightly better)
test --> 0.9820466786355476 (slightly better)
dev --> 0.9748653500897666 (.5% worse)


"""
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
        no_punct_text = "".join([x for x in text.lower() if not x in string.punctuation or x in ['$', '!', '*', '&', '?']])
        return [word for word in no_punct_text.split()]


    """
    Given a stopword_file, read in all stop words and remove them from self.attribute_types
    Implement this for extra credit.
    """
    def remove_stopwords(self, stopword_file):
        with open(stopword_file):
            stopwords = []
            for line in stopword_file:
                stopwords.append(line)
        self.attribute_types.difference(set(stopwords))

    """
    Given a training datafile, add all features that appear at least m times to self.attribute_types
    """
    def collect_attribute_types(self, training_filename, m=1):
        counts = {}
        result = []
        with open(training_filename) as training_file:
            for line in training_file:
                splt = line.split('\t')
                words = self.extract_words(splt[1])
                #for each word excluding the training labe
                for word in words:
                    if word not in counts:
                        counts[word] = 1
                    else:
                        counts[word] += 1
        for word in counts:
            if counts[word] >= m:
                result.append(word)

        self.attribute_types = set(result)


    """
    Given a training datafile, estimate the model probability parameters P(Y) and P(F|Y).
    Estimates should be smoothed using the smoothing parameter k.
    """
    def train(self, training_filename, k=.02):
        self.label_prior = {}
        self.word_given_label = {}

        count_prior = {'ham': 0, 'spam': 0}
        count_words_spam = {}
        count_words_ham = {}
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

        # denominator = count_prior_sum + k*len(self.attribute_types)
        spam_denominator = count_prior['spam'] + k*len(self.attribute_types)
        ham_denominator = count_prior['ham'] + k*len(self.attribute_types)



        for word in self.attribute_types:
            word_spam = (word, 'spam')
            if word in count_words_spam:
                spam_numerator = count_words_spam[word] + k
            else:
                spam_numerator = 0 + k

            word_ham = (word, 'ham')
            if word in count_words_ham:
                ham_numerator = count_words_ham[word] + k
            else:
                ham_numerator = 0+k

            self.word_given_label[word_spam] = spam_numerator/spam_denominator
            self.word_given_label[word_ham] = ham_numerator/ham_denominator

    """
    Given a piece of text, return a relative belief distribution over all possible labels.
    The return value should be a dictionary with labels as keys and relative beliefs as values.
    The probabilities need not be normalized and may be expressed as log probabilities.
    """
    def predict(self, text):

        result = {}
        for label in self.label_prior:
            prob = math.log(self.label_prior[label])
            for word in self.extract_words(text):
                try:
                    prob += math.log(self.word_given_label[(word, label)])
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
