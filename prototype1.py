
# 
# IMPORTS
#

from flask import Flask, render_template, request, redirect, url_for, session, flash 
import html
import random  
import sys
import requests
  

# 
# APP SET UP
#
""" Standard code to make the app work"""

app = Flask(__name__)

app.secret_key = "placeholder-secret-key-for-version1_hci584-june-2025"



# 
# GAME ENGINE FUNCTIONS
#
""" Includes all of the functions that control the game"""

# TODO #

# set up dictionary for game data
# get questions from API >> https://opentdb.com/api_config.php
##      for phase 2, may allow user to choose between question types - topic or difficulty - 
##      thus needing separate possible API configs
# check each answer against API data during game play
# give countdown of how many questions are left

# USER JOURNEY STEP 2.1 (BACKGROUND): GET QUESTIONS FROM OPEN TRIVIA DATABASE
def get_questions():
    """ This function calls the Open Trivia Database (https://opentdb.com/api_config.php) API to retrieve the trivia 
    questions and converts it into json format. Each game has a baker's dozen (13) of multiple choice questions. 
    If the app encounters an error loading the questions, gives user an error message to try restarting 
    the game (error message listed in Flask functions for user journey step 2).

    Data returned includes:
    - response_code
    - results
    -- type
    -- difficulty
    -- category
    -- question
    -- correct_answer
    -- incorrect_answers

    No arguments
    """
    url = f"https://opentdb.com/api.php?amount=13&category=23&difficulty=medium&type=multiple"
    try:
        response = requests.get(url)
        data = response.json()
        if data['response_code'] == 0:
            return data['results']
        else:
            return None
    except:    
        return None


# USER JOURNEY STEP 2.2 (BACKGROUND): CLEAN QUESTION AND ANSWER DATA FROM API
def clean_up_questions(all_raw_questions):
    """ This function takes the raw data from the API and makes it presentable for human game play. This includes
    updating HTML character codes so they are readable by humans (e.g., changing &#039; to ' or &quot; to ") and 
    and randomizing the answer order so that the correct answer is not always in the same list location. Returns
    the cleaned up questions, the cleaned up answer, and the location of the correct answer for ALL questions. 
        
    Arguments:
    - all_raw_questions: questions retrieved from API via get_questions
    
    Returns:
    - dictionary of cleaned question and answer data
    """
    
    if not all_raw_questions:
        return None
    
    questions = []
    
    for question_details in all_raw_questions:
        question = html.unescape(question_details['question'])
        
        raw_answers = [question_details['correct_answer']] + question_details['incorrect_answers']
        answers = []
        for a in raw_answers:
            cleaned_answers = html.unescape(a)
            answers.append(cleaned_answers)
        cleaned_correct_answer = html.unescape(question_details['correct_answer'])
        
        random.shuffle(answers)
        correct_index = answers.index(cleaned_correct_answer)
        
        cleaned_question = {
            'question': question,
            'answers': answers,
            'correct_index': correct_index
        }
        questions.append(cleaned_question)
    
    return questions


# USER JOURNEY STEP 2.3 (BACKGROUND): CHECK IF SUBMITTED ANSWER IS CORRECT

def check_answer(user_answer_index, question_data):
    """ This function checks if the answer the user submitted matches the correct answer from the API data.
    
    Arguments:
    - user_answer_index: the index of the answer the user selected (0-3)
    - question_data: dictionary containing question info including correct_index
    
    Returns:
    - True if answer's answer matches the correct answer index
    - False if it does not match the correct answer
    """
    
    correct_index = question_data['correct_index']

    if user_answer_index == correct_index:
        return True
    else:
        return False













# 
# FLASK FUNCTIONS
#
""" Includes all the Flask routes and basic HTML - will update with separate HTML/CSS/JS files as needed 
    in phase 2 once the basic app structure is built and tested"""

# TODO #

