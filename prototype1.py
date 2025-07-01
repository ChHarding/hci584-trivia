
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



