import pymysql
from flask import render_template, request, session, redirect, flash, send_from_directory, url_for
from flask import Flask
import uuid

import datetime
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())



def dbconn():
    return pymysql.connect(host='35.226.87.238', port=3306, user='root', password='kfoPkgr8xKQC', db='iowa_air_gcp')


def delete_user_by_id(id):
    conn = dbconn()
    sql = "DELETE FROM users WHERE idusers = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()
    conn.close()


def delete_flight_by_id(id):
    conn = dbconn()
    sql = "DELETE FROM flights WHERE idflights = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()
    conn.close()

def delete_aircraft_by_id(id):
    conn = dbconn()
    sql = "DELETE FROM Aircraft WHERE AircraftID= %s"
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


def get_id_by_flightid(id):
    conn = dbconn()
    sql = "SELECT idflights FROM flights WHERE idflights = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    rows = cursor.fetchall()
    conn.close()
    if cursor.rowcount > 0:
        return str(rows[0][0])
    else:
        return None

def get_id_by_craftname(name):
    conn = dbconn()
    sql = "SELECT AircraftID FROM Aircraft WHERE Name = %s"
    cursor = conn.cursor()
    cursor.execute(sql, name)
    rows = cursor.fetchall()
    conn.close()
    if cursor.rowcount > 0:
        return str(rows[0][0])
    else:
        return None


def get_user_is_admin(id):
    conn = dbconn()
    sql = "SELECT is_admin FROM users WHERE idusers = %s"
    cursor = conn.cursor()
    cursor.execute(sql, id)
    rows = cursor.fetchall()
    conn.close()
    if cursor.rowcount > 0:
        if rows[0][0] is 0:
            return False
        if rows[0][0] is 1:
            return True
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


def count_flights_by_gate(gate):
    conn = dbconn()
    sql = "SELECT COUNT(idflights) FROM flights WHERE Gate = %s"
    cursor = conn.cursor()
    cursor.execute(sql, gate)
    rows = cursor.fetchall()
    conn.close()
    return rows[0][0]


def check_if_id_exists(id):
    conn = dbconn()
    sql = "SELECT idusers FROM users WHERE idusers = %s"
    # sql = "SELECT idusers FROM users WHERE idusers = " + str(id)
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.close()
    if cursor.rowcount > 0:
        return True
    else:
        return False




def add_user(email, first_name=None, last_name=None, password=None, is_admin=False):

    # If a user with the given email already exists, do not allow a new email with this email to be created
    if get_idusers_by_email(email) is not None:
        return None
    else:
        conn = dbconn()
        sql = "INSERT INTO users(idusers, first_name, last_name, email, password, is_admin) " \
              "VALUES(%s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()

        id = get_uuid()
        print("UUID is " + str(id))
        cursor.execute(sql, (id, first_name, last_name, email, password, is_admin))  # the 1 at the end logs the user in
        current_user_id = id
        # session['username'] = str(id)
        conn.commit()
        conn.close()
        return current_user_id



def add_flight( Departure_Datetime="2019-01-01 00:00:00", Arrival_Datetime="2019-01-01 00:00:00", Gate=None,  Aircraft=None, Departing_City=None,  Arriving_City=None):

    # If a user with the given email already exists, do not allow a new email with this email to be created
    id = get_uuid()
    if get_id_by_flightid(id) is not None:
        return None
    else:
        conn = dbconn()
        sql = "CALL add_flight(%s,%s,%s,%s,%s,%s,%s)"
        cursor = conn.cursor()
        cursor.execute(sql, (
            id, Departure_Datetime, Arrival_Datetime, Gate, Aircraft, Departing_City, Arriving_City))
        # session['username'] = str(id)
        conn.commit()
        conn.close()
        return id


def add_aircraft( name, capacity):

    # If a user with the given email already exists, do not allow a new email with this email to be created
    id = get_uuid()
    if get_id_by_craftname(name) is not None:
        return None
    else:
        conn = dbconn()
        sql = "CALL add_aircraft(%s,%s,%s)"
        cursor = conn.cursor()
        cursor.execute(sql, (
            id,name, capacity))
        # session['username'] = str(id)
        conn.commit()
        conn.close()
        return id


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
    is_admin = False
    if 'idusers' in session:
        first_name = get_first_name_by_id(session['idusers'])
        idusers = session['idusers']
        is_admin = get_user_is_admin(idusers)
    return render_template("home.html", first_name=first_name, idusers=idusers, is_admin=is_admin)


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

# @app.route('/viewall')
# def viewAllFlights():
#     return render_template('list.html')

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


