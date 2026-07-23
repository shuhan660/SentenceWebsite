from flask import Blueprint, render_template, request, redirect, session
from .models import db, Student, Sentence, Selection

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/submit", methods=["POST"])
def submit():

    student_id = request.form["student_id"]
    name = request.form["name"]
    gender = request.form["gender"]
    region = request.form["region"]

    student = Student.query.filter_by(student_id=student_id).first()

    if not student:
        student = Student(
            student_id=student_id,
            name=name,
            gender=gender,
            region=region
        )
        db.session.add(student)
        db.session.commit()

    return redirect(f"/select/{region}/{gender}")


@main.route("/select/<region>/<gender>")
def select(region, gender):

    sentences = Sentence.query.filter_by(
        region=region,
        gender=gender,
        selected=False
    ).all()

    return render_template("select.html", sentences=sentences)


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")

        return "登入失敗"

    return render_template("login.html")



@main.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    sentences = Sentence.query.all()

    return render_template("admin.html", sentences=sentences)



@main.route("/add_sentence", methods=["POST"])
def add_sentence():

    if not session.get("admin"):
        return "no permission"

    content = request.form["content"]
    region = request.form["region"]
    gender = request.form["gender"]

    sentence = Sentence(
        content=content,
        region=region,
        gender=gender,
        selected=False
    )

    db.session.add(sentence)
    db.session.commit()

    return redirect("/admin")



from . import db

@main.route("/rebuild")
def rebuild():

    db.drop_all()
    db.create_all()

    return "Database rebuilt!"