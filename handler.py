# import libraries
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from num2fawords import words
from collections import Counter
from hazm import *

ABSOLUTE_PATH = "./source_file"


def get_all_files_path():
    list_files = []
    for dir in os.listdir(ABSOLUTE_PATH):
        for file_name in os.listdir(ABSOLUTE_PATH + f"/{dir}"):
            list_files.append(ABSOLUTE_PATH + f"/{dir}/{file_name}")
    return list_files


def load_persian_stopwords():
    persian_stop_words = []
    with open('./persian_stopwords', 'r', encoding='utf-8') as reader:
        for line in reader.readlines():
            persian_stop_words.append(line.strip())
    return persian_stop_words


def remove_punctuation(ctx: str) -> str:
    symbols = r"[!\"#$%&()\'،*+-.,/:;<=>?@[\]^_`{|}~©\n]"
    ctx = re.sub(symbols, ' ', ctx)
    ctx = re.sub(r'\s+', ' ', ctx)
    return ctx


def convert_numbers(ctx: str) -> str:
    data = ''
    for word in ctx.split():
        if re.search('^\d+[\.\d]+$', word) is not None:
            if (len(word) < 5):
                data += f'{words(word)}'
        elif re.findall(r'\d+', word):
            if (len(word) < 5):
                number = list(map(int, re.findall(r'\d+', word)))[0]
                data += f' {words(number)} '
        elif len(word) < 2:
            continue
        else:
            data += f'{word}'
        data += " "
    return data