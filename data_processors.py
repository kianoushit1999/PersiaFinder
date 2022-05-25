import re
import math
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from num2fawords import words
from collections import Counter
from hazm import *

from handler import load_persian_stopwords, \
    get_all_files_path, remove_punctuation, convert_numbers

PERSIAN_STOPWORDS = load_persian_stopwords()

def fetch_data_per_path():
    #define variables
    processed_text = []
    processed_title = []
    dataframe = []
    document_number = 0

    for path in get_all_files_path():
        print(path)
        root = ET.parse(path).getroot()
        for doc_id, url_tag, html_body in zip(root.findall('DOC/DOCID'), root.findall('DOC/URL'),
                                              root.findall('DOC/HTML')):
            document_number += 1

            document_id = doc_id.text
            document_url = url_tag.text

            bs = BeautifulSoup(html_body.text, 'html5lib')
            title: str = bs.title.get_text() if(bs.title) is not None else ""

            stemmer = Stemmer()
            if(title != ""):
                title = re.sub(r'\<\!\-\-.*\-\-\>', ' ', title)
                title = re.sub(r'[a-zA-Z]', '', title)
                title = remove_punctuation(title)
                title = convert_numbers(title)
                title = re.sub(r'\s+', ' ', title)

                # natural language processing
                tokenized_words_title = word_tokenize(title)
                title_words = [stemmer.stem(word) for word in tokenized_words_title if
                               not word in set(PERSIAN_STOPWORDS)]
                title_words = ' '.join(title_words)
                title_words = remove_punctuation(title_words)
                title_words = convert_numbers(title_words)
            else:
                title_words = title

            body_content: BeautifulSoup = bs.body
            body_content = re.sub(r'\<\!\-\-.*\-\-\>', ' ', body_content.get_text())
            body_content = re.sub(r'[a-zA-Z]', '', body_content)
            body_content = remove_punctuation(body_content)
            body_content = convert_numbers(body_content)
            body_content = re.sub(r'\s+', ' ', body_content)

            # natural language processing
            tokenized_words_body = word_tokenize(body_content)
            body_words = [stemmer.stem(word) for word in tokenized_words_body if not word in set(PERSIAN_STOPWORDS)]
            body_words = ' '.join(body_words)

            # process through body
            body_words = remove_punctuation(body_words)
            body_words = convert_numbers(body_words)

            processed_text.append(body_words.split())
            processed_title.append(title_words.split())
            dataframe.append([document_id, document_url, title, body_content])

    return (
        document_number,
        processed_title,
        processed_text,
        dataframe
    )


def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

# TF-IDF Cosine Similarity Ranking
def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim

def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((N + 1) / (df + 1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q


def cosine_similarity(query):
    print("Cosine Similarity")
    query = re.sub(r'[a-zA-Z]', '', query)
    query = remove_punctuation(query)
    query = convert_numbers(query)
    preprocessed_query = re.sub(r'\s+', ' ', query)

    stemmer = Stemmer()
    tokenized_words_query = word_tokenize(preprocessed_query)
    tokens = [stemmer.stem(word) for word in tokenized_words_query if not word in set(PERSIAN_STOPWORDS)]

    print("\nQuery:", query)
    print("")
    print(tokens)

    d_cosines = []

    query_vector = gen_vector(tokens)

    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[:][::-1]

    return out

if __name__ == '__main__':

    document_number, processed_title, processed_text, dataframe = fetch_data_per_path()
    print("Enterd main .........")
    dataframe = pd.DataFrame(columns=("doc_id", "doc_url", "title", "body"), data=dataframe)

    N = document_number
    DF = {}
    for i in range(N):
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

        tokens = processed_title[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])
    # print(DF)

    total_vocab_size = len(DF)
    total_vocab = [x for x in DF]

    # TFIDF for body
    doc = 0
    tf_idf = {}
    for i in range(N):

        tokens = processed_text[i]

        counter = Counter(tokens + processed_title[i])
        words_count = len(tokens + processed_title[i])

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token)
            idf = np.log((N + 1) / (df + 1))
            tf_idf[doc, token] = tf * idf

        doc += 1

    # TFIDF for title
    doc = 0

    tf_idf_title = {}

    for i in range(N):

        tokens = processed_title[i]
        counter = Counter(tokens + processed_text[i])
        words_count = len(tokens + processed_text[i])

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token)
            idf = np.log((N + 1) / (df + 1))  # numerator is added 1 to avoid negative values
            tf_idf_title[doc, token] = tf * idf
        doc += 1

    print(tf_idf)
    # Merging the TF-IDF according to weights
    alpha = 0.3
    for i in tf_idf:
        tf_idf[i] *= alpha

    for i in tf_idf_title:
        tf_idf[i] = tf_idf_title[i]

    print(len(tf_idf))

    D = np.zeros((N, total_vocab_size), dtype='uint8')
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
        except:
            pass

    print("Ended vectorizing")
    Q = cosine_similarity("به سايت پرديس ابوريحان دانشگاه تهران")
    print(Q)
    print(dataframe.loc[Q[0], :].title)
    print(dataframe.loc[Q[1], :].title)
    print(dataframe.loc[Q[2], :].title)