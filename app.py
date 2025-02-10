from flask import Flask, render_template, request, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

# Charger les questions
with open('data.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)["questions"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def questions_page():
    return render_template('questions.html', questions=questions)

@app.route('/get_questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    user_answers = request.json.get('answers', {})
    session['user_answers'] = user_answers
    return jsonify({'message': 'Réponses enregistrées'})

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    scores = calculate_results(user_answers)
    return render_template('results.html', scores=scores)


def calculate_results(user_answers):
    scores = {}
    for question in questions:
        axis = question['axis']
        if axis not in scores:
            scores[axis] = []
        scores[axis].append(user_answers.get(question['text'], 0))
    
    # Calculer la moyenne des scores pour chaque axe
    for axis in scores:
        scores[axis] = sum(scores[axis]) / len(scores[axis])
    
    return scores

if __name__ == '__main__':
    app.run(debug=True)
