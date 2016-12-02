import nltk
def build_history(data_list, supported_tags):
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
                    if updates[i]['tag'] == "Model" :
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
