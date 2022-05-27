import json
import time
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from data_processors import fetch_data_per_path
from mongodb_handler import fetch_data_page_handler
from query_handler import prepare_engine, query_handler

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/start-engine', methods=["GET"])
def prepare_suitable_data():
    print("entered in start engine")
    try:
        # fetch_data_per_path()
        prepare_engine()
        return jsonify({
            "response": "success"
        })
    except Exception as e:
        return jsonify({
            "response": "fail"
        })

@app.route('/fetch-related-data', methods=["GET", "POST"])
def fetch_data():
    print("entered in func")
    if request.method == "POST":
        searched_token = json.loads(request.data)["sentence"]
        print(searched_token)
        index_data = query_handler(searched_token)
        content = fetch_data_page_handler(index_data[:10])
    return jsonify({
        "list": index_data,
        "content": content
    })

@app.route('/fetch-page', methods=["GET", "POST"])
def fetch_page_data():
    print("entered in func")
    if request.method == "POST":
        list_ids = json.loads(request.data)
        content = fetch_data_page_handler(list_ids["listContent"])

    return jsonify({
        "content": content
    })


if __name__ == '__main__':
    app.run()
