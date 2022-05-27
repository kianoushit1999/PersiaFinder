import re
import xml.etree.ElementTree as ET
import time
import numpy as np
from bs4 import BeautifulSoup
from hazm import *
from handler import load_persian_stopwords, \
    get_all_files_path, remove_punctuation, convert_numbers
from mongodb_handler import insert_dataframe, processed_text, processed_title


def fetch_data_per_path():
    # define variables
    document_number = 0
    word_counter = 0
    PERSIAN_STOPWORDS = load_persian_stopwords()

    for path in get_all_files_path():
        if (path.startswith("./source_file/TehranUni_DUH")):
            continue
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
