import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    """Creates database table to stores the data in sql database"""
    db.execute("CREATE TABLE if not exists details (id INTEGER NOT NULL, name TEXT, symbol TEXT,\
                price NUMERIC, shares NUMERIC, cash NUMERIC, total NUMERIC, grand NUMERIC)")
    db.execute("CREATE TABLE if not exists transactions (id INTEGER NOT NULL, name TEXT, symbol TEXT,\
                price NUMERIC, shares NUMERIC, cash NUMERIC, total NUMERIC, grand NUMERIC, type TEXT )")

    # Feching data from the sql table
    rows = db.execute("SELECT symbol, name, price,\
                        SUM(shares) as shares,\
                        SUM(cash) as cash,\
                        SUM(total) as total,\
                        SUM(grand) as grand\
                        FROM details\
                        WHERE id = ?\
                        GROUP BY symbol", session["user_id"])
    grand = 10000.00

    # """Ensures their will any data"""
    if len(rows) > 0:
        cash = grand - db.execute("SELECT SUM(total) AS total FROM details WHERE id = ?",
                                  session["user_id"])[0]["total"]
    else:
        cash = 0000

    # User reached homepage (as by clicking a link)
    return render_template("index.html", rows=rows, cash=cash, grand=grand)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # Ensures request method is POST
    if request.method == "POST":

        # Fetch data form the user from
        symbol = request.form.get("symbol")

        # Ensures shares is positive integer
        try:
            shares = int(request.form.get("shares"))
            if shares < 0 or isinstance(shares, float):
                return apology("Nagative/Fraction shares aren't allowed.", 400)
        except:
            return apology("Invalid shares!", 400)

        # Ensures existance of stock's symbol
        if not symbol or lookup(symbol) == None:
            return apology("Invalid stock's symbol", 400)

        # if symbol exists
        else:
            price = lookup(symbol)["price"]
            name = lookup(symbol)["name"]
            total = price * int(shares)
            grand_total = 10000.00
            cash = db.execute(
                "SELECT SUM(cash) AS cash FROM DETAILS WHERE id = ? ", session["user_id"])[0]["cash"]
            have_cash = db.execute(
                "SELECT SUM(total) AS total FROM DETAILS WHERE id = ? ", session["user_id"])[0]["total"]

            # Ensures you have inuff cash to buy the shares
            try:
                if have_cash > cash:
                    return apology("You did not have inuff cash to buy shares.")
            except:
                pass

            """Inserting data into database tables"""
            db.execute("INSERT INTO details VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"],
                       name, symbol, price, int(shares), cash, total, grand_total)
            db.execute("INSERT INTO transactions VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"],
                       name, symbol, price, int(shares), cash, total, grand_total, "buy")

        # Redirect the user to homeapge
        return redirect("/")

    # user reached route route by clicking on the link or by redirecting
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Fetch data from the tables
    rows = db.execute(
        "SELECT * FROM transactions WHERE id = ?", session["user_id"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget finance
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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Ensures that request method is GET
    if request.method == "GET":
        return render_template("quote.html")

    # Ensures that request method is POST
    else:
        # Ensures symbol exists in the database
        try:
            symbol = request.form.get("symbol")
            return render_template("quoted.html", data=lookup(symbol))
        except:
            return apology("Symbol not found", 400)


@app.route("/register", methods=["POST", "GET"])
def register():
    """Register user"""

    # Ensures requesr method is POST
    if request.method == "POST":

        # Feching data from the user form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        users = []

        # Fetching data form users database
        user = db.execute("SELECT username FROM users")

        # Storing users name
        for h in user:
            users.append(h["username"])

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure username did not exists
        elif username in users:
            return apology("user already registerd", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password match
        elif not password == confirmation:
            return apology("password did not match", 400)

        else:
            # Generating hatsh of the password
            hashpassword = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8)

            # stroring hash of the password
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                       username, hashpassword)

        # Redirect user to home page
        return redirect("/")

    # user reach route via clicking on link or redirecting
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Ensures request method is POST
    if request.method == "POST":

        # Fetching data from users form
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        # Fetching data from details database
        have_shares = db.execute(
            "SELECT shares FROM details WHERE symbol = ? AND id = ? GROUP BY symbol", symbol, session["user_id"])[0]["shares"]

        # Ensures you have inuff shares to sell
        if int(shares) > have_shares:
            return apology("Insuffient shares!", 400)

        # Fetch data from the details database
        db.execute("UPDATE details\
                    SET shares = shares - ?,\
                        total = total - price * ?\
                        WHERE symbol = ?\
                        AND id = ?", int(shares), int(shares), symbol, session["user_id"])

        price = lookup(symbol)["price"]
        name = lookup(symbol)["name"]
        total = price * int(shares)
        grand_total = 10000.00
        cash = db.execute(
            "SELECT SUM(cash) AS cash FROM DETAILS WHERE id = ? ", session["user_id"])[0]["cash"]

        db.execute("INSERT INTO transactions VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"],
                   name, symbol, price, int(shares), cash, total, grand_total, "sell")

        # Redirecting userd to the homepage
        return redirect("/")

    # user reach route via clicking on link or redirecting
    else:

        # Fetching data from details database
        data = db.execute(
            "SELECT * FROM details WHERE id = ? GROUP BY symbol", session["user_id"])

        return render_template("sell.html", data=data)
