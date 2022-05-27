import numpy as np
import pymongo

def processed_text(doc_id, text):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col = db["processed_text"]
    col.insert_one({
        "doc_id": doc_id,
        "list": text
    })
    client.close()

def fetch_processed_texts():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col = db["processed_text"]
    return list(map(lambda x: x['list'], col.find({}, {"_id": 0, "list": 1})))

def processed_title(doc_id, text):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col = db["processed_title"]
    col.insert_one({
        "doc_id": doc_id,
        "list": text
    })
    client.close()

def fetch_processed_title():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col = db["processed_title"]
    return list(map(lambda x: x['list'], col.find({}, {"_id": 0, "list": 1})))

def insert_dataframe(doc_number, doc_id, doc_url, doc_title, doc_body):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col_df = db["dataFrame"]
    col_df.insert_one({
        "doc_number": doc_number,
        "doc_id": doc_id,
        "doc_url": doc_url,
        "doc_title": doc_title,
        "doc_body": doc_body
    })


def fetch_dataframe_by_doc_id(doc_num):
    return col_df.find_one({"doc_number": doc_num}, {
        "doc_url": 1,
        "doc_title": 1,
        "doc_body": 1,
        "_id": 0
    }).values()

def fetch_data_page_handler(list):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["searchEngine"]
    col_df = db["dataFrame"]
    result_list = []
    for id in list:
        result_list.append(col_df.find_one({"doc_number": id}, {
            "doc_url": 1,
            "doc_title": 1,
            "doc_body": 1,
            "_id": 0
        }))
    return result_list

# def insert_general_into_db(N=0, total_vocab_size=0, total_vocab=[], DF={}):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["searchEngine"]
#     col = db["generalInfo"]
#     col.insert_one({
#         "N": N,
#         "total_vocab_size": total_vocab_size,
#         "total_vocab": total_vocab,
#         "DF": DF
#     })
#
#
# def fetch_general_info():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["searchEngine"]
#     col = db["generalInfo"]
#     data = list(col.find({}, {}))[0]
#     return (data['N'],
#             data['total_vocab_size'],
#             data['total_vocab'],
#             data['DF'])

#
# def insert_tfidf(doc_id, word, tfidf):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["searchEngine"]
#     col_tfidf = db["tfidfInfo"]
#
#     col_tfidf.insert_one({
#         "doc_id": doc_id,
#         "word_id": word,
#         "tfidf": tfidf
#     })
#
#
# def find_by_doc(doc_id):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["searchEngine"]
#     col_tfidf = db["tfidfInfo"]
#
#     return list(map(lambda x: (x["word_id"], x["tfidf"]), np.array(list(col_tfidf.find({"doc_id": doc_id}, {
#         "word_id": 1, "tfidf": 1, "_id": 0
#     }).sort("word_id")))))

