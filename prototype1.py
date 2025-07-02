
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

app_secret_key = placeholder-secret-key-for-version1_hci584-june-2025



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

# USER JOURNEY STEP 2 (BACKGROUND): GET QUESTIONS FROM OPEN TRIVIA DATABASE
def get_questions(amount=13):
    """ This function calls the Open Trivia Database (https://opentdb.com) API to retrieve the trivia 
    questions and converts it into json format. Each game has a baker's dozen (13) general knowledge, 
    multiple choice questions. If the app encounters an error loading the questions, gives user an 
    error message to try restarting the game (error message listed in Flask functions for user journey step 2).
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
        pass
    
    return None




# 
# FLASK FUNCTIONS
#
""" Includes all the Flask routes and basic HTML - will update with separate HTML/CSS/JS files as needed 
    in phase 2 once the basic app structure is built and tested"""

# TODO #

# homepage
##      user selects to play game
##      app starts game play
# question/answer - uses same basic template for each question/answer
##      question is asked; user inputs answer
##      app displays answer result and correct/incorrect user message
##      app moves to next question
# final result page with option to start new game or exit

# USER JOURNEY STEP 1: VISIT HOMEPAGE, LAUNCH GAME
@app.route('/')
def home():
    """ This function is for the very first step of the user journey:
        - user visits homepage, sees welcome message/instructions
        - user selets button to launch game
    """
    return """
    <html>
    <head>
        <title>Hello, Smarty Pants: A trivia game for smart people</title>
    </head>
    <body>
        <h1>Hello, Smarty Pants. Let's test how smart you really are.</h1>
        <p>Think you're oh-so-smart, don't you? We'll see about that.</p>
        <p>Hello, Smarty Pants is a general knowledge trivia game that only the smartest people can beat.
        But don't worry&mdash;you'll be playing by yourself, and we'll never let anyone know if you're A+ 
        material or just another average thinks-they-know-it-all.</p>
        <p>Ready to get started?</p>
        <a href="/start">
            <button>Bring. It. On.</button>
        </a>
    </body>
    </html>
    """

@app.route('/start')
def start():
    """ This function launches the actual game after user input on homepage.
    """
    return """
    <html>
    <head>
        <title>Hello, Smarty Pants: Let's get this game going</title>
    </head>
    <body>
        <h1>Time to prove your smarts!</h1>
        <p>Think you're oh-so-smart, don't you? We'll see about that.</p>
        <p>Hello, Smarty Pants is a general knowledge trivia game that only the smartest people can beat.
        But don't worry&mdash;you'll be playing by yourself, and we'll never let anyone know if you're A+ 
        material or just another average thinks-they-know-it-all.</p>
        <p>Ready to get started?</p>

        <p>PLACEHOLDER FOR GAME</p>

        <p>Whoa, whoa, whoa! 
            <a href="/">Take me back home.</a>
        </p>
    </body>
    </html>
    """



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
if __name__ == "__main__":
    print("Starting Flask app...")
    print("Visit http://127.0.0.1:5000 to see your homepage")
    # app.run(debug=True)