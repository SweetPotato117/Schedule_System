from flask import Flask, render_template,url_for,request,session,redirect,g
import os
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "website"

mysql = MySQL(app)






#routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    cur = mysql.connection.cursor()

    users = cur.execute("SELECT * FROM users")
    if users > 0:
        userDetails = cur.fetchall()
    
    return render_template('login.html', userDetails = users)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)", (id, username, password))

        mysql.connection.commit() 

        cur.close()

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

