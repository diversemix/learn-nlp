import urllib2
from bs4 import BeautifulSoup

#articleURL = "https://elifesciences.org/labs/5b56aff6/sciencebeam-using-computer-vision-to-extract-pdf-data"
articleURL = "https://elifesciences.org/articles/38519"

################################################################################
# Retrieve the page and extract the relevant elements from the HTML
################################################################################
page = urllib2.urlopen(articleURL).read().decode('utf8', 'ignore')
soup = BeautifulSoup(page, "lxml")
[s.extract() for s in soup('figure')]
[s.extract() for s in soup('a')]
# print(soup)

################################################################################
# Extract all the text from these elements
################################################################################
sections = soup.findAll("div", {"class": "article-section__body"})
text = ''.join([ sec.text for sec in sections])
text = text.encode('ascii', errors='replace').replace('?', ' ')
# print(text)

################################################################################
# Tokenize the sentences
################################################################################
from nltk.tokenize import word_tokenize, sent_tokenize
article_sentences = sent_tokenize(text)
article_words = word_tokenize(text.lower())

################################################################################
# Build a list of stopwords and remove them
################################################################################
from nltk.corpus import stopwords
from string import punctuation
customStopWords=set(stopwords.words('english')+list(punctuation))
article_words = [ word for word in article_words if word not in customStopWords]
# print(word_sent)

################################################################################
# Calculate word frequencies in the article
################################################################################
from nltk.probability import FreqDist
word_freq = FreqDist(article_words)

################################################################################
# Print the top words - just to take a look.
################################################################################
from heapq import nlargest
top = nlargest(20, word_freq, key=word_freq.get)
for j in top:
    print(j, word_freq[j])

################################################################################
# Score the sentences given the word frequencies.
################################################################################
from  collections import defaultdict
ranking = defaultdict(int)
for i, sentence in enumerate(article_sentences):
    for word in word_tokenize(sentence.lower()):
        if word in word_freq:
            ranking[i] += word_freq[word]

################################################################################
# Print out the top 10 sentences
################################################################################
sents_idx = nlargest(10, ranking, key=ranking.get)
for j in sorted(sents_idx):
    print("\n**** Sentence({}, {})\n{}".format(j, ranking[j], article_sentences[j]))

print("\nSUMMARY Words: {}, Sentences: {}".format(len(article_words),
        len(article_sentences)))