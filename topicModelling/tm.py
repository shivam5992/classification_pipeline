from gensim import corpora, models
from scrap import scrap
import csv 
import logging
from collections import Counter 
import operator
from textblob import TextBlob
import os 
from collections import Counter
import matplotlib.pyplot as plt
import math



class TopicModelling:
	def __init__(self):
		self.important_tags = ['JJ','NN','NNS','VB','VBD','VBG','VBN','VBP','VBZ']

	def tf(self, word, blob):
		return blob.words.count(word) / len(blob.words)

	def n_containing(self, word, bloblist):
		return sum(1 for blob in bloblist if word in blob.words)

	def idf(self, word, bloblist):
		return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

	def tfidf(self, word, blob, bloblist):
		return self.tf(word, blob) * self.idf(word, bloblist)


	def process(self, texts, config):
		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]
		ldamodel = models.ldamodel.LdaModel(corpus, config['num_of_topics'], id2word = dictionary, passes = config['passes'])
		results = ldamodel.print_topics(num_topics=config['num_of_topics'], num_words=config['topic_terms'])
		for topic in results:
			if topic.count("0.000") != config['topic_terms']:
				print topic

	def clean(self, text):
		c = scrap.remove_spaces(text)
		c = scrap.digit_free(c)
		c = scrap.punctuation_free(c)
		c = scrap.stopword_free(c)
		c = scrap.removeAlphanumerals(c)
		c = scrap.remove_short_words(c,2)
		c = scrap.lemmatize_sentence(c)
		c = c.lower()
		return c 


	def eda_params(self, counter_list, Category):
		topfive = len(counter_list) * 5 / 100

		frequencies = [x[1] for x in counter_list]
		total_sum = sum(frequencies)

		freq_count = dict(Counter(frequencies))
		sorted_x = sorted(freq_count.items(), key=operator.itemgetter(1), reverse = True)
		
		xx = [a[0] for a in sorted_x]
		yy = [a[1] for a in sorted_x]
		plt.bar(xx, yy)
		plt.show()

	def createBatches(self, l, n):
		"""Yield successive n-sized chunks from l."""
		for i in range(0, len(l), n):
			yield l[i:i+n]


	def prepare_data_files(self, listOfFilesNames, config):
		texts = []	
		compiled = []
		AvgWrdFrequencies = []
		bloblist = []
		for filename in listOfFilesNames:
			text = open(path+"/"+filename).read().strip()
			clean = self.clean(text)
			
			''' TF IDF '''			
			# bloblist.append(TextBlob(clean))
		
			words = clean.split()
			AvgWrdFrequencies.append(float(len(words) / len(set(words))))

			texts.append(words)
			compiled.extend(words)


		''' TF IDF '''
		# for i, blob in enumerate(bloblist):
		# 	scores = {}
		# 	for word in blob.words:
		# 		try:
		# 			scores[word] = self.tfidf(word, blob, bloblist)
		# 		except Exception as E:
		# 			print E 
		# 			continue
		# 	for x,y in scores.iteritems():
		# 		print x +"\t"+ str(y)
		''' TF IDF Ends '''


		''' Frequency Filter '''
		frequency_threshold = min(AvgWrdFrequencies)
		freq_count = dict(Counter(compiled))
		sorted_x = sorted(freq_count.items(), key=operator.itemgetter(1), reverse = True)
		sorted_x = [x[0] for x in sorted_x if x[1] > frequency_threshold]
		''' Frequency Filter Ends '''


		# self.eda_params(sorted_x, path.split("/")[-1])


		''' POS Tag Filter '''
		vocab = []
		for x in sorted_x:
			tag = TextBlob(x).tags[0][1]
			if tag in self.important_tags:
				vocab.append(x)

		refined = []
		for txt in texts:
			nl = [wrd for wrd in txt if wrd in vocab]
			refined.append(nl)
		''' POS Tag Filter Ends '''

		return refined

if __name__ == '__main__':
	tm = TopicModelling()

	config = {"num_of_topics" : 20,
			  "passes": 30, 
			  "topic_terms":10,
		      "batch_size":200, 
		      "batch_count" : 10,
		      "input_path":'/media/inno/01D04251141467101/WKData/icspipeline1'}
	
	relevant = ["060-Health insurance  or  insurers"]
	
	for folders in os.listdir(config['input_path']):
		if folders not in relevant:
			continue

		path = config['input_path']+"/"+folders
		files = os.listdir(path)


		# for file in files:
		# 	outpat = config['input_path'].replace("/icspipeline1","/clean/")+ file
		# 	fout = open(outpat,"w")
		# 	fout.write(tm.clean(open(path+"/"+file).read()))

		chunks = tm.createBatches(files, config['batch_size'])
					
		batch_index = 0
		for chunk in chunks:
			if batch_index == config['batch_count']:
				break
			batch_index += 1

			dataset = tm.prepare_data_files(chunk, config)
			print 
			print "Category : " + folders
			for key,val in config.iteritems():
				print key + " : " + str(val)
			print "Topics : "
			tm.process(dataset, config)
			print 
			print "-------------------------------------------------"