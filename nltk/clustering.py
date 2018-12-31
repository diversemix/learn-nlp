import re
import json
import sys
from os import listdir
from os.path import isfile, join
from nltk.corpus import stopwords
from string import punctuation

n_clusters = int(sys.argv[1])
re_html = re.compile('<.*?>')
re_braces = re.compile('\(.*?\)')

def clean_text(raw_html):
    if type(raw_html) != str:
        print(type(raw_html))
        print(raw_html)
        raise "WTF"
    cleantext = re.sub(re_html, '', raw_html)
    cleantext = re.sub(re_braces, '', cleantext)
    return cleantext

def process_body(body, depth=0):
    text = ""
    for item in body:
        if type(item) == list:
            text += " " + process_body(item, depth+1)
        elif type(item) == dict and 'content' in item:
            text += " " + process_body(item['content'], depth+1)
        elif 'text' in item:
            if type(item['text']) == list:
                text += " " + process_body(item['text'], depth+1)
            else:
                text += " " + clean_text(item['text'])
    return text

def get_articles():
    corpus_path = "../elifesciences-corpus"
    articles = [join(corpus_path, f) for f in listdir(corpus_path) if f.endswith('json') and isfile(join(corpus_path, f))]

    articles_text = []
    for article in articles:
        with open(article) as f:
            text = ""
            try:
                data = json.load(f)
                text = process_body(data['body'])
            except ValueError as e:
                print(article, e)
            if len(text) > 0:
                articles_text.append(text)

    return articles_text


print("Loading articles...")
articles = get_articles()
print("Loaded {} articles.".format(len(articles)))

from sklearn.feature_extraction.text import TfidfVectorizer
print("Vectorizing...")
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
X = vectorizer.fit_transform(articles)

from sklearn.cluster import KMeans
print("Clustering... K={}".format(n_clusters))
km = KMeans(n_clusters=n_clusters,
            init='k-means++',
            max_iter=100,
            n_init=1,
            verbose=True)

print("Fitting K-Means...")
km.fit(X)

from numpy import unique
result = unique(km.labels_, return_counts=True)
print("Result of fit: {}".format(result))

print("Building entire text for each cluster...")
text = {}
total = len(km.labels_)
for i, cluster in enumerate(km.labels_):
    if (i % 100) == 0:
        print("    ...{}/{}".format(i, total))
    article = articles[i]
    if cluster not in text.keys():
        text[cluster] = article
    else:
        text[cluster] += " " + article

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest

print("Building stopwords...")
elife_stopwords = set(stopwords.words('english') +
    list(punctuation) +
    ['et', 'al', 'mm']
)

print("Get top words for each cluster...")
keywords = {}
counts = {}
words = {}

for cluster in range(n_clusters):
    print("    Cluster {}".format(cluster))

    words[cluster] = word_tokenize(text[cluster].lower())
    words[cluster] = [ word for word in words[cluster] if word not in elife_stopwords]
    freq = FreqDist(words[cluster])

    keywords[cluster] = nlargest(200, freq, key=freq.get)
    counts[cluster] = freq
    print("    - Unique Words: {}".format(len(set(words[cluster]))))
    print("    - Top Words: {}".format("\n     - ".join(keywords[cluster][:10])))

################################################################################
# Just to get: total_unqiue_words
################################################################################
total_words = set()
for cluster in range(n_clusters):
    total_words = total_words.union(words[cluster])
total_unqiue_words = len(total_words)
total_words = set()

print("Get words unqiue to each cluster...")
for cluster in range(n_clusters):
    print("    Cluster {}".format(cluster))
    other_clusters = list(set(range(n_clusters)) - set([cluster]))

    kw_in_other_clusters = set()
    words_in_other_clusters = set()
    for oc in other_clusters:
        kw_in_other_clusters = kw_in_other_clusters.union(keywords[oc])
        words_in_other_clusters = words_in_other_clusters.union(words[oc])

    unique_keywords = set(keywords[cluster]) - kw_in_other_clusters

    uniq_words = set(words[cluster]) - words_in_other_clusters
    print("    - Unique: {0} ({1:.2f}%)".format(len(uniq_words),
        round(100*len(uniq_words) / total_unqiue_words, 2)))

    inter_words = set(words[cluster]).intersection(words_in_other_clusters)
    print("    - Intersect: {0} ({1:.2f}%)".format(len(inter_words),
        round(100*len(inter_words) / total_unqiue_words, 2)))

    key_list = nlargest(20, unique_keywords, key=counts[cluster].get)
    str_list = "\n     - ".join(key_list)
    print("    - List: {}".format(str_list))
