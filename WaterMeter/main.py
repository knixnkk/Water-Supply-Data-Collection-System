from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import timedelta
from user.models import User
import os
import linkedDB as db
import linkedHistory as history
from flask import Flask, session
import pymongo
from pymongo import MongoClient
import requests
import socket   
from datetime import datetime
import json

hostname=socket.gethostname()   
hostip=socket.gethostbyname(hostname)     
app = Flask(__name__, static_url_path = "/static", static_folder = "static")

@app.route("/")
def home():
    if len(session) != 0:
        username = db.check_for_user(session["username"])
        if(username):
            return render_template("indexSession.html")
    return render_template("indexNotSession.html")
@app.route("/dashboard")
def dashboard():
    if len(session) != 0:
        username = db.check_for_user(session["username"])
        if(username):
            addr,unit,price,time,name = db.getDashboard(session["username"])
            #return item['Username'], item["Password"], item["telephone"], item["Addr"], item['Unit'], item["time"]
            
            return render_template("dashboard.html", Unit=unit, addr=addr, Price=int(price)+(int(price)*0.07), time=time, name=name)
    return redirect("/")

@app.route("/contact")
def contactUs():
    if len(session) != 0:
        username = db.check_for_user(session["username"])
        if(username):
            return render_template("contactusSession.html")
    return render_template("contactusNoSession.html")
@app.route("/signin", methods = ['POST', 'GET'])
def login():
    if(request.method == "POST"):
        user = User()
        success_flag = user.login()
        if(success_flag):
            return redirect('/table')
        else:
            return redirect('/signin')
    
    return render_template("signin.html")
@app.route("/signout")
def signout():
    session.clear()
    return redirect('/')

@app.route("/table")
def table():
    currentMonth = datetime.now().strftime("%B")
    if len(session) != 0:
        username = db.check_for_user(session["username"])
        if (username) and session["username"] == "Kina":
            data = db.getAllData()
            #print(data)
            return render_template("table.html", input_data=data, month=currentMonth)
    return redirect("/")

"""Example Payload
data = {
    "Update" : True,
    "Username": "Kina",
    "Unit": "50"
}
"""
@app.route("/updateAPI", methods = ['POST'])
def updateAPI():
    if(request.method == "POST"):
        jsondata = request.get_json()  # Retrieve the JSON data from the request
        print("Received data:", jsondata)  # Print the received data
        for i in jsondata:
            if str(i) == "Update" and jsondata[i]:
                print(jsondata["Username"], jsondata["Unit"])
                db.updateUnit(jsondata["Username"], jsondata["Unit"])
        """
        data= request.form
        for i in jsondata:
            if str(i) == "Update" and data[i]:
                print(data["Username"], data["Unit"])
                db.updateUnit(data["Username"], data["Unit"])
        """
    return "Hello"
if __name__ == "__main__":
    app.secret_key="anystringhere"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host=hostip,debug=True)

##################