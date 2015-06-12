#!flask/bin/python
from flask import Flask, request, jsonify
from word_bubble_solver import *

app = Flask(__name__)


@app.route('/api/solve', methods=['GET', 'POST'])
def solve():
    bubbles = str(request.args.get('bubble'))
    word1_length = int(request.args.get('word1-length'))
    word2_length = int(request.args.get('word2-length'))
    word3_length = int(request.args.get('word3-length'))
    print word2_length
    print word2_length
    print bubbles

    if isinstance(bubbles, str) and word1_length > 1 and word2_length > 1:
        solver = WordBubbleSolver(
            word1_length, word2_length, word3_length,
            bubbles, './words')
        words = solver.find_all_words()
        print words
        return jsonify({
            'result': words
        })
    else:
        return jsonify({
            'result': 'error in query string parameters'
        })


@app.route('/')
def index():
    return """
    To get a solution in JSON format:<br>
    Use: <br>
      /api/solve?bubble='xxx|xxx|xxx'&word1_length=n&word2_length=n&word3_length=n <br>
    For example: <br>
      /api/solve?bubble='pse|opn|std'&word1_length=4&word2_length=5&word3_length=0 <br>
    If there's a bubble missing, use '#'.
    """
# if __name__ == '__main__':
    # app.run(debug=True)
