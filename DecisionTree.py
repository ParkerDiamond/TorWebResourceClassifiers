import sys
import os
import random
import tldextract
import numpy
import scipy.stats
import sklearn.tree
import sklearn.feature_selection

random.seed(0)
site_resources = {}
page_loads = {}

def featureSelection():
    max_len = max(len(x) for x in page_loads.values())

    for key in page_loads:
        tmp_list = []
        for item in page_loads[key]:
            tmp_list.append(hash(item))

        while len(tmp_list) < max_len:
            tmp_list.append(hash(''))

        page_loads[key]=tmp_list

    selector = sklearn.feature_selection.VarianceThreshold(threshold = (.8 * (1-.8)))
    data = selector.fit_transform(list(page_loads.values()))

    for idx,key in enumerate(page_loads):
        page_loads[key] = data[idx]
    
def fitTree():
    inputs = []
    outputs = []

    for key in page_loads:
        outputs.append(key[1])
        inputs.append(page_loads[key])

    dtc = sklearn.tree.DecisionTreeClassifier()
    dtc.fit(inputs, outputs)
    
    total = 0.0
    for idx,item in enumerate(inputs):
        guess = dtc.predict([item])
        if guess == outputs[idx]:
            total += 1.0

    total /= len(inputs)
    print(total)
    print(dtc.tree_.max_depth)

def readResources(base_dir,criteria=None):
    for root, ases, files in os.walk(base_dir):
        for as_dir in ases:
            for as_root, dirs, site_files in os.walk(os.path.join(base_dir,as_dir)):
                for site_file in site_files:

                    url = site_file[:site_file.rfind('.')]
                    url_domain = tldextract.extract(url).domain

                    with open(os.path.join(base_dir,as_root,site_file), 'r') as f:
                        for line in f.readlines():
                            resource = line.strip().split(',')[0]
                            resource_domain = tldextract.extract(resource).domain

                            if url not in site_resources:
                                site_resources[url] = set()

                            if (as_root,url) not in page_loads:
                                page_loads[(as_root,url)] = set()

                            if (criteria=='~TLD' and (url_domain != resource_domain)):
                                page_loads[(as_root,url)].add(resource)
                            elif (criteria=='TLD' and (url_domain == resource_domain)):
                                page_loads[(as_root,url)].add(resource)
                            elif criteria is None:
                                page_loads[(as_root,url)].add(resource)
                                
                            site_resources[url].add(resource)

if __name__ == "__main__":
    readResources(sys.argv[1])
    featureSelection()
    fitTree()
    pass
