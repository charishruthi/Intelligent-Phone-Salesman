import random
input_ds = {"output":[{"product":"Galaxy","brand":"Samsung","dummy_price":10000},{"product":"IPhone","brand":"Apple","dummy_price":20000}],"status":True,"message":"","relation":"price_query","answer_type":"multiple"}
statement = ""
single_response = "May we suggest the phone <phone> which matches your requirements?"
prefixes = ["You're in luck! We have the following options!","We have a variety pf choices that will cater to your requirements.","We have some suggestions for you."]
main_response = "<prefix>\n<output>"

def convert(input_ds):
	if(input_ds["status"] == True):
		if(input_ds["relation"] == "price_query"):
			if(input_ds["answer_type"]=="boolean"):
				print (input_ds["message"])
			else:
				if(len(input_ds["output"])>1):
					st = ""
					if(len(input_ds["output"])==2):
						st += "Would you like to see "
						prefix = "You're in luck! We have the following options!"
					else:
						index = random.randint(0,2)
						prefix = prefixes[index]
					response = main_response
					response=response.replace("<prefix>",prefix)
					products = map(lambda x:"\n\t"+x['brand']+" "+x['product'],input_ds['output'])
					if(len(input_ds["output"])==2):
						output_response = st+products[0]+" or "+products[1]
					else:
						output_response = reduce(lambda x,y:x+"\n"+y,products)
					response=response.replace("<output>",output_response)
					print "System: "+response

		elif(input_ds["relation"] == "feature_query"):
			if(input_ds["answer_type"]=="boolean"):
				print (input_ds["message"])
			else:
				if(len(input_ds["output"])>1):
					st = ""
					if(len(input_ds["output"])==2):
						st += "Would you like to see "
						prefix = "You're in luck! We have the following options!"
					else:
						index = random.randint(0,2)
						prefix = prefixes[index]
					response = main_response
					response=response.replace("<prefix>",prefix)
					products = map(lambda x:x['brand']+" "+x['product']+"\n\tFeatures: "+x["feature"]+"\n\tValue: "+x["value"],input_ds['output'])
					if(len(input_ds["output"])==2):
						output_response = st+products[0]+" or "+products[1]
					else:
						output_response = reduce(lambda x,y:x+"\n"+y,products)
					response=response.replace("<output>",output_response)
					print "System: "+response
		elif(input_ds["relation"] == "intent_interest"):
			print "System: Sorry Intent_Interest not yet supported"
		elif(input_ds["relation"] == "irrelevant"):
			print "I'm sorry, what phones are you interested in?"
		elif(input_ds["relation"] == "comparison"):
			print "System: Sorry comparison not yet supported"
		elif(input_ds["relation"] == "agreement"):
			print "Thank you!"
		elif(input_ds["relation"] == "disagreement"):
			print "I'm sorry, would you please present your requirements again?"
		elif(input_ds["relation"] == "acknowledgement"):
			print "Thank you!"
		elif(input_ds["relation"] == "greeting"):
			print "Hello!"
		else:
			pass
	else:
		pass