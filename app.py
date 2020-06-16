from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import random
from helpers import *

# Configure application
app = Flask(__name__)

# Set Secret Key
app.secret_key=str(hash(random.uniform(0,1)))

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set session type = filesystem
app.config["SESSION_TYPE"] = "filesystem"

# Setup database connection
db = DB_Handler('nostos.db')

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Landing page: Login"""
    return redirect("/fireplace")
    #return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    """User login page"""

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        res = list(db.execute("SELECT * FROM User WHERE Username = ?", username))
        
        if len(res) == 0:
            return render_template("login.html", error = "Incorrect username.")

        if check_password_hash(res[0][2], password):
            session["user_id"] = res[0][0]
            return redirect("/fireplace")
        else:
            return render_template("login.html", error = "Incorrect password.")

    return render_template("login.html")


@app.route("/register", methods=["POST","GET"])
def register():
    """User registration page"""
    if request.method == "POST":

        error = None

        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re-password")

        hash_pwd = generate_password_hash(password)
        print(username)
        print(password)
        print(re_password)

        if len(list(db.execute("SELECT * FROM User WHERE Username=?", username))) > 0:
            error = "Username already exists!"
        elif password == '':
            error = "No password!"
        elif re_password == '':
            error = "No re-password!"
        elif password != re_password:
            error = "Password mismatch!"

        if error:
            return render_template("register.html", error = error)
        
        db.execute("INSERT INTO User (Username, Hash_pwd) VALUES (?, ?)", username, hash_pwd)
        return render_template("register.html", success = True)
    return render_template("register.html")
    
@app.route("/fireplace")
@login_required
def fireplace():
    """Fireplace: Logged in Home page for User"""

    return render_template("fireplace.html")


@app.route("/study", methods=["POST", "GET"])
@login_required
def study():
    """Study:  Page for work related things"""

    # TODO
    return render_template("study.html")


@app.route("/tasks", methods=["POST", "GET"])
@login_required
def tasks():
    """Study: Page for work related things"""

    """
    1. get all of MY dos from doables table
    
    2. POST::
        2.1 check if not already in doables, by name
        2.2 if not already
            2.2.1 insert new doable
        2.3 Reload page
    
    """

    if request.method == "POST":

        # Details of new doable
        new_do = request.form.get("name")
        notes = request.form.get("description")
        ref = request.form.get("references")

        print(new_do)

        query = "INSERT INTO Doables (User_ID, Name, note, reference) VALUES (?, ?, ?, ?);"
        db.execute(query, session["user_id"], new_do, notes, ref)

        
    query = "SELECT ID, User_ID, Name, note, reference, done FROM Doables WHERE User_ID = ?;"
    
    dos = list(db.execute(query, session["user_id"]))

    return render_template("tasks.html", data=dos)

@app.route("/tasks_done", methods=["POST"])
@login_required
def tasks_done():
    """
    Update item in doables ("Doables" table) records for 'done' value
    """
    
    done = request.form.get("done")
    item_id = request.form.get("item_id")
    try:
        query = "UPDATE Doables SET done = ? WHERE User_ID = ? AND ID = ?;"
        result = list(db.execute(query, done, session["user_id"], item_id))
        return "1"
    except:
        return "0"

@app.route("/tasks_del", methods=["POST"])
@login_required
def tasks_del():
    """
    Delete item from doables ("Doables" table) records 
    """

    item_id = request.form.get("item_id")
    try:
        query = "DELETE FROM Doables WHERE User_ID = ? AND ID = ?;"
        db.execute(query, session["user_id"], item_id)
        return "1"
    except:
        return "0"


@app.route("/library", methods=["POST", "GET"])
@login_required
def library():
    """Tasks: Page for tasks to be done"""
    
    """
    1. get all of MY readables
        1.1 join tables read and readables
        1.2 filter select for only mine
    
    2. POST::
        2.1 check if not already in readables, by name
        2.2 if not already
            2.2.1 insert new readable
        2.3 if not in MY Reads
            2.3.1 insert references in Read
        2.4 Reload page
    
    """
    print("called lib also")
    if request.method == "POST":

        # Details of new book to add to reads list
        new_book = request.form.get("name")
        notes = request.form.get("description")
        ref = request.form.get("references")

        # Check if book already exists with DB
        query = "SELECT * FROM Readables WHERE Name = ?;"
        res = list(db.execute(query, new_book))

        # If does not exist, add it to DB
        if len(res) == 0:
            query = "INSERT INTO Readables (Name, reference) VALUES (?, ?);"
            db.execute(query, new_book, ref)

        # Check if book already in User's Read list
        query = "SELECT * FROM Readables JOIN Read on Read.Read_ID = Readables.ID WHERE Read.User_ID = ? AND Readables.Name = ?;"
        toread = list(db.execute(query, session["user_id"], new_book))

        # If no result (doesn't exist), add it
        if len(toread) == 0:
            query = "SELECT ID FROM Readables WHERE Name = ?"
            read_id = list(db.execute(query, new_book))[0][0]
            query = "INSERT INTO Read (User_ID, Read_ID, note, done) VALUES (?, ?, ?, 0);"
            print(read_id, res)
            res = db.execute(query, session["user_id"], read_id, notes)
    
    
    query = "SELECT Read.Read_ID, Read.User_ID, Readables.Name, Read.note, Readables.reference, Read.done, User.Username FROM Read JOIN Readables ON Read.Read_ID = Readables.ID JOIN User ON User.ID = Read.User_ID WHERE User_ID = ? ;"
    reads = list(db.execute(query, session["user_id"]))

    return render_template("library.html", data=reads)

@app.route("/library_done", methods=["POST"])
@login_required
def library_done():
    """
    Update item in library ("Read" table) records for 'done' value
    """
    
    done = request.form.get("done")
    item_id = request.form.get("item_id")
    try:
        query = "UPDATE Read SET done = ? WHERE User_ID = ? AND Read_ID = ?;"
        result = list(db.execute(query, done, session["user_id"], item_id))
        return "1"
    except:
        return "0"

@app.route("/library_del", methods=["POST"])
@login_required
def library_del():
    """
    Delete item from library ("Read" table) records 
    """

    item_id = request.form.get("item_id")
    try:
        query = "DELETE FROM Read WHERE User_ID = ? AND Read_ID = ?;"
        db.execute(query, session["user_id"], item_id)
        return "1"
    except:
        return "0"

@app.route("/leisure")
@login_required
def leisure():
    """Leisure: Page for leisurely activities"""

    # TODO
    return render_template("leisure.html")

@app.route("/play", methods=["POST", "GET"])
@login_required
def play():
    """Games for Playing"""

    """
    1. get all of MY games
        1.1 join tables play and playables
        1.2 filter select for only mine
    
    2. POST::
        2.1 check if not already in playables, by name
        2.2 if not already
            2.2.1 insert new playable
        2.3 if not in MY Plays
            2.3.1 insert references in Play
        2.4 Reload page
    
    """

    if request.method == "POST":

        # Details of new game to add to play list
        new_game = request.form.get("name")
        notes = request.form.get("description")
        ref = request.form.get("references")
        
        print(new_game)

        # Check if game already exists with DB
        query = "SELECT * FROM Playables WHERE Name = ?;"
        res = list(db.execute(query, new_game))

        # If does not exist, add it to DB
        if len(res) == 0:
            query = "INSERT INTO Playables (Name, reference) VALUES (?, ?);"
            db.execute(query, new_game, ref)

        # Check if game already in User's Play list
        query = "SELECT * FROM Playables JOIN Play on Play.Play_ID = Playables.ID WHERE Play.User_ID = ? AND Playables.Name = ?;"
        toplay = list(db.execute(query, session["user_id"], new_game))

        # If no result (doesn't exist), add it
        if len(toplay) == 0:
            query = "SELECT ID FROM Playables WHERE Name = ?"
            play_id = list(db.execute(query, new_game))[0][0]
            query = "INSERT INTO Play (User_ID, Play_ID, note, done) VALUES (?, ?, ?, 0);"
            print(play_id, res)
            res = db.execute(query, session["user_id"], play_id, notes)
    
    
    query = "SELECT Play.Play_ID, Play.User_ID, Playables.Name, Play.note, Playables.reference, Play.done, User.Username FROM Play JOIN Playables ON Play.Play_ID = Playables.ID JOIN User ON User.ID = Play.User_ID WHERE User_ID = ? ;"
    
    games = list(db.execute(query, session["user_id"]))

    return render_template("play.html", data=games)


@app.route("/play_done", methods=["POST"])
@login_required
def play_done():
    """
    Update item in play ("Play" table) records for 'done' value
    """
    
    done = request.form.get("done")
    item_id = request.form.get("item_id")

    try:
        query = "UPDATE Play SET done = ? WHERE User_ID = ? AND Play_ID = ?;"
        result = list(db.execute(query, done, session["user_id"], item_id))
        return "1"
    except:
        return "0"

@app.route("/play_del", methods=["POST"])
@login_required
def play_del():
    """
    Delete item from play ("Play" table) records 
    """

    item_id = request.form.get("item_id")

    try:
        query = "DELETE FROM Play WHERE User_ID = ? AND Play_ID = ?;"
        db.execute(query, session["user_id"], item_id)
        return "1"
    except:
        return "0"


@app.route("/watch", methods=["POST","GET"])
@login_required
def watch():
    """Watching"""

    """Games for Playing"""

    """
    1. get all of MY movs
        1.1 join tables watch and watchables
        1.2 filter select for only mine
    
    2. POST::
        2.1 check if not already in watchables, by name
        2.2 if not already
            2.2.1 insert new watchables
        2.3 if not in MY Watchs
            2.3.1 insert references in Watch
        2.4 Reload page
    
    """

    if request.method == "POST":

        # Details of new game to add to play list
        new_mov = request.form.get("name")
        notes = request.form.get("description")
        ref = request.form.get("references")
        
        print(new_mov)

        # Check if mov already exists with DB
        query = "SELECT * FROM Watchables WHERE Name = ?;"
        res = list(db.execute(query, new_mov))

        # If does not exist, add it to DB
        if len(res) == 0:
            query = "INSERT INTO Watchables (Name, reference) VALUES (?, ?);"
            db.execute(query, new_mov, ref)

        # Check if mov already in User's Play list
        query = "SELECT * FROM Watchables JOIN Watch on Watch.Watch_ID = Watchables.ID WHERE Watch.User_ID = ? AND Watchables.Name = ?;"
        towatch = list(db.execute(query, session["user_id"], new_mov))

        # If no result (doesn't exist), add it
        if len(towatch) == 0:
            query = "SELECT ID FROM Watchables WHERE Name = ?"
            watch_id = list(db.execute(query, new_mov))[0][0]
            query = "INSERT INTO Watch (User_ID, Watch_ID, note, done) VALUES (?, ?, ?, 0);"
            print(watch_id, res)
            res = db.execute(query, session["user_id"], watch_id, notes)
    
    
    query = "SELECT Watch.Watch_ID, Watch.User_ID, Watchables.Name, Watch.note, Watchables.reference, Watch.done, User.Username FROM Watch JOIN Watchables ON Watch.Watch_ID = Watchables.ID JOIN User ON User.ID = Watch.User_ID WHERE User_ID = ? ;"
    
    movs = list(db.execute(query, session["user_id"]))

    return render_template("watch.html", data=movs)


@app.route("/watch_done", methods=["POST"])
@login_required
def watch_done():
    """
    Update item in watch ("Watch" table) records for 'done' value
    """
    
    done = request.form.get("done")
    item_id = request.form.get("item_id")

    try:
        query = "UPDATE Watch SET done = ? WHERE User_ID = ? AND Watch_ID = ?;"
        result = list(db.execute(query, done, session["user_id"], item_id))
        return "1"
    except:
        return "0"

@app.route("/watch_del", methods=["POST"])
@login_required
def watch_del():
    """
    Delete item from watch ("Watch" table) records 
    """

    item_id = request.form.get("item_id")

    try:
        query = "DELETE FROM Watch WHERE User_ID = ? AND Watch_ID = ?;"
        db.execute(query, session["user_id"], item_id)
        return "1"
    except:
        return "0"

def errorhandler(e):
    """Handle error"""
    return render_template("error.html", error=e.code)

# Listen for errors of all types (every error code)
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)