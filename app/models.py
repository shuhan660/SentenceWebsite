from datetime import datetime
from . import db


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(10), nullable=False)


class Sentence(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    gender = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(10), nullable=False)

    selected = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    selected_by_student_id = db.Column(db.String(30), nullable=True)

class Selection(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    sentence_id = db.Column(db.Integer, db.ForeignKey("sentence.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)