from flask import session, redirect, url_for
from flask import Blueprint, render_template, request
from .models import db, Student, Sentence

main = Blueprint("main", __name__)


# =========================
# 首頁
# =========================
@main.route("/")
def index():
    return render_template("index.html")


# =========================
# 表單送出
# =========================
@main.route("/submit", methods=["POST"])
def submit():

    student_id = request.form["student_id"]
    name = request.form["name"]
    gender = request.form["gender"]
    region = request.form["region"]

    # 防重複學號
    if Student.query.filter_by(student_id=student_id).first():
        return "❌ 學號已存在"

    student = Student(
        student_id=student_id,
        name=name,
        gender=gender,
        region=region
    )

    db.session.add(student)
    db.session.commit()

    # 分流到句子頁
    return f"/select/{region}/{gender}"


@main.route("/select/<region>/<gender>")
def select(region, gender):

    sentences = Sentence.query.filter_by(
        region=region,
        gender=gender,
        selected=False
    ).all()

    return render_template(
        "select.html",
        sentences=sentences,
        region=region,
        gender=gender
    )


from sqlalchemy import select

@main.route("/choose/<int:id>", methods=["POST"])
def choose(id):
    sentence = Sentence.query.get_or_404(id)

    if sentence.selected:
        return "已被選走"

    sentence.selected = True
    db.session.commit()

    return "ok"

@main.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    sentences = Sentence.query.all()
    return render_template("admin.html", sentences=sentences)


@main.route("/delete/<int:id>")
def delete(id):

    sentence = Sentence.query.get(id)

    db.session.delete(sentence)
    db.session.commit()

    return "deleted"


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


@main.route("/add_sentence", methods=["POST"])
def add_sentence():

    if not session.get("admin"):
        return "no permission"

    region = request.form["region"]
    gender = request.form["gender"]
    content = request.form["content"]

    sentence = Sentence(
        region=region,
        gender=gender,
        content=content,
        selected=False
    )

    db.session.add(sentence)
    db.session.commit()

    return redirect("/admin")



@main.route("/reset")
def reset():

    if not session.get("admin"):
        return "no permission"

    Sentence.query.update({Sentence.selected: False})
    db.session.commit()

    return redirect("/admin")


from flask import send_file
from openpyxl import Workbook
from .models import Student

@main.route("/export")
def export():

    wb = Workbook()
    ws = wb.active
    ws.title = "students"

    # 標題列
    ws.append(["學號", "姓名", "性別", "地區"])

    students = Student.query.all()

    for s in students:
        ws.append([s.student_id, s.name, s.gender, s.region])

    file_path = "students.xlsx"
    wb.save(file_path)

    return send_file(file_path, as_attachment=True)