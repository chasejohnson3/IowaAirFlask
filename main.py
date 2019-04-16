import base64
from base64 import b64encode, b64decode
import os

import pymysql
from flask import render_template, request, redirect, flash, send_from_directory
from flask import Flask
import uuid

from werkzeug.utils import secure_filename
import datetime
app = Flask(__name__)

import base64



def dbconn():
    return pymysql.connect(host='35.226.87.238', port=3306, user='root', password='kfoPkgr8xKQC', db='iowa_air_gcp')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/adduser')
def addUser():
    return render_template('AddUser.html')


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

# Adds a user's information to the database
@app.route('/adduser', methods=['POST', 'GET'])
def users():
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


        conn = dbconn()
        sql = "INSERT INTO users(idusers, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, gender, country, state, city, address, postal_code, email, phone_number, password, secure_traveler) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()

        id = get_uuid()
        print("UUID is " + str(id))
        # cursor.execute(sql, (id, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, gender, country, state, city, address, postal_code, email, phone_number, password, secure_traveler))
        cursor.execute(sql, (id, first_name, last_name, middle_name, suffix, preferred_name, date_of_birth, gender, country, state, city, address, postal_code, email, phone_number, password, secure_traveler))

        conn.commit()
        msg = "Record successfully added"
        return render_template("users.html", result=request.form, msg=msg)
        conn.close()


# addrec does not do anything useful yet
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        # try:
        nm = request.form['FlightName']

        conn = dbconn()

        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(idusers, first_name) VALUES(4,'test')")
        conn.commit()
        msg = "Record successfully added"
        return render_template("addrec.html", result=request.form, msg=msg)
        conn.close()

def get_uuid():
    id = str(datetime.datetime.now().year)[2:4] + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(
    datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)
    return id

if __name__ == '__main__':
    app.run(debug=True)
