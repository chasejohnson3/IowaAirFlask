import PIL
import PIL.Image
import base64
from base64 import b64encode, b64decode
import os

import pymysql
from flask import render_template, request, redirect, flash, send_from_directory
from flask import Flask
import json
from datetime import datetime, date

from werkzeug.utils import secure_filename

app = Flask(__name__)

import base64
import io

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def dbconn():
	return pymysql.connect(host='localhost', user='root', password='root', db='sys')


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		return render_template("addrec.html", result=result)

@app.route('/flightnoti')
def flightnoti():
	return render_template('flight-notification.html')


@app.route('/viewall')
def viewall():
	conn = dbconn()
	sql = "SELECT * FROM Student"
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()

	print(rows)

	print(request.form.get('vendor_select'))
	data = []

	for row in rows:
		temp = [row[0], row[1], row[2], row[3].decode('UTF-8')]
		data.append(list(temp))

	# filename = rows[0][3]
	# img = PIL.Image.open(filename)
	# img.show()

	options = ["Select Vendor", "VendorA", "VendorB", "VendorC"]

	conn.close()
	# return render_template("list.html", rows=data, image=filename.decode('UTF-8'))
	return render_template("list.html", rows=data, options=options)


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		try:
			nm = request.form['Name']
			marks = request.form['Marks']
			admissiondate = request.form['Admission Date']

			print(admissiondate)
			file = request.files['file']

			if file.filename == '':
				flash('No selected file')
				return redirect(request.url)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			conn = dbconn()

			sql = "INSERT INTO Student VALUES(%s, %s, %s,%s)"
			cursor = conn.cursor()
			cursor.execute(sql, (nm, marks, admissiondate, base64.b64encode(file.read())))
			conn.commit()
			msg = "Record successfully added"
		except Exception as e:
			print(e)
			msg = "Error in Insert operation"
			conn.rollback()


		finally:
			return render_template("addrec.html", result=request.form, msg=msg)
			conn.close()



if __name__ == '__main__':
	app.run(debug=True)
