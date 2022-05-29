import re
from time import time

from hazm import Stemmer, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from handler import remove_punctuation, convert_numbers, load_persian_stopwords
from mongodb_handler import fetch_processed_texts, fetch_processed_title

PERSIAN_STOPWORDS = []
processed_text = []
processed_title = []

tfidf_title = None
tfidf_body = None
queryTFIDF_title = None
queryTFIDF_body = None


def prepare_engine():
    global PERSIAN_STOPWORDS, processed_text, processed_title, tfidf_title, tfidf_body,\
        queryTFIDF_body, queryTFIDF_title
    processed_text = fetch_processed_texts()
    processed_title = fetch_processed_title()
    PERSIAN_STOPWORDS = load_persian_stopwords()

    tfidf_title = TfidfVectorizer().fit_transform(processed_title)
    tfidf_body = TfidfVectorizer().fit_transform(processed_text)
    # for query
    queryTFIDF_title = TfidfVectorizer().fit(processed_title)
    queryTFIDF_body = TfidfVectorizer().fit(processed_text)


def query_handler(Q):
    global tfidf_title, tfidf_body, queryTFIDF_body, queryTFIDF_title
    Q = re.sub(r'[a-zA-Z]', '', Q)
    Q = remove_punctuation(Q)
    Q = convert_numbers(Q)
    Q = re.sub(r'\s+', ' ', Q)

    stemmer = Stemmer()
    tokenized_words_Q = word_tokenize(Q)
    Q_words = [stemmer.stem(word) for word in tokenized_words_Q if
               not word in set(PERSIAN_STOPWORDS)]
    Q_words = ' '.join(Q_words)
    Q_words = remove_punctuation(Q_words)
    Q_words = convert_numbers(Q_words)

    queryTFIDF_matrix_title = queryTFIDF_title.transform([Q_words])
    queryTFIDF_matrix_body = queryTFIDF_body.transform([Q_words])

    cosine_sim_title = cosine_similarity(queryTFIDF_matrix_title, tfidf_title) * 0.75
    cosine_sim_body = cosine_similarity(queryTFIDF_matrix_body, tfidf_body) * 0.25

    total_cosine = (cosine_sim_title + cosine_sim_body)[0, :]
    print(sorted(range(len(total_cosine)), key=total_cosine.__getitem__)[::-1])
    return sorted(range(len(total_cosine)), key=total_cosine.__getitem__)[::-1]