# question/answer - uses same basic template for each question/answer
##      app displays answer result and correct/incorrect user message
##      app moves to next question
# final result page with option to start new game or exit

# USER JOURNEY STEP 1: VISIT HOMEPAGE, LAUNCH GAME
@app.route('/')
def home():
    """ This function is for the very first step of the user journey:
        - user visits homepage, sees welcome message/instructions
        - user selets button to launch game"""
    return """
    <html>
    <head>
        <title>Hello, Smarty Pants: A trivia game for smart people</title>
    </head>
    <body>
        <h1>Hello, Smarty Pants. Let's test how smart you really are.</h1>
        <p>Think you're oh-so-smart, don't you? We'll see about that.</p>
        <p><strong>Hello, Smarty Pants</strong> is a general knowledge trivia game that only the smartest people can beat.
        But don't worry&mdash;you'll be playing by yourself, and we'll never let anyone know if you're A+ 
        material or just another average thinks-they-know-it-all.</p>
        <p><em>Ready to get started?</em></p>
        <a href="/start">
            <button>Bring. It. On.</button>
        </a>
    </body>
    </html>
    """

@app.route('/start')
def start():
    """ This function launches the actual game after user input on homepage. After a 5 second welcome message, it redirects 
        to the '/question' view to show the first question."""

    raw_questions = get_questions()
    questions = clean_up_questions(raw_questions)

    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    
    #TODO#
    return """
    <html>
    <head>
        <title>Hello, Smarty Pants: Let's get this game going!</title>
        <script>
            setTimeout(function() {
                window.location.href = '/question';
            }, 5000);
        </script>
    </head>
    <body>
        <h1>Time to prove your smarts!</h1>
        <p>Think you're oh-so-smart don't you? We'll see about that.</p>
        <p><em>Get ready, get set&hellip;</em></p>
    </body>
    </html>
    """

# USER JOURNEY STEP 2: VIEW QUESTION AND SELECT/SUBMIT ANSWER
#TODO#
@app.route('/question')
def show_question():
    """ This function shows the cleaned up questions and available answer options to the user. In addition, the user 
        can see which question they are on (i.e., Question X of Y). The user selects an answer from a 
        list of radio buttons. The answer is automatically submitted once a radio button is active; there 
        is no separate submit button."""
    
    current_num = session.get('current_question', 0)
    questions = session.get('questions', [])

    if current_num >= len(questions):
        return "That's it. You're answered them all. There're no more questions. Zip, Zero. Zilch. Nada. "

    question_data = questions[current_num]

    radio_buttons = ""
    for i, answer in enumerate(question_data['answers']):
        radio_buttons += (
            f'<input type="radio" name="answer" value="{i}" '
            f'id="answer{i}" onchange="submitAnswer()">'
            f'<label for="answer{i}"> {answer}</label>'
            f'<br><br>'
        )

    return f"""
    <html>
    <head>
        <title>Hello, Smarty Pants: We've got questions. You've got answers.</title>
        <script>
            function submitAnswer() {{
                document.getElementById('answerForm').submit();
            }}
        </script>
    </head>
    <body>
        <p>Question {current_num + 1} of {len(questions)}</p>
        <h2>{question_data['question']}</h2>
        <form id="answerForm" method="POST" action="/answer">
        {radio_buttons}
        </form>
    </body>
    </html>"""

# USER JOURNEY STEP 2: VIEW CORRECT ANSWER AND MOVE ONTO NEXT QUESTION



#
# TESTING AND DEBUGGING
#
""" Includes any code necessary for testing to ensure game works; will be commented out prior to actual implementation"""

# TODO #

# TBD as game is developed


# 
# RUN APP
#
""" Includes final code to make this bad boy run"""

# execute game play when user selects to play game
#if __name__ == "__main__":
    #print("Starting app...")
    #print("Local homepage for testing: http://127.0.0.1:5000") # for local hosting only; update once on Python anywhere