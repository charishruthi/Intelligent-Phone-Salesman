'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import os

from MyMaxEnt import MyMaxEnt
from memm import Memm
from ner_metrics import NerMetrics
#from ner_client import get_brand_product_bigrams_dict
from feature_functions import FeatureFunctions

import requests

service_url = "http://jnresearch.com/"
upload_url = service_url + "upload_file"
prod_bigrams_url = service_url + "get_brand_product_bigrams"

    
def build_history(data_list, supported_tags):
    history_list = [] # list of all histories
    sents = []
    count = 0
    expected = []
    for data in data_list: # data is the inputs entered by a given student
        data1 = data['data']
        for rec in data1:
            updates = rec['updates']
            sent = rec['sentence']
            words = []

            expected.append(updates)
            
            for i in range(len(updates)):
                words.append(updates[i]['word'])
                '''
                #------------------------------------------------------------------------------------------------
                # NOTE: below code is a temporary hack to build the MAxEnt for just 2 tags - we will change this later
                if (updates[i]['tag'] not in supported_tags):
                    if updates[i]['tag'] == "Model":
                        updates[i]['tag'] = "Version"
                    else:
                        updates[i]['tag'] = "Other"                
                #------------------------------------------------------------------------------------------------
                '''
                if (updates[i]['tag'] not in supported_tags):
                    if updates[i]['tag'] == "Model":
                        updates[i]['tag'] = "Family"
                    elif updates[i]['tag'] == "Size":
                        updates[i]['tag'] = "Feature"
                    else:
                        updates[i]['tag'] = "Other"                


            sents.append(words)
            
            for i in range(len(updates)):
                history = {}
                history["i"] = i
                if i == 0:
                    history["ta"] = "*" # special tag
                    history["tb"] = "*" # special tag
                elif i == 1:
                    history["ta"] = "*" # special tag
                    history["tb"] = updates[i - 1]['tag']
                else:
                    history["ta"] = updates[i - 2]['tag'] 
                    history["tb"] = updates[i - 1]['tag']
                history["wn"] = count
                history_list.append((history, updates[i]['tag'], ))
            count += 1
    return (history_list, sents, expected)

def ner_tag(sent):
    #----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
    json_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER/all_data.json"
    #pickle_file = r"C:\home\ananth\research\pesit\nlp\ner\all_data.p"
    pickle_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER/all_data.p"
    history_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerat1or/NER/history.p"
    model_metrics_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER/model_metrics.p"
    # ----------------------------------------------------------------
    ner_client = NerClient("1PI11CS196", "g04")    
    ret = ner_client.get_brand_product_bigrams_dict()
    
    supported_tags = ["Org", "OS", "Version", "Phone", "Other", "Price", "Family", "Size", "Feature"]    
    
    data = json.loads(open(json_file).read())['root']
    #print "num stu = ", len(data)
    (history_list, sents, expected) = build_history(data, supported_tags)
    (his1, wmap1) = build_history_1(data, supported_tags)
    myhis = (history_list, sents, expected, ) 
    
    func_obj = FeatureFunctions(wmap1, supported_tags, ret) #FeatureFunctions(supported_tags)
    #print "Number of features defined: ", len(func_obj.flist)
    clf = Memm(func_obj, pickle_file)

    func_obj.set_wmap(sents)
    #print "After build_history"
        

    #TRAIN = int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
    TRAIN = 0
    if TRAIN == 1:
        clf.train(history_list[:7500], reg_lambda = 0.02) # 10000
    else:
        clf.load_classifier()

    #print "Model: ", clf.model, " tagset = ", clf.tag_set

    test_sents = []
    test_sents.append(sent.split(" "))
    result = clf.tag(test_sents)
    return result


def test(clf, history_list):
    result = []
    for history in history_list:
        mymap = wmap[history[0]["wn"]]
        words = mymap['words']
        tags = mymap['pos_tags']    
        index = history[0]["i"]
        val = clf.classify(history[0])
        result.append({'predicted': val, 'word': words[index], 'expected': history[1]})
    return result


def upload_file(fn, pw, group):
    comps = os.path.split(fn) # get the components of file name
    headers = {'content-type': 'application/json'}
    r = requests.post(upload_url, data = json.dumps({"data": open(fn, 'rb').read(), "password": pw, "group": group, "filename": comps[1]}), headers = headers) #
    if r.text.isdigit():
        return int(r.text)
    return None
    

class NerClient(object):
    def __init__(self, password, group):
        self.group = group
        self.password = password
        self.headers = {'content-type': 'application/json'}
        return

    def upload(self, fn):
        ret = upload_file(fn, self.password, self.group)
        return ret

    def get_brand_product_bigrams_dict(self):
        r = requests.post(prod_bigrams_url, data = json.dumps({"password": self.password, "group": self.group}), headers = self.headers) #
        return r.text


