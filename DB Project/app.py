from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'example.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            designation TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == "POST":
        action = request.form['action']
        name = request.form['name']
        designation = request.form['dec']

        db = get_db()
        cursor = db.cursor()

        if action == 'add':
            cursor.execute("INSERT INTO users (name, designation) VALUES (?, ?)", (name, designation))
            db.commit()
            message = f"Added user: {name} with designation: {designation}"

        elif action == 'delete':
            cursor.execute("DELETE FROM users WHERE name=? AND designation=?", (name, designation))
            db.commit()
            message = f"Deleted user: {name} with designation: {designation}"

        elif action == 'list':
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            message = '<br>'.join([str(user) for user in users])

    return render_template('index.html', message=message)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
