import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter- don't  need this for studybuddy
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///studybuddy.db")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
 # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Missing username.")
        elif not password:
            return apology("Missing password.")
        elif password != request.form.get("confirmation"):
            return apology("Passwords do not match.")
        elif not username.lower().endswith("@yale.edu"):
            return apology("Username must be a valid yale email.")
        insert = db.execute("INSERT INTO users (username, password) VALUES (:username, :hash)", username = request.form.get("username"), hash = generate_password_hash(request.form.get("password")))
        if not insert:
            return apology("Your username is already taken.")
        session["user_id"] = insert
        flash("You are registered.")
        return redirect("/")


#not sure if you need methods for this
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    """display all posts"""
    if request.method == "GET":
        db.execute("TODO")
        return render_template("feed.html")
    if request.method == "POST":
        return redirect("/")


@app.route("/myposts")
@login_required
def myposts():
    """Show history of posts"""
    return render_template("myposts.html")



@app.route("/guts", methods=["GET", "POST"])
@login_required
def guts():
    if request.method == "GET":
        return render_template("guts.html")
    if request.method == "POST":


@app.route("/studyguides", methods=["GET", "POST"])
@login_required
def studyguides():
    """make a studyguide"""
    if request.method == "GET":
        return render_template("studyguides.html")
    if request.method == "POST":
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
