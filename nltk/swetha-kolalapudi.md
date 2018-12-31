
# Getting Started

## nltk

Mostly from the [Pluralisght course](https://app.pluralsight.com/player?course=python-natural-language-processing&author=swetha-kolalapudi&name=python-natural-language-processing-m1&clip=0&mode=live)

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

## machine-learning
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

# Auto-Summarizing

- Find the important words - based on frequency
- Define a significance score - score each sentance
- Rank them and pick the top 'n'

Tasks to perform:

- Retrieve html from webpage and extract text
- Pre-Process by tokenizing into sentences, tokenise words and remove stopwords
- Extract sentences, compute frequences of words and compute the significance score of each sentence, ranks and pick the top 'N'
