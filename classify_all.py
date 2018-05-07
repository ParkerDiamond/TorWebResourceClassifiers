import numpy as np

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

def read_file(filename):
    lines = np.array([np.array(line.rstrip('\n').split(',')) for line in open(filename)])
    X = lines[:, :-1]
    Y = lines[:, -1]
    return X, Y


def svm_classify(datafile):
    X, Y = read_file(datafile)

    print('Size of X is ', len(X), ' rows and', len(X[0]), ' columns')

    X = X.astype(float)

    # reduction

    # pca = PCA(n_components=1000)
    # X = pca.fit_transform(X)
    #
    # print("reduction to 1000 PC components is done")

    train_f, test_f, train_l, test_l = train_test_split(
        X, Y, test_size=0.35, random_state=26)

    print("split data into training and testing datasets is done")
    print("training set has %d rows; testing set has %d rows" % (len(train_f), len(test_f)))

    # clf = svm.SVC()
    # clf = RandomForestClassifier()
    clf = MLPClassifier()
    clf.fit(train_f, train_l)

    print('fitting is done')

    y_true, y_pred = test_l, clf.predict(test_f)

    print('testing is done, printing results')

    print(classification_report(y_true, y_pred))
    print(accuracy_score(y_true, y_pred))

if __name__ == "__main__":
    svm_classify('output_matrix_fastest')
