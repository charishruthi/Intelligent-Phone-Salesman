'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import re
import os
import ast
from MyMaxEnt import MyMaxEnt

phones = ["phone", "phones", "smartphone", "smartphones", "mobile","tablet","tablets","phablet","phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry',
            'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio',
            'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list = [m.lower() for m in org_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees","price","cheaper","expensive","cheapest","dollar","dollars"]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list = [m.lower() for m in os_list]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
features = ["camera","wifi","gsm","cdma","gps","2g","3g","screen","battery","memory","ram","sim","bluetooth","life"]
class FeatureFunctions(object):    
    def __init__(self, wmap, tag_list,prodlist):
        self.wmap = wmap
        self.supported_tags = tag_list
	temp = ast.literal_eval(prodlist)
	self.prodlist = []
	self.modellist = []
	for i in temp:
	    self.prodlist.append(i.lower())
	    for j in temp[i]:
		self.modellist.append(j.lower())
	
	#print(prodlist)
        #self.flist = [ self.f1,self.f2,self.f3,self.f4,self.f5,self.f6,self.f7,self.f8,self.f9,self.f10 ,self.f11,
#self.f12,self.f13,self.f14,self.f15, self.f16,self.f17,self.f18,self.f19]
        self.flist = [ self.f1, self.f5, self.f2, self.f3,self.f4,self.f6,self.f7,self.f9,
self.f11,self.f13,self.f14,self.f11,self.f18,self.f16,self.f17,self.f19,self.f20,self.f21,self.f22,self.f23,self.f24,self.f25,self.f26,
self.f28,self.f30,self.f31,self.f34,self.f35,self.f36,self.f37,self.f38,self.f39,self.f40,self.f41,self.f42,self.f43,self.f44,self.f45,
self.f46,self.f47,self.f48,self.f49,self.f50,self.f51,self.f52]
        #self.flist = self.generateBigram(bigrams) + self.generateTrigram(trigrams)
        return

    # NOTE: Added by Ananth ro make it work - clean these later
    def set_wmap(self, sents, pic = None): # given a list of words sets wmap
        #print "pic from ff = ", pic
        if (pic == None):
            for i in range(len(sents)):
                self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        if (pic != None):
            if os.path.isfile(pic): # we will now setup wmap from pickle file
                self.wmap = pickle.load(open(pic, "rb"))
            else:
                for i in range(len(sents)):
                    self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
                pickle.dump(self.wmap, open(pic, "wb"))                
        return
    
    
    def getword(self,h):
	    return  self.wmap[h["wn"]]["pos_tags"][h["i"]][0]

    def gettag(self,h):
	    return  self.wmap[h["wn"]]["pos_tags"][h["i"]][1]
    
    def getnextword(self,h):
	if h["i"]+1  <  len(self.wmap[h["wn"]]["pos_tags"]):
	    return self.wmap[h["wn"]]["pos_tags"][h["i"]+1][0]	
    
    def getprevword(self,h):
	if h["i"]-1 >=0 :
	    return self.wmap[h["wn"]]["pos_tags"][h["i"]-1][0]	
    
    def getnexttag(self,h):
	if h["i"]+1 < len(self.wmap[h["wn"]]["pos_tags"]):
	    return self.wmap[h["wn"]]["pos_tags"][h["i"]+1][1]	
    
    def getprevtag(self,h):
	if h["i"]-1 >= 0 :
	    return self.wmap[h["wn"]]["pos_tags"][h["i"]-1][1]
    def f1(self, h, tag): #First Letter capital Family
        if tag == "Family" and self.getword(h)[0].isupper() and h["i"] >= 1:
            return 1
        else :
            return 0
    def f5(self, h, tag): #First Letter Capital Org
        if tag == "Org" and self.getword(h)[0].isupper() and h["i"] >= 1:
            return 1
        else :
            return 0  
    
    def f2(self, h, tag): #All caps Org
        if tag == "Org" and self.getword(h).isupper():
            return 1
        else:
            return 0

    def f3(self, h, tag): #All caps Family
        if tag == "Family" and self.getword(h).isupper():
            return 1
        else:
            return 0
    
    def f4(self, h, tag): #No in between Family
        pattern = re.compile(r"^\w+\d+\w*") 
        if(tag=="Family" and pattern.search(self.getword(h)) and h["tb"] == "Family"):
            return 1
        else:
            return 0 
    
    def f6(self, h, tag): #All lower
        if tag=="Other" and self.getword(h).islower():
            return 1
        else :
            return 0  
    def f49(self,h,tag):
	if tag == "Other"  and self.getword(h)[0].isupper() and h["i"] == 0:
	    return 1
	return 0
    def f50(self,h,tag):
	if tag == "Other" and self.gettag(h) == 'NNP':
	    return 1
	return 0
    def f7(self, h, tag): #Org Family Bigram
        if tag == "Family" and h["tb"] == "Org":
            return 1
        else:
            return 0
        
    def f8(self, h, tag): #Other Other Bigram
        if tag == "Other" and h["tb"] == "Other":
            return 1
        else:
            return 0
    
    def f9(self, h, tag): #Other Org Bigram
        if tag == "Org" and h["tb"] == "Other":
            return 1
        else:
            return 0
    def f10(self, h, tag): # Other being a noun , determiner , adjective etc
        commontags = [ 'CC', 'JJ', 'NN','NNS', 'DT','VB','VBD','WDT','WP','WRB','VBZ','VBP','.','VBG'
,'RP','RBS','RBR','RB','PRP','POS','PRP$','PDT','MD','JJR','JJS']
        if tag == "Other" and self.gettag(h) in commontags:
            return 1
        else:
            return 0

    def f11(self, h, tag): # Price being a number
        pattern = re.compile(r"(Rs\.?)?\d{4,}")
        if(tag == "Price" and  pattern.search(self.getword(h))):
            return 1
        else:
            return 0            

    def f51(self, h, tag): # Price being a number
        pattern = re.compile(r"^\d(/,/d{3})*")
        if(tag == "Price" and  pattern.search(self.getword(h))):
            return 1
        else:
            return 0            
    def f12(self, h, tag): #Price followed by Price
        if(tag == "Price" and h["tb"] == "Price" ):
	    if self.prevword(h):
		if self.prevword(h) in currency_symbols:
		    return 1
 		return 0
            else:
		    return 0
        else:
            return 0
    def f18(self, h, tag): #Other Price Bigram
        if(tag == "Price" and h["tb"] == "Other"):
            return 1
        else:
            return 0

   
    def f13(self, h, tag): # Common words for phone
        if tag == "Phone" and self.getword(h).lower() in phones :
            return 1
        else :
            return 0
    def f14(self, h, tag): # Other Phone Bigram
        if tag == "Phone" and h["tb"] == "Other":
            return 1
        else :
            return 0
    def f15(self,h,tag): # Other beginning the sentence
        if tag == "Other" and h["tb"] == "*" and h["ta"] == "*": 
            return 1
        else:
            return 0    
    def f16(self,h,tag): # Org being a proper noun
        if tag == "Org" and self.gettag(h) in ['NNP','NNPS']:
            return 1
        else :
            return 0
    def f17(self,h,tag): #Family being a proper noun
        if tag == "Family" and self.gettag(h) in ['NNP','NNPS']:
            return 1
        else :
            return 0
    def f19(self,h,tag): #Price
        if tag=="Price" and self.gettag(h) in ['CD']:
            return 1
        else :
            return 0    
    def f20(self,h,tag): #Price ending with k
	pattern = re.compile("\d+[kK]")
	if tag == 'Price' and pattern.search(self.getword(h)):
	    return 1
	else:
	    return 0
    def f21(self,h,tag): #.?
	if tag=="Other" and self.getword(h) in ['.','?',' ','',',','!']:
	    return 1
	else:
	    return 0   
    def f22(self,h,tag):
	if tag == "Org" and self.getprevtag(h) in ["VBZ","WDT"]:
	    return 1
	return 0
    def f23(self,h,tag):
	if tag == "Org" and h["tb"] == "*":
	    return 1
	return 0
    def f24(self,h,tag):
	if tag == "Other" and h["tb"] == "Phone":
	    return 1
	return 0
    def f25(self,h,tag):
	if tag == "Other" and h["tb"] == "Family":
	   return 1
	return 0
    def f26(self,h,tag):
	if tag == "Org" and self.getword(h).lower() in org_list:
	    return 1
	return 0
    def f27(self,h,tag):
	if tag == "Family" and h["tb"] == "Other":
	    return 1
	return 0  
    def f28(self,h,tag):
	if tag == "Other" and h["tb"] == "Org":
	    return 1
	return 0  
    def f29(self,h,tag):
	if tag == "Family" and h["tb"] == "Family":
	    return 1
	return 0
    def f30(self,h,tag):
	if tag == "Other" and h["tb"] == "Price":
	    return 1
	return 0
    def f31(self,h,tag):
	if tag == "Phone" and h["ta"] == "Other" and h["tb"] == "Other":
	    return 1
	return 0 
    def f32(self,h,tag):
	if tag == "Family" and self.getword(h).lower() in self.prodlist:
	    return 1
	return 0 
    def f33(self,h,tag):
	if tag == "Family" and h["tb"] == "Family" and self.getword(h).lower() in self.modellist:
	    return 1
	return 0
    def f34(self,h,tag):
	if tag == "Price" and  self.getword(h).lower() in currency_symbols:
	    return 1
	return 0 
    def f35(self,h,tag):
	if tag == "OS" and h["tb"] == "Other" :
	   return 1
	return 0
    def f36(self,h,tag):
	if tag == "OS" and self.getword(h).lower() in os_list:
	    return 1
	return 0
    def f37(self,h,tag):
	word = self.getword(h)
	if tag == "OS" and (word[0].isupper() or word.isupper()):
	    return 1
	return 0
    def f38(self,h,tag):
	if tag == "Version" and h["tb"] in  ["OS","Version"]:
	    return 1
	return 0 
    def f39(self,h,tag):
	if tag == "Version" and h["tb"] in ["OS"] and re.search(r"\d+(.\d+)?",self.getword(h)):
	    return 1
	return 0
    def f40(self,h,tag):
	if tag == "Feature" and h["tb"] == "Feature" and self.getword(h).lower() in size_list:
	    return 1
	return 0
    def f41(self,h,tag):
	if tag == "Feature" and h["tb"] == "Other" :
	    return 1
	return 0
    def f42(self,h,tag):
	if tag == "Feature" and h["tb"] == "Feature":
	    return 1
	return 0
    def f43(self,h,tag):
	if tag == "Price" and h["tb"] == "Other" and h["ta"] == "Other":
	   return 1
	return 0
    def f44(self,h,tag):
	if tag == "Price" and h["tb"] == "Price" and h["ta"] == "Price":
	    return 1
	return 0
    def f45(self,h,tag):
	if tag == "Feature" and h["tb"] == "Other" and re.search("\d{1,2}(\.\d)?",self.getword(h)):
	    return 1
	return 0	
    def f46(self,h,tag):
	if tag == "Feature" and self.getword(h).lower() in features:
	    return 1
	return 0
    def f47(self,h,tag):
	prev = [ "than","for","to","below","costs","between","above"]
	if tag == "Price" :
	    prevw = self.getprevword(h)
	    if prevw:
		if prevw.lower() in prev:
		    return 1
		return 0 
	    else:
	    	return 0
	return 0
    def f48(self,h,tag):
	prev = ["has","having","with","a","the","is"]
	if tag == "Feature":
	    prevw = self.getprevword(h)
	    if prevw:
		if prevw.lower() in prev:
		    return 1
		return 0
	    else:
		return 0
	return 0
    def f52(self,h,tag):
	nextw = self.getnextword(h)
	if tag == "Feature" and nextw :
	    if nextw.lower() in size_list and re.search(r"^\d{1,2}(\.\d)?",self.getword(h)):
		return 1
	    return 0
	return 0 
    def evaluate(self, xi, tag):
        feats = []
        for f in self.flist:
            feats.append(int(f(xi, tag)))
        return feats

