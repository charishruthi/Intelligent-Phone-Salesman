'''
MyMaxEnt.py
MaxEnt Classifier
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014
'''
import json
import numpy
import math
import pickle

from scipy.optimize import minimize as mymin 
import datetime

# ----------------------------------------------------------------------------------------
# maxent implementation
# ----------------------------------------------------------------------------------------
class MyMaxEnt(object):
    def __init__(self, history_tuples, function_obj, reg_lambda = 0.01, pic_file = None): 
        # history_tuples is of the form: ((ta, tb, wn, i), tag) where ta = tag t-2, tb = tag t-1, wn = pointer to a sentence, i = current index
        # function_list is of the form: [(pointer_to_function_f1, tag_for_f1), (pointer_to_function_f2, tag_for_f2)...]
        # reg_lambda = regularization coefficient
        # pic_file = Name of file where the classifier is pickled
        self.h_tuples = history_tuples
        self.func = function_obj
        self.reg = reg_lambda
        self.dataset = None # this will be set by create_dataset
        self.tag_set = self.func.supported_tags #None # this will be also be set by create_dataset - this is the set of all tags
        self.create_dataset()
        #print self.dataset
        self.dim = self.dataset.shape[1]
        #print "dim = " + str(self.dim)
        self.num_examples = self.dataset.shape[0]  #self.dataset.shape[1]
        self.model = numpy.array([0 for d in range(self.dim)]) # initialize the model to all 0
        #print self.model
        self.pic_file = pic_file
        return

    def create_dataset(self):
        self.dataset = []
        self.all_data = {}
        for h in self.h_tuples[:2000]+self.h_tuples[-100:]: # h represents each example x that we will convert to f(x, y)
            for tag in self.tag_set:
                feats = self.all_data.get(tag, [])
                val = self.get_feats(h[0], tag)
                feats.append(val)
                self.all_data[tag] = feats
                if (h[1] == tag):
                    self.dataset.append(val)
        for k, v in self.all_data.items():
            self.all_data[k] = numpy.array(v)
        self.dataset = numpy.array(self.dataset)
        return

    def get_feats(self, xi, tag): # xi is the history tuple and tag is y belonging to Y (the set of all labels
        # xi is of the form: history where history is a 4 tuple by itself
        # self.func is the function object
        return self.func.evaluate(xi, tag)

    def train(self):
        dt1 = datetime.datetime.now()                   
        print 'before training: ', dt1         
        params = mymin(self.cost, self.model, method = 'L-BFGS-B') #, jac = self.gradient) # , options = {'maxiter':100}
        self.model = params.x
        dt2 = datetime.datetime.now()
        print 'after training: ', dt2, '  total time = ', (dt2 - dt1).total_seconds()
        
        if self.pic_file != None:
            pickle.dump(self.model, open(self.pic_file, "wb"))
        return

    def classify_sent(self,feat_obj, hist_obj):
        val = self.classify(hist_obj)
        if(val == "irrelevant"):
            if(feat_obj.rule_Agreement(hist_obj)):
                val = "agreement"
            elif(feat_obj.rule_Disagreement(hist_obj)):
                val = "disagreement"
            elif(feat_obj.rule_Acknowledgement(hist_obj)):
                val = "acknowledgement"
            elif(feat_obj.rule_Greeting(hist_obj)):
                val = "greeting"
        return val
            

    def test(self, feat_obj, history_list):
        result = []
        for history in history_list:
            val = self.classify(history[0])
            if(val == "irrelevant"):
                if(feat_obj.rule_Agreement(history[0])):
                    val = "agreement"
                elif(feat_obj.rule_Disagreement(history[0])):
                    val = "disagreement"
                elif(feat_obj.rule_Acknowledgement(history[0])):
                    val = "acknowledgement"
                elif(feat_obj.rule_Greeting(history[0])):
                    val = "greeting"
            result.append({'predicted': val, 'sentence': history[0]["sentence"], 'expected': history[1]})
        return result

    def test_viterbi(self,feat_obj,history_list):
        result = []
        count = 0
        histlist = []
        for i in feat_obj.wmap.keys()[0:50]:
            partial_sentence = []
            histlist = []
            for words in feat_obj.wmap[i]['words']:
                partial_sentence.append(words)
                histlist.append(history_list[count])
                count += 1
            #print count
            #print history_list[i]
            tag_sequence = self.viterbi(partial_sentence,histlist)
            #print 'predicted' + str(tag_sequence) + 'sentence' + str(feat_obj.wmap[i]['words'])
            result.append({'predicted': tag_sequence, 'sentence': feat_obj.wmap[i]['words']})
        return result
    
    def p_y_given_x(self, xi, tag): # given xi determine the probability of y - note: we have all the f(x, y) values for all y in the dataset
        normalizer = 0.0
        feat = self.get_feats(xi, tag)
        dot_vector = numpy.dot(numpy.array(feat), self.model)
        for t in self.tag_set:
            feat = self.get_feats(xi, t)
            dp = numpy.dot(numpy.array(feat), self.model)
            if dp == 0:
                normalizer += 1.0
            else:
                normalizer += math.exp(dp)
        if dot_vector == 0:
            val = 1.0
        else:
            val = math.exp(dot_vector) # 
        result = float(val) / normalizer
        return result

    def classify(self, xi):
        if self.pic_file != None:
            self.model = pickle.load(open(self.pic_file, "rb"))
        maxval = 0.0
        result = None
        for t in self.tag_set:
            val = self.p_y_given_x(xi, t)
            if val >= maxval:
                maxval = val
                result = t
        return result

    def viterbi(self,words,history):
        self.pi = []
        self.back = []
        l = len(words)
        s = []
        tag_list = []
        s.append(['*'])
        #s.append(['*'])
        for i in range(0,len(words)):
            s.append(self.tag_set)
        self.pi.append({})
        self.back.append({})  
        self.pi.append({})
        self.back.append({})
        for i in range(0,len(words)):
            self.pi.append({})
            self.back.append({})
        self.pi[0]['*,*'] = 1
        """for i in self.tag_set:
            self.pi[1]['*,'+i]=1"""
        for k in range(0,len(words)):
            for u in s[k]:
                for v in s[k+1]:
                    max = 0
                    t = ""
                    inter_list = []
                    if( k == 0):
                        inter_list=['*']
                    else:
                        inter_list = s[k-1]
                    for w in inter_list:
                        l = self.pi[k][w + ',' + u] * self.p_y_given_x(history[k][0],v)
                        if l>max:
                            max=l
                            t = w
                    self.pi[k+1][u+','+v] = max;
                    self.back[k+1][u+','+v] = t
                    #tag_list.append(t)
        max_res = 0
        max_v = ""
        max_u = ""
        g = []
        f = []
        #print words
        if(len(words)==0):
            return []
        if(len(words)==1):
            g=['*']
            f=s[len(words)-1]
        else:
            g=s[len(words)-2]
            f=s[len(words)-1]
        for z in g:
            for y in f:
                tem = self.pi[len(words)-1][z+","+y]
                if tem> max_res:
                    max_res = tem
                    max_v = y
                    max_u = z
        tag_list.append(max_v)
        tag_list.append(max_u)
        prev_u = max_u #n-1
        prev_v = max_v #n
        if(len(words)>2):
            for i in range(len(words)-2)[::-1]:
                j = self.back[i+2][prev_u+","+prev_v]
                prev_v = prev_u
                prev_u = j
                tag_list.append(j)          
        return tag_list[::-1]


    def cost(self, params):
        self.model = params
        sum_sqr_params = sum([p * p for p in params]) # for regularization
        reg_term = 0.5 * self.reg * sum_sqr_params                
        dot_vector = numpy.dot(self.dataset, self.model)
        
        empirical = numpy.sum(dot_vector) # this is the emperical counts            
        expected = 0.0
        
        for j in range((self.num_examples)):
            mysum = 0.0
            for tag in self.tag_set: # get the jth example feature vector for each tag
                fx_yprime = self.all_data[tag][j] #self.get_feats(self.h_tuples[j][0], tag)
                '''
                dot_prod = 0.0
                for f in range(len(fx_yprime)):
                    if fx_yprime[f] != 0:
                        dot_prod += self.model[f]
                '''
                dot_prod = numpy.dot(fx_yprime, self.model)
                if dot_prod == 0:
                    mysum += 1.0
                else:
                    mysum += numpy.exp(dot_prod)
            expected += math.log(mysum)
        print "Cost = ", (expected - empirical + reg_term)
        return (expected - empirical + reg_term)

    def gradient(self, params):
        self.model = params        
        gradient = []
        for k in range(self.dim): # vk is a m dimensional vector
            reg_term = self.reg * params[k]
            empirical = 0.0
            expected = 0.0
            for dx in self.dataset:
                empirical += dx[k]
            for i in range(self.num_examples):
                mysum = 0.0 # exp value per example
                for t in self.tag_set: # for each tag compute the exp value
                    fx_yprime = self.all_data[t][i] #self.get_feats(self.h_tuples[i][0], t)

                    # --------------------------------------------------------
                    # computation of p_y_given_x
                    normalizer = 0.0
                    dot_vector = numpy.dot(numpy.array(fx_yprime), self.model)
                    for t1 in self.tag_set:
                        feat = self.all_data[t1][i]
                        dp = numpy.dot(numpy.array(feat), self.model)
                        if dp == 0:
                            normalizer += 1.0
                        else:
                            normalizer += math.exp(dp)
                    if dot_vector == 0:
                        val = 1.0
                    else:
                        val = math.exp(dot_vector) # 
                    prob = float(val) / normalizer
                    # --------------------------------------------------------
                    
                    mysum += prob * float(fx_yprime[k])                    
                expected += mysum
            gradient.append(expected - empirical + reg_term)
        return numpy.array(gradient)

if __name__ == "__main__":
    pass
