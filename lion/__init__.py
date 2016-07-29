import os
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import gc
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/lion'


db = SQLAlchemy(app)

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    
    id = db.Column('id', db.Integer, primary_key=True)
    fname = db.Column('fname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    username = db.Column('username', db.Unicode)
    email = db.Column('email', db.Unicode)
    password = db.Column('password', db.Unicode)
    admin = db.Column('admin', db.Boolean)
    
    def __init__(self, fname, lname, username, email, password, admin):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        
        
class Press(db.Model):
    __tablename__ = 'press'
    
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode)
    body = db.Column('body', db.Unicode)
    author = db.Column('author', db.Unicode)
    date_posted = db.Column('date_posted', db.DateTime)
    
    def __init__(self, title, body, author, date_posted):
        self.title = title
        self.body = body
        self.author = author
        self.date_posted = date_posted
        
        
class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    telephone = db.Column('telephone', db.Unicode)
    email = db.Column('email', db.Unicode)
    msg = db.Column('msg', db.Unicode)
    
    def __init__(self, name, telephone, email, msg):
        self.name = name
        self.telephone = telephone
        self.email = email
        self.msg = msg
        
        
    
        
        
        
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('volunteer_login'))
    return wrap

import lion.views