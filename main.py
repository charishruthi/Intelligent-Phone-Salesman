import sys
sys.path.append("C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NER")
from ner_main import ner_tag
sys.path.append("C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/RER")
from rer_main import rer_tag
sys.path.append("C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/QueryGen")
from qGen import *
sys.path.append("C:/Users/admin/Documents/Studies/7th Sem/Natural Language Processing/SeeEvaluation/SEE/SEE/QueryGenerator/NLG")
from nlg import *

if __name__ == "__main__":
    print "System: Hello! How are you? How may I help you?"
    flag = 1
    while(flag):
        input_sentence = raw_input("Customer: ")
        #input_sentence = input_sentence.title()
        sent_word_list = input_sentence.split(" ")
        #for i in range(len(sent_word_list)):
            #sent_word_list[i][0]=sent_word_list[i][0].upper()
        if("Bye" in sent_word_list or "bye" in sent_word_list):
            print "Salesman: Thank you! It was nice talking to you!"
            flag = 0
        else:
            ner_res = ner_tag(input_sentence)
            ner_result = []
            for i in range(len(sent_word_list)):
                ner_result.append((sent_word_list[i],ner_res[0][i]))
            rer_result = rer_tag(input_sentence, ner_result)
            query_ds = {}
            query_ds["sentence"] = input_sentence
            query_ds["wordList"] = ner_result
            query_ds["relation"] = rer_result
            #print rer_result
            #print query_ds
            result = queryBuilder(query_ds)
            temp_dict = {}
            #print type(result)
            if(type(result)!="NoneType"):
                if(len(result)>0):
                    temp_dict["status"] = True
                    temp_dict["message"] = "default"
                    if(len(result)<4):
                        temp_dict["output"] = result
                    else:
                        temp_dict["output"] = result[0:4]
                    temp_dict["answer_type"] = "multiple"
                    temp_dict["relation"] = rer_result
                else:
                    temp_dict["status"] = False
                    temp_dict["message"] = "default"
                    temp_dict["output"] = result
                    temp_dict["answer_type"] = "multiple"
                    temp_dict["relation"] = rer_result
                convert(temp_dict)
            else:
               print "System: Sorry don't meet your requirements we think"