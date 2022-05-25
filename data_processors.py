import re
import xml.etree.ElementTree as ET
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from hazm import *

from handler import load_persian_stopwords, \
    get_all_files_path, remove_punctuation, convert_numbers
from mongodb_handler import insert_general_into_db, insert_tfidf, insert_dataframe, fetch_general_info

PERSIAN_STOPWORDS = load_persian_stopwords()


def doc_freq(word, DF):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


def fetch_data_per_path():
    # define variables
    processed_text = []
    processed_title = []
    document_number = 0

    word_counter = 0
    for path in get_all_files_path():
        print(path)
        if (path.startswith("./source_file/Tebyan")):
            continue
        if (word_counter == 2):
            break
        root = ET.parse(path).getroot()
        for doc_id, url_tag, html_body in zip(root.findall('DOC/DOCID'), root.findall('DOC/URL'),
                                              root.findall('DOC/HTML')):
            document_number += 1

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

            processed_text.append(body_words.split())
            processed_title.append(title_words.split())

            insert_dataframe(doc_number=document_number - 1, doc_id=document_id, doc_url=document_url, doc_title=title,
                             doc_body=body_content)
        word_counter += 1

    return (
        document_number,
        processed_title,
        processed_text
    )


if __name__ == '__main__':

    document_number, processed_title, processed_text = fetch_data_per_path()
    print("Entered main .........")

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

    insert_general_into_db(N, total_vocab_size, total_vocab, DF)

    # TFIDF for body
    doc = 0
    tf_idf = {}
    for i in range(N):

        tokens = processed_text[i]

        counter = Counter(tokens + processed_title[i])
        words_count = len(tokens + processed_title[i])

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token, DF)
            idf = np.log((N + 1) / (df + 1))
            tf_idf[doc, token] = tf * idf
        doc += 1

    print("start tfidf")
    # TFIDF for title
    doc = 0
    tf_idf_title = {}

    for i in range(N):

        tokens = processed_title[i]
        counter = Counter(tokens + processed_text[i])
        words_count = len(tokens + processed_text[i])

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token, DF)
            idf = np.log((N + 1) / (df + 1))  # numerator is added 1 to avoid negative values
            tf_idf_title[doc, token] = tf * idf
        doc += 1

    # Merging the TF-IDF according to weights
    print("start alpha")
    alpha = 0.3
    for i in tf_idf:
        tf_idf[i] *= alpha

    for i in tf_idf_title:
        tf_idf[i] = tf_idf_title[i]

    for i in tf_idf:
        ind = total_vocab.index(i[1])
        insert_tfidf(doc_id=i[0], word=ind, tfidf=tf_idf[i])

    fetch_general_info()
    # print("Ended vectorizing")
    # Q = cosine_similarity("به سايت پرديس ابوريحان دانشگاه تهران")
    # print(Q)
    # print(dataframe.loc[Q[0], :].title)
    # print(dataframe.loc[Q[1], :].title)
    # print(dataframe.loc[Q[2], :].title)
