from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database and table
def create_table():
    conn = sqlite3.connect("contacts.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

# Display contact form
@app.route('/')
def home():
    return render_template('index.html')

# Save contact details
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect("contacts.db")
    conn.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    conn.commit()
    conn.close()

    return "Contact details submitted successfully!"

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
