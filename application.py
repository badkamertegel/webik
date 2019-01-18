# https://github.com/MaT1g3R/Python-Trivia-API

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import aiohttp, requests
import urllib.request
import json
from pytrivia import Category, Diffculty, Type, Trivia

app = Flask(__name__)

data = Trivia(True)
response = data.request(2, Category.History ,Diffculty.Hard, Type.Multiple_Choice)
informatie = []

for info in response['results']:
    informatie.append(info)

for element in range(len(informatie)):
    categorie = informatie[element]['category']
    vraag = informatie[element]['question']
    goed_antwoord = informatie[element]['correct_answer']
    foute_antwoorden = informatie[element]['incorrect_answers']
    moeilijkheidsgraad = informatie[element]['difficulty']

print(categorie, vraag, goed_antwoord, foute_antwoorden, moeilijkheidsgraad)


@app.route("/index")
def index():

    categories = ['Maths', 'History']

    if request.method =="POST":

        return redirect(url_for("create.html"))

    else:
        # print(categorie)
        return render_template("index.html", category=categorie, vraag=vraag, goed=goed_antwoord, fout=foute_antwoorden, moeilijkheidsgraad=moeilijkheidsgraad)
@app.route("/")
@login_required
def index():
    return apology("TODO", 200)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must choose a username")

        elif not request.form.get("password"):
            return apology("must choose a password")

        elif not request.form.get("confirmation"):
            return apology("must fill in password again")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords must be the same")

        password = request.form.get("password")
        hash = pwd_context.hash(password)

        result = db.execute("INSERT INTO user2 (username, hash) VALUES (:username, :password)",
                            username=request.form.get("username"), password=hash)

        if not result:
            return apology("username is already in use")
        else:
            return apology("registration complete", 200)

        session["user_id"] = result

        return redirect(url_for("index"))
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM user2 WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return "invalid username and/or password"

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/teacherlogin", methods=["GET","POST"])
def teacherlogin():

    session.clear()


    if request.method == "POST":


        if not request.form.get("username"):
            return apology("must provide username")


        elif not request.form.get("password"):
            return apology("must provide password")


        rows = db.execute("SELECT * FROM teachers WHERE username = :username", username=request.form.get("username"))


        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return "invalid username and/or password"


        session["user_id"] = rows[0]["id"]


        return redirect(url_for("index"))


    else:
        return render_template("login.html")

@app.route("/teacherRegister", methods=["GET","POST"])
def teacherRegister():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must choose a username")

        elif not request.form.get("password"):
            return apology("must choose a password")

        elif not request.form.get("confirmation"):
            return apology("must fill in password again")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords must be the same")

        password = request.form.get("password")
        hash = pwd_context.hash(password)

        result = db.execute("INSERT INTO teachers (username, hash) VALUES (:username, :password)",
                            username=request.form.get("username"), password=hash)

        if not result:
            return apology("username is already in use")
        else:
            return apology("registration complete", 200)

        session["user_id"] = result

        return redirect(url_for("index"))
    else:
        return render_template("register.html")
