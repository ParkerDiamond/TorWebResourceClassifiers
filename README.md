# TorWebResourceClassifiers
Project for UTK COSC560

## Data Set
The data set is compressed in the file `tor_web_resources.tar.gz`, and it is organized in a hierarchical manner. The uppermost directory contains directories corresponding to autonomous system numbers. These are the ASes which have an exit relay through which we visited the Alexa Top 1000. Each of these directories contains 1000 flat text files. They contain the hostnames and their corresponding IP addresses of the resources that were loaded when visiting the web site specified in the file name.

For example, a file might have a path `/tor_web_resources/3/rt.com.txt`. The website rt.com is being visited through a exit relay in AS 3, and the contents are the hostname, IP address pairs for all of the resources loaded when visiting that website in a browser through that exit relay.

## Classifiers

The Jaccard Index classifier is in `JaccardIndexClassifier.py`. It accepts up to two comman line arguments. The first one is mandatory and it is the uppermost directory of the data set (the one that has all the directories). The second argument is optional and can have value (~TLD, TLD, ALL). The ~TLD tells the classifier to classify only resources not belonging to the TLD of each URL. The TLD option is the opposite of the ~TLD option. The ALL option just uses all resources to classify a website load.

The Decision Tree classifier is in `DecisionTree.py`. It only accepts the uppermost directory of the data set and prints the accuracy of the classification and the max depth of the decision tree it generates.

`svc_mlp_rf.py` uses 1 of 3 - linear SVC, random forrest or multi-layer perceptron, to classify the dataset. It has to be specified which algorithm to use. There are also options that can be specified for requested resources: "tld", "nontld". 

## Results

All results are saved into .txt file with corresponding names.
