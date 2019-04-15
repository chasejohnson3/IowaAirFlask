import base64
from base64 import b64encode, b64decode
import os

import pymysql
from flask import render_template, request, redirect, flash, send_from_directory
from flask import Flask
import uuid

from werkzeug.utils import secure_filename

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


# @app.route('/result', methods=['POST', 'GET'])
# def result():
# 	if request.method == 'POST':
# 		result = request.form
# 		return render_template("addrec.html", result=result)


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


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        # try:
        nm = request.form['FlightName']

        conn = dbconn()

        sql = "INSERT INTO flights(idflights, Departing_City) VALUES(%d, %s)"
        cursor = conn.cursor()
        # id = uuid.uuid4()
        # print("UUID is " + id)
        # cursor.execute(sql, (2, nm))
        cursor.execute("INSERT INTO flights(idflights, Departing_City) VALUES(4,'test')")
        conn.commit()
        msg = "Record successfully added"
        # except Exception as e:
        #     print("ERR: ",e)
        #     msg = "Error in Insert operation"
        #     conn.rollback()
        # finally:
        return render_template("addrec.html", result=request.form, msg=msg)
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
