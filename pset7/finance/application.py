from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Logged in homepage - show user their holdings."""
    
    # greet user
    getuser = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    crntuser = getuser[0]["username"]
    
    # get user cash
    usercash = getuser[0]["cash"]

    # get user individual stock holdings
    holdings = db.execute("SELECT symbol, SUM(num_shares) AS TotalShares FROM holdings GROUP BY symbol, user_id HAVING user_id = :userid", userid=session["user_id"])
    
    # create list for lookup dicts
    stocklist = []
    
    # use yahoo to lookup symbol values, apend to stocklist
    for purchaserow in holdings:
        lookupval = lookup(purchaserow["symbol"])
        lookupval["numshares"] = purchaserow["TotalShares"]
        stocklist.append(lookupval)
    
    # calculate current stock values
    stocksvalue = 0
    stockvalue = 0
    
    # iterate through stockholdings, append current price, add to value
    for stockrow in stocklist:
        stockvalue = (stockrow["numshares"]*stockrow["price"])
        stocksvalue = stocksvalue + stockvalue

    totalval = usercash+stocksvalue
        
    return render_template("index.html", username=crntuser, cash=usd(usercash), stocks=stocklist, stocksvalue=usd(stocksvalue), total=usd(totalval))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """ Allow user to update their password """
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure current password was submitted
        if not request.form.get("currentpassword"):
            return apology("must provide current password")

        # ensure new password was submitted
        elif not request.form.get("newpassword"):
            return apology("must provide new password")
            
        # ensure new password was confirmed
        elif not request.form.get("cnfmnewpassword"):
            return apology("must confirm provide new password")
        
        # ensure passwords match
        if request.form.get("newpassword") != request.form.get("cnfmnewpassword"):
            return apology("new password must match")
            
        # hash current password
        hashc = pwd_context.encrypt(request.form.get("currentpassword"))
        
        # identify user
        currentuser = session["user_id"]
        
        # check that current password matches input
        hashp = db.execute("SELECT hash FROM users WHERE id = :userid", userid=currentuser)

        if hashc != hashp[0]["hash"]:
            return apology("current password does not match existing password")
        
        # hash new password
        hashn = pwd_context.encrypt(request.form.get("newpassword"))
        
        # valid password change, insert into user table
        db.execute("UPDATE users SET hash = :hash WHERE id = :user", hash=hashn, user=currentuser)
        
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("profile.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Allow user to buy new stocks with cash."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide company symbol to purchase")

        # ensure password was submitted
        elif not request.form.get("shares"):
            return apology("must provide number of shares to purchase")
        
        # use yahoo to lookup symbol
        symbol = request.form.get("symbol")
        
        lookupval = lookup(symbol)
        
        # check if symbol was valid
        if lookupval == None:
            return apology("symbol was not valid")
        
        # ensure order shares is positive integer
        num_order = int(request.form.get("shares"))
        
        if num_order < 1:
            return apology("number of shares must be greater than 0")
        
        # calculate cost of transaction
        cost = lookupval["price"]*num_order
        
        # retrieve user funds
        funds = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        
        # check user funds against share purchase cost
        if funds[0]["cash"] < cost:
            return apology("you do not have sufficient funds to complete this transaction")
        
        # valid purchase, check if user holds that stock already
        if not db.execute("SELECT symbol FROM holdings WHERE symbol = :symbol AND user_id = :user", symbol=request.form.get("symbol"), user=session["user_id"]):
            
            # if not, insert into holdings table
            db.execute("INSERT INTO holdings (user_id, symbol, num_shares) VALUES(:user, :symbol, :num_shares)", user=session["user_id"], symbol=request.form.get("symbol"), num_shares=request.form.get("shares"))
        
        else:
            
            # update num_shares
            db.execute("UPDATE holdings SET num_shares = (num_shares + :num_order) WHERE user_id = :user AND symbol = :symbol", num_order=num_order, user=session["user_id"], symbol=request.form.get("symbol"))
        
        # update user balance
        db.execute("UPDATE users SET cash = (cash - :cost) WHERE id = :user", cost=cost, user=session["user_id"])
        
        # update user history
        db.execute("INSERT INTO userhistory (user_id, type, symbol, value, num_shares) VALUES(:user, :type, :symbol, :value, :num_shares)", user=session["user_id"], type="bought", symbol=request.form.get("symbol"), value=cost, num_shares=request.form.get("shares"))
            
        return redirect(url_for("index"))
            
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Allow user to see their transaction history."""
    
    # get user individual stock holdings
    history = db.execute("SELECT * FROM userhistory WHERE user_id = :userid", userid=session["user_id"])
    
    # create list for history dicts
    historylist = []
    
    # append histories to historylist
    for historyrow in history:
        historylist.append(historyrow)
        
        
    return render_template("history.html", histories=historylist)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure quote was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol to quote")
        
        # use yahoo to lookup symbol
        symbol = request.form.get("symbol")
        
        lookupval = lookup(symbol)
        
        # check if symbol was valid
        if lookup(symbol) == None:
            return apology("symbol to quote was not valid")
        
        retsymbol = lookupval["symbol"]
        retprice = usd(lookupval["price"])
        retname = lookupval["name"]
        
        # redirect user to quote data
        return render_template("quotereturn.html", symbol=retsymbol, name=retname, price=retprice)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        # ensure confirm password was submitted
        elif not request.form.get("rptpassword"):
            return apology("must confirm password")
        
        # ensure password matches confirm 
        if request.form.get("password") != request.form.get("rptpassword"):
            return apology("passwords must match")

        # query database for username, if exists, reject
        result = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        if result:
            return apology("username already exists")
            
        # hash password
        hash = pwd_context.encrypt(request.form.get("password"))
        
        # valid registration, insert into user table
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
            
        # find the username
        rowst = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            
        # log in user
        session["user_id"] = rowst[0]["id"]
            
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Allow user to sell stocks they own."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide company symbol to purchase")

        # ensure number to sell was submitted
        elif not request.form.get("numtosell"):
            return apology("must provide number of shares to sell")
        
        # use yahoo to lookup symbol
        symbol = request.form.get("symbol")
        
        lookupval = lookup(symbol)
        
        # check if symbol was valid
        if lookupval == None:
            return apology("symbol was not valid")
        
        # ensure num sold shares is positive integer
        num_sell = int(request.form.get("numtosell"))
        
        if num_sell < 1:
            return apology("number of shares must be greater than 0")
        
        # calculate value of transaction
        salevalue = lookupval["price"]*num_sell
        
        # get user individual stock holdings
        holdings = db.execute("SELECT symbol, SUM(num_shares) AS TotalShares FROM holdings GROUP BY symbol HAVING user_id = :userid AND symbol = :symbol", userid=session["user_id"], symbol=request.form.get("symbol"))
        
        # check if user even owns that stock
        if not holdings:
            return apology("you do not have sufficient shares to complete this transaction")
            
        # check user holdings against desired sale
        if holdings[0]["TotalShares"] < num_sell:
            return apology("you do not have sufficient shares to complete this transaction")
            
        # update num_shares
        db.execute("UPDATE holdings SET num_shares = (num_shares - :num_sell) WHERE user_id = :user AND symbol = :symbol", num_sell=num_sell, user=session["user_id"], symbol=request.form.get("symbol"))
        
        # update user balance
        db.execute("UPDATE users SET cash = (cash + :salevalue) WHERE id = :user", salevalue=salevalue, user=session["user_id"])
        
        # update user history
        db.execute("INSERT INTO userhistory (user_id, type, symbol, value, num_shares) VALUES(:user, :type, :symbol, :value, :num_shares)", user=session["user_id"], type="sold", symbol=request.form.get("symbol"), value=salevalue, num_shares=num_sell)
            
        return redirect(url_for("index"))
            
    else:
        return render_template("sell.html")

