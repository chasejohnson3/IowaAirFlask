import pymysql
from flask import render_template, request, session, redirect, flash, send_from_directory, url_for
from flask import Flask
import uuid

import datetime
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())



def dbconn():
    return pymysql.connect(host='35.226.87.238', port=3306, user='root', password='kfoPkgr8xKQC', db='iowa_air_gcp')


def check_for_logged_on():
    conn = dbconn()
    sql = "Select Count(idusers) FROM users WHERE logged_in=1"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows[0][0])
    if rows[0][0] > 0:
        print("Someone is logged on")
    else:
        print("No one is logged on")

    conn.close()


def delete_user_by_id(id):
    conn = dbconn()
    sql = "DELETE FROM users WHERE idusers = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()
    conn.close()



def get_first_name_by_id(id):
    conn = dbconn()
    sql = "SELECT first_name FROM users WHERE idusers = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]

def log_everyone_off():
    conn = dbconn()
    sql = "UPDATE users SET logged_in = 0"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_idusers_by_email(email):
    conn = dbconn()
    sql = "SELECT idusers FROM users WHERE email = %s"
    cursor = conn.cursor()
    cursor.execute(sql, email)
    rows = cursor.fetchall()
    conn.close()
    if cursor.rowcount > 0:
        return str(rows[0][0])
    else:
        return None


def count_users_by_name(first_name):
    conn = dbconn()
    sql = "SELECT COUNT(idusers) FROM users WHERE first_name = %s"
    cursor = conn.cursor()
    cursor.execute(sql, first_name)
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]


def check_if_id_exists(id):
    conn = dbconn()
    sql = "SELECT idusers FROM users WHERE idusers = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.close()
    if cursor.rowcount > 0:
        return True
    else:
        return False


def add_user(email, first_name=None, last_name=None, middle_name=None, suffix=None, preferred_name=None, date_of_birth=None, gender=None, country=None, state=None,
             city=None, address=None, postal_code=None, phone_number=None, password=None, secure_traveler=None):

    # If a user with the given email already exists, do not allow a new email with this email to be created
    if get_idusers_by_email(email) is not None:
        return None
    else:
        conn = dbconn()
        sql = "INSERT INTO users(idusers, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, " \
              "gender, country, state, city, address, postal_code, email, phone_number, password, secure_traveler, " \
              "logged_in) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()

        id = get_uuid()
        print("UUID is " + str(id))
        cursor.execute(sql, (
            id, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, gender, country, state, city,
            address, postal_code, email, phone_number, password, secure_traveler, 1))  # the 1 at the end logs the user in
        current_user_id = id
        # session['username'] = str(id)
        conn.commit()
        conn.close()
        return current_user_id


def check_password_by_email(email, password):
    conn = dbconn()
    cursor = conn.cursor()
    sql = "SELECT idusers FROM users WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, password))
    rows = cursor.fetchall()
    print(rows)
    if cursor.rowcount > 0:
        return True
    return False


@app.route('/')
def home():
    first_name = ""
    idusers = None
    if 'idusers' in session:
        first_name = get_first_name_by_id(session['idusers'])
        idusers = session['idusers']
    return render_template("home.html", first_name=first_name, idusers=idusers)


@app.route('/logout')
def logout():
    session.pop('idusers', None)
    # return render_template('home.html')
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/adduser')
def addUser():
    return render_template('AddUser.html')

@app.route('/bookflight-single')
def bookFlightSingle():
    return render_template('BookFlight-Single.html')

@app.route('/flight-notification')
def flight_notification():
    return render_template('flight-notification.html')

@app.route('/bookflight-roundtrip')
def bookFlightRound():
    return render_template('BookFlight-RoundTrip.html')

@app.route('/bookflight-multicity')
def bookFlightMulti():
    return render_template('BookFlight-MultiCity.html')

@app.route('/login')
def login():
    return render_template('LogIn.html')

