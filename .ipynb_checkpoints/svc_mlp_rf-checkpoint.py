# Written by: Ksenia Burova
# Data processing for classification

import numpy as np
from os import listdir
import os
import sys
from os.path import join
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier


def svm_classify(X, Y, method=None):

    X = X.astype(float)

    train_f, test_f, train_l, test_l = train_test_split(
        X, Y, test_size=0.35, random_state=56)

    print("split data into training and testing datasets is done")

    # We make svc as a default classification method
    clf = LinearSVC()

    if method == 'mlp':
        clf = MLPClassifier()
    elif method == 'forest':
        clf = RandomForestClassifier()
    elif method != 'svc':
        print('Specify another method: "svm", "mlp" or "forrest"')
        exit(0)

    clf.fit(train_f, train_l)

    print('fitting is done')

    y_true, y_pred = test_l, clf.predict(test_f)

    print('testing is done, printing results')

    print(classification_report(y_true, y_pred))
    print('Accuracy: ', accuracy_score(y_true, y_pred))


def create_matrix(all_resources, accessed_resources, total_size, clf=None):

    datapoints = np.zeros(shape=(total_size, len(all_resources)), dtype=int)

    labels = np.array([])
    label_nums = np.array([], dtype=int)
    resources_arr = np.array(all_resources)

    # we want to iterate trough all the resources
    # and create boolean matrix in which each row
    # corresponds to which resources were requested
    # while loading a page that is our label

    index = 0
    count = 0
    for label, resources_groups in accessed_resources.items():

        rows_num = len(resources_groups)

        # we want to avoid rows that have all the 0s
        for i in range(rows_num):
            datapoints[i+index] = np.in1d(resources_arr, resources_groups[i]).astype(int)

        labels = np.append(labels, np.full((1, rows_num), label))
        label_nums = np.append(label_nums, np.full((1, rows_num), count))


        print("Rows for ", label," - ", count, " created; ", rows_num, " rows were added")

        count += 1
        index += rows_num

    # got the boolean matrix, now call function that processes it

    print('Matrix is created...')
    svm_classify(datapoints, label_nums, clf)


def read_from_dir(path, mode, clf=None):
    dirs = listdir(path)

    accessed_resources = {}
    all_resources = set()
    total_size = 0

    for dir in dirs:
        newpath = join(path, dir)
        files = listdir(newpath)

        # get the name of the file which contains requested resources
        # strip .txt to save it as label for classification
        # create path name to access the file

        for file in files:
            filepath = join(newpath,file)
            if os.stat(filepath).st_size == 0:
                continue

            r_list = []
            key = file[:-4]

            if key[0:3] == 'www':
                key = key[4:]

            if not bool(accessed_resources.get(key)):
                accessed_resources[key] = []
            lines = [line.rstrip('\n') for line in open(filepath)]

            # each line has hostname and ip address
            # we only need hostname and we want to strip 'www.'
            # we add each resource to the overall set of resources ever accessed +
            # we add resources for current key to be added to hash table later by key

            tld = key.split('.')[0]

            for line in lines:
                requested_resource = line.split(',')[0]
                if (mode == "nontld" and tld in line) or (mode == "tld" and tld not in line):
                    continue
                if requested_resource[0:3] == 'www':
                    requested_resource = requested_resource[4:]
                all_resources.add(requested_resource)
                r_list.append(requested_resource)

            # we want to crate a row only if has at least one '1'
            # If list of resources is empty than there will no such thing

            if r_list:
                accessed_resources[key].append(r_list)
                total_size += 1

    print('Files are processed...')
    create_matrix(list(all_resources), accessed_resources, total_size, clf)


if __name__ == "__main__":
    read_from_dir(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
