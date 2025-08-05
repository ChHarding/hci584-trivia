![Hello, Smarty Pants: a simple, single-player trivia game web app powered by Python Flask](/_img/Hello-Smarty-Pants-Dev-Guide.png)

## **Overview**
**Hello, Smarty Pants** is a simple, browser-based web application that allows individual users to play a self-serve, multiple-choice trivia game. It uses Flask 3.1.0 as the web framework, Tailwind 4.1 for styling, and the [Open Trivia Database] (https://opentdb.com/api_config.php) API as the question engine. 

You can test play the deployed prototype at [https://joellenroberts.pythonanywhere.com](https://joellenroberts.pythonanywhere.com) 

The game app flow is as follows:

1. User visits the app homepage →
2. User selects option to start game →
3. App presents first question →
4. Player uses radio button to select answer →
5. App processes answer and displays a feedback message indicating whether they were correct/incorrect →
6. Repeat steps 3–6 until user completes all questions →
7. App calculates and displays user’s final score and feedback message →
8. User chooses to play again or exit

This app was originally built as a student project for Iowa State University’s HCI 5840 course in summer 2025. 

## **Project Files**

```
├── app.py                          # main app (created with Python 3.13.0)
├── requirements.txt                # required Python libraries (Flask 3.1.0 and Requests 2.32.3)
├── templates/                      
│   ├── home.html                   # app home
│   ├── start.html                  # start page
│   ├── question.html               # primary game play page
│   └── results.html                # end results summary page
├── static/
│   └── css/
│       └── style.css               # custom styling (otherwise Tailwind 4.1)
├── _docs/                          # reference docs
│   └── dev-guide.md                # developer's guide
├── _img/                           # reference images (not required to run app)
│   ├── Hello-Smarty-Pants-User-Guide.png  
│   ├── Hello-Smarty-Pants-Dev-Guide.png 
│   ├── Hello-Smarty-Pants-Start-Game.png 
│   ├── Hello-Smarty-Pants-Play-Game.png
│   └── Hello-Smarty-Pants-Results.png
├── LICENSE                         # MIT license
└── README.md                       # user's guide
```

## **Installation and Use**

### ***Requirements and Considerations***

This single-player trivia game was built using Python 3.13.0 and relies on the following Python libraries and modules to run:

**Python Standard Library Modules**
- `html` - used for cleaning up data from API
- `random` - use to randomize answer option order

**Third-Party Libraries**
- `Flask` >= 3.1.0 - web framework
- `Requests` >= 2.32.3 - used to fetch API data

If you haven't already installed these third-party libraries, you'll need to install them before running the main app program. The easiest way to do this is by installing `requirements.txt` using the command line (if `pip` doesn’t work, try `pip3`).

```
pip install -r requirements.txt
```

### ***Open Trivia Database***

**Hello, Smarty Pants** uses the Open Trivia Database API to supply the game's questions and answers. It ***does not*** require an API key.

### ***Local Use***

To run the app on a local machine, follow these steps:

1\. Download the program files.

2\. Install the required `Flask` and `Requests` libraries via `requirements.txt`.  

3\. Run the main program file from the terminal command line.  
```
python app.py
```

If `python` doesn’t work, try `python3`.

4\. Open a browser and navigate to `http://127.0.0.1:5000`. Once open, use the yellow CTA button to start. 

### ***Web Server Deployment***

1\. If you choose the deploy on a public web server, make the following changes to the `app.py` file:
- Replace the secret key.

  ``` 
  app.secret_key = "placeholder-secret-key" 
  ```

  This variable is necessary for the `Flask session` function, which drives much of the game play, but is currently a generic placeholder. For security purposes, change the generic password to a random, cryptographically secure value. The easiest way to do this is to use the Python `secrets` function to generate a random hex value:

  ``` 
  import secrets

  secret_key = secrets.token_hex(16)  # 16 bytes = 32 hex characters
  print(secret_key)
  ```

- Update the final `run.app` function. It is currently:

  ``` 
  if __name__ == "__main__":
  print("Starting app...")
  print("Local homepage for testing: http://127.0.0.1:5000")
  app.run(debug=True)
  ```
  
  The print() functions and debugger are not needed for web deployment, so update it to:

  ``` 
  if __name__ == "__main__":
  app.run()
  ```

- Replace the current placeholder TypeKit link with the correct webfont link. It is found as an `@import` link at the top of the `style.css` file and in the `<head>` section of each HTML template. 
  
  The two primary fonts used within the app are Rockwell and Segoe UI. The latter is a standard font that comes with Windows and Microsoft Office. Both [Rockwell](https://fonts.adobe.com/fonts/rockwell) and [Segoe UI](https://fonts.adobe.com/fonts/segoe-ui) are also available as web fonts through Adobe Fonts and MyFonts. 

  While the app will work if you don't update this link, the specified fallback fonts will be loaded. You will probably also receive backend error messages. 

2\. You will need to upload these files in this structure for the app to work:
```
├── app.py
├── templates/                      
│   ├── home.html
│   ├── start.html
│   ├── question.html 
│   └── results.html
└── static/
    └── css/
      └── style.css
```

3\.Please check your web host’s documentation for additional deployment instructions, including whether you need to install the latest `Flask` and `Requests` libraries separately, as this varies between servers.

## **User-side Game Play**

### ***User Flow Step 1: Start Game***

A user visits the trivia game web app using a desktop or mobile browser. On the homepage, they see a welcome message and a button that let's them launch a single player, 13-question general knowledge trivia game. They press the button to play. 

![Hello, Smarty Pants: Start Game](/_img/Hello-Smarty-Pants-Start-Game.gif)

### ***User Flow Step 2: Play Game***

Now the game play officially begins. Player sees the first question and four answer choices. The player selects their answer by radio button, after which they see a user feedback message about whether they were correct or incorrect via a pop-up overlay: If the player guessed right, they get a “correct” message; if the guess is wrong, the player gets an “incorrect” message, indicating which answer they selected. They can also see their cumulative score. 

![Hello, Smarty Pants: Play Game](/_img/Hello-Smarty-Pants-Play-Game.gif)

They are then automatically taken to the next question and follow the same process until they complete all 13 questions. 

### ***User Flow Step 3: View Results***

Once the player answers all 13 questions, they are redirected to a page that displays the final results as a raw number of questions answered correctly and as a percentage of the whole, plus one of four use feedback messages based on the percentage of questions they answered correctly. 

![Hello, Smarty Pants: Final Results](/_img/Hello-Smarty-Pants-Results.png)

From here, they can choose to return to the beginning and start a new game.

## **Back-End Game Engine**

### ***Basic Structure***
This app is built on the Python Flask web framework (3.1.0). Most of the functions used to power the app and user game play are a combination of custom functions listed under the `# GAME ENGINE FUNCTIONS` section of `app.py` (found in the top half of the file) and these `Flask` functions:

- `Flask` - creates web app
- `render_template` - merges data into HTML templates before loading in browser
- `request` - captures user input data from answer submission form (via radio buttons)
- `redirect` - automatically redirects user to new page
- `url_for` - generates url for each `Flask @route`
- `session` - stores data that persists aross pages
- `jsonify` - converts Python data to JSON so it can be used by JavaScript within templates

In addition, many front-end features like animations and messaging overlays are driven by JavaScript functions.

### ***User Flow Step 1: Start Game***
When the user lands on the homepage, the app populates and loads the homepage template via `Flask @app.route('/')`. The only possible user input on this page is selecting the yellow CTA button that launches the game. 

When that happens, the app loads start page via `@app.route('/start')`. This is the first `Flask` route that contains substantial functionality: it calls the Open Trivia Database API to fetch the question and answer data (using the `get_questions()` custom function) and cleans them up so they are ready for game play (using the custom `clean_up_questions()` function). It also uses the `Flask session` function to initialize the new game session. 

Data does not persist between games, so the game session always begins with fresh questions and a zero score.

`'/start'` is contains a dynamic 3-2-1-GO countdown timer, which is entirely driven by JavaScript. See `templates/start.html` for full JavaScript details and `static/css/style.css` for animation styling.

### ***User Flow Step 2: Play Game***
The app displays questions from the API one at a time using `@app.route('/question')`. This route uses the `session` function to get the current question and loads the questions and answer options of the page when it returns `render_template`.

Once the user submits their answer (radio buttons on the `/question` template), the app automatically uses `@app.route('/answer')` to process the answer and determine if it's correct or incorrect (using `check_answer()` custom function), update the cumulative score(using the `update_total_score()` custom function) and load the appropriate user feedback message (using `user_feedback()` custom function). 

Please note that `@app.route('/answer')` does not load a new template. Instead, it returns the temporary user feedback message in a JavaScript-powered pop-up overlay on top of the current `/question` page. See `templates/answer.html` and `static/css/style.css` for more details about the JavaScript that powers this as well as its styling.

After a few seconds, the `/question` page is reloaded with a new question and the process repeats for 13 total questions.

### ***User Flow Step 3: View Results***
After the user answers all questions, they are automatically redirected to the `/results` page where `@app.route('/results')` renders the final `session` score as both a total number of correct answers and the percentage of all questions. Based on the percentage score, the app shows one of four user messages.

## **TLDR**
**Hello, Smarty Pants** is simple trivia game with questions retrieved via the Open Trivia Database API and powered by Python `Flask`. It depends heavily on `Flask session` functions for game functions and JavaScript for front-end messaging display and animations. Custom functions pull questions from the API, clean them up for human readability, grade answers, update scores, an determine appropriate user feedback messages. It features a total of five `Flask` routes and four HTML templates.

## **Possible Enhancements and Variations**

While **Hello, Smarty Pants** is designed to be a simple, straightforward application, there are a number of ways it could be enhanced.

- Adding the option to allow users to specify game attributes like number of questions, topic, or question difficulty; this could be acheived by dynamically building the API URL to include specific parameter values
- Adding an additional, alternative game at an easier level of difficulting and showing it as an option on the `/results` page to people who score below a certain threshold
- Creating a database of custom questions and using it instead of questions from the Open Trivia Database API  
- Improving overall styling, especially the user feedback messaging
