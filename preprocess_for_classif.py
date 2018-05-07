# Written by: Ksenia Burova
# Data processing for classification

import numpy as np
from os import listdir
import os
from os.path import join

def create_matrix(all_resources, accessed_resources, total_size):

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

    # adding labels

    print(len(datapoints))
    print(len(label_nums))

    datapoints = np.hstack((datapoints, label_nums.reshape(-1,1) ))

    print('--Writing to file--')
    print('MAtrix has ', len(datapoints), ' rows')
    np.savetxt('output_matrix_fastest', datapoints, delimiter=",", fmt="%d")
    np.savetxt('labels', labels, delimiter=",", fmt="%s")

def read_from_dir(path):
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
            print(lines)
            total_size += 1
            # each line has hostname and ip address
            # we only need hostname and we want to strip 'www.'
            # we add each resource to the overall set of resources ever accessed +
            # we add resources for current key to be added to hash table later by key

            for line in lines:
                requested_resource = line.split(',')[0]
                if requested_resource[0:3] == 'www':
                    requested_resource = requested_resource[4:]
                all_resources.add(requested_resource)
                r_list.append(requested_resource)

            accessed_resources[key].append(r_list)

    create_matrix(list(all_resources), accessed_resources, total_size)
    # f1 = open('output_file', 'w')
    # print(accessed_resources, file=f1)

if __name__ == "__main__":
    read_from_dir("tor_alexa_resolutions/")