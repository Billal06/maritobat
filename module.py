import sqlite3, random, os
from flask import *

def form(arg):
	return request.form.get(arg)

def konek():
	return sqlite3.connect("dbs/dbs.db")

def args(arg):
	return request.args.get(arg)

def download(file):
	return send_file(file, as_attachment=True)

def allowed_file(filename):
	format = {"mp3", "mp4", "txt"}
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in format

def ambil_id():
	d = []
	a = list("1234567890")
	for _ in range(3):
		d.append(random.choice(a))
	return "".join(d)

def hapus(id, kon):
	c = kon.cursor()
	c.execute("DELETE FROM lagu WHERE id=?", (id,))
	kon.commit()
	try:
		os.remove("music/"+str(id)+".mp3")
	except IOError:
		pass
