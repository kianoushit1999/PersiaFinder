import json
import time
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/start-engine', methods=["GET"])
def prepare_suitable_data():
    print("entered in start engine")
    tic = time.time()
    time.sleep(5)
    toc = time.time()
    return jsonify({
        "response": "success"
    })


@app.route('/fetch-related-data', methods=["GET", "POST"])
def fetch_data():
    print("entered in func")
    if request.method == "POST":
        searched_token = json.loads(request.data)["sentence"]
    return jsonify({
        "id": 1,
        "response": "Alex"
    })


if __name__ == '__main__':
    app.run()
