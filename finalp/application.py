from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from addfunctions import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///scheduler.db")

@app.route("/")
@login_required
def index():
    """Logged in homepage"""
    
    # get user individual availabilities
    availability = db.execute("SELECT selected_dt, availability_id FROM availability WHERE user_id = :userid", userid=session["user_id"])
    
    availlist = []
    
    # reformat relative availabities into human readable format
    for dtrow in availability:
        dtrow["selected_dt"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dtrow["selected_dt"]))
        availlist.append(dtrow)
        
    return render_template("index.html", availability = availlist)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()
    
    # if user reached route via POST
    if request.method == "POST":

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE email_address = :email_address", email_address=request.form.get("email_address"))

        # check user and password, flash error if need
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash('Invalid credentials')
            return render_template("login.html")
        
        # login
        else:
            # remember which user has logged in
            session["user_id"] = rows[0]["user_id"]
            flash('You were successfully logged in')
            return redirect(url_for('index'))
            
    # else if user reached route via GET
    else:
        return render_template("login.html")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # query database for username, if exists, reject
        result = db.execute("SELECT * FROM users WHERE email_address = :email_address", email_address=request.form.get("email_address"))
        
        if result:
            flash('This email address is already associated with an account')
            return redirect(url_for("register"))
            
        # hash password
        hash = pwd_context.encrypt(request.form.get("password"))
        
        # valid registration, insert into user table
        db.execute("INSERT INTO users (email_address, hash, first_name, last_name) VALUES(:email_address, :hash, :first_name, :last_name)", email_address=request.form.get("email_address"), hash=hash, first_name=request.form.get("first_name"), last_name=request.form.get("last_name"))
            
        # find the user
        rowst = db.execute("SELECT * FROM users WHERE email_address = :email_address", email_address=request.form.get("email_address"))
            
        # log in user
        session["user_id"] = rowst[0]["user_id"]
            
        # valid registration, add pref rows
        db.execute("INSERT INTO prefs (user_id) VALUES (:userid)", userid=session["user_id"])
        
        flash('You were successfully registered')
            
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))
    
@app.route("/find", methods=["GET", "POST"])
def find():
    """Allow user to find friends"""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # query for other users with close match to user search
        friendslist = db.execute("SELECT first_name || ' ' || last_name AS full_name, user_id FROM users WHERE full_name LIKE :name", name="%"+request.form.get("friend_name")+"%")
        
        # get user individual relationships (for re-rendering of page)
        relations = db.execute("SELECT * FROM relationships WHERE user_id = :userid OR friend_id = :userid", userid=session["user_id"])
    
        relationlist = []
        
        for rerow in relations:
            relationlist.append(rerow)
    
        userrequest = session["user_id"]
        
        # handle cannot find any users matching search string
        if len(friendslist) != 1:
            flash('No matches')
            return render_template("friends.html", relations=relationlist, user=userrequest)
        
        else:
            return render_template("friends.html", foundfriends=friendslist, relations=relationlist, user=userrequest)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("friends.html")

@app.route("/changepref", methods=["POST"])
def changepref():
    """Handle updates to activity preferences"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db.execute("UPDATE prefs SET :activity = :state WHERE user_id = :user", user=session["user_id"], state=request.form['state'], activity=request.form['activities'])
        return 'Pref updated'

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")
        
@app.route("/addavail", methods=["POST"])
def addavail():
    """Allow user to add availability"""
    
    # call conversion function (send to DB as seconds)
    dtcon = convert_dt_s(request.form.get("dtpicker"))
    
    # update user availability
    db.execute("INSERT INTO availability (user_id, selected_dt) VALUES(:user, :selected_dt)", user=session["user_id"], selected_dt=dtcon)
    return redirect(url_for("index"))
    
@app.route("/addfriend", methods=["POST"])
def addfriend():
    """Allow user to send requests to new friends"""
    
    # get user individual relationships (for re-rendering of page)
    relations = db.execute("SELECT * FROM relationships WHERE user_id = :userid OR friend_id = :userid", userid=session["user_id"])
    
    relationlist = []
    
    userrequest = session["user_id"]
            
    for rerow in relations:
        relationlist.append(rerow)
    
    # handle if user has requested themselves
    if userrequest == request.form.get("friend"):
        flash('You cannot request yourself as a friend')
        return render_template("friends.html", relations=relationlist, user=userrequest)

    # check request against existing relationships
    checkfriend = db.execute("SELECT friend_id, user_id, status FROM relationships WHERE (user_id = :user OR user_id = :friend AND friend_id = :friend OR user_id = :user) AND (status='accepted' OR status='sent')", user=session["user_id"], friend=request.form.get("friend"))

    # handle if user is already friends with requested user, or if a request has already been sent
    if len(checkfriend) > 0:
        flash('You are already have a relationship with that user')
        return render_template("friends.html", relations=relationlist, user=userrequest)
    
    # update relationship
    else:
        db.execute("INSERT INTO relationships (user_id, status, friend_id) VALUES(:user, :status, :friend)", user=session["user_id"], status='sent', friend=request.form.get("friend"))
        flash('Request sent!')
        return render_template("friends.html", relations=relationlist, user=userrequest)

@app.route("/deleteavail", methods=["POST"])
def deleteavail():
    """Allow user to remove availability dates"""
    
    # delete availability posted by user
    db.execute("DELETE FROM availability WHERE availability_id = :selectedavail", selectedavail=request.form.get("discreteavail"))
    
    flash('Availability deleted!')
    return render_template("index.html")

@app.route("/friends")
def friends():
    """Container page for find and adding friends"""
    
    # get user individual relationships
    relations = db.execute("SELECT * FROM relationships WHERE user_id = :userid OR friend_id = :userid", userid=session["user_id"])
    
    relationlist = []
    
    userrequest = session["user_id"]
    
    # append to dict and return to template
    for rerow in relations:
        relationlist.append(rerow)
        
    return render_template("friends.html", relations = relationlist, user = userrequest)
    
@app.route("/acceptrequest", methods=["POST"])
def acceptrequest():
    """Allow user to accept friend requests"""
    
    # update status of pending relationship
    db.execute("UPDATE relationships SET status = 'accepted' WHERE relationship_id = :relationid", relationid=request.form.get("relationid"))

    flash('Request accepted!')
    return render_template("friends.html")

    