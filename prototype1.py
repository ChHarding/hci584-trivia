
# 
# IMPORTS -- delete documentation links prior to live implementation
#

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user 
from flask_wtf import FlaskForm
from flask_socketio import SocketIO, emit, join_room, leave_room 
    ###  documentation: https://flask.palletsprojects.com/en/stable/

from jinja2 import Template
    ###  documentation: https://jinja.palletsprojects.com/en/stable/
  
import os # for phase 2 upgrade from sqlite (initial prototype) to PostgreSQL (needed for 10+ simultaeous players)
import json
from datetime import datetime 
from random import randint


# 
# APP SET UP
#

app = Flask(__name__)

# TODO #



#
# DATABASE TABLES
#

#Admin # TODO #
""" This class is for the Game Administrator account type. This is a persistant account type that can log in 
    with their email and password. It will include:
    - Unique user ID (auto-generated random integer)
    - User's first name
    - User's last name
    - Email
    - Password for logging in (hash protected?)
    - Date the user's account was created
    - Date the user last logged in
    
    **Needs to link to all of their games
"""

#Player # TODO #
"""This class is for the Player account type. This is a temporary account type that is only used for a single game.
    It will include:
    - Username (unique within the game they are playing)
    - Email 
    - When the joined the game
    - Which question they are on
    - Their current score
    
    **Needs to link to the associated game and the answers they submitted**
"""

#Game # TODO #
"""This class is for the actual game itself—-a single game instance. It will include:
    - The game "owner" aka the associated Game Admin account 
    - Unique game ID (uses associated admin account ID as base)
    - Game title
    - Game description
    - Unique URL slug
    - API settings TBD
    - Game status (i.e., draft, active, completed) 
    - When game was created
    - When game started
    - When the game ended
    - Which question is currently being shown 
    - All the questions fetched from the API 

    **Needs to generate unique URL slug from the title (determines the link users will visit to play game),
    get the current question being shown via API, and link to all player and admin accounts**
"""

#Submissions # TODO #
"""This class handles all of the answer submissions: one player's answer to one question. 
    It will include:
    - The player submitting the answer 
    - The game it's for
    - The question number 
    - The answer the player selected 
    - The correct answer 
    - Whether they got it right (True/False)
    - Timestamp for when it was submitted 
    
    **Needs to link to associated player and game. Must ensure players can only submit a 
    single answer and cannot change it once submitted (submitting no answer by the time question closes 
    qualifies as answer).**
"""

#
# FORMS
#

#NewAccountForm # TODO #
""" Form to register for a new admin user account. Includes:
    - Field: First Name (required)
    - Field: Last Name (required)
    - Field: Email (required - must be in acceptable format) 
    - Field: Password (required - must be in acceptable format) 
    - Field: Confirm Password (required - must match first password submission exactly) 
    - Button: Create Account 
"""

#LogInForm # TODO #
""" Form that allows registered admin users to log into the app. Includes:
    - Field: Email (required) 
    - Field: Password (required) 
    - Button: Log In 
"""

#PlayerJoinForm # TODO #
""" Form that allows player to join a game. Includes:
    - Field: username (required) 
    - Field: Email (optional) 
    - Button: Join Game 
"""

#CreateGameForm # TODO #
""" Form for creating a new game. Fields for this are TBD now that I'm switching to using the Q/A API, but may include:
    - Field: Game Name (required) 
    - Field: Game Description (optional) 
    - Field: Game Date and Time (optional - text field for user messaging only, doesn't control game play)
    - Other fields TBD based on API
    - Button: Create Game
""" 




