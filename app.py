from flask import *
from module import form, konek, args, download, ambil_id, hapus
from werkzeug.utils import secure_filename as sf
import os, re

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "music"
app.config["SECRET_KEY"] = "billalfauzan"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	kon = konek()
	db = kon.cursor()
	db.execute("SELECT * FROM lagu")
	return render_template("index.html", db=db)

@app.route('/music')
def music():
	id = args("id")
	return download("music/"+id+".mp3")

@app.route("/upload", methods=["GET", "POST"])
def upload():
	if request.method == "GET":
		return render_template("upload.html")
	elif request.method == "POST":
		target = os.path.join(APP_ROOT, 'music/')
		if not os.path.isdir(target):
			os.mkdir(target)
		for upload in request.files.getlist("file"):
			id = ambil_id()
			filename = upload.filename
			if not filename:
				return render_template("upload.html", type="danger", pesan="Masukan File AUDIO")
			kontol = konek()
			by = form("nama")
			if not by:
				return render_template("upload.html", pesan="Masukan Nama Anda", type="danger")
			kon = kontol.cursor()
			kon.execute("INSERT INTO lagu VALUES(%s, '%s', '%s', '%s')" % (id, "/music?id="+str(id), filename, by))
			kontol.commit()
			kon.close()
			kontol.close()
			nama = filename.replace(filename, id+".mp3")
			nama = "/".join([target, nama])
			upload.save(nama)
		return render_template("upload.html", pesan="Sukses Upload", type="success")

@app.route("/login", methods=["GET", "POST"])
def login():
	session.clear()
	if request.method == "GET":
		return render_template("login.html")
	elif request.method == "POST":
		user = form("user")
		pasw = form("pasw")
		if user == "admin":
			if pasw == "ganteng":
				session["user"] = user
				session["pasw"] = pasw
				return redirect("/admin")
			else:
				return render_template("login.html", pesan="Gagal Login")
		else:
			return render_template("login.html", pesan="Gagal Login")

@app.route("/admin", methods=["POST", "GET"])
def admin():
	if session.get("user") == "admin":
		if request.method == "GET":
			kon = konek()
			db = kon.cursor()
			db.execute("SELECT * FROM lagu")
			action = request.args.get("action")
			id = request.args.get("id")
			if not id:
				if not action:
					return render_template("admin.html", db=db)
			if id:
				if action == "delete":
					hapus(id, kon)
					return render_template("admin.html", db=db, pesan="Success", type="success")
				else:
					return render_template("admin.html", pesan="ERROR", type="danger", db=db)
	else:
		session.clear()
		return redirect("/login")

if __name__ == "__main__":
	port = os.environ.get("PORT")
	app.run(debug=True, host="0.0.0.0", port=port)
