import time

from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def show_index():
    return render_template("index.html")

@app.route('/start-engine')
def prepare_suitable_data():
    print("entered in start engine")
    tic = time.time()
    time.sleep(5)
    toc = time.time()
    return jsonify({
        "response": "success"
    })

@app.route('/fetch-related-data', methods=["GET"])
def fetch_data():
    print("entered in func")
    return jsonify({
        "id": 1,
        "name": "Alex"
    })


if __name__ == '__main__':
    app.run()
