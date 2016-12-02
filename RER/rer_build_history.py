import nltk
from nltk.tag import pos_tag
from nltk.corpus import conll2000


def build_history(data_list, supported_tags_phones,supported_tags):
	history_list = [] # list of all histories
	sents = []
	count = 0
	expected = []

	for data in data_list: # data is the inputs entered by a given student
		data1 = data['data']

		#data1 is for every sentence entered by user
		for rec in data1:
			updates = rec['updates']
			sent = rec['sentence']  
			relatedTags=[]
			relations=[]
			if "rels" in rec.keys():
				relatedEntities = rec['rels']   
				expected.append(relatedEntities)            
				for i in relatedEntities:
					relations.append(i.keys())
					for j in i[i.keys()[0]]:
						relatedTags.append(j)
			words = []
			posTaggedSent = postagger(sent)
			#chunkPhrases = chunker(sent)

			
			if len(updates) == len(posTaggedSent):
				for i in range(len(updates)):               
					words.append({"word":updates[i]['word'],"pos":posTaggedSent[i],"tag":updates[i]['tag']})
					#------------------------------------------------------------------------------------------------
					# NOTE: below code is a temporary hack to build the MAxEnt for just 2 tags - we will change this later
					if (updates[i]['tag'] not in supported_tags_phones):
						if updates[i]['tag'] == "Model":
							updates[i]['tag'] = "Version"
						else:
							updates[i]['tag'] = "Other"                
					#------------------------------------------------------------------------------------------------

			sents.append(words)
			history={}
			history['sentence'] = words
			history['i'] = count+1
			#history['phrases'] = chunkPhrases
			history['relatedTags'] = relatedTags
			if len(relations) > 0:
				history_list.append((history,relations[0][0],))
			else:
				history_list.append((history,"None",))
			count += 1


	return (history_list,sents,expected)

def postagger(sent):
	text = nltk.word_tokenize(sent)
	posTagged = pos_tag(text)
	#simplifiedTags = [map_tag('en-ptb', 'universal', tag) for word, tag in posTagged]
	return posTagged

def chunker(sent):

#a = [("I","PRP"),("hear","VBP"),("Jerusalem","NNP"),("bells","NNS"),("ringing","VBG")]
#input_sent = " Rockwell said the agreement calls for it to supply 200 addititonal so-called shipsets for the planes."
	input_sent = sent 
	text = nltk.word_tokenize(input_sent)
	a = nltk.pos_tag(text)
	phrases = []

	tup = ()
	'''test_sents = conll2000.chunked_sents('test.txt', chunk_types=['VP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types=['VP'])
	test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])'''
	NP_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
	VP_sents = conll2000.chunked_sents('train.txt', chunk_types=['VP'])
	class ChunkParser(nltk.ChunkParserI):
		def __init__(self, train_sents):
			train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
			self.tagger = nltk.TrigramTagger(train_data)
		def parse(self, sentence):
			pos_tags = [pos for (word,pos) in sentence]
			tagged_pos_tags = self.tagger.tag(pos_tags)
			chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
			conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
			return nltk.chunk.util.conlltags2tree(conlltags)

	NPChunker = ChunkParser(NP_sents)
	VPChunker = ChunkParser(VP_sents)
	#print (NPChunker.parse("I hear Jerusalem bells ringing"))
	parsed_sent = NPChunker.parse(a)
	for i in parsed_sent:
		if (type(i)!=type(tup)):
			l=[]
			for t in tuple(i):
				l.append(t[0])
			phrases.append({"NP":" ".join(l)})
	parsed_sent = VPChunker.parse(a)
	for i in parsed_sent:
			if (type(i)!=type(tup)):
				l=[]
				for t in tuple(i):
					l.append(t[0])
				phrases.append({"VP":" ".join(l)})
	return phrases


