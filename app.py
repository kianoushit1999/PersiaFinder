from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def show_index():
    return render_template("index.html")

@app.route('/fetch-related-data', methods=["GET"])
def fetch_data():
    print("entered in func")
    return jsonify({
        "id": 1,
        "name": "Alex"
    })


if __name__ == '__main__':
    app.run()