def build_history_1(data_list, supported_tags):

    history_list = [] # list of all histories

    words_map = {}

    count = 0

    for data in data_list: # data is the inputs entered by a given student

        data1 = data['data']

        for rec in data1:

            updates = rec['updates']

            sent = rec['sentence']

            words = []

            

            for i in range(len(updates)):

                words.append(updates[i]['word'])

                #------------------------------------------------------------------------------------------------
                # NOTE: below code is a temporary hack to build the MAxEnt for just 2 tags - we will change this later
                if (updates[i]['tag'] not in supported_tags):
                    if updates[i]['tag'] == "Model":
                        updates[i]['tag'] = "Family"
                    elif updates[i]['tag'] == "Size":
                        updates[i]['tag'] = "Feature"
                    else:
                        updates[i]['tag'] = "Other"                
                #------------------------------------------------------------------------------------------------
            words_map[count] = {'words': words, 'pos_tags': nltk.pos_tag(words)}
            for i in range(len(updates)):

                history = {}

                history["i"] = i

                if i == 0:

                    history["ta"] = "*" # special tag

                    history["tb"] = "*" # special tag

                elif i == 1:

                    history["ta"] = "*" # special tag

                    history["tb"] = updates[i - 1]['tag']

                else:

                    history["ta"] = updates[i - 2]['tag'] 

                    history["tb"] = updates[i - 1]['tag']

                history["wn"] = count

                history_list.append((history, updates[i]['tag'], ))

            count += 1

    return (history_list, words_map)



if __name__ == "__main__":
    #----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
    json_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER/all_data.json"
    #pickle_file = r"C:\home\ananth\research\pesit\nlp\ner\all_data.p"
    pickle_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER/all_data.p"
    history_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/NER/history.p"
    model_metrics_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/NER/model_metrics.p"
    # ----------------------------------------------------------------
    ner_client = NerClient("1PI11CS196", "g04")    
    ret = ner_client.get_brand_product_bigrams_dict()
    
    supported_tags = ["Org", "OS", "Version", "Phone", "Other", "Price", "Family", "Size", "Feature"]    
    
    build = int(raw_input("Enter 1 for Building history from json, 0 to use pickeled file:  "))
    #if build == 1:
    data = json.loads(open(json_file).read())['root']
    print "num stu = ", len(data)
    (history_list, sents, expected) = build_history(data, supported_tags)
    (his1, wmap1) = build_history_1(data, supported_tags)
    myhis = (history_list, sents, expected, ) 
    pickle.dump(myhis, open(history_file, "wb"))        
    #print history_list[:100]
    #raw_input("Enter to continue")
    '''
    else:
        print 'getting data from file'
        (history_list, sents, expected) = pickle.load(open(history_file, "rb"))        
        print 'got history data from file'
    '''

    func_obj = FeatureFunctions(wmap1, supported_tags, ret) #FeatureFunctions(supported_tags)
    print "Number of features defined: ", len(func_obj.flist)
    clf = Memm(func_obj, pickle_file)

    func_obj.set_wmap(sents)
    print "After build_history"
        

    TRAIN = int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
    if TRAIN == 1:
        clf.train(history_list[:7500], reg_lambda = 0.02) # 10000
    else:
        clf.load_classifier()

    print "Model: ", clf.model, " tagset = ", clf.tag_set

    #test_sents = [["I", "need", "a", "Microsoft", "Windows", "2", "Smartphone"]]
    #test_sents = [["Samsung", "released", "a", "Android", "2", "Smartphone"]]
    
    test_sents = [
        ["I", "need", "a", "Microsoft", "Galaxy", "2", "Smartphone"],
        ["Samsung", "released", "a", "Android", "2", "Smartphone"],
        ["I", "have", "a", "Blackberry", "OS", "Smartphone"],
        ["Microsoft", "announced", "the", "quarterly", "results", "today"],
        
    ]
    

    print "Number of sentences = ", len(sents)
    
    start = -700
    end = -600 # -10
    
    
    start = -1300
    end = -1200 # -10

    
    start = -800
    end = -300 # -10

    print "Start sentence = ", start
    print "End sentence = ", end
    
    test_sents = sents[start:end] #sents[-70:-50]
    result = clf.tag(test_sents)
    #mg = NerMetrics(expected[-70:-50], result)
    mg = NerMetrics(expected[start:end], result)
    metrics = mg.compute()
    #mg.print_results()

    model_metrics = {'model': clf.model, 'expected': expected[start:end], 'predicted': result, 'metrics': metrics}
    pickle.dump(model_metrics, open(model_metrics_file, "wb"))        
    

    print '#' * 10, "METRICS", '#' * 10
    for k, v in metrics.items():
        print "For the tag: ", k, " the metrics are: "
        print '\tPrecision = ', v["precision"], "  Recall = ", v["recall"], "  f1 = ", v["f1"]
