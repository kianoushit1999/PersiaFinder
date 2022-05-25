import re
import numpy as np
from collections import Counter
import math
from hazm import *
from data_processors import doc_freq
from handler import remove_punctuation, convert_numbers, load_persian_stopwords
from mongodb_handler import fetch_general_info, find_by_doc, fetch_dataframe_by_doc_id

N = 0
total_vocab = []
total_vocab_size = 0
DF = {}

PERSIAN_STOPWORDS = load_persian_stopwords()

def initializer_constraint():
    global DF, N, total_vocab, total_vocab_size
    N, total_vocab_size, total_vocab, DF = fetch_general_info()

# TF-IDF Cosine Similarity Ranking
def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim

def gen_vector(tokens):
    global total_vocab, DF, N
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token, DF)
        idf = math.log((N + 1) / (df + 1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q


def cosine_similarity(query):
    global N, total_vocab_size
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
    print(len(query_vector))
    print(find_by_doc(0))
    for counter in range(N):
        D = np.zeros((1, total_vocab_size))
        for doc_id, tfidf in find_by_doc(counter):
            D[0][doc_id] = tfidf
        print(len(D), len(query_vector))
        d_cosines.append(cosine_sim(query_vector, D[0]))

    out = np.array(d_cosines).argsort()[:][::-1]

    return out

def execute_query(query):
    print("Ended vectorizing")
    Q = cosine_similarity(query)
    return Q

if __name__ == '__main__':
    initializer_constraint()
    doc_id_list = execute_query("به سايت پرديس ابوريحان دانشگاه تهران خوش آمديد")
    print(doc_id_list)
    for id in doc_id_list:
        print(fetch_dataframe_by_doc_id(int(id)))