import re
import xml.etree.ElementTree as ET
import time
import numpy as np
from bs4 import BeautifulSoup
from hazm import *
from handler import load_persian_stopwords, \
    get_all_files_path, remove_punctuation, convert_numbers
from mongodb_handler import insert_dataframe, processed_text, processed_title, fetch_processed_title, \
    fetch_processed_texts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

PERSIAN_STOPWORDS = load_persian_stopwords()

def fetch_data_per_path():
    # define variables
    document_number = 0

    word_counter = 0
    for path in get_all_files_path():
        print(path)
        root = ET.parse(path).getroot()
        for doc_id, url_tag, html_body in zip(root.findall('DOC/DOCID'), root.findall('DOC/URL'),
                                              root.findall('DOC/HTML')):
            document_id = doc_id.text
            document_url = url_tag.text

            bs = BeautifulSoup(html_body.text, 'html5lib')
            title: str = bs.title.get_text() if (bs.title) is not None else ""

            stemmer = Stemmer()
            if (title != ""):
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

            processed_text(doc_id=document_number, text=body_words)
            processed_title(doc_id=document_number, text=title_words)
            insert_dataframe(doc_number=document_number, doc_id=document_id, doc_url=document_url, doc_title=title,
                             doc_body=body_content)
            document_number += 1

if __name__ == '__main__':

    # fetch_data_per_path()
    processed_text = fetch_processed_texts()
    processed_title = fetch_processed_title()

    print("ENTERED ....")
    Q = "موسسه باستان شناس دانشگاه تهران"
    Q = re.sub(r'[a-zA-Z]', '', Q)
    Q = remove_punctuation(Q)
    Q = convert_numbers(Q)
    Q = re.sub(r'\s+', ' ', Q)
    #
    # # natural language processing
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

    start = time.time()
    tfidf_query_matrix_title = tfidf_vectorizer.transform([Q_words, *processed_title])
    tfidf_query_matrix_body = tfidf_vectorizer_body.transform([Q_words, *processed_text])

    print("for title")
    cosine_sim_title = cosine_similarity(tfidf_matrix, tfidf_matrix)[0, 1:]*0.75
    print(cosine_sim_title)
    print("for body")
    cosine_sim_body = cosine_similarity(tfidf_matrix_body, tfidf_matrix_body)[0, 1:]*0.25
    print(cosine_sim_body)

    print("result")
    total_cosine = (cosine_sim_title + cosine_sim_body)
    print("Time taken: %s seconds" % (time.time() - start))

    print(sorted(range(len(total_cosine)), key=total_cosine.__getitem__))