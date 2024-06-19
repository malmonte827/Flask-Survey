from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)

session_keys = 'responses'

@app.route('/')
def homepage():
    """ Display Survey Homepage"""

    return render_template('survey-homepage.html', survey = survey)

@app.route('/start', methods=['POST'])
def start_survey():
    """Clear session of responses"""

    session[session_keys] = []

    return redirect('/questions/0')


@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Display Question"""
    responses = session.get(session_keys)
    
    # Accessing question out of order
    if (len(responses) != question_id):
        flash('Invalid Question ID.')
        return redirect(f'/questions/{len(responses)}')
    
    # Answered all questions. Thank them
    if (len(responses) == len(survey.questions)):
        return redirect('/finish')
    
    question = survey.questions[question_id]

    return render_template('questions.html', question = question)



@app.route('/answer', methods=['POST'])
def save_answer():
    """ Appends answer to responses redirects to next question"""
    # Get answer from form and append them to responses
    choice = request.form['answer']

    responses = session[session_keys]
    responses.append(choice)
    session[session_keys] = responses

    # Answered all questions. Thank them
    if (len(responses) == len(survey.questions)):
        return redirect('/finish')
    else:
        # Sends them to next question
        return redirect(f'/questions/{len(responses)}')


@app.route('/finish')
def finish():
    """Display finsih page"""

    return render_template('finish.html')

