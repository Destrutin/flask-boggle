from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
boggle_game = Boggle()

@app.route('/')
def show_board():
    """Render the template for the board"""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    """Check if the submitted word valid"""

    guess = request.args['guess']
    board = session['board']
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route('/update-stats', methods=['POST'])
def update_stats():
    """Update stats for player"""
    data = request.json
    score = data['score']
    high_score = data['highScore']
    play_count = data['playCount']

    return jsonify({'status': 'success', 'message': 'Stats updated'})

