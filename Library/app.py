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
            Book TEXT NOT NULL,
            Author TEXT,
            dept TEXT,
            price TEXT
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
        Book = request.form.get('Book')
        Author = request.form.get('Author')
        dept = request.form.get('dept')
        price = request.form.get('price')

        db = get_db()
        cursor = db.cursor()

        if action == 'add':
            cursor.execute("INSERT INTO users (Book, Author,dept,price) VALUES (?, ?,?,?)", (Book, Author,dept,price))
            db.commit()
            message = f"Added user: {Book} with Author: {Author} From Department of : {dept} Price : :price"

        elif action == 'delete':
            cursor.execute("DELETE FROM users WHERE Book=? AND Author=?", (Book, Author,dept,price))
            db.commit()
            message = f"Deleted user: {Book} with Author: {Author} From Department of : {dept} Price :{price}"

        elif action == 'list':
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            message = '<br>'.join([str(user) for user in users])

    return render_template('index.html', message=message)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