@app.route('/bookflight-single', methods=['POST', 'GET'])
def singlesearch():
    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        departure_date = request.form['departure_date']

    conn = dbconn()
    sql = 'SELECT * FROM iowa_air_gcp.flights WHERE `Departing_City` = "'+from_city+'" AND `Arriving_City` = "'+to_city+'" AND `Departure_Datetime` LIKE "' + departure_date + '%";'

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
            data.append(list(temp))
        cursor.close()
        conn.close()
        return render_template("FlightsResult.html", rows=data)

    except:
        return render_template('Empty.html')


@app.route('/empty')
def empty():
    return render_template('Empty.html')


@app.route('/single-result')
def fligtresult():
    return render_template('FlightsResult.html')


@app.route('/round-result')
def fligtresult2():
    return render_template('FlightsResult.html')


@app.route('/bookflight-roundtrip', methods=['POST', 'GET'])
def roundsearch():
    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']

    sql1 = "SELECT * FROM flights WHERE `Departing_City` = %s AND `Arriving_City` = %s AND `Departure_Datetime` = %s;"
    sql2 = "SELECT * FROM flights WHERE `Departing_City` = %s AND `Arriving_City` = %s AND `Departure_Datetime` = %s;"
    conn = dbconn()
    cursor = conn.cursor()

    try:
        cursor.execute(sql1, (from_city, to_city, departure_date))
        rows1 = cursor.fetchall()
        data = []
        for row in rows1:
            temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
            data.append(list(temp))

        cursor.execute(sql2, (to_city, from_city, return_date))
        rows2 = cursor.fetchall()
        for row in rows2:
            temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
            data.append(list(temp))
        cursor.close()
        conn.close()
        return render_template("FlightsResult.html", rows=data)

    except:
        return render_template('Empty.html')

@app.route('/viewall')
def viewall():
    conn = dbconn()
    sql = "SELECT * FROM flights"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    data=[]
    for row in rows:
        temp = [row[1], row[2]]
        data.append(list(temp))
    conn.close()
    return render_template("list.html", rows=data)

@app.route('/flight-link', methods=['POST', 'GET'])
def flightlink():
    if request.method == 'POST':
        id = request.form['id']
        from_ = request.form['from']
        to = request.form['to']
    conn = dbconn()
    cursor = conn.cursor()
    sql = "SELECT * FROM flights WHERE idflights` = %s AND Departing_City` = %s AND `Arriving_City` = %s ;"
    try:
        cursor.execute(sql, (id, from_, to))
        rows = cursor.fetchall()
        data = []
        for row in rows:
            temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
            data.append(list(temp))
        cursor.close()
        conn.close()
        return render_template("flight-link.html", rows=data)

    except:
        return render_template('Empty.html')

    sql = "SELECT * FROM flights WHERE ID=id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    data=[]
    for row in rows:
        temp = [row[1], row[2]]
        data.append(list(temp))
    conn.close()
    return render_template("list.html", rows=data)

  
@app.route('/login', methods=['POST', 'GET'])
def login_action():
    email = request.form['email']
    password = request.form['password']
    if check_password_by_email(email, password):
        session['idusers'] = get_idusers_by_email(email)
    else:
        return render_template("LogIn.html", error="Incorrect Username/Password")

    return render_template("home.html", first_name=get_first_name_by_id(session['idusers']))


# Adds a user's information to the database
@app.route('/adduser', methods=['POST', 'GET'])
def users():
    #log_everyone_off()
    if request.method == 'POST':
        # try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        suffix = request.form['suffix']
        preferred_name = request.form['preferred_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        address = request.form['address']
        postal_code = request.form['postal_code']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        secure_traveler = request.form['secure_traveler']

        user_id = add_user(email, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, gender, country, state,
                 city, address, postal_code, phone_number, password, secure_traveler)
        if user_id is not None:
            session['idusers'] = user_id
            msg = "Record successfully added"
            return render_template("users.html", result=request.form, msg=msg)
        else:
            return render_template("AddUser.html", error="A user with this email already exists")
        conn.close()



def get_uuid():
    id = str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(
    datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)
    return id

class searchError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    app.run(debug=True)
