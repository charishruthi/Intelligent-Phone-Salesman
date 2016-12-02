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
import collections
from rer_client import *


rer_client = RerClient("1PI11CS196","g104")
brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
for v in rer_client.get_brand_product_bigrams_dict().values():
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
for p in product_names:
    product_name_tokens.extend(p.split())


class FeatureFunctions(object):
    def __init__(self, sents, supported_tags, tag_list = None):
        self.wmap = {}
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    if(len(k[1:].split("_")) == 2 ):
                        tag = k[1:].split("_")[0]
                    else:
                        tag = k[1:].split("_")[0]+"_"+k[1:].split("_")[1]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        self.supported_tags = self.fdict.keys()
        #self.supported_tags = supported_tags        
        return

    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0

        #------------------------------- Price tag ---------------------------------------------------------
    # The following is an example for you to code your own functions
    # returns True if wi is in phones tag = Phone
    # h is of the form {'ta':xx, 'tb':xx, 'wn':xx, 'i':xx}
    # self.wmap provides a list of sentences (tokens) where each element in the list is a dict {'words': word_token_list, 'pos_tags': pos_tags_list}
    # each pos_tag is a tuple returned by NLTK tagger: (word, tag)
    # h["wn"] refers to a sentence number
    
    def fprice_query_1(self, h, tag):
        if tag != "price_query":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if ("Price" in h['relatedTags']):
            return 1
        else:
            return 0


    #------------------------------- Functions for Feature_query tag ---------------------------------------------------------
    # May need to be changed
    def ffeature_query_1(self, h, tag):
        if tag != "feature_query":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if ("Feature" in h['relatedTags']):
            return 1
        else:
            return 0

    
    #------------------------------- Functions for Comparison tag ---------------------------------------------------------  

    def fcomparison_1(self, h, tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']
        l=h['relatedTags']
        words = map(lambda x:x["word"],h["sentence"])
        counter=collections.Counter(l)
        if("Org" in l):  
            if (dict(counter.most_common(len(l)))['Org'] and (('superior' in words and 'to' in words) or ('inferior' in words and 'to' in words) or ('or' in words) or ('over' in words) or ('between' in words ) or ('of' in words and 'the' in words and 'two' in words) or ('better' in words) or ('worse' in words))):
                return 1
            else:
                return 0
        return 0

    def fcomparison_2(self,h,tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']   
        l=h['relatedTags']
        words = map(lambda x:x["word"],h["sentence"])
        counter=collections.Counter(l)
        if("Family" in l):     
            if (dict(counter.most_common(len(l)))['Family'] and (('superior' in words and 'to' in words) or ('inferior' in words and 'to' in words) or ('or' in words) or ('over' in words) or ('between' in words ) or ('of' in words and 'the' in words and 'two' in words) or ('better' in words) or ('worse' in words))):
                return 1
            else:
                return 0
        return 0

    def fcomparison_3(self, h, tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']
        l=h['relatedTags']
        words = map(lambda x:x["word"],h["sentence"])
        counter=collections.Counter(l)
        if("OS" in l):        
            if (dict(counter.most_common(len(l)))['OS'] and (('superior' in words and 'to' in words) or ('inferior' in words and 'to' in words) or ('or' in words) or ('over' in words) or ('between' in words ) or ('of' in words and 'the' in words and 'two' in words) or ('better' in words) or ('worse' in words))):
                return 1
            else:
                return 0
        return 0

    def fcomparison_4(self, h, tag):
        if tag != "comparison":
            return 0
        #words = self.wmap[h["wn"]]['words']
        l=h['relatedTags']
        words = map(lambda x:x["word"],h["sentence"])
        counter=collections.Counter(l)
        if("Version" in l):        
            if (dict(counter.most_common(len(l)))['Version'] and (('superior' in words and 'to' in words) or ('inferior' in words and 'to' in words) or ('or' in words) or ('over' in words) or ('between' in words ) or ('of' in words and 'the' in words and 'two' in words) or ('better' in words) or ('worse' in words))):
                return 1
            else:
                return 0
        return 0

    #------------------------------- Functions for Intent_query tag ---------------------------------------------------------        

    def finterest_intent_1(self, h, tag):
        if tag != "interest_intent":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        words = map(lambda x:x["word"],h["sentence"])
        if len(words)> 0:
            if (("buy" in words and 'want' in words) or ("purchase" in words and 'want' in words) or ('need' in words and 'I' in words) or ('need' in words and 'i' in words) or ((words[0].lower() == 'when') or (words[0].lower() == 'is')) or ('looking' in words and 'for') or ('wish' in words and 'to' in words and 'know') or ('interested' in words) or ('would' in words and 'like' in words and 'know' in words)):
                return 1
            else:
                return 0
        return 0

    
    #------------------------------- Functions for Irrelevant tag ---------------------------------------------------------

    def firrelevant_1(self, h, tag):
        tags_copy=self.supported_tags[:]
        tags_copy.remove('irrelevant')
        if tag != "irrelevant":
            return 0
        #words = self.wmap[h["wn"]]['words']        
        if (tag not in tags_copy):
            return 1
        else:
            return 0

    #def rule_Ack(self,h,tag)
    def rule_Acknowledgement(self,h):
        words = map(lambda x:x["word"],h["sentence"])
        if (("thanks" in words) or ("thank" in words) or ('yes' in words)):
            return 1
        else:
            return 0
    
    def rule_Disagreement(self,h):
        words = map(lambda x:x["word"],h["sentence"])
        if (("not" in words) or ("no" in words) or ('else' in words) or ('alternative' in words) or ('inconvenience' in words) or ('inconvenient' in words) or ('but' in words)):
            return 1
        else:
            return 0
    
    def rule_Greeting(self,h):
        words = map(lambda x:x["word"],h["sentence"])
        if (("hi" in words) or ('hello' in words) or ('hey' in words)):
            return 1
        else:
            return 0

    def rule_Agreement(self,h):
        words = map(lambda x:x["word"],h["sentence"])
        if (("true" in words) or ("yes" in words) or ('indeed' in words)):
            return 1
        else:
            return 0

    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats

if __name__ == "__main__":
    pass
