from flask import Flask, jsonify, request, render_template, redirect, flash, url_for, session
from passlib.hash import pbkdf2_sha256
import uuid
import linkedDB as db
import datetime
import requests

# Line variables
url = 'https://notify-api.line.me/api/notify'
token = 'xxxxxxxxxxxxxxxxx'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
##################
class User:


    def signup(self):
        """Signs a user up by creating a new entry to the database. Main use
        is with the registration page.
        """
        mydate = datetime.datetime.now()
        timenow = (mydate.strftime("%X"))
        user = {
            "_id": uuid.uuid4().hex,
            "citizenid": request.form.get('citizen'),
            "username": request.form.get('username'),
            "telephone": request.form.get('tele'),
            "seat" : None,
            "status" : None,
            "time" : timenow
        }
        # Check for duplicate entries
        if db.check_for_user(user["citizenid"]) or db.checkUser(user["username"]) or db.checkTelephone(user["telephone"]):
            return False
        else:
            db.add_user(user)
            return True
    def login(self):
        """Checks for user on database and assigns a session for them accordignly.
        """
        #print(db.getData(request.form.get('username')))
        # Get user from database by email
        user_exists = db.check_for_user(request.form.get('username'))
        user = db.get_user(request.form.get('username'))
        listData = db.getData(request.form.get('username'))
        
        # Check user credentials
        """
        if user_exists and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            session['username'] = request.form.get('name')
            return True
        else:
            return False
        """
        if user_exists and listData[1] == request.form.get('password'):
            session['username'] = request.form.get('username')
            session['password'] = request.form.get('password')
            return True
        else:
            return False
    def logout(self):
        if 'username' in session:
            session.pop('username')
            return True
        else:
            return False