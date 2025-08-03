# See https://joellenroberts.pythonanywhere.com for live demo


# 
# IMPORTS
#

from flask import Flask, render_template, request, redirect, url_for, session, jsonify 
import html
import random  
import requests

# 
# APP SET UP
#
""" Standard code to make the app work"""

app = Flask(__name__)

# NOTE: if deploying on a public server, update to a unique value; not needed for local use
app.secret_key = "placeholder-secret-key-for-version1_hci584-june-2025"

# 
# GAME ENGINE FUNCTIONS
#
""" Includes all of the functions that control the game.
    AI disclosure: Used Claude Sonnet 4 for troubleshooting and debugging. """


# USER JOURNEY STEP 2.1 (BACKGROUND): GET QUESTIONS FROM OPEN TRIVIA DATABASE

def get_questions():
    """ This function calls the Open Trivia Database API to retrieve the trivia 
    questions and converts it into JSON format. Each game consists of randomized, multiple choice questions. If the 
    app encounters an error loading the questions, gives user an error message to try restarting the game (error 
    message listed in Flask functions for user journey step 2).

    The OTD API does not require an API key for use. To change the category, quantity of questions, or difficulty level,
    visit the API configuration page (https://opentdb.com/api_config.php) to retrieve a new URL.

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

    url = f"https://opentdb.com/api.php?amount=13&difficulty=hard&type=multiple"
    try:
        response = requests.get(url)
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
        else:
            return None
    except:    
        return None


# USER JOURNEY STEP 2.2 (BACKGROUND): CLEAN QUESTION AND ANSWER DATA FROM API

def clean_up_questions(all_raw_questions):
    """ This function takes the raw data from the Open Trivia Database API and makes it presentable for human 
    game play. This includes updating HTML character codes so they are readable by humans (e.g., changing 
    &#039; to ' or &quot; to ") and randomizing the answer order so that the correct answer is not always 
    in the same list location (i.e., the correct answer is not always in position 1). Returns the cleaned up 
    questions, the cleaned up answer, and the location of the correct answer for ALL questions. 
        
    Arguments:
    - all_raw_questions: questions retrieved from API via get_questions
    
    Returns:
    - list of cleaned question and answer data
    """
    
    # if the function get_questions() fails to pull in any questions, the loop stops as there's no data to clean up
    if not all_raw_questions:
        return None
    
    # create list to hold all the cleaned-up question data
    questions = []
    
    for question_details in all_raw_questions:
        
        # first, cleans up special HTML characters and makes the questions human readable
        question = html.unescape(question_details["question"])
        
        # creates a combined list to all answers by pulling together all correct and incorrect answers
        raw_answers = [question_details["correct_answer"]] + question_details["incorrect_answers"]
        
        # create list to hold all the cleaned-up answer data for a each question
        answers = []

        # for each of the answer options, clean up special HTML characters so they're human readable
        for a in raw_answers:
            cleaned_answers = html.unescape(a)
            answers.append(cleaned_answers)
        cleaned_correct_answer = html.unescape(question_details["correct_answer"])
        
        # random shuffle all the cleaned-up answer options so the correct answers are not predictable, then make a note
        # of the index for the correct answer for that specific question so it can be used to grade user answer input
        random.shuffle(answers)
        correct_index = answers.index(cleaned_correct_answer)
        
        # documents final cleaned-up questions, saves question, answers, and correct index fields to questions dictionary
        cleaned_question = {
            "question": question,
            "answers": answers,
            "correct_index": correct_index
        }
        questions.append(cleaned_question)
    
    return questions


# USER JOURNEY STEP 2.3 (BACKGROUND): CHECK IF SUBMITTED ANSWER IS CORRECT

def check_answer(user_answer_index, question_data):
    """ This function checks if the answer the user submitted matches the correct answer from the API data.
    
    Arguments:
    - user_answer_index: the index of the answer the user selected
    - question_data: list containing current question's info including correct_index
    
    Returns:
    - True if answer's answer matches the correct answer index
    - False if it does not match the correct answer
    """
    
    # identity the index for correct answer to the current question
    correct_index = question_data["correct_index"]

    # use index to determine if user's answer is right or wrong
    if user_answer_index == correct_index:
        return True
    else:
        return False


# USER JOURNEY STEP 2.4 (BACKGROUND): UPDATE RUNNING SCORE AFTER ANSWER CHECKED

def update_total_score(current_score, user_correct):
    """ This function updates the user's running total score for the game thus far based on whether their
    answer to the previous question was correct or incorrect. It uses the check_answer function to determine
    if the user had a correct (True) answer or incorrect (False) answer.
    
    Arguments:
    - current_score: the user's current score (i.e., prior to the question just answered)
    - user_correct: True/False if the answer was right as determined by check_answer function
    
    Returns:
    - updated score (current_score + 1 if correct, no change if incorrect)
    """

    # uses check_answer and current score to determine new score
    if user_correct == True:
        return current_score + 1
    else:
        return current_score

# USER JOURNEY STEP 2.5 (BACKGROUND): USER FEEDBACK AFTER SUBMITTING ANSWER
##  in phase 2, may update this to display to currect answer as part of the message rather than a simple right/wrong message

def user_feedback(result, user_chosen_answer=None):
    """ This function provides a user feedback message after the user has answered a question, alerting them 
    whether they were correct or incorrect.
    
    Arguments:
    - result: from check_answer (True/False)
    - user_chosen_answer: the text of the answer the user selected (for incorrect answers)
    
    Returns:
    - User messaging indicating whether the answer was correct or incorrect
    """

    # uses check_answer to determine if user gets a correct vs. incorrect temporary feedback message 
    if result == True:
        return f"Woohoo! You are smart (and you've got the correct answers to prove it)."
    else:
        return f"Smart? Not on this question. <br><span class='text-red font-bold text-shadow-sm'>{user_chosen_answer}</span> is the wrong answer."

# 
# FLASK FUNCTIONS
#
""" Includes all the Flask routes and basic HTML - will update with separate HTML/CSS/JS files as needed 
    in phase 2 once the basic app structure is built and tested
    
    AI disclosure: Used Claude Sonnet 4 to generate HTML and JavaScript for Flask routes, as well as for 
    troubleshooting and debugging."""

# USER JOURNEY STEP 1: VISIT HOMEPAGE, LAUNCH GAME
@app.route('/')
def home():
    """ This function is for the very first step of the user journey:
        - user visits homepage, sees welcome message/instructions
        - user selets button to launch game
        
        Returns:
        - App '/' homepage
        """
    
    return render_template("home.html")

@app.route('/start')
def start():
    # possible phase 2 augmentation: show dynamic countdown clock
    """ This function launches the actual game after user input on homepage.
        
        Returns:
        - Game '/start' sequence
        - First question '/question' page (delayed autodirect)
        """

    # runs first two game engine functions to pull questions from the API and get them cleaned and ready to display
    raw_questions = get_questions()
    questions = clean_up_questions(raw_questions)

    # error handling
    # AI disclosure: added this from Claude during troubleshooting
    if not questions:
        return render_template('start.html', error=True)

    # initializes the game session using the pulled questions
    session["questions"] = questions
    session["current_question"] = 0
    session["score"] = 0
    
    return render_template("start.html", error=False)

# USER JOURNEY STEP 2: VIEW QUESTION AND SELECT/SUBMIT ANSWER

@app.route('/question')
def show_question():
    """ This function shows the cleaned up questions and available answer options to the user. In addition, the user 
        can see which question they are on (i.e., Question X of Y). The user selects an answer from a 
        list of radio buttons. The answer is automatically submitted once a radio button is active; there 
        is no separate submit button.
        
        Returns:
        - Main game play '/questions' page
        """
    
    # establishes the number of current question and the question data for the current game session  
    current_num = session.get("current_question", 0)
    questions = session.get("questions", [])

    # Displays special message if there are no more questions to answer
    if current_num >= len(questions):
        return "That's it. You're answered them all. There're no more questions. Zip, Zero. Zilch. Nada. "

    # Pulls the data for the current question number so it can be displayed on the page
    question_data = questions[current_num]

    return render_template("question.html",
                            question_data=question_data,
                            current_question_num=current_num + 1,
                            total_questions=len(questions))

@app.route('/answer', methods=['POST'])
def answer():
    """ This function processes the user's selected answer from the form on '/quetion' using the check_answer game 
        logic function. It then displays a user message based on results and automatically redirects the user to
        the next question.
        
        Returns:
        - '/answer', an intermediary page with a user message that redirects to the next question after 3 seconds"""
    
    # user's answer based on radio button selected on '/question'
    user_answer = int(request.form.get("answer", -1))
    
    # establishes the number of current question, the question data, and score for the current game session   
    current_num = session.get("current_question", 0)
    questions = session.get("questions", [])
    score = session.get("score", 0)

    # if there are no more questions, redirects to '/results' page instead of the question page
    if current_num >= len(questions):
        return redirect(url_for("results"))
    
    # gets info about the current question (based on question number)
    current_question_data = questions[current_num]

    # determine if user's answer is current question correct
    is_correct = check_answer(user_answer, current_question_data)

    # updates score
    new_score = update_total_score(score, is_correct)

    # pulls text from user's selected answer to use in incorrect answer feedback message
    user_answer_text = current_question_data["answers"][user_answer]

    # grabs associated feedback message
    if is_correct:
        feedback_message = user_feedback(is_correct) 
    else:
        feedback_message = user_feedback(is_correct, user_answer_text) 
    
    # calculate next question number
    next_question_num = current_num + 1
    
    # save user progress
    session["score"] = new_score
    session["current_question"] = next_question_num 
    
    # Return JSON response for the overlay
    # AI disclousure: reflects addition of JSON required for JavaScript dynamic display derived from Claude Sonnet 4
    response_data = {
        "is_correct": is_correct,
        "feedback_message": feedback_message,
        "current_score": new_score,
        "current_question_num": next_question_num,
        "total_questions": len(questions),
        "has_more_questions": next_question_num < len(questions)
    }
    
    return jsonify(response_data)

# USER JOURNEY STEP 3: SEE FINAL RESULTS AT END OF GAME

@app.route('/results')
def results():
    """ This function displays the final score at the end of the game. Both the raw (number of questions 
        answered coreectly) and the percentage (answered correctly out of the total number of questions) is show. 
        Also shows a final message based on the number of questions the user got correct. User has the option to 
        return to the homepage and start a new game.
    
        Returns:
        - '/results' page at the end of the game."""
    
    # get the final number of correct answers and use that to calculate a percent-based final score
    questions = session.get("questions", [])
    score = session.get("score", 0)
    score_percentage = round(score / len(questions)) * 100

    # final user score message on results page is based on the number of answers the user guessed correctly
    if score_percentage == 100:
        final_score_message = f"Daaaaaaamn... you sure are smart!"
    elif 100 > score >= 75:
        final_score_message = f"OK, we'll admit it: You are pretty smart. <br>This time."
    elif 75 > score >= 50:
        final_score_message = f"Meh. You could've done better. <br>Of course, you could have done worse. <br>Consider yourself solidly average."
    else:
        final_score_message = f"Smart? Sorry, not this time. <br>Perhaps trivia isn't your game?"
    
    return render_template("results.html",
                            final_score=score,
                            score_percentage=score_percentage,
                            final_score_message=final_score_message)

# 
# RUN APP
#
""" Includes final code to make this bad boy run"""


if __name__ == "__main__":
    print("Starting app...")
    print("Local homepage for testing: http://127.0.0.1:5000")
    app.run(debug=True)