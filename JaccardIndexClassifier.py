import sys
import os
import random
import tldextract
import numpy
import scipy.stats

random.seed(0)
site_resources = {}
page_loads = {}

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

def JaccardIndex(a,b):
    return len(a&b)/len(a|b)

def calcConfidence(indices):
    vals, keys = zip(*indices)
    return scipy.stats.zscore(vals)[0]

def classifyRandomLoad():
    load = random.choice(list(page_loads.keys()))
    asn,url = load
    resources = page_loads[load]

    jindex = map(lambda x: (JaccardIndex(x[1],resources),x[0]), site_resources.items())
    jindex = sorted(jindex, key=lambda x:x[0],reverse=True)

    guess = jindex[0][1]
    match = jindex[0][0]

    #print("Prediction: {0} --- {1}".format(guess,match))
    #print("Actual: {0}".format(url))

    #confidence = jindex[0][0] - jindex[1][0]
    confidence = calcConfidence(jindex)
    if numpy.isnan(confidence):
        confidence = 0

    return(guess==url, confidence)

if __name__ == "__main__":

    if len(sys.argv) >= 3:
        readResources(sys.argv[1], criteria=sys.argv[2])
    else:
        readResources(sys.argv[1])

    average_correct = 0.0
    average_correct_conf = 0.0
    average_wrong_conf = 0.0

    for i in range(10000):
        correct,confidence = classifyRandomLoad()
        if correct:
            average_correct += 1.0
            average_correct_conf += confidence
        else:
            average_wrong_conf += confidence

    average_correct_conf /= int(average_correct)
    average_wrong_conf /= (10000-int(average_correct))
    average_correct /= 10000.0

    print("Correctness: {0}".format(average_correct))
    print("Average Confidence (Correct): {0}".format(average_correct_conf))
    print("Average Confidence (Incorrect): {0}".format(average_wrong_conf))

