from flask import Flask, render_template,url_for,request,session,redirect,g
import os
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = '12345'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "website"

mysql = MySQL(app)

#routes
@app.route('/')
def home():
    return render_template('home.html')


# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select id, password from users where id = {id}")
        user = cur.fetchone()
        cur.close()
        if user is None:
            return render_template('login.html', error ='You do not have an account')
        elif id and password == user[1]:
            session['id'] = user[0]
            return render_template('mainp.html')
        else:
            return render_template('login.html', error ='Invalid or wrong password')
    return render_template('login.html')


#register
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

@app.route('/mainp')
def main():
    return render_template('/mainp.html')


if __name__ == '__main__':
    app.run(debug=True)

