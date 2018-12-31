# NLTK Notes

Taken from the [Pluralisght course](https://app.pluralsight.com/player?course=python-natural-language-processing&author=swetha-kolalapudi&name=python-natural-language-processing-m1&clip=0&mode=live)

Three sections:

- Getting Started
- Auto Summarizing Text
- Classification using Machine Learning

## Getting Started

Applications in document processing:

- summarising
- genre classification
- themes / topics

Tasks:

- Tokenization - breaking down words and sentances.
- Stopword Removal - removing words that don't help meaning.
- N-Grams - groups of words
- Word Sense Disambiguation - example "cool"
- Parts-of-speech Tagging - Noun, Verb, etc
- Stemming, same meaning different endings.

### machine-learning
Used when:

- difficult to express in terms of rules
- a large amount of historical data is available
- patterns and relationships are dynamic

Typical ML workflow:

- Identify which type of problem - classifying and clustering
- Represent Data using numeric attributes - TF / IDF (frequency analysis)
- Use a standard algorithm to find a model
    - Classification => Naive Bayes, Support Vector Machines
    - Clustering => K-Means, Hierarchical Clustering

## Auto-Summarizing

- Find the important words - based on frequency
- Define a significance score - score each sentance
- Rank them and pick the top 'n'

Tasks to perform:

- Retrieve html from webpage and extract text
- Pre-Process by tokenizing into sentences, tokenise words and remove stopwords
- Extract sentences, compute frequences of words and compute the significance score of each sentence, ranks and pick the top 'N'

Most of the notes are enshirened in two files:

- getting-started.py
- summarizing.py

## Classification using Machine Learning

Identifying themes....

- Need a large corpus of articles
- Need to break these into themes (classifications)
- This allows a new article to be classified by the model.

The demo that follows is primarily detailing how to get text from a blog site - going to use elifesciences.org articles so we don't need to do this.

Clustering - a solution to the problem of how to create groups based on similarities.

- Maximise intra-cluster similarities.
- Minimize inter-cluster similarities.

On to the machine learning part of picking features and creating a model.

### Term Frequency - TF-IDF

- Create a list of words in the entire corupus
- Generate a frequency of word occurances in an article given this list of words. This is the the "Term Frequency Representation" (these are the features) - "Bag of Words" model as just a collection of words
- Some words differentiate a document - these are the rarity of the word.
- The weighting of is the inverse of the document frequency (IDF):

 Weight = 1 / (No. of documents the word appears in)

- Now apply the standard "K-Means Custering" algorithm
- N-Dimensional matricies
- K = the number of clusters
- Start by initialising the K centroids.
- Cluster based on these centroids.
- Re-define the centroids as the centre of the clusters and repeat

Note to Self: This was done by Colin (RSC) showed in slides - see if I cen get them.

So this was done in the course by using the blog site's posts.
K=3 and the main amount of work was then trying to figure out what were the words (features) that were unique to these clusters.
This was done by finding the top words unique words in each cluster.

### Classification

The final part of this is to assign a theme (classification) to a new article.
This in itself is a new ML problem of `classification`

- Problem Statement
- Features (these come from the TF-IDF step)
- Training
- Test
