from rer_build_history import *
from rer_feature_functions import *
from rer_MyMaxEnt import *
from rer_metrics import *
import json


def rer_tag(sent, ner_result):
    json_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/RER/rer_all_data.json"
    pickle_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/RER/rer_all_data.p"
    word_list = sent.split(" ")
    relatedTags = []
    words = []
    for i in ner_result:
        words.append({"word":i[0],"tag":i[1]})
        if(i[1]!="Other"):
            relatedTags.append(i[1])

    history_input={}
    history_input['sentence'] = words
    history_input['i'] = 1
    history_input['relatedTags'] = relatedTags
            
    #TRAIN = int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
    TRAIN = 0
    supported_tags_phones = ["Org","Family", "OS", "Version", "Phone", "Feature", "Other"]
    supported_tags = ["feature_query","price_query", "comparison", "interest_intent", "irrelevant"]# "Phone", "Feature", "Other"]
    data = json.loads(open(json_file).read())['root']
    #print "num stu = ", len(data)
    #(history_list, wmap) = build_history(data, supported_tags)
    (history_list, sents, expected, ) = build_history(data, supported_tags_phones, supported_tags)
    #print "After RER build_history"
    func_obj = FeatureFunctions(sents, supported_tags)
    clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
    if TRAIN == 1:
        clf.train()
    input_sent = []
    input_sent.append(words)
    func_obj.set_wmap(sent.split(" "))
    result = clf.classify_sent(func_obj, history_input)
    return result




if __name__ == "__main__":
        #----- REPLACE THESE PATHS FOR YOUR SYSTEM ---------------------
        json_file = r"rer_all_data.json"
        pickle_file = r"C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/RER/rer_all_data.p"

        TRAIN = int(raw_input("Enter 1 for Train, 0 to use pickeled file:  "))
        supported_tags_phones = ["Org","Family", "OS", "Version", "Phone", "Feature", "Other"]
        supported_tags = ["feature_query","price_query", "comparison", "interest_intent", "irrelevant"]# "Phone", "Feature", "Other"]

        """tag_set = {"Org": 0, "Other": 1}
        dims = 9
        trg_data_x = []
        trg_data_y = []
        trg_data = {'Org': [], 'Other': []}"""
        data = json.loads(open(json_file).read())['root']
        print "num stu = ", len(data)
        #(history_list, wmap) = build_history(data, supported_tags)
        (history_list, sents, expected, ) = build_history(data, supported_tags_phones, supported_tags)
        print "After build_history"
        func_obj = FeatureFunctions(sents, supported_tags)
        clf = MyMaxEnt(history_list, func_obj, reg_lambda = 0.001, pic_file = pickle_file)
        if TRAIN == 1:
                clf.train()
        result = clf.test(func_obj, history_list[-100:])
        expected_list = []
        input_sent = []
        expected_tags = []
        for r in result:
                print  r['predicted'], r['expected']
                input_sent.append(r['predicted'])
                expected_tags.append(r['expected'])
        rer_metrics = NerMetrics(input_sent, expected_tags)
        met = rer_metrics.compute()
        print met
        """result_viterbi = clf.test_viterbi(func_obj, history_list)
        for r in result_viterbi:
                print "Sentence: "+str(r['sentence'])+"\n"+"Predicited: "+str(r['predicted'])+"\n"+"Expected: "+str(expected_list)+"\n\n"
    """            

