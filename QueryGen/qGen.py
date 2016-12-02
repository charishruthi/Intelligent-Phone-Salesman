from client import *
import re

query_ds = {}
query_ds["sentence"] = "What are the Memory specs of Samsung Galaxy ?"
query_ds["wordList"] = [('What','Other'),('are','Other'),('Memory','Feature'),('specs','Other'),('of','Other'),('Samsung','Org'),('Galaxy','Family')]
query_ds["relation"] = "feature_query"
                
supported_tags = ["Org","Family", "OS", "Version", "Price", "Phone", "Feature", "Other"]
supported_tags_phone = ["feature_query","price_query", "comparison", "interest_intent", "irrelevant"]
ner = NerClient("1PI11CS196", "g104")
status = True
def queryBuilder(trainedTuple):
	wordList = trainedTuple['wordList']
	sentence = trainedTuple['sentence']
	relation = trainedTuple['relation']
	products = []
	brands = []
	specs = []
	relevant = []
	for i in wordList:
		if(i[1] == "Org"):
			brands.append(i[0])
		elif(i[1] == "Family" or i[1] == "Phone"):
			products.append(i[0])			
	queryItems = {}	
	queryItems['brands'] = brands
	queryItems['products'] = products
	#queryItems['specs'] = specs
	ret = []
	specList = []
	global ner
	if ((len(products) > 0) and (len(brands) > 0)):
		ret = ner.get_products(brands[0],products[0])
		specList = ner.specsBuilder(brands,products)
	elif((len(products) < 0) and (len(brands) > 0)):
		ret = ner.get_products(brands[0])
		specList = ner.specsBuilder(brands,"")
	elif((len(brands)<0) and (len(products)>0)):
		ret = ner.get_products("",products[0])
		specList = ner.specsBuilder("",products)
	else:
		brands = ner.get_brands()
		#specList = specsBuilder(brands=brands,products=[])
		ret = []
		for i in brands:
			r1 = ner.get_products(i)
			for j in r1:
				ret.append(j)
		
	
	"""print "Specifications of device"
	for i in specList:
		print i"""		
	if relation == "price_query":
		price_range,status = price_query(wordList,sentence)	
		if(status != False):				
			queryItems['price_min'] = price_range[0]
			queryItems['price_max'] = price_range[1]
			relevant=[]
			for i in ret:
					if((i['dummy_price'] >= queryItems['price_min']) and (i['dummy_price'] <= queryItems['price_max'])):
						relevant.append(i)
		#print relevant
		return relevant
				#print relevant		
	elif relation == "feature_query":
		(features,isBooleanAns,status,message) = feature_query(wordList)
		#print "Length of features " + str(len(features))
		relevant = []
		if(len(features) > 0):	
			#print "Len fee" + str(features[0])			
			for i in features:
				new_Featlist = [x for x in specList.keys() if re.search(i, x)]
				#print len(new_Featlist)
				for i in new_Featlist:
					relevant.append(specList[i])
				new_Featlist = []
		return relevant

	elif relation == "comparison":
			pass
	elif relation == "interest_intent":
			pass
	elif relation == "irrelevant":
			pass
	return relevant

"""def price_query(wordList,sent):
	currency = ["Rs.","Rs","rupees","dollars","$","pounds","euros"]
	price_range = []
	if (("between" in sent) or (("lesser" in sent) and ("greater" in sent)) or (("above" in sent) and ("below" in sent)) or ((("less than" in sent) and ("more than" in sent)))):
		price = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		price_items= map(lambda x: int(x[0]),price)
		if(len(price_items)==2):
			price_range.append(min(price_items))
			print "Min" + str(min(price_items))
			price_range.append(max(price_items))
			print "Max " + str(max(price_items))
		else:
			global status
			status = False
	elif(("lesser" in sent) or ("below" in sent) or ("less than" in sent)):
		price_items = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		if(len(price_items)==1):
			price_range.append(0)
			price_range.append(int(price_items[0][0]))
		else:
			global status
			status = False
	elif(("greater" in sent) or ("more than" in sent) or ("above" in sent)):
		price_items = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		if(len(price_items)==1):
			price_range.append(int(price_items[0][0]))
			price_range.append(1000000)
		else:
			global status
			status = False
	else:
		global status 
		status = False
	return price_range"""


def price_query(wordList,sent):
	currency = ["Rs.","Rs","rupees","dollars","$","pounds","euros"]
	price_range = []
	status = True
	if (("between" in sent) or (("lesser" in sent) and ("greater" in sent)) or ((("less than" in sent) and ("more than" in sent)))):
		price = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		price_items=map(lambda x:int(x[0]),price)
		if(len(price_items)==2):	
			#print "these are price items: ",price_items
			price_range.append(min(price_items))
			price_range.append(max(price_items))
			#print price_range
		else:
                        status = False
	elif(("lesser" in sent) or ("less than" in sent)):
		price_items = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		#print "price items: ",price_items
                if(len(price_items)==1):
					price_range.append(0)
					price_range.append(int(price_items[0][0]))
                else:
                    status = False
	elif(("greater" in sent) or ("more than" in sent)):
		price_items = filter(lambda x:x[1]=="Price" and (x[0] not in currency),wordList)
		if(len(price_items)==1):
			price_range.append(int(price_items[0][0]))
			price_range.append(1000000)
		else:
			status = False
	return (price_range,status)

def feature_query(wordList):
	features=[]
	models=[]
	message=None
	status = True
	isBooleanAns=False
	i=0
	if (wordList[0][0]=='is' or wordList[0][0]=='was' or wordList[0][0]=='does'):
		isBooleanAns=True
	while i<len(wordList):
		if (wordList[i][1]=='Feature'):
			featureToAdd=""
			while i<(len(wordList)) and wordList[i][1]=='Feature':
				featureToAdd+=wordList[i][0]+" "
				i+=1
			featureToAdd=featureToAdd[:-1]
			features.append(featureToAdd)
		i+=1
	if (features==[]):
		status=False
		message='It\'ll be great if you could specify the feature you wish to know for a particular model'
	return (features,isBooleanAns,status,message)



#trainedTuple={'wordList':[('Apple','Org'),('iPhone','Family'),('should','Other'),('be','Other') ,('Camera','Feature') ,('enabled','Other') ],'sentence':"Apple iPhone should be Camera enabled",'relation':'feature_query'}
#rs = queryBuilder(query_ds)
#print rs
