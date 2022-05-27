import re

from hazm import Stemmer, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data_processors import fetch_data_per_path
from handler import remove_punctuation, convert_numbers, load_persian_stopwords
from mongodb_handler import fetch_processed_texts, fetch_processed_title

PERSIAN_STOPWORDS = []
processed_text = []
processed_title = []

def prepare_engine():
    global PERSIAN_STOPWORDS, processed_text, processed_title
    processed_text = fetch_processed_texts()
    processed_title = fetch_processed_title()
    PERSIAN_STOPWORDS = load_persian_stopwords()

    print(processed_title)


def query_handler(Q):
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

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer_body = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([Q_words, *processed_title])
    tfidf_matrix_body = tfidf_vectorizer_body.fit_transform([Q_words, *processed_text])

    print("for title")
    cosine_sim_title = cosine_similarity(tfidf_matrix, tfidf_matrix)[0, 1:] * 0.75
    print(cosine_sim_title)
    print("for body")
    cosine_sim_body = cosine_similarity(tfidf_matrix_body, tfidf_matrix_body)[0, 1:] * 0.25
    print(cosine_sim_body)

    print("result")
    total_cosine = (cosine_sim_title + cosine_sim_body)

    return sorted(range(len(total_cosine)), key=total_cosine.__getitem__)[::-1]
