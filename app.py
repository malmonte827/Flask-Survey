from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def homepage():
    """ Display Survey Homepage"""

    return render_template('survey-homepage.html', survey = survey)



@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Display Question"""

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
    responses.append(choice)

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

