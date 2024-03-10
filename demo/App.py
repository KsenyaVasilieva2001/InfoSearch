# импортируем Flask
from flask import Flask, render_template, request, send_from_directory
from task5.VectorSearcher import VectorSearcher

import nltk

nltk.download('punkt')

app = Flask(__name__, template_folder='template')


@app.route('/')
def search():
    result = []
    query = request.args.get('query')
    if query:
        result = vector.search(query)
    return render_template('base.html', result=result)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == "__main__":
    vector = VectorSearcher()
    app.run(debug=False)