def call_find_flight(from_city, to_city, departure_date):
    conn = dbconn()
    sql = "CALL findFlight(%s,%s,%s);"
    cursor = conn.cursor()
    cursor.execute(sql, (from_city, to_city, departure_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.route('/bookflight-single', methods=['POST', 'GET'])
def singlesearch(from_city=None, to_city=None, departure_date=None):
    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        departure_date = request.form['departure_date']

    try:
        rows = call_find_flight(from_city, to_city, departure_date)
        data = []
        for row in rows:
            temp = [row[0], row[1], row[2], from_city, to_city]
            data.append(list(temp))
        return render_template("FlightsResult.html", rows=data, from_city_html=from_city)

    except:
        return render_template('Empty.html')


@app.route('/bookflight-roundtrip', methods=['POST', 'GET'])
def roundsearch():
    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']

    data = []

    try:
        rowsQ = call_find_flight(from_city, to_city, departure_date)
        for row in rowsQ:
            temp = [row[0], row[1], row[2], from_city, to_city]
            data.append(list(temp))

        rowsH = call_find_flight(to_city, from_city, return_date)
        for row in rowsH:
            temp = [row[0], row[1], row[2], to_city, from_city]
            data.append(list(temp))

        return render_template("FlightsResult.html", rows=data)

    except:
        return render_template('Empty.html')


@app.route('/empty')
def empty():
    return render_template('Empty.html')

@app.route('/bookalready')
def bookagain():
    return render_template('BookAlready.html')

@app.route('/nomoreseat')
def nomore():
    return render_template('RunOutOfCapacity.html')


@app.route('/bookConfirm', methods=['POST', 'GET'])
def confirm():
    if 'idusers' in session:
        first_name = get_first_name_by_id(session['idusers'])
        idusers = session['idusers']
        t_flight_id = request.form["flight_id"]
        print(first_name)
        print(idusers)
        print(t_flight_id)
        return render_template("bookConfirm.html", first_name=first_name, idusers=idusers, flightid=t_flight_id)

    else:
        return render_template('LogIn.html', error="You need to login first")


@app.route('/bookSuccess', methods=['POST', 'GET'])
def success():

    flightid = request.form['flight_id']
    userid = request.form['user_id'][0:-1]

    check_number_sql = "SELECT COUNT(idflights) FROM iowa_air_gcp.tickets WHERE idflights = %s"
    check_aircraftid_sql = "SELECT AircraftID FROM iowa_air_gcp.flights WHERE idflights = %s"
    check_capacity_sql = "SELECT Capacity FROM iowa_air_gcp.Aircraft WHERE AircraftID = %s"


    conn = dbconn()
    cursor = conn.cursor()

    cursor.execute(check_number_sql, flightid)
    count = cursor.fetchall()[0][0]

    cursor.execute(check_aircraftid_sql, flightid)
    aircraftid = cursor.fetchall()[0][0]

    cursor.execute(check_capacity_sql, aircraftid)
    capacity = cursor.fetchall()[0][0]

    if(count >= int(capacity)):
        return render_template('RunOutOfCapacity.html')


    try:
        sql = "CALL bookflight(%s,%s);"
        cursor.execute(sql, (flightid, userid))
        conn.commit()
    except:
        return render_template('BookAlready.html')
    cursor.close()
    conn.close()
    return render_template("bookSuccess.html")



@app.route('/single-result')
def fligtresult():
    return render_template('FlightsResult.html')


@app.route('/round-result')
def fligtresult2():
    return render_template('FlightsResultRound.html')


@app.route('/addflight')
def addFlight():
    if request.method == 'POST':
        id = request.form['id']
    conn = dbconn()
    cursor = conn.cursor()
    sql = "SELECT Name FROM Aircraft;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            temp = [row[0]]
            data.append(list(temp))
        cursor.close()
        conn.close()
        return render_template('AddFlight.html', rows=data)


    except:
        return render_template('Empty.html')


@app.route('/addcraft')
def addCraft():
    return render_template('AddAircraft.html')


@app.route('/bookflight-roundtrip', methods=['POST', 'GET'])
def roundsearch2():
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


def get_count_of_flights():
    conn = dbconn()
    sql = "Select * from flights;"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows.__len__()


def view_all_flights():
    conn = dbconn()
    sql = "CALL view_all_flights;"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.route('/viewall')
def viewall():
    rows = view_all_flights()
    data = []
    for row in rows:
        data.append(row)
    return render_template("list.html", rows=data)


@app.route('/deleteFlight', methods=['POST', 'GET'])
def deleteFlight():
    delete_flight_by_id(request.form['flight_id'])
    return render_template("deletedFlight.html")

@app.route('/editFlightPage', methods=['POST', 'GET'])
def editFlightPage():
    flight_id=request.form['flight_id']
    departure_datetime=request.form['departure_time']
    arrival_datetime=request.form['arrival_time']
    gate=request.form['gate']
    aircraft_name=request.form['aircraft_name']
    departing_city=request.form['departing_city']
    arriving_city=request.form['arriving_city']

    departure_date = departure_datetime.split(" ")[0]
    departure_time = departure_datetime.split(" ")[1]
    arrival_date = arrival_datetime.split(" ")[0]
    arrival_time = arrival_datetime.split(" ")[1]

    print("departure time is " + departure_time)

    return render_template("editFlight.html", flight_id=flight_id,
                           departure_time=departure_time,
                           departure_date=departure_date,
                           arrival_time=arrival_time,
                           arrival_date=arrival_date,
                           gate=gate,
                           aircraft_name=aircraft_name,
                           departing_city=departing_city,
                           arriving_city=arriving_city)

def get_gate_by_flight_id(flight_id):
    sql = "Select Gate from flights WHERE idflights=%s"
    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute(sql, flight_id)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows[0][0]


@app.route('/editFlight', methods=['POST', 'GET'])
def editFlight():
    # for key in request.form.keys():
    #     print(key + ": " + request.form.keys[key])
    flight_id = request.form['flight_id']
    departure_time = request.form['departure_date'] + " " + request.form['departure_time']
    arrival_time = request.form['arrival_date'] + " " + request.form['arrival_time']
    gate = request.form['gate']
    aircraft_name = request.form['aircraft_name']
    departing_city = request.form['departing_city']
    arriving_city = request.form['arriving_city']
    new_aircraft_id = get_uuid()
    new_d_city_id = get_uuid()
    new_a_city_id = get_uuid()
    new_endpoints_id = get_uuid()
    conn = dbconn()
    sql = "CALL update_flight(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor = conn.cursor()
    cursor.execute(sql, (flight_id,
                         departure_time,
                         arrival_time,
                         gate,
                         aircraft_name,
                         departing_city,
                         arriving_city,
                         new_aircraft_id,
                         new_d_city_id,
                         new_a_city_id,
                         new_endpoints_id))
    conn.commit()
    return render_template("updateFlightConfirmation.html", gate=gate)


@app.route('/flight-link', methods=['POST', 'GET'])
def flightlink():
    if request.method == 'POST':
        id = request.form['id']

    conn = dbconn()
    cursor = conn.cursor()
    sql = "SELECT * FROM flights WHERE idflights = %s;"
    try:
        cursor.execute(sql, (id))
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
    data = []
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
    # return redirect("/", first_name=get_first_name_by_id(session['idusers']))
    return render_template("home.html", first_name=get_first_name_by_id(session['idusers']), is_admin=get_user_is_admin(session['idusers']))


# Adds a user's information to the database
@app.route('/adduser', methods=['POST', 'GET'])
def users():
    #log_everyone_off()
    if request.method == 'POST':
        # try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        is_admin = request.form['is_admin']

        user_id = add_user(email, first_name, last_name, password, is_admin=is_admin)
        if user_id is not None:
            session['idusers'] = user_id
            msg = "Record successfully added"
            return render_template("users.html", result=request.form, msg=msg)
        else:
            return render_template("AddUser.html", error="A user with this email already exists")
        conn.close()


@app.route('/addflight', methods=['POST', 'GET'])
def Flights():
    if request.method == 'POST':
        # try:
        de_city = request.form['de_city']
        ar_city = request.form['ar_city']
        de_time = request.form['de_time']
        de_date = request.form['de_date']
        ar_time = request.form['ar_time']
        ar_date = request.form['ar_date']
        gate = request.form['gate']
        aircraft = request.form['aircraft']
        de = de_date+" "+ de_time+ ":00";
        ar = ar_date + " " + ar_time + ":00";

        flightid = add_flight(de, ar,  gate, aircraft, de_city, ar_city)
        if flightid is not None:
            if get_id_by_flightid(flightid)!=flightid:
                msg = "The flight already exist"
            else:
                msg = "Record successfully added"
            return render_template("flights.html", result=request.form, msg=msg)
            # return render_template("users.html", result=request.form, msg=msg)
        else:

            return render_template("AddFlight.html", error="A flight with this id already exists")


@app.route('/addcraft', methods=['POST', 'GET'])
def Aircraft():
    if request.method == 'POST':
        # try:
        name = request.form['name']
        capacity = request.form['capacity']

        flightid = add_aircraft(name,capacity)
        if flightid is not None:
            msg = "Record successfully added"
            return render_template("addcraftsuccess.html", result=request.form, msg=msg)
            # return render_template("users.html", result=request.form, msg=msg)
        else:
            return render_template("AddAircraft.html", error="A Aircraft with this id already exists")


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
