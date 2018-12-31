# coding: utf-8
import nltk
print("\n---- Tokenizing...")
from nltk.tokenize import word_tokenize, sent_tokenize
text = "Mary had a little lamb. Her fleece was white as snow."
sents = sent_tokenize(text)
words = [word_tokenize(sent) for sent in sents]
print(text)
print("In sentences: ", sents)
print("In words: ", words)

print("\n---- StopWords...")
from nltk.corpus import stopwords
from string import punctuation
customStopWords=set(stopwords.words('english')+list(punctuation))
wordsWOStopwords=[word for word in word_tokenize(text) if word not in customStopWords]
print("Without stopwords: ", wordsWOStopwords)


print("\n---- Bi-grams...")
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordsWOStopwords)
bigrams = sorted(finder.ngram_fd.items())
print(bigrams)


print("\n---- Stemming...")
from nltk.stem.lancaster import LancasterStemmer
text2 = "Mary closed on the closing night close to when she was in the mood to close."
st = LancasterStemmer()
stemmedWords = [ st.stem(word) for word in word_tokenize(text2)]
print(text2)
print("Stemmed words: ", stemmedWords)


print("\n---- Tokenizing...")
tokens = nltk.pos_tag(word_tokenize(text2))
print(tokens)

print("\n---- Definitions of 'bass'...")
from nltk.corpus import wordnet as wn
for ss in wn.synsets('bass'):
    print(ss, ss.definition())


print("\n---- Sense of words...")
from nltk.wsd import lesk
sent1 = "Sing in a lower tone, along with the bass"
sense1 = lesk(word_tokenize(sent1), "bass")

print (sent1)
print (sense1, sense1.definition())

sent2 = "The sea bass was really hard to catch"
sense2 = lesk(word_tokenize(sent2), "bass")
print (sent2)
print (sense2, sense2.definition())
