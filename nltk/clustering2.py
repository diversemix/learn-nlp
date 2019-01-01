#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import collections
import re
import sys
import json


from os import listdir
from os.path import isfile, join

from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from pprint import pprint
from numpy import unique

MAX_ARTICLES = 10000

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
    print("Found {} files.".format(len(articles)))
    for article in articles:
        if len(articles_text) >= MAX_ARTICLES:
            break

        with open(article) as f:
            text = ""
            try:
                data = json.load(f)
                if 'body' in data:
                    text = process_body(data['body'])
            except ValueError as e:
                print(article, e)
            if len(text) > 0:
                articles_text.append(text)
    return articles_text


def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation
    """
    text = text.translate(string.punctuation)
    tokens = word_tokenize(text)

    if stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens


def cluster_texts(texts, clusters=3):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means
    """
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)

    print("Transforming...")
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters, verbose=True)
    print("Fitting...")
    km_model.fit(tfidf_model)

    clustering = collections.defaultdict(list)

    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    result = unique(km_model.labels_, return_counts=True)
    print("Result of fit: {}".format(result))

    return clustering


if __name__ == "__main__":
    articles = get_articles()
    print("Loaded {}".format(len(articles)))
    clusters = cluster_texts(articles, n_clusters)
    # pprint(dict(clusters))

