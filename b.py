from flask import Flask, render_template, request
import sqlite3

class Web:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/about', 'about', self.about)
        self.app.add_url_rule('/contacts', 'contacts', self.contacts)
        self.app.add_url_rule('/call', 'call', self.call)
        self.app.add_url_rule('/reg', 'reg', self.reg, methods=['GET', 'POST'])

        self.init_sqlite_db()

    def init_sqlite_db(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                nickname TEXT NOT NULL,
                work TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def index(self):
        return render_template('index.html')

    def about(self):
        return render_template('about.html')

    def contacts(self):
        return render_template('contacts.html')

    def call(self):
        return render_template('call.html')

    def reg(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            nickname = request.form['nickname']
            work = request.form['work']
            address = request.form['address']
            self.save_to_db(email, nickname, work, address, password)
            return 'Form submitted successfully!'
        return render_template('reg.html')

    def save_to_db(self, email, nickname, work, address, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, nickname, work, address, password) VALUES (?, ?, ?, ?, ?)', 
                       (email, nickname, work, address, password))
        conn.commit()
        conn.close()

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    ap = Web()
    ap.run()
