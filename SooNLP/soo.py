from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from icecream import ic
from pathlib2 import Path
import pdb
import numpy as np 
import nltk
import os

# Code taken from https://meenavyas.wordpress.com/2017/09/09/finding-similarity-between-text-documents/

considerations = []

# Create a function to open documents, and tokenize the words
def process(file):
	raw = open(file).read()
	tokens = word_tokenize(raw)
	words = [w.lower() for w in tokens]

	# porter will stem the words i.e. reducing them to root words. For example "making" becomes "make"
	porter = nltk.PorterStemmer()
	stemmed_tokens = [porter.stem(t) for t in words]

	# Remove stop words such as "a" "the" "and"
	# Removing HVAC related words like "on" and "off" from the stop_words set
	stop_words = set(stopwords.words('english')) - set(['on', 'off', 'above','below','until'])
	filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]

	# Count words
	count = nltk.defaultdict(int)
	for word in filtered_tokens:
		count[word] += 1
	return count

# Using numpy -- create a function which gives you the cosign similarity of two documents.
# This guy explains cosign similarity really well --> https://www.youtube.com/watch?v=Ze6A08Pw5oE
def cos_sim(a, b):
	dot_product = np.dot(a,b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	return dot_product / (norm_a * norm_b)

def get_Similarity(dict1,dict2):
	# Create a bag of words in the form of a list
	all_words_list = []
	# add all of the words from both documents to the list
	for key in dict1:
		all_words_list.append(key)
	for key in dict2:
		all_words_list.append(key)
	# get the length of the list
	all_words_list_size = len(all_words_list)
	# create two lists of all 0's that are the same length as your word list (bag of words)
	v1 = np.zeros(all_words_list_size,dtype=np.int)
	v2 = np.zeros(all_words_list_size,dtype=np.int)
	i = 0
	for (key) in all_words_list:
		v1[i] = dict1.get(key,0)
		v2[i] = dict2.get(key,0)
		i = i + 1
	return cos_sim(v1, v2)

hvac_abbreviations = [{'chw':'chilled water'},{'hhw':'heating hot water'}]

def replace_words(file):
	path = Path('new_sequence.txt')
	text = path.read_text()
	for i in hvac_abbreviations:
		for key, val in i.items():
			text = text.replace(key,val)
			path.write_text(text)
	

if __name__=='__main__':
	replace_words("new_sequence.txt")
	dict1 = process("new_sequence.txt")
	arr_txt = [x for x in os.listdir() if x.endswith(".txt")]
	for txt in range(0,len(arr_txt)):
		if arr_txt[txt] != "new_sequence.txt":
			replace_words(arr_txt[txt])
			dict2 = process(arr_txt[txt])
			similarity = get_Similarity(dict1,dict2) * 100
			ic(similarity)
			if similarity < 100:
				similarity = f"{similarity:.2f}"
				considerations.append({'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
			else:
				similarity = f"{similarity:.2f}"
				considerations.insert(0,{'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
considerations_sorted = sorted(considerations, key = lambda i: i['Similarity'],reverse=True)
print('Here is a list of sequences which are somewhat similar to yours:')
for consideration in considerations_sorted:
    print(consideration)