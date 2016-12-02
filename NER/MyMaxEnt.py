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

#from scipy.optimize import minimize as mymin 
#from scipy.optimize import fmin_l_bfgs_b as mymin 
import datetime

# ----------------------------------------------------------------------------------------
# maxent implementation
# ----------------------------------------------------------------------------------------
class MyMaxEnt(object):
    def __init__(self, function_obj, pic_file = None): 
        # history_tuples is of the form: ((ta, tb, wn, i), tag) where ta = tag t-2, tb = tag t-1, wn = pointer to a sentence, i = current index
        # function_list is of the form: [(pointer_to_function_f1, tag_for_f1), (pointer_to_function_f2, tag_for_f2)...]
        # reg_lambda = regularization coefficient
        # pic_file = Name of file where the classifier is pickled
        self.pic_file = pic_file
        self.tag_set = None
        self.model = None # this may be set by load_classifier or by train methods
        #self.model = numpy.array([0 for d in range(self.dim)]) # initialize the model to all 0        
        self.func = function_obj
        self.iteration = 0
        self.cb_count = 0
        self.cost_value = None
        return

    def load_classifier(self):
        if self.pic_file != None:
            data = pickle.load(open(self.pic_file, "rb"))
            self.model = data['model']
            self.tag_set = data['tag_set']
            #self.func = data['func']
        return        

    def create_dataset(self):
        self.dataset = []
        self.all_data = {}
        for h in self.h_tuples: # h represents each example x that we will convert to f(x, y)
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

    def cb(self, params):
        #print "cb count = ", self.cb_count
        self.cb_count += 1
        return

    def train(self, history_tuples, reg_lambda = 0.01):        
        # history_tuples, function_obj, reg_lambda = 0.01,
        self.iteration = 0
        self.h_tuples = history_tuples
        self.reg = reg_lambda
        self.dataset = None # this will be set by create_dataset
        self.tag_set = self.func.supported_tags #None # this will be also be set by create_dataset - this is the set of all tags
        self.create_dataset()
        self.dim = self.dataset.shape[1] #len(self.dataset[0])
        self.num_examples = self.dataset.shape[0]
        if (self.model == None) or (self.model.shape[0] != self.dim):
            self.model = numpy.array([0 for d in range(self.dim)]) # initialize the model to all 0
        #self.model = numpy.array([0 for d in range(self.dim)]) # initialize the model to all 0

        dt1 = datetime.datetime.now()                   
        #print 'before training: ', dt1
        try:
            from scipy.optimize import minimize as mymin
            params = mymin(self.cost, self.model, method = 'L-BFGS-B', callback = self.cb, options = {'maxiter':25}) #, jac = self.gradient) # , options = {'maxiter':100}
        except:
            #print "Importing alternate minimizer fmin_l_bfgs_b"
            from scipy.optimize import fmin_l_bfgs_b as mymin 
            params = mymin(self.cost, self.model, fprime = self.gradient) # , options = {'maxiter':100}
        
        self.model = params.x
        dt2 = datetime.datetime.now()
        #print 'after training: ', dt2, '  total time = ', (dt2 - dt1).total_seconds()
        
        if self.pic_file != None:
            pickle.dump({'model': self.model, 'tag_set': self.tag_set}, open(self.pic_file, "wb"))
        return self.cost_value

    def old_p_y_given_x(self, xi, tag): # given xi determine the probability of y - note: we have all the f(x, y) values for all y in the dataset
        #print 'TAGS = ', self.tag_set
        normalizer = 0.0
        feat = self.get_feats(xi, tag)
        #print "TAG = ", tag
        #print "Feats for ", tag, " = ", feat
        #for i in range(len(feat)):
            #print feat[i], self.model[i]
            
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
        #print 'dotv = ', dot_vector, ' norm = ', normalizer, ' val = ', val
        result = float(val) / normalizer
        return result

    def p_y_given_x(self, xi, tag): # given xi determine the probability of y - note: we have all the f(x, y) values for all y in the dataset
        #print 'TAGS = ', self.tag_set
        normalizer = 0.0
        feat = self.get_feats(xi, tag)
        #print "TAG = ", tag
        #print "Feats for ", tag, " = ", feat
        #for i in range(len(feat)):
            #print feat[i], self.model[i]
            
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
        #print 'dotv = ', dot_vector, ' norm = ', normalizer, ' val = ', val
        result = float(val) / normalizer
        return result


    def classify(self, xi):
        maxval = 0.0
        result = None
        for t in self.tag_set:
            val = self.p_y_given_x(xi, t)
            if val >= maxval:
                maxval = val
                result = t
        return result

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
                    try:
                        mysum += math.exp(dot_prod)
                    except:
                        pass
                        #print "dot_prod = ", dot_prod, " tag = ", tag, " f = ", fx_yprime, " m = ", self.model 
            expected += math.log(mysum)
        if (self.iteration % 100) == 0:
            pass
            #print "Iteration = ", self.iteration, "Cost = ", (expected - empirical + reg_term)
        self.iteration += 1
        self.cost_value = (expected - empirical + reg_term)
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
