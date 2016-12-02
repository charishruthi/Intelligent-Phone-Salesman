'''
memm.py
MaxEnt Markov Model Tagger
Author: Anantharaman Narayana Iyer
Date: 22 Nov 2014
'''
import pickle
import datetime
from MyMaxEnt import MyMaxEnt
# ----------------------------------------------------------------------------------------
# maxent implementation
# ----------------------------------------------------------------------------------------
class Memm(MyMaxEnt):
    #def __init__(self, history_list, func_obj, reg_lambda = 0.001, pic_file = None): 
    def __init__(self, func_obj, pic_file = None): 
        # MEMM inherits from maxent classifier class and so has access to all the class attributes
        # NOTE: The supported tags are taken from maxent.tag_set
        #super(Memm, self).__init__(history_list, func_obj, reg_lambda, pic_file)
        super(Memm, self).__init__(func_obj, pic_file)
        #self.sk_set = [["*"], self.tag_set] # Sk-1 for k = 1 is * for every other k it is full tag set
        self.pi = {}
        self.bp = {}
        self.pi[-1] ={
                "*": {
                    "*": 1.0
                    }
            }
        self.bp[-1] = {
                "*": {
                    "*": "*"
                    }
            }
        return

    def tagold(self, sents):
        result = []
        self.func.set_wmap(sents) #set the map for the given sentence to be tagged
        for sent in sents:
            result.append(self.tagw(sent, sents.index(sent)))
        return result


    def tag(self, sents):
        result = []
        self.func.set_wmap(sents) #set the map for the given sentence to be tagged
        #print "len of sents in memm = ", len(sents)
        for i in xrange(len(sents)):
            result.append(self.tagw(sents[i], i))
        return result    
    
    def oldtagw(self, words, sindex): # given the sentence as a set of word tokens tag it
        #print 'Tagging: ', words
        
        if (self.tag_set == None) or (self.model == None):
            #print "The classifier model or tag_set is None"
            return
        self.sk_set = [["*"], self.tag_set] # Sk-1 for k = 1 is * for every other k it is full tag set        
        #self.func.set_wmap(words) #set the map for the given sentence to be tagged
        mybp = []
        tn = None
        tn_1 = None
        for k in range(0, len(words)):
            sk_1 = self.sk_set[int((k) > 0)]
            sk = self.sk_set[1]
            sk_2 = self.sk_set[int((k-1) > 0)]
            self.pi[k] = {}
            self.bp[k] = {}            
            #print "sk1 = ", sk_1, "  sk_2 = ", sk_2, "  sk = ", sk
            for u in sk_1:
                self.pi[k][u] = {}
                self.bp[k][u] = {}
                for v in sk:
                    temp_pi = []
                    temp_bp = []
                    for t in sk_2:
                        #print "Computing pi[%s, %s, %s]" % (k, u, v)
                        #print "k-1, t, u: ", k - 1, t, u
                        #hk = {'tb': t, "ta": u, "wn": sindex, "i": k }
                        hk = {'ta': t, "tb": u, "wn": sindex, "i": k }
                        prob = self.p_y_given_x(hk, v)
                        #print "Tagging: ", words[k], "  his = ", hk, "  p_y_given_x is: ", prob, "  for the tag: ", v
                        #print "pi[k-1, t, u] = ", self.pi[k-1][t][u]
                        prob = self.pi[k-1][t][u] * prob                        
                        #print "hk: ", hk, " prob = ", prob, " pi[k-1, t, u] = ", self.pi[k-1][t][u], "  v = ", v
                        temp_pi.append(prob)
                    val = max(temp_pi)
                    argmax_t = sk_2[temp_pi.index(val)]
                    self.pi[k][u][v] = val
                    self.bp[k][u][v] = argmax_t
                    #print "temp_pi = ", temp_pi
                    #print 'Assigning pi[%d][%s][%s] to %f' % (k, u, v, val)
        result = []
        out = self.pi[len(words) - 1] # this is pi(n) - we now need to see which (u, v) maximized this
        mymax = 0.0
        for k, v in out.items():
            for k1, v1 in v.items():
                #print k, k1, v1
                if v1 > mymax:
                    mymax = v1
                    tn = k1
                    tn_1 = k
        result.append(tn)
        result.append(tn_1)
        for k in xrange(len(words) - 3, -1, -1):
            t = (self.bp[k+2][tn_1][tn])
            tn = tn_1
            tn_1 = t
            result.append(t)
        return result[::-1]
    
    
    def tagw(self, words, sindex): # given the sentence as a set of word tokens tag it
        #print 'Tagging: ', words
        
        if (self.tag_set == None) or (self.model == None):
            return
            #print "The classifier model or tag_set is None"
        self.sk_set = [["*"], self.tag_set] # Sk-1 for k = 1 is * for every other k it is full tag set        
        #self.func.set_wmap(words) #set the map for the given sentence to be tagged
        mybp = []
        tn = None
        tn_1 = None
        for k in range(0, len(words)):
            sk_1 = self.sk_set[int((k) > 0)]
            sk = self.sk_set[1]
            sk_2 = self.sk_set[int((k-1) > 0)]
            self.pi[k] = {}
            self.bp[k] = {}            
            #print "sk1 = ", sk_1, "  sk_2 = ", sk_2, "  sk = ", sk
            for u in sk_1:
                self.pi[k][u] = {}
                self.bp[k][u] = {}
                for v in sk:
                    temp_pi = []
                    temp_bp = []
                    for t in sk_2:
                        #print "Computing pi[%s, %s, %s]" % (k, u, v)
                        #print "k-1, t, u: ", k - 1, t, u
                        #hk = {'tb': t, "ta": u, "wn": sindex, "i": k }
                        hk = {'ta': t, "tb": u, "wn": sindex, "i": k }
                        prob = self.p_y_given_x(hk, v)
                        #print "Tagging: ", words[k], "  his = ", hk, "  p_y_given_x is: ", prob, "  for the tag: ", v
                        #print "pi[k-1, t, u] = ", self.pi[k-1][t][u]
                        prob = self.pi[k-1][t][u] * prob                        
                        #print "hk: ", hk, " prob = ", prob, " pi[k-1, t, u] = ", self.pi[k-1][t][u], "  v = ", v
                        temp_pi.append(prob)
                    val = max(temp_pi)
                    argmax_t = sk_2[temp_pi.index(val)]
                    self.pi[k][u][v] = val
                    self.bp[k][u][v] = argmax_t
                    #print "temp_pi = ", temp_pi
                    #print 'Assigning pi[%d][%s][%s] to %f' % (k, u, v, val)
        result = []
        out = self.pi[len(words) - 1] # this is pi(n) - we now need to see which (u, v) maximized this
        mymax = 0.0
        for k, v in out.items():
            for k1, v1 in v.items():
                #print k, k1, v1
                if v1 > mymax:
                    mymax = v1
                    tn = k1
                    tn_1 = k
        result.append(tn)
        result.append(tn_1)
        for k in xrange(len(words) - 3, -1, -1):
            t = (self.bp[k+2][tn_1][tn])
            tn = tn_1
            tn_1 = t
            result.append(t)
        return result[::-1]
            

if __name__ == "__main__":
    mx = Memm()
