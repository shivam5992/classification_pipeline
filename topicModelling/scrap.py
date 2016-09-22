'''
	Complete package for python important functions
'''

import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import Levenshtein
import re, itertools
import operator


lmtzr = WordNetLemmatizer()
exclude = string.punctuation
stopwords = stopwords.words('english')
custom_stopwords = ['shall','statewide','average','first',"donot","section"]
timex = ['qtr',"monthly","year"]
stopwords.extend(custom_stopwords)
stopwords.extend(timex)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


class functions:

	def remove_encoded(self, line):
		line = str([line])
		patt = r"\\x[a-z0-9]{2}"
		line = re.sub(patt, "", line)
		line = UnicodeDammit(line)
		line = line.unicode_markup.encode('utf-8')[2:-2]
		return line

	def make_string_proper(self, line):
		line = ast.literal_eval(line)
		return line
	
	def destrip(self, line):
		return ' ' + line + ' '
	
	def remove_spaces(self, text):
		text = text.replace("\n"," ")
		text = text.replace("\t"," ")
		text = text.replace("\r"," ")
		text = " ".join(text.split())
		return text

	def generate_tokens(self, text):
		tokens = nltk.word_tokenize(text)
		return tokens

	def digit_free(self, text):
		text_list = text.split()
		text_list = [x for x in text_list if not x.isdigit()]
		text = " ".join(text_list)
		return text

	def punctuation_free(self, text):
		text = "".join([x for x in text if x not in exclude])
		return text

	def stopword_free(self, text):
		puncfree = self.punctuation_free(text)
		puncFree_words = puncfree.split()
		stopfree = [x for x in puncFree_words if x.lower() not in stopwords]
		stopfree_text = " ".join(stopfree)
		return stopfree_text


	def lemmatize_word(self, word):
		wrd = lmtzr.lemmatize(word,'v')
		if wrd == word:
			wrd = lmtzr.lemmatize(word,'n')
		return wrd


	def lemmatize_sentence(self, text):
		words = text.split()
		lemmed = []
		for wrd in words:
			wrd = self.punctuation_free(wrd)
			lem_words = self.lemmatize_word(wrd)
			lemmed.append(lem_words)
		lem_text = " ".join(lemmed)
		return lem_text


	def levenshtein_distance(self, s1, s2):
		return Levenshtein.distance(s1, s2)


	def split_attached_words(self, text):
		if len(text.split()) == 1 and not text.isupper():
			lis = re.findall('[A-Z][^A-Z]*', text)
			if len(lis) == 0:
				line = text
			else:
				line = " ".join(re.findall('[A-Z][^A-Z]*', text))
		else:
			newd = []
			for word in text.split():
				if not word.isupper():
					lis = re.findall('[A-Z][^A-Z]*', word)
					if len(lis) == 0:
						newd.append(word)
					else:
						newd.append(" ".join(lis))
				else:
					newd.append(word)
			line = " ".join(newd)
		return line


	def repeated_chars(self, text, level=2):
		text = ''.join(''.join(s)[:level] for _, s in itertools.groupby(text))
		return text


	def generate_ngrams(self, inp, n=2, islist = False):
		if not islist:
			inp = inp.split()
		output = []
		for i in range(len(inp)-n+1):
			output.append(inp[i:i+n])
		return output


	def sort_counter(self, adict, freq = False, rvrse = True):
		top = sorted(adict.items(),key=lambda(k,v):(v,k), reverse = rvrse)
		if freq:
			top = top[:freq]
		return top

	def split_into_sentences(self, text):
		sents = tokenizer.tokenize(text)
		return sents

	def removeAlphanumerals(self, text):
		rs = [wrd for wrd in text.split() if not any(dig in wrd for dig in "0123456789")]
		return " ".join(rs)	

	def remove_short_words(self, text, limit):
		rs = [wrd for wrd in text.split() if len(wrd)>limit ] 
		return " ".join(rs)	



	def sort_dict_value(self, y):
		sx = sorted(y.items(), key = operator.itemgetter(1))
		return sx

	def reform_json(line):
		line = line.replace(": true", ": True")
		line = line.replace(": false", ": False")
		line = line.replace(": null", ": None")
		return line

scrap = functions()