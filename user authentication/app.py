
from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Create database
def create_table():
    con = sqlite3.connect("users.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    con.commit()
    con.close()

create_table()

# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if len(username) < 3 or len(password) < 8:
            message = "Username must have 3 characters and password 8 characters."
        else:
            hashed_password = generate_password_hash(password)

            try:
                con = sqlite3.connect("users.db")
                con.execute(
                    "INSERT INTO users(username, password) VALUES (?, ?)",
                    (username, hashed_password)
                )
                con.commit()
                con.close()

                return redirect("/login")

            except sqlite3.IntegrityError:
                message = "Username already exists."

    return render_template_string("""
        <h2>User Registration</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <br><br>
            <input type="password" name="password"
                   placeholder="Password" required>
            <br><br>
            <button type="submit">Register</button>
        </form>
        <p>{{ message }}</p>
        <a href="/login">Login</a>
    """, message=message)


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        con = sqlite3.connect("users.db")
        user = con.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        con.close()

        if user and check_password_hash(user[2], password):
            session.clear()
            session["username"] = username
            return redirect("/home")
        else:
            message = "Invalid username or password."

    return render_template_string("""
        <h2>User Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <br><br>
            <input type="password" name="password"
                   placeholder="Password" required>
            <br><br>
            <button type="submit">Login</button>
        </form>
        <p>{{ message }}</p>
        <a href="/register">Register</a>
    """, message=message)


# Home page (only for logged-in users)
@app.route("/home")
def home():
    if "username" not in session:
        return redirect("/login")

    return render_template_string("""
        <h2>Welcome, {{ username }}!</h2>
        <p>You are successfully logged in.</p>
        <a href="/logout">Logout</a>
    """, username=session["username"])


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
