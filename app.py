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
            word1_length, word2_length, word3_length, bubbles, built_dictionary)
        words = solver.find_all_words()
        # words = []
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
      /api/solve?bubble=xxx|xxx|xxx&word1-length=n&word2-length=n&word3-length=n <br>
    For example: <br>
      /api/solve?bubble=pse|opn|std&word1-length=4&word2-length=5&word3-length=0 <br>
    If there's a bubble missing, use '@'. <br>

    -- Victor Chiu
    """
if __name__ == '__main__':
    built_dictionary = WordBubbleSolver.build_anagram_dict('./words')
    app.run(debug=True)
